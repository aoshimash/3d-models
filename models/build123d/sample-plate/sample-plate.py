"""Sample build123d model: a parametric plate with a filleted edge and a through hole."""

from pathlib import Path

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    Circle,
    Mode,
    Rectangle,
    export_stl,
    extrude,
    fillet,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None

PLATE_WIDTH = 60.0  # mm - X dimension of the plate
PLATE_DEPTH = 30.0  # mm - Y dimension of the plate
PLATE_THICKNESS = 4.0  # mm - Z thickness (>=1.2 mm wall minimum on A1 Mini)
EDGE_FILLET = 3.0  # mm - corner fillet radius for a softer look
HOLE_DIAMETER = 5.0  # mm - through hole (e.g. for M4 with clearance)
FIT_TOLERANCE = 0.2  # mm - per-side clearance for sliding fit

OUTPUT_PATH = Path(__file__).parent / "output" / "sample-plate.stl"


with BuildPart() as plate:
    with BuildSketch() as sk:
        Rectangle(PLATE_WIDTH, PLATE_DEPTH)
        Circle(radius=(HOLE_DIAMETER + FIT_TOLERANCE) / 2, mode=Mode.SUBTRACT)
    extrude(amount=PLATE_THICKNESS)
    fillet(plate.edges().filter_by(Axis.Z), radius=EDGE_FILLET)


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
export_stl(plate.part, str(OUTPUT_PATH))
print(f"Exported: {OUTPUT_PATH}")

if show is not None:
    try:
        show(plate.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
