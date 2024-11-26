import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from github_search_engine.github_search_engine import GithubSearchEngine


search_engine: GithubSearchEngine | None = None


class Repository(BaseModel):
  owner: str
  repository_name: str


@asynccontextmanager
async def lifespan(app: FastAPI):
  global search_engine
  github_access_token = os.environ["GITHUB_PAT"]
  search_engine = GithubSearchEngine(
    github_access_token, qdrant_location=":memory:"
  )
  yield
  del search_engine


api = FastAPI(lifespan=lifespan)


@api.post("/index")
async def index(repository: Repository):
  await search_engine.index_repository(
    repository.owner,
    repository.repository_name,
  )
  return {"message": "Repository indexed"}


@api.get("/search")
async def search(owner: str, repository: str, query: str):
  results = search_engine.search(owner, repository, query)
  summary = search_engine.summarise_results(results, owner, repository, query)
  return summary
