import inspect
import logging
import sys
from typing import List
from typing import Optional

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
  def __init__(
    self,
    github_access_token: str,
    qdrant_location: Optional[str] = None,
    qdrant_path: Optional[str] = None,
  ):
    logging.basicConfig(level=logging.WARNING)

    self._github_client = GithubClientManager(access_token=github_access_token)
    self._database_client = QdrantClient(
      location=qdrant_location,
      path=qdrant_path,
    )
    self._ollama_client = OllamaClientManager()

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
    self,
    results: List[QueryResponse],
    owner: str,
    repository_name: str,
    query: str,
  ):
    prompt_template = """
    Please briefly summarise the content and discussion of the following github issues.
    Keep it short, concise and to the point and explain how it relates to '{{originalQuery}}'
    Do not write headings or titles, simply summarize into a single 2-3 sentence paragraph.

      # {{issue.title}}
      {{issue.body}}

      Comments:
      {{#comments}}
      * {{body}}
      {{/comments}}
    """
    prompt_template = inspect.cleandoc(prompt_template)
    logging.info("Summarising issues")
    summaries = []
    for issue in results:
      summary = self._ollama_client.chat(
        chevron.render(
          template=prompt_template,
          data={
            "issue": issue.metadata,
            "comments": [
              {"body": comment.body}
              for comment in self._github_client.get_issue_comments(
                owner=owner,
                repository_name=repository_name,
                issue_number=issue.metadata["number"],
              )
            ],
            "originalQuery": query,
          },
        )
      )
      summary = f"""
      # Issue [#{issue.metadata["number"]}]({issue.metadata["html_url"]})
      
      {summary}
      """
      summaries.append(inspect.cleandoc(summary))
    final_summary = "\n\n".join(summaries)
    logging.info("Done")
    return final_summary

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

  def search(
    self, owner: str, repository_name: str, text: str
  ) -> List[QueryResponse]:
    if not self._database_client.collection_exists(
      collection_name=f"{owner}/{repository_name}",
    ):
      logging.error(
        "DB Collection not found. Try indexing the repository first."
      )
      sys.exit(1)
    else:
      results = self._database_client.query(
        collection_name=f"{owner}/{repository_name}",
        query_text=text,
        score_threshold=0.8,
        limit=5,
      )

      # Filter empty issues
      results = [result for result in results if result.metadata["body"]]
      return results
