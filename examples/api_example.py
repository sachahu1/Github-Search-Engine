"""Using GitHubSearchEngine in an API.

First, build a simple API using FastAPI. The API handles indexing a repo, and searching through an indexed repo.

.. literalinclude:: /../../github_search_engine/_api/api.py
   :language: python
   :linenos:

Then, we can launch the API with uvicorn.

.. literalinclude:: /../../examples/api_example.py
   :language: python
   :linenos:
   :lines: 19-
"""

__all__ = []

import uvicorn


if __name__ == "__main__":
  uvicorn.run("github_search_engine._api.api:api", host="0.0.0.0", port=8000)
