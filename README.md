# 3d-models

Parametric 3D models built with [CadQuery](https://cadquery.readthedocs.io/) (Python).

All dimensions are parameterized — tweak the variables at the top of each script to fit your needs.

## Models

| Model | Description | STL |
|-------|-------------|-----|
| [macbook-stand](models/macbook-stand/) | Side rail for a dual MacBook Pro 13″ shelf stand. Print 2 copies. | [STL](models/macbook-stand/output/macbook-stand.stl) |
| [sample-box](models/sample-box/) | Simple box with rounded edges — demonstrates CadQuery basics. | [STL](models/sample-box/output/sample-box.stl) |

> **Tip:** GitHub renders `.stl` files as interactive 3D previews — click the STL links above to see the models.

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
git clone https://github.com/aoshimash/3d-models.git
cd 3d-models
uv sync
```

### Generate STL

```bash
uv run python models/<model-name>/<model-name>.py
```

The STL file will be written to `models/<model-name>/output/`.

## Adding a New Model

1. Create a directory under `models/` (e.g. `models/my-part/`)
2. Add a script with the same name (e.g. `models/my-part/my-part.py`)
3. Follow the conventions in existing scripts:
   - Define all dimensions as variables at the top with comments
   - Assign the final shape to `result`
   - Export to `output/<model-name>.stl`

## License

[MIT](LICENSE)
