# 3d-models

Parametric 3D models for FDM printing on Bambu Lab A1 Mini, authored across multiple CAD tools.

All dimensions are parameterized — tweak the variables at the top of each script to fit your needs.

## Models

| Model | Tool | Description | STL |
|-------|------|-------------|-----|
| [macbook-stand](models/cadquery/macbook-stand/) | CadQuery | Dual MacBook Pro 13″ shelf stand. Two-part rail joined by diagonal tenon, connected with 8 bridge bars. Print 4 rails + 8 bridges. | [STL](models/cadquery/macbook-stand/output/) |
| [sample-box](models/cadquery/sample-box/) | CadQuery | Simple box with rounded edges — demonstrates CadQuery basics. | [STL](models/cadquery/sample-box/output/sample-box.stl) |
| [macbook-stand](models/jscad/macbook-stand/) | JSCAD | JSCAD port of the dual MacBook Pro 13″ shelf stand side rail. | [STL](models/jscad/macbook-stand/output/) |
| [macbook-stand](models/openscad/macbook-stand/) | OpenSCAD | Dual MacBook shelf stand built with BOSL2 dovetail joiners. Rail split into front/back parts (rail_depth exceeds 180 mm build volume) plus bridges. | [STL](models/openscad/macbook-stand/output/) |

> **Tip:** GitHub renders `.stl` files as interactive 3D previews — open the `output/` directory and click a file to view it.

## Getting Started

### Prerequisites

- **CadQuery models:** Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- **JSCAD models:** Node.js
- **OpenSCAD models:** [OpenSCAD](https://openscad.org/) (nightly recommended) with the [BOSL2](https://github.com/BelfrySCAD/BOSL2) library installed

### Setup

```bash
git clone https://github.com/aoshimash/3d-models.git
cd 3d-models

# CadQuery
uv sync

# JSCAD
cd models/jscad && npm install && cd ../..
```

### Generate STL

```bash
# CadQuery
uv run python models/cadquery/<model-name>/<model-name>.py

# JSCAD
node models/jscad/<model-name>/<model-name>.js

# OpenSCAD
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD \
  -o models/openscad/<model-name>/output/<model-name>.stl \
  models/openscad/<model-name>/<model-name>.scad
```

STL files are written to each model's `output/` subdirectory.

## Adding a New Model

1. Pick a tool directory: `models/cadquery/`, `models/jscad/`, or `models/openscad/`
2. Create a subdirectory named after the model (e.g. `models/openscad/my-part/`)
3. Add a script with the same name (e.g. `my-part.scad`)
4. Follow the conventions in [CLAUDE.md](CLAUDE.md):
   - Define all dimensions as variables at the top with unit + purpose comments
   - Make the script runnable standalone to export STL
   - Write output to an `output/` subdirectory

## License

[MIT](LICENSE)
