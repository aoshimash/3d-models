# 3D Models

Parametric 3D model repository using CadQuery (Python). Designed for FDM printing on Bambu Lab A1 Mini.

## Tech Stack

- **CAD**: CadQuery
- **Runtime**: Python 3.13+ managed by uv
- **Lint / Format**: ruff
- **Nix**: flake.nix provides dev shell with native dependencies (libstdc++, libGL, etc.)

## Commands

```bash
# Enter dev shell (required on NixOS - provides native libs for cadquery-ocp)
nix develop

# Environment
uv sync                                          # Install dependencies
uv add <package>                                  # Add a dependency

# Run a model script to generate STL
uv run python models/<name>/<name>.py

# Code quality (always run in this order after writing code)
uv run ruff format .
uv run ruff check --fix .
```

## Rules

### Python Environment

- NEVER use raw `pip`, `pip install`, `python`, or `python3` directly
- ALL Python operations go through `uv` (`uv run`, `uv add`, `uv sync`)

### Code Quality

- After writing or editing any Python file, always run `ruff format` then `ruff check --fix`

### Project Structure

```
models/
  <model-name>/
    <model-name>.py       # CadQuery script (single file per part)
    output/               # Generated STL files (gitignored)
pyproject.toml
```

- One directory per part/model under `models/`
- Script filename matches directory name
- STL output goes to `output/` subdirectory within each model directory

### CadQuery Conventions

- Define all dimensions as variables at the top of the script (never hardcode dimensions inline)
- Add a comment with unit (mm) and purpose for each parameter
- Explicitly define print tolerances as parameters (e.g., `fit_tolerance = 0.2  # mm - clearance for press-fit joints`)
- Use fluent API chaining for shape construction
- Assign the final shape to `result`
- Include `show_object(result)` for CQ-editor compatibility (guarded with `try/except NameError`)
- Each script must be runnable standalone to export STL:

```python
from pathlib import Path

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
result.export(str(output_dir / "<model-name>.stl"))
```

### 3D Printing (Bambu Lab A1 Mini)

- Build volume: 180 x 180 x 180 mm
- Default wall thickness: minimum 1.2 mm (3 perimeters at 0.4 mm nozzle)
- Default fit tolerance: +0.2 mm per side for sliding fit
