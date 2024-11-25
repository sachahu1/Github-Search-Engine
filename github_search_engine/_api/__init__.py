import importlib.util


fastapi_package = importlib.util.find_spec("fastapi")
if fastapi_package is None:
  raise ImportError(
    "Please install 'api' dependencies with 'pip install github-search-engine[api]'"
  ) from None
