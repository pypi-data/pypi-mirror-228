# G3
All-in-one CLI to commit your work to Github [[Presentation](https://docs.google.com/presentation/d/1BZN4cfeGYR9U4UjXF6wH_-x9l8DwGOgJRZr7UDKXiMQ/), [Design](https://docs.google.com/document/d/1b3SkLVnrB_P-lYsD2Kv-fO-oUHciovQbTQbKsNswHtA)]

[![Watch the video](docs/g.png)](https://youtu.be/dTKCxIoPC54)

## Install
```bash
pip install g3
```

#### Alias

You can, optionally, create the `alias g=g3` so that you execute simply `g commit` and `g pr`.

## Configuration

```bash
g3 configure
```

You will be asked to enter:
- your Github token 
- your open-ai key
- the openai model you want to use
- the temperature which will be used to generate the commit messages and PR descriptions
- the openai api version
- the tone which will be used in the commit messages and PR descriptions
- the commit message max characters
- the PR description max words


## Usage

### Commit

```bash
g3 commit
```

#### Options:
- --tone: The tone to use
- --jira: The jira ticket(s) to reference
- --include: A phrase you want to include
- --edit: The hash of the commit you want to rephrase

### PR

```bash
g3 pr
```

#### Options:
- --tone: The tone to use
- --jira: The jira ticket(s) to reference
- --include: A phrase you want to include
- --edit: The number of the PR you want to rephrase

## Development

The project requires `Python 3.11` and [Poetry](https://python-poetry.org/docs/#installation) for dependency management. 

Optionally configure poetry to create the virtual environment within the project as follows:
```shell script
poetry config virtualenvs.in-project true
```

### Build

Now install the project, along with its development dependencies, in a local virtual environment as follows:

```shell
poetry install
```
You may enable the virtual environment, so that you run modules without the `poetry run` prefix, as follows:
```
source `poetry env info -p`/bin/activate
```
or simply as follows:
```
poetry shell
```

### Contribution

You are expected to enable pre-commit hooks so that you get your code auto-sanitized before being committed.
* mypy:   Static type checker of variables and functions based on [PEP 484](https://peps.python.org/pep-0484/) 
* isort:  Optimizes imports
* black:  Opinionated code formatter based on [PEP 8](https://peps.python.org/pep-0008/) 
* flake8: Improves code style and quality based on [PEP 8](https://peps.python.org/pep-0008/)

Install pre-commit before starting to contribute to the project as follows:
```
pre-commit install
```
