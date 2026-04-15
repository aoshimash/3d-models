# build123d models

Independent uv project for build123d-based parametric models, separated from the
root CadQuery environment.

## Setup

```bash
cd models/build123d
uv sync
```

## Generate STL

```bash
# from models/build123d/
uv run python <model-name>/<model-name>.py
```

## Live preview with ocp_vscode

1. Install the VS Code extension: `bernhard-42.ocp-cad-viewer`
2. Command Palette → `OCP CAD Viewer: Open Viewer`
3. Run a model script — `show(part)` pushes geometry to the viewer.

## Code quality

```bash
uv run ruff format .
uv run ruff check --fix .
```
