"""Two sliding trays and the open-front box that holds them, one above the other.

Each tray is 160 x 100 x 20 mm (outer). A finger notch in its front wall sits
under a matching scoop in the box's shelf / top plate, so a fingertip can hook
the low lip that remains even though the tray ends flush with the box front.

Print notes
-----------
- Print two copies of tray.stl and one copy of box.stl.
- Tray: flat on the build plate, floor down. No supports.
- Box: back wall down, open front up (the STL is exported this way). All walls
  rise straight and every cut-out is open toward the top, so no supports.
- Box: enable a 5 mm brim. The part is ~102 mm tall on a narrow footprint, and
  the width leaves ~8 mm of plate on each side for it.
- Layer height: 0.2 mm.
"""

from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Location,
    Locations,
    Mode,
    Plane,
    RectangleRounded,
    chamfer,
    export_stl,
    extrude,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Build volume (mm, Bambu Lab A1 Mini) ---
BUILD_SIZE = 180.0  # usable X / Y / Z
BRIM_WIDTH = 5.0  # brim that must still fit around the box on the plate

# --- Tray, outer (mm) ---
TRAY_WIDTH = 160.0  # X - side to side
TRAY_DEPTH = 100.0  # Y - front to back
TRAY_HEIGHT = 20.0  # Z - floor underside to rim
TRAY_WALL = 1.6  # side walls: 4 perimeters at 0.4 mm nozzle
TRAY_FLOOR = 1.6  # 8 solid layers at 0.2 mm
TRAY_CORNER_RADIUS = 3.0  # outer vertical corners
TRAY_BOTTOM_CHAMFER = 0.4  # absorbs first-layer flare so the tray slides cleanly

# --- Finger notch in the tray's front wall (mm) ---
NOTCH_WIDTH = 30.0  # X - room for one fingertip
NOTCH_DEPTH = 9.0  # Z - measured down from the rim; leaves an 11 mm lip to hook
NOTCH_RADIUS = 3.0  # rounded lower corners

# --- Box (mm) ---
SLIDE_CLEARANCE = 0.3  # per side, sliding fit between tray and slot
BACK_CLEARANCE = 0.5  # tray back to box back wall; tray ends just inside the front
BOX_WALL = 1.6  # top, bottom, side and back walls
SHELF_THICKNESS = 2.0  # between the two slots; thicker because its front edge is free
BOX_CORNER_RADIUS = 2.0  # outer edges along the slide direction

# --- Finger scoop in the box's shelf and top plate (mm) ---
SCOOP_WIDTH = NOTCH_WIDTH  # X - lines up with the tray notch
SCOOP_DEPTH = 6.0  # Y - back from the box front; lets a fingertip pass behind the tray wall
SCOOP_RADIUS = 3.0  # rounded inner corners

# --- Derived box dimensions (mm) ---
SLOT_WIDTH = TRAY_WIDTH + 2 * SLIDE_CLEARANCE  # X
SLOT_HEIGHT = TRAY_HEIGHT + 2 * SLIDE_CLEARANCE  # Z
SLOT_DEPTH = TRAY_DEPTH + BACK_CLEARANCE  # Y
LOWER_SLOT_Z = BOX_WALL  # underside of the lower slot
SHELF_Z = LOWER_SLOT_Z + SLOT_HEIGHT  # underside of the shelf
UPPER_SLOT_Z = SHELF_Z + SHELF_THICKNESS  # underside of the upper slot
BOX_WIDTH = SLOT_WIDTH + 2 * BOX_WALL  # X
BOX_DEPTH = SLOT_DEPTH + BOX_WALL  # Y
BOX_HEIGHT = UPPER_SLOT_Z + SLOT_HEIGHT + BOX_WALL  # Z

CUT_OVERRUN = 1.0  # extends cutting tools past a face to avoid coplanar booleans

