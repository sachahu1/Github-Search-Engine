from cleo.application import Application

from github_search_engine import _cli as cli


def run():
  application = Application()
  application.add(cli.ApiCommand())
  application.add(cli.IndexCommand())
  application.add(cli.SearchCommand())

  application.run()
