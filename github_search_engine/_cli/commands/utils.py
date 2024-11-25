from typing import Optional

from github_search_engine.github_search_engine import GithubSearchEngine


def initialise_github_search_engine(
  github_access_token: str, db_path: Optional[str], db_location: str
):
  if not db_path:
    github_search_engine = GithubSearchEngine(
      github_access_token,
      qdrant_location=db_location,
    )
  else:
    github_search_engine = GithubSearchEngine(
      github_access_token,
      qdrant_path=db_path,
    )
  return github_search_engine
