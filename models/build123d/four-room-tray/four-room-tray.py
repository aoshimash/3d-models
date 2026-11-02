"""Parametric tray with two item rooms plus two spare rooms — A1 Mini's largest footprint.

Outer footprint: 178 x 178 mm (A1 Mini's 180 mm bed minus a 2 mm margin, same as
pen-tray). Height: 20 mm, matching pen-tray and drawer-tray.

Internal layout: the two item rooms sit one behind the other on the left, so both
items keep their stated orientation, and the width left over beside each becomes
a spare room:
  - Room A (back left) holds an item of 78 mm (Y) x 88 mm (X)
  - Room B (front left) holds an item of 64 mm (Y) x 115 mm (X)
  - Room C (back right) and room D (front right) are spare

Side by side would need 88 + 115 = 203 mm and does not fit the bed. All spare
depth is shared equally between rooms A and B as room to get fingers in beside
the item, and the same margin is applied across the width.

Print notes
-----------
- Orientation: flat on the build plate (bottom face on bed). No supports.
- Layer height: 0.2 mm recommended (floor = 10 solid layers for rigidity).
- Infill: 15 % gyroid is plenty for desk use.
- Bed margin: 2 mm on X and Y (178 vs 180) — no room for a brim, so keep the bed
  clean; large flat prints are the ones that lift at the corners.
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
TRAY_WIDTH = 178.0  # X — A1 Mini build plate 180 mm minus 2 mm safety margin
TRAY_DEPTH = 178.0  # Y — A1 Mini build plate 180 mm minus 2 mm safety margin
TRAY_HEIGHT = 20.0  # Z — same as pen-tray and drawer-tray

# --- Items to store (mm) ---
ITEM_A_DEPTH = 78.0  # Y — "tate" of the item in room A
ITEM_A_WIDTH = 88.0  # X — "yoko" of the item in room A
ITEM_B_DEPTH = 64.0  # Y — "tate" of the item in room B
ITEM_B_WIDTH = 115.0  # X — "yoko" of the item in room B

# --- Walls & floor (mm) ---
WALL_THICKNESS = 2.4  # exterior walls: 6 perimeters at 0.4 mm nozzle + buffer
DIVIDER_THICKNESS = 2.0  # internal dividers carry less load, saves material
FLOOR_THICKNESS = 2.0  # 10 solid layers at 0.2 mm for rigidity

# --- Fillets / chamfers (mm) ---
OUTER_VERTICAL_FILLET = 6.0  # softly rounded outer vertical corners
TOP_CHAMFER = 0.6  # top-rim bevel for finger comfort (chamfer is robust on thin dividers)
OUTER_BOTTOM_FILLET = 0.6  # small — keep first-layer adhesion solid
INNER_FLOOR_FILLET = 1.5  # cavity floor/wall junction (cleanable, printable)

OUTPUT_PATH = Path(__file__).parent / "output" / "four-room-tray.stl"


INNER_WIDTH = TRAY_WIDTH - 2 * WALL_THICKNESS  # 173.2
INNER_DEPTH = TRAY_DEPTH - 2 * WALL_THICKNESS  # 173.2
CAVITY_HEIGHT = TRAY_HEIGHT - FLOOR_THICKNESS  # 18.0
CAVITY_CORNER_RADIUS = max(OUTER_VERTICAL_FILLET - WALL_THICKNESS, 0.5)

# Spare depth is split equally so each room gets the same margin beside its item
ROOM_MARGIN = (INNER_DEPTH - DIVIDER_THICKNESS - ITEM_A_DEPTH - ITEM_B_DEPTH) / 2  # 14.6
ROOM_A_DEPTH = ITEM_A_DEPTH + ROOM_MARGIN  # 92.6 — back rooms (+Y)
ROOM_B_DEPTH = ITEM_B_DEPTH + ROOM_MARGIN  # 78.6 — front rooms (-Y)
ROOM_A_WIDTH = ITEM_A_WIDTH + ROOM_MARGIN  # 102.6
ROOM_B_WIDTH = ITEM_B_WIDTH + ROOM_MARGIN  # 129.6

CAVITY_LEFT = -INNER_WIDTH / 2  # -86.6
CAVITY_FRONT = -INNER_DEPTH / 2  # -86.6
CAVITY_BACK = INNER_DEPTH / 2  # 86.6
DIVIDER_Y = CAVITY_FRONT + ROOM_B_DEPTH + DIVIDER_THICKNESS / 2  # -7.0 — back rooms / front rooms
DIVIDER_A_X = CAVITY_LEFT + ROOM_A_WIDTH + DIVIDER_THICKNESS / 2  # 17.0 — room A / room C
DIVIDER_B_X = CAVITY_LEFT + ROOM_B_WIDTH + DIVIDER_THICKNESS / 2  # 44.0 — room B / room D

assert ROOM_MARGIN > 0, f"Items do not fit: ROOM_MARGIN = {ROOM_MARGIN} mm"
assert ROOM_B_WIDTH + DIVIDER_THICKNESS < INNER_WIDTH, "No width left for the spare rooms"


with BuildPart() as tray:
    # Outer solid — RectangleRounded gives pre-rounded vertical corners
    with BuildSketch():
        RectangleRounded(TRAY_WIDTH, TRAY_DEPTH, OUTER_VERTICAL_FILLET)
    extrude(amount=TRAY_HEIGHT)

    # Hollow out the cavity from the floor upward, keeping rounded inner corners
    with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
        RectangleRounded(INNER_WIDTH, INNER_DEPTH, CAVITY_CORNER_RADIUS)
    extrude(amount=CAVITY_HEIGHT, mode=Mode.SUBTRACT)

    # Full-width divider between the back rooms and the front rooms
    with Locations(Pos(0, DIVIDER_Y, FLOOR_THICKNESS)):
        Box(
            INNER_WIDTH,
            DIVIDER_THICKNESS,
            CAVITY_HEIGHT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
    # Divider between rooms A and C — back wall down to the full-width divider
    with Locations(Pos(DIVIDER_A_X, DIVIDER_Y, FLOOR_THICKNESS)):
        Box(
            DIVIDER_THICKNESS,
            CAVITY_BACK - DIVIDER_Y,
            CAVITY_HEIGHT,
            align=(Align.CENTER, Align.MIN, Align.MIN),
        )
    # Divider between rooms B and D — front wall up to the full-width divider
    with Locations(Pos(DIVIDER_B_X, CAVITY_FRONT, FLOOR_THICKNESS)):
        Box(
            DIVIDER_THICKNESS,
            DIVIDER_Y - CAVITY_FRONT,
            CAVITY_HEIGHT,
            align=(Align.CENTER, Align.MIN, Align.MIN),
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
