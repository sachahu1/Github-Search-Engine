"""Simple GitHubSearchEngine example.

.. literalinclude:: /../../examples/basic_example.py
   :language: python
   :linenos:
   :lines: 11-24
"""

__all__ = []

import os

from github_search_engine.cli import run


if __name__ == "__main__":
  github_pat = os.environ.get("GITHUB_PAT")
  result = run(
    github_access_token=github_pat,
    owner="PyGithub",
    repository_name="PyGithub",
    query="Why is there no Async support?",
  )
  print(result)
