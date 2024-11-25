from typing import List

from githubkit import GitHub
from githubkit.versions.v2022_11_28.models import Issue
from githubkit.versions.v2022_11_28.models import IssueComment
from githubkit.versions.v2022_11_28.models import TimelineCrossReferencedEvent


class GithubClientManager:
  def __init__(self, access_token: str):
    """A GithubClientManager to handle interactions with the GitHub API.

    Initializes a GitHub API client manager.

    Args:
        access_token: The personal access token used to authenticate with the GitHub API.
    """
    self.github_client = GitHub(
      auth=access_token,
    )

  async def get_repository_issues(
    self, owner: str, repository_name: str
  ) -> List[Issue]:
    """Retrieve issues from a specified GitHub repository.

    This function connects to a given GitHub repository and retrieves a list of
    issues using the GitHub API client. It returns a paginated list of issues
    associated with the repository.

    Args:
        owner: The owner of the repository from which to retrieve issues.
        repository_name: The name of the repository from which to retrieve
        issues.

    Returns:
        A paginated list of issues retrieved from the specified
        repository.
    """
    issues = []
    async for issue in self.github_client.paginate(
      self.github_client.rest.issues.async_list_for_repo,
      owner=owner,
      repo=repository_name,
      state="all",
    ):
      issue: Issue

      issues.append(issue)
    return issues

  def get_issue_comments(
    self, owner: str, repository_name: str, issue_number: int
  ) -> List[IssueComment]:
    """Retrieve comments for a specific issue in a repository.

    Args:
        owner: The owner of the repository.
        repository_name: The name of the repository.
        issue_number: The number of the issue.

    Returns:
        A list of comments for the specified issue.
    """
    return self.github_client.rest.issues.list_comments(
      owner=owner,
      repo=repository_name,
      issue_number=issue_number,
    ).parsed_data

  def get_issue_references(
    self,
    owner: str,
    repository_name: str,
    issue_number: int,
  ) -> List[TimelineCrossReferencedEvent]:
    """Fetch mentions to a given issue.

    Fetches the timeline events for a specific issue and filters out the
    cross-referenced events. This returns a list of the other issues mentioning
    the current issue.

    Args:
        owner: The owner of the repository.
        repository_name: The name of the repository.
        issue_number: The number of the issue.

    Returns:
        A list of cross-referenced events.
    """
    timeline = self.github_client.rest.issues.list_events_for_timeline(
      owner=owner,
      repo=repository_name,
      issue_number=issue_number,
    ).parsed_data

    cross_reference_events = [
      event
      for event in timeline
      if isinstance(event, TimelineCrossReferencedEvent)
    ]
    return cross_reference_events
