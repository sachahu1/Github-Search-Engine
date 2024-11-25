"""Simple GitHubSearchEngine example.

.. literalinclude:: /../../examples/basic_example.py
   :language: python
   :linenos:
   :lines: 11-
"""

__all__ = []

import asyncio
import os

from github_search_engine.github_search_engine import GithubSearchEngine


def run(
  github_access_token: str,
  owner: str,
  repository_name: str,
  query: str,
):
  github_search_engine = GithubSearchEngine(github_access_token)

  asyncio.run(github_search_engine.index_repository(owner, repository_name))
  results = github_search_engine.search(owner, repository_name, query)
  summary = github_search_engine.summarise_results(
    results, owner, repository_name, query
  )
  return summary


if __name__ == "__main__":
  github_pat = os.environ["GITHUB_PAT"]
  result = run(
    github_access_token=github_pat,
    owner="PyGithub",
    repository_name="PyGithub",
    query="Can I use async?",
  )
  print(result)
