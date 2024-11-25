import os
from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import option
from cleo.io.inputs.option import Option
from dotenv import load_dotenv


class ApiCommand(Command):
  name = "api"
  description = "Start the API"
  options: ClassVar[list[Option]] = [
    option(
      "port",
      "p",
      description="Port to run the API on.",
      flag=False,
      default=8000,
    ),
    option(
      "host",
      description="Host URL to run the API on.",
      flag=False,
      default="0.0.0.0",
    ),
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
  ]

  def handle(self):
    try:
      import uvicorn
    except ImportError:
      raise ImportError(
        "Please install 'api' dependencies with 'pip install github-search-engine[api]'"
      ) from None

    port = self.option("port")
    host = self.option("host")

    if self.option("github_access_token"):
      os.environ["GITHUB_PAT"] = self.option("github_access_token")

    if self.option("env_file"):
      load_dotenv(self.option("env_file"))

    if os.environ.get("GITHUB_PAT") is None:
      self.line(
        "No Github Access Token provided. Please provide a token via the GITHUB_PAT environment variable or using an envFile.",
        style="error",
      )
      exit(1)

    uvicorn.run("github_search_engine._api.api:api", host=host, port=port)
