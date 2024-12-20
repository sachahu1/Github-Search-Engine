import inspect
import logging
import sys

import chevron
import onnxruntime
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
    qdrant_location: str | None = None,
    qdrant_path: str | None = None,
  ):
    """A GithubSearchEngine to search GitHub repositories.

    Initializes a client manager for GitHub, Qdrant, and Ollama services, setting up
    logging and database model configuration.

    Args:
      github_access_token: The GitHub access token for accessing GitHub API.
      qdrant_location: The location of the Qdrant server. Default is None.
      qdrant_path: The path to the Qdrant database. Default is None.
    """
    logging.basicConfig(level=logging.WARNING)

    self._github_client = GithubClientManager(access_token=github_access_token)
    self._database_client = QdrantClient(
      location=qdrant_location,
      path=qdrant_path,
    )
    self._ollama_client = OllamaClientManager()

    self._database_client.set_model(
      "snowflake/snowflake-arctic-embed-m",
      providers=onnxruntime.get_available_providers(),
    )

  @staticmethod
  def summarise_issue(issue: Issue) -> str:
    """Construct a summary string from an Issue object.

    Summarizes the given issue by combining its title and body. This function takes an Issue object and returns a formatted
    string containing the issue's title and body, separated by two newline characters.

    Args:
        issue: The issue to be summarised. The issue must have 'title' and 'body' attributes.

    Returns:
        A formatted string containing the issue's title and body.
    """
    issue_summary = f"""
    {issue.title}

    {issue.body}
    """
    return issue_summary

  def summarise_results(
    self,
    results: list[QueryResponse],
    owner: str,
    repository_name: str,
    query: str,
  ) -> str:
    """Summarizes the content and discussion of GitHub issues.

    Summarizes the content and discussion of given GitHub issues, presenting how they relate to a
    specified query. The summary is concise, devoid of headings or titles, and presented in a
    single 2-3 sentence paragraph.

    Args:
        results: A list of QueryResponse objects containing GitHub issues to summarize.
        owner: The owner of the GitHub repository.
        repository_name: The name of the GitHub repository.
        query: The original query to relate the issues to.

    Returns:
        A single string containing the summarized content and discussions of all provided GitHub issues.
    """
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
    """Index a GitHub repository.

    Retrieves all issues from the specified repository and index them into a
    vector database for further processing or querying.

    Args:
        owner: The owner of the GitHub repository.
        repository_name: The name of the GitHub repository.
    """
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
  ) -> list[QueryResponse]:
    """Searches for issues in the specified repository that match the given text.

    This method searches the database for issues within the given repository that
    match the specified text query. If the repository's collection does not exist
    in the database, an error is logged and the program exits. The search results
    are filtered to exclude issues with empty bodies.

    Args:
        owner: The owner of the repository.
        repository_name: The name of the repository.
        text: A natural language query to search for within the repository's issues.

    Returns:
        A list of query responses that match the search criteria.
    """
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
