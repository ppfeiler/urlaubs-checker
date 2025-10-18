default:
  @just --list

run *ARGS:
    uv run urlaubs-checker {{ARGS}}

test:
    uv run pytest

check:
    uv run pre-commit run --all-files

install-pre-commit:
    uv run pre-commit install
