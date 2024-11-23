import logging
from typing import List

import chevron
from githubkit.versions.v2022_11_28.models import Issue
from qdrant_client import QdrantClient
from qdrant_client.http.models import QueryResponse

from github_search_engine.clients.github_client_manager import (
  GithubClientManager,
)
from github_search_engine.clients.ollama_client_manager import (
  OllamaClientManager,
)


class GithubSearchEngine:
  def __init__(self, github_access_token: str):
    logging.basicConfig(level=logging.WARNING)

    self._github_client = GithubClientManager(access_token=github_access_token)
    self._database_client = QdrantClient(":memory:")
    self._ollama_client = OllamaClientManager()

    self._collection = None
    self._owner = None
    self._repository_name = None

    self._database_client.set_model(
      "snowflake/snowflake-arctic-embed-m",
      providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
    )

  @staticmethod
  def summarise_issue(issue: Issue) -> str:
    issue_summary = f"""
    {issue.title}

    {issue.body}
    """
    return issue_summary

  def summarise_results(
    self, results: List[QueryResponse], owner: str, repository_name: str
  ):
    logging.info("Summarising issues")
    issues = {
      "issues": [
        {
          "issue": issue.metadata,
          "comments": [
            {"body": comment.body}
            for comment in self._github_client.get_issue_comments(
              owner=owner,
              repository_name=repository_name,
              issue_number=issue.metadata["number"],
            )
          ],
        }
        for issue in results
      ]
    }
    prompt_template = """
    Please briefly summarise the content and discussion of the following github issues.
    Try to keep it short, concise and to the point.

    {{#issues}}
      # {{issue.title}}
      {{issue.body}}

      Comments:
      {{#comments}}
      * {{body}}
      {{/comments}}
    {{/issues}}
    """
    summary = self._ollama_client.chat(
      chevron.render(template=prompt_template, data=issues)
    )
    logging.info("Done")
    return summary

  async def index_repository(self, owner: str, repository_name: str):
    logging.info(f"Fetching Issues from {owner}/{repository_name}")
    issues = await self._github_client.get_repository_issues(
      owner, repository_name
    )

    logging.info("Adding to Vector DB")
    self._database_client.add(
      collection_name=f"{owner}/{repository_name}",
      documents=[self.summarise_issue(issue) for issue in issues],
      metadata=[issue.model_dump() for issue in issues],
    )
    logging.info("Done")

  def search(self, text: str) -> List[QueryResponse]:
    results = self._database_client.query(
      collection_name=self._collection,
      query_text=text,
      score_threshold=0.8,
    )
    return results

  def set_collection(self, owner: str, repository_name: str):
    self._collection = f"{owner}/{repository_name}"
    self._owner = owner
    self._repository_name = repository_name
