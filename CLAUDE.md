# 3D Models

Parametric 3D model repository for FDM printing on Bambu Lab A1 Mini.
Multiple CAD tools supported, organized by tool under `models/`.

## Tech Stack

- **CAD (CadQuery)**: Python 3.13+ managed by uv, linted with ruff
- **CAD (build123d)**: Python 3.13+ managed by uv, linted with ruff
- **CAD (JSCAD)**: Node.js, @jscad/modeling + @jscad/stl-serializer
- **CAD (OpenSCAD)**: OpenSCAD nightly + BOSL2 library

## Commands

```bash
# --- CadQuery (Python) ---
# CadQuery has its OWN uv project under models/cadquery/ (isolated venv)
cd models/cadquery
uv sync                                           # Install dependencies (first time)
uv run python <name>/<name>.py                    # Generate STL
uv run ruff format .
uv run ruff check --fix .

# --- build123d (Python) ---
# build123d has its OWN uv project under models/build123d/ (isolated venv)
cd models/build123d
uv sync                                           # Install dependencies (first time)
uv run python <name>/<name>.py                    # Generate STL
uv run ruff format .
uv run ruff check --fix .

# --- JSCAD (JavaScript) ---
cd models/jscad
npm install                                       # Install dependencies
node <model-name>/<model-name>.js                 # Generate STL

# --- OpenSCAD ---
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -o output.stl model.scad   # CLI export
# Or open .scad file in OpenSCAD GUI (F5=preview, F6=render)
```

## Rules

### Python Environments (CadQuery / build123d)

- Each Python-based CAD tool has its OWN uv project (isolated venv, separate dependencies):
  - CadQuery: `models/cadquery/pyproject.toml`
  - build123d: `models/build123d/pyproject.toml`
- There is NO root-level `pyproject.toml` — always `cd` into the tool directory before running uv commands
- NEVER use raw `pip`, `pip install`, `python`, or `python3` directly
- ALL Python operations go through `uv` (`uv run`, `uv add`, `uv sync`)
- After writing or editing any Python file, always run `ruff format` then `ruff check --fix` inside the corresponding project directory

### Project Structure

```
models/
  cadquery/                   # CadQuery (Python) — independent uv project
    pyproject.toml            # CadQuery-specific dependencies
    .python-version           # pinned to 3.13 (cadquery-ocp has no 3.14 wheel)
    uv.lock
    .venv/                    # not committed
    <model-name>/
      <model-name>.py         # CadQuery script
      output/                 # Generated STL files (committed)
  build123d/                  # build123d (Python) — independent uv project
    pyproject.toml            # build123d-specific dependencies
    .python-version           # pinned to 3.13
    uv.lock
    .venv/                    # not committed
    <model-name>/
      <model-name>.py         # build123d script
      output/                 # Generated STL files (committed)
  jscad/                      # JSCAD (JavaScript) models
    package.json
    <model-name>/
      <model-name>.js         # JSCAD script
      output/                 # Generated STL files (committed)
  openscad/                   # OpenSCAD models
    <model-name>/
      <model-name>.scad       # OpenSCAD script (uses BOSL2)
      output/                 # Generated STL files (committed)
```

No root-level `pyproject.toml` / `uv.lock` — each CAD tool is self-contained.

- One directory per part/model under each tool directory
- Script filename matches directory name
- STL output goes to `output/` subdirectory within each model directory

### CadQuery Conventions

- Define all dimensions as variables at the top of the script (never hardcode dimensions inline)
- Add a comment with unit (mm) and purpose for each parameter
- Explicitly define print tolerances as parameters (e.g., `fit_tolerance = 0.2  # mm - clearance for press-fit joints`)
- Use fluent API chaining for shape construction
- Assign the final shape to `result`
- Include `show_object(result)` for CQ-editor compatibility (guarded with `try/except NameError`)
- Each script must be runnable standalone to export STL

### build123d Conventions

- Define all dimensions as module-level constants at the top of the script (never hardcode inline)
- Add a comment with unit (mm) and purpose for each parameter
- Explicitly define print tolerances as parameters (e.g., `FIT_TOLERANCE = 0.2  # mm`)
- Prefer the Builder API (`with BuildPart() as part:` / `Box(...)` / `extrude(...)`) over direct algebra for readability
- Extract the final shape via `part.part` and export with `export_stl(part.part, "output/<name>.stl")`
- Each script must be runnable standalone via `uv run python <script>.py` to export STL

### JSCAD Conventions

- Define all dimensions as constants at the top of the script
- Add a comment with unit (mm) and purpose for each parameter
- Use CSG operations: `union()`, `subtract()`, `intersect()`
- Use explicit `translate()`, `rotate()` for positioning (no implicit coordinate transforms)
- Each script must be runnable standalone via `node <script>.js` to export STL
- Use `@jscad/stl-serializer` for binary STL output

### OpenSCAD Conventions

- Define all dimensions as variables at the top of the script
- Add a comment with unit (mm) and purpose for each parameter
- Use BOSL2 library (`include <BOSL2/std.scad>`) for shapes and joiners
- Use BOSL2 joiners for joints: `dovetail()`, `snap_pin()`, `snap_pin_socket()`, etc.
- Use `$slop` for global fit tolerance (default 0.1 for FDM)
- Use explicit `translate()`, `rotate()` for positioning (no implicit coordinate transforms)
- Each script must be runnable standalone via OpenSCAD CLI to export STL
- Use `$fn` for circle resolution (24 for preview, 48+ for export)

### 3D Printing (Bambu Lab A1 Mini)

- Build volume: 180 x 180 x 180 mm
- Default wall thickness: minimum 1.2 mm (3 perimeters at 0.4 mm nozzle)
- Default fit tolerance: +0.2 mm per side for sliding fit
