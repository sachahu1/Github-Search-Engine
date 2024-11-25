# Github-Search-Engine

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sachahu1/Github-Search-Engine/run-tests.yaml?branch=main&label=Tests)

![GitHub Release](https://img.shields.io/github/v/release/sachahu1/Github-Search-Engine)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/github_search_engine)
![GitHub Repo stars](https://img.shields.io/github/stars/sachahu1/Github-Search-Engine)

## Getting Started

To get started simply install the package:
```shell
pip install git+https://github.com/sachahu1/Github-Search-Engine.git
```
You can then start using the tool with the CLI:
```shell
github_search_engine
```

### Using as a CLI tool
You can use this package as a CLI tool, to do that, start by indexing your favourite GitHub repository:
```shell
github_search_engine index <owner> <repository_name> --db_path=./local-store --github_access_token=<Your GitHub Personal Access Token>
```
Then, search through any issue using:
```shell
github_search_engine search <owner> <repository_name> "<Your query>" --db_path=./local-store --github_access_token=<Your GitHub Personal Access Token>
```

### Launching an API server
You can use this package as an API. To do that, simply run:
```shell
github_search_engine api --github_access_token=<Your GitHub Personal Access Token>
```

## Building the documentation
### Using Docker
To access the documentation locally, the easiest way is to use the docker image. To do so, simply run:
```shell
docker build . -f Dockerfile --target documentation -t github_search_engine-docs
docker run -p 80:80 -it github_search_engine-docs
```
Then navigate to [http://localhost](http://localhost)

### Manually
Alternatively you can build the documentation yourself.
First, make sure you have the dependencies installed:
```shell
poetry install --with=documentation
```
Then build the documentation:
```shell
poetry run sphinx-build -M html docs/source/ docs/build
```
Then open the documentation in your browser:
```shell
open docs/build/html/index.html
```
