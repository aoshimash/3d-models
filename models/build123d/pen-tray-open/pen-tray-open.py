"""Parametric pen tray — low-profile, single open compartment (no dividers).

Outer footprint: 150 x 178 mm (15 cm wide; 178 mm fits A1 Mini's 180 mm bed
with a 2 mm margin). Height: 20 mm — low enough that pens resting horizontally
stay visible and easy to grab, tall enough that a tipped pen won't roll out.

Internal layout: one open compartment with no dividers.

Print notes
-----------
- Orientation: flat on the build plate (bottom face on bed). No supports.
- Layer height: 0.2 mm recommended (floor = 10 solid layers for rigidity).
- Infill: 15 % gyroid is plenty for desk use.
- Bed margin: 2 mm on Y (178 vs 180), 30 mm on X (150 vs 180).
"""

from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Locations,
    Mode,
    Plane,
    Pos,
    RectangleRounded,
    chamfer,
    export_stl,
    extrude,
    fillet,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Outer dimensions (mm) ---
TRAY_WIDTH = 150.0  # X — user-specified (15 cm)
TRAY_DEPTH = 178.0  # Y — A1 Mini build plate 180 mm minus 2 mm safety margin
TRAY_HEIGHT = 20.0  # Z — low profile: pens rest horizontally

# --- Walls & floor (mm) ---
WALL_THICKNESS = 2.4  # exterior walls: 6 perimeters at 0.4 mm nozzle + buffer
DIVIDER_THICKNESS = 2.0  # internal dividers carry less load, saves material
FLOOR_THICKNESS = 2.0  # 10 solid layers at 0.2 mm for rigidity

# --- Fillets / chamfers (mm) ---
OUTER_VERTICAL_FILLET = 6.0  # softly rounded outer vertical corners
TOP_CHAMFER = 0.6  # top-rim bevel for finger comfort (chamfer is robust on thin dividers)
OUTER_BOTTOM_FILLET = 0.6  # small — keep first-layer adhesion solid
INNER_FLOOR_FILLET = 1.5  # cavity floor/wall junction (cleanable, printable)

# --- Compartments ---
NUM_COMPARTMENTS = 1  # single open compartment — no dividers

OUTPUT_PATH = Path(__file__).parent / "output" / "pen-tray-open.stl"


def _equal_divider_positions(
    num_compartments: int, inner_width: float, divider_thickness: float
) -> list[float]:
    """Return divider center X positions (world coords, symmetric around 0)."""
    num_dividers = num_compartments - 1
    if num_dividers <= 0:
        return []
    compartment = (inner_width - num_dividers * divider_thickness) / num_compartments
    step = compartment + divider_thickness  # divider-to-divider center distance
    return [(i - (num_dividers - 1) / 2) * step for i in range(num_dividers)]


INNER_WIDTH = TRAY_WIDTH - 2 * WALL_THICKNESS
INNER_DEPTH = TRAY_DEPTH - 2 * WALL_THICKNESS
CAVITY_HEIGHT = TRAY_HEIGHT - FLOOR_THICKNESS
CAVITY_CORNER_RADIUS = max(OUTER_VERTICAL_FILLET - WALL_THICKNESS, 0.5)
DIVIDER_POSITIONS = _equal_divider_positions(NUM_COMPARTMENTS, INNER_WIDTH, DIVIDER_THICKNESS)


with BuildPart() as tray:
    # Outer solid — RectangleRounded gives pre-rounded vertical corners
    with BuildSketch():
        RectangleRounded(TRAY_WIDTH, TRAY_DEPTH, OUTER_VERTICAL_FILLET)
    extrude(amount=TRAY_HEIGHT)

    # Hollow out the cavity from the floor upward, keeping rounded inner corners
    with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
        RectangleRounded(INNER_WIDTH, INNER_DEPTH, CAVITY_CORNER_RADIUS)
    extrude(amount=CAVITY_HEIGHT, mode=Mode.SUBTRACT)

    # Add equal-spaced divider walls inside the cavity
    if DIVIDER_POSITIONS:
        with Locations(*[Pos(x, 0, FLOOR_THICKNESS) for x in DIVIDER_POSITIONS]):
            Box(
                DIVIDER_THICKNESS,
                INNER_DEPTH,
                CAVITY_HEIGHT,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )

    # Round the cavity floor/wall junction (easier to clean, prints cleanly)
    fillet(
        tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[1],
        radius=INNER_FLOOR_FILLET,
    )
    # Small bottom fillet on the outer bed-contact perimeter for aesthetics
    fillet(
        tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
        radius=OUTER_BOTTOM_FILLET,
    )
    # Chamfer the top rim — robust even where the thin divider meets the top
    chamfer(
        tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
        length=TOP_CHAMFER,
    )


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
export_stl(tray.part, str(OUTPUT_PATH))
print(f"Exported: {OUTPUT_PATH}")

if show is not None:
    try:
        show(tray.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
