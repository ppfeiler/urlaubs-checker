# urlaubs-checker

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)



## Installation

The recommended way to install this tool is via [uv](https://github.com/astral-sh/uv):
```bash
uv tool install https://github.com:ppfeiler/urlaubs-checker.git
```

## Upgrading

To update an installation via [uv](https://github.com/astral-sh/uv) use this command:
```bash
uv tool upgrade urlaubs-checker
```

## Development

To contribute to this project, first checkout the code.
We use [uv](https://github.com/astral-sh/uv) for working with python projects.

[uv](https://github.com/astral-sh/uv) will install all dependencies automatically. You can run the application with:
```bash
uv run urlaubs-checker
```

To run the tests:
```bash
uv run pytest
```

### pre-commit

This project uses [pre-commit](https://pre-commit.com) for commit hooks. When working the first time with this project, run the following command to install pre-commit:
```bash
uv run pre-commit install
```

## Just

For simplicity, we also use [just](https://github.com/casey/just) for some common tasks.
For example you can also run this project with the following:
```bash
just run
```

or for linting:
```bash
just check
```

see the [justfile](justfile) or run `just` for more infos.
