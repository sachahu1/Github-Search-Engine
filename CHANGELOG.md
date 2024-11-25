# CHANGELOG


## v0.1.0 (2024-11-25)

### Documentation

- Add initial Sphinx documentation setup
  ([`5aaa59a`](https://github.com/sachahu1/Github-Search-Engine/commit/5aaa59a8f5f8d6c401251407068f08211182615d))

Added Makefile, make.bat, conf.py, and templates for Sphinx documentation. Set up basic
  configuration and structure for the documentation project. Included instructions for installing
  Poetry and building the documentation.

### Features

- Update Python versions in workflows
  ([`b5bdd75`](https://github.com/sachahu1/Github-Search-Engine/commit/b5bdd7518b1faea939f46fc37ef5b72b5843920b))

Update Python versions to 3.11.0 and add 3.12 in test matrix.

- Add workflows for release and running tests
  ([`064ff4d`](https://github.com/sachahu1/Github-Search-Engine/commit/064ff4d2cf10a5b297f95e41693822a8fcb9169d))

- Added workflows for releasing the project and running tests. - Workflows include steps for
  building, deploying, and testing.

- Add initial test files for GitHub search engine
  ([`b239f7e`](https://github.com/sachahu1/Github-Search-Engine/commit/b239f7ebfd161bb986051b85a11fdebe9e7f4a98))

Added test files for initialization and a sample test case.

- Add Dockerfile and .dockerignore files
  ([`6a168ff`](https://github.com/sachahu1/Github-Search-Engine/commit/6a168ffb07b32c67299b9458230d29d1efb1110d))

Include Dockerfile with Python setup and ignore unnecessary files in Docker build.

- Update README with new Getting Started instructions
  ([`ea53008`](https://github.com/sachahu1/Github-Search-Engine/commit/ea53008508b2f2375f8c6fb605a6fb2e29b093a3))

Added detailed instructions for installing the package, using it as a CLI tool, launching an API
  server, accessing documentation via Docker or manually.

- Add API example and refactor basic example
  ([`2c382cf`](https://github.com/sachahu1/Github-Search-Engine/commit/2c382cf261d883cd66eff52fd8103fa6ad09628b))

Added a new API example using FastAPI for repo indexing and search. Refactored the basic example to
  use GithubSearchEngine class for async operations.

- **cli**: Add CLI commands for API, indexing, and searching
  ([`ce56301`](https://github.com/sachahu1/Github-Search-Engine/commit/ce56301aae5019b537476c215a86e4bf5571a688))

- Added CLI commands for starting the API, indexing a repository, and searching an indexed
  repository. The commands include options for setting port, host URL, Github Access Token, EnvFile
  to load, database path, and Qdrant Database location.

- **api**: Add FastAPI initialization and endpoints
  ([`5b7b689`](https://github.com/sachahu1/Github-Search-Engine/commit/5b7b689357d48b0a046e9c6955210c653f6aa476))

- Initialize FastAPI with lifespan context manager - Define POST endpoint to index repositories -
  Define GET endpoint to search repositories

- Add optional parameters to constructor and update search method
  ([`ef12cdf`](https://github.com/sachahu1/Github-Search-Engine/commit/ef12cdfaf02544c43f97d60121995069237e30eb))

- Added optional parameters to the constructor for flexibility. - Updated the search method to
  handle collection existence check and filtering empty issues.

- Add new packages and dependencies
  ([`87beb42`](https://github.com/sachahu1/Github-Search-Engine/commit/87beb4280b1dd7f7697b8a0b2d32ac4a75c16772))

Added new packages "cleo", "click", "crashtest", "dnspython", "email-validator", "fastapi", and
  their respective dependencies. Included package extras for optional features.

- Add .gitignore and .pre-commit-config.yaml files
  ([`bb71c2f`](https://github.com/sachahu1/Github-Search-Engine/commit/bb71c2f09b6c75f1004b7947ec36993798f484e5))

Include Python template in .gitignore, configure pre-commit hooks in .pre-commit-config.yaml.

- Add basic example for GitHubSearchEngine
  ([`b408727`](https://github.com/sachahu1/Github-Search-Engine/commit/b40872798b985e03960d68f0ce70f7b379fae7c6))

Include a simple example demonstrating usage of the GitHubSearchEngine library to query a specific
  repository.

- **cli**: Add CLI module for running Github search engine
  ([`82a9566`](https://github.com/sachahu1/Github-Search-Engine/commit/82a9566c2736119e97ec0a77f53e03685369bdc9))

- Introduce a new CLI module to run Github search engine with async support.

- Add GithubSearchEngine class with methods
  ([`a09336e`](https://github.com/sachahu1/Github-Search-Engine/commit/a09336e716d544bf17d0aa8e737de6591c67c02e))

- Added a new class `GithubSearchEngine` with methods for summarizing issues, summarizing search
  results, indexing repositories, searching text, and setting collection details.

- Add OllamaClientManager for embedding and chat functionality
  ([`0d99701`](https://github.com/sachahu1/Github-Search-Engine/commit/0d997011ba61a7a27b010e207d79c626b0c5f454))

- Implement OllamaClientManager class with embed and chat methods.

- **clients**: Add GithubClientManager for GitHub API interactions
  ([`44d2b70`](https://github.com/sachahu1/Github-Search-Engine/commit/44d2b709c5d2fe8abd4e92b221053f3f9b7f2a00))

- Implement methods to retrieve repository issues, issue comments, and cross-referenced events from
  the GitHub API.

- Add new packages and versions to poetry.lock
  ([`b5fcd24`](https://github.com/sachahu1/Github-Search-Engine/commit/b5fcd2469fec50bd3e110d164e4b97e9dfc8302a))

Added multiple packages with their respective versions, descriptions, Python version compatibility,
  and file hashes to the poetry.lock file.