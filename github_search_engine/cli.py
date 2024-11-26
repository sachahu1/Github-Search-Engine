"""The simplest way to use this tool is via the cli.

To get started, run the CLI tool with:

.. code-block:: bash

  $ github-search-engine -h

"""

from cleo.application import Application

from github_search_engine import _cli as cli


def _run():
  application = Application()
  application.add(cli.ApiCommand())
  application.add(cli.IndexCommand())
  application.add(cli.SearchCommand())

  application.run()