# --- Sanity checks ---
assert TRAY_WIDTH <= BUILD_SIZE, "Tray exceeds A1 Mini bed"
assert TRAY_DEPTH <= BUILD_SIZE, "Tray exceeds A1 Mini bed"
assert BOX_WIDTH + 2 * BRIM_WIDTH <= BUILD_SIZE, "Box and brim exceed A1 Mini bed"
assert BOX_DEPTH <= BUILD_SIZE, "Box exceeds A1 Mini build height"

OUTPUT_DIR = Path(__file__).parent / "output"


def build_tray():
    """Build one tray: X centered, front wall at -Y, floor underside at Z=0."""
    with BuildPart() as tray:
        with BuildSketch():
            RectangleRounded(TRAY_WIDTH, TRAY_DEPTH, TRAY_CORNER_RADIUS)
        extrude(amount=TRAY_HEIGHT)
        chamfer(tray.faces().sort_by(Axis.Z)[0].edges(), TRAY_BOTTOM_CHAMFER)

        with BuildSketch(Plane.XY.offset(TRAY_FLOOR)):
            RectangleRounded(
                TRAY_WIDTH - 2 * TRAY_WALL,
                TRAY_DEPTH - 2 * TRAY_WALL,
                TRAY_CORNER_RADIUS - TRAY_WALL,
            )
        extrude(amount=TRAY_HEIGHT - TRAY_FLOOR + CUT_OVERRUN, mode=Mode.SUBTRACT)

        # Centered on the rim so only its rounded lower half cuts the wall.
        # Plane.XZ faces -Y, so a negative extrude runs toward the tray interior.
        with BuildSketch(Plane.XZ.offset(TRAY_DEPTH / 2 + CUT_OVERRUN)):
            with Locations((0, TRAY_HEIGHT)):
                RectangleRounded(NOTCH_WIDTH, 2 * NOTCH_DEPTH, NOTCH_RADIUS)
        extrude(amount=-(TRAY_WALL + 2 * CUT_OVERRUN), mode=Mode.SUBTRACT)
    return tray.part


def build_box():
    """Build the box in use position: X centered, open front at Y=0, base at Z=0."""
    with BuildPart() as box:
        with BuildSketch(Plane.XZ):
            with Locations((0, BOX_HEIGHT / 2)):
                RectangleRounded(BOX_WIDTH, BOX_HEIGHT, BOX_CORNER_RADIUS)
        extrude(amount=-BOX_DEPTH)

        for slot_z in (LOWER_SLOT_Z, UPPER_SLOT_Z):
            with Locations((0, -CUT_OVERRUN, slot_z)):
                Box(
                    SLOT_WIDTH,
                    SLOT_DEPTH + CUT_OVERRUN,
                    SLOT_HEIGHT,
                    align=(Align.CENTER, Align.MIN, Align.MIN),
                    mode=Mode.SUBTRACT,
                )

        # Runs from the shelf underside up through the top, leaving the box floor whole.
        with BuildSketch(Plane.XY.offset(SHELF_Z)):
            RectangleRounded(SCOOP_WIDTH, 2 * SCOOP_DEPTH, SCOOP_RADIUS)
        extrude(amount=BOX_HEIGHT - SHELF_Z + CUT_OVERRUN, mode=Mode.SUBTRACT)
    return box.part


def to_print_orientation(box_part):
    """Stand the box on its back wall, with the open front facing up."""
    return Location((0, 0, BOX_DEPTH)) * (Location((0, 0, 0), (-90, 0, 0)) * box_part)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    tray = build_tray()
    box = build_box()
    export_stl(tray, str(OUTPUT_DIR / "tray.stl"))
    export_stl(to_print_orientation(box), str(OUTPUT_DIR / "box.stl"))
    print(f"Tray: {TRAY_WIDTH} x {TRAY_DEPTH} x {TRAY_HEIGHT} mm")
    print(f"Box:  {BOX_WIDTH:.1f} x {BOX_DEPTH:.1f} x {BOX_HEIGHT:.1f} mm")
    if show is not None:
        try:
            show(tray, box)
        except Exception:
            pass  # no viewer running


if __name__ == "__main__":
    main()
