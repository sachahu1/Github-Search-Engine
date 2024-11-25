import asyncio
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


class IndexCommand(Command):
  name = "index"
  description = "Index a repository."
  arguments: ClassVar[list[Argument]] = [
    argument("owner", "Owner of the repository."),
    argument("repository", "The name of the repository."),
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
      f"Indexing {owner}/{repository}.",
      style="info",
    )

    github_search_engine = initialise_github_search_engine(
      github_access_token,
      self.option("db_path"),
      self.option("db_location"),
    )

    asyncio.run(github_search_engine.index_repository(owner, repository))

    self.line(
      f"Successfully indexed {owner}/{repository}.",
      style="comment",
    )
