# CadQuery models

Independent uv project for CadQuery-based parametric models.

## Setup

```bash
cd models/cadquery
uv sync
```

## Generate STL

```bash
# from models/cadquery/
uv run python <model-name>/<model-name>.py
```

## Code quality

```bash
uv run ruff format .
uv run ruff check --fix .
```
