import asyncio

from github_search_engine.github_search_engine import GithubSearchEngine


def run(
  github_access_token: str,
  owner: str = "PyGithub",
  repository_name: str = "PyGithub",
  query: str = "Why is there no Async support?",
):
  github_search_engine = GithubSearchEngine(github_access_token)

  github_search_engine.set_collection(
    owner=owner,
    repository_name=repository_name,
  )

  asyncio.run(github_search_engine.index_repository(owner, repository_name))
  results = github_search_engine.search(query)
  summary = github_search_engine.summarise_results(
    results, owner, repository_name
  )
  return summary
