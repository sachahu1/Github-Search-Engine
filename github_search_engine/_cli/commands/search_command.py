import os
from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from dotenv import load_dotenv

from github_search_engine._cli.commands.utils import (
  initialise_github_search_engine,
)


class SearchCommand(Command):
  name = "search"
  description = "Search an indexed repository."
  arguments: ClassVar[list[Argument]] = [
    argument("owner", "Owner of the repository."),
    argument("repository", "The name of the repository."),
    argument("query", "The query to search for."),
  ]
  options: ClassVar[list[Option]] = [
    option(
      "github_access_token",
      "g",
      description="Github Access Token.",
      flag=False,
    ),
    option(
      "env_file",
      "e",
      description="EnvFile to load.",
      flag=False,
    ),
    option(
      "db_path",
      description="Persist storage to path.",
      flag=False,
    ),
    option(
      "db_location",
      description="Qdrant Database location.",
      flag=False,
      default=":memory:",
    ),
  ]

  def handle(self):
    owner = self.argument("owner")
    repository = self.argument("repository")
    query = self.argument("query")

    if self.option("github_access_token"):
      os.environ["GITHUB_PAT"] = self.option("github_access_token")

    if self.option("env_file"):
      load_dotenv(self.option("env_file"))

    github_access_token = os.environ.get("GITHUB_PAT")
    if github_access_token is None:
      self.line(
        "No Github Access Token provided. Please provide a token via the GITHUB_PAT environment variable or using an envFile.",
        style="error",
      )
      exit(1)

    self.line(
      f"Searching through {owner}/{repository}.",
      style="info",
    )

    github_search_engine = initialise_github_search_engine(
      github_access_token,
      self.option("db_path"),
      self.option("db_location"),
    )

    results = github_search_engine.search(owner, repository, query)

    if not results:
      self.line("No good results found.", style="comment")
      exit(0)

    summary = github_search_engine.summarise_results(
      results, owner, repository, query
    )
    self.line(summary, style="comment")
