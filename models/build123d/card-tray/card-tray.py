"""Parametric business card tray — fits a 30 mm (3 cm) tall drawer, orientation-agnostic.

Stores ~50 business cards (≈ credit-card sized, 91×55 mm standard JP meishi) stacked
loose inside a shallow open-top tray. The tray is designed to sit inside a drawer
regardless of orientation (long or short edge against the drawer wall). All four
walls carry a finger notch reaching down to the cavity floor so any card — including
the bottom one — can be pinched and lifted from any side.

Print notes
-----------
- Orientation: flat on the build plate (bottom face on bed). No supports required.
- Layer height: 0.2 mm (floor = 10 solid layers for rigidity).
- Infill: 15 % gyroid is plenty for desk use.
- Footprint (~96 × 60 × 22 mm) fits trivially on the A1 Mini's 180 × 180 mm bed.
"""

from pathlib import Path

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    Circle,
    Locations,
    Mode,
    Plane,
    Rectangle,
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


# --- Card spec (Japanese business card ≈ credit-card size) ---
CARD_WIDTH = 91.0  # mm — long edge (standard JP meishi; use 85.6 for strict credit card)
CARD_DEPTH = 55.0  # mm — short edge (use 54.0 for strict credit card)
CARD_COUNT = 50  # number of cards to store in the stack
CARD_THICKNESS = 0.3  # mm — typical business card paper

# --- Fit ---
FIT_TOLERANCE = 0.5  # mm — per-side clearance so the card stack slides freely

# --- Shelf / drawer constraint ---
SHELF_INNER_HEIGHT = 30.0  # mm — internal height of the drawer/shelf
VERTICAL_CLEARANCE = 2.0  # mm — empty space above the tray inside the drawer

# --- Tray walls ---
WALL_THICKNESS = 2.0  # mm — 5 perimeters at 0.4 mm nozzle
FLOOR_THICKNESS = 2.0  # mm — 10 solid layers at 0.2 mm
TOP_MARGIN = 5.0  # mm — head-room above the card stack for easy drop-in / top-grab

# --- Finger notches (4 total: U-shaped opening on each wall) ---
NOTCH_WIDTH = 20.0  # mm — width of the U (same on all 4 walls)
NOTCH_FLOOR_LIFT = 0.0  # mm — notch bottom raise above cavity floor (0 = reach bottom card)

# --- Cosmetic ---
OUTER_CORNER_RADIUS = 3.0  # mm — soft outer vertical corner rounding
TOP_CHAMFER = 0.4  # mm — small bevel on top rim
BOTTOM_FILLET = 0.6  # mm — first-layer adhesion on outer bed-contact perimeter


# --- Derived dimensions ---
STACK_HEIGHT = CARD_COUNT * CARD_THICKNESS
INNER_HEIGHT = STACK_HEIGHT + TOP_MARGIN
TRAY_HEIGHT = INNER_HEIGHT + FLOOR_THICKNESS
assert TRAY_HEIGHT + VERTICAL_CLEARANCE <= SHELF_INNER_HEIGHT, (
    f"TRAY_HEIGHT ({TRAY_HEIGHT} mm) + VERTICAL_CLEARANCE ({VERTICAL_CLEARANCE} mm) "
    f"exceeds SHELF_INNER_HEIGHT ({SHELF_INNER_HEIGHT} mm)"
)

TRAY_WIDTH = CARD_WIDTH + 2 * (WALL_THICKNESS + FIT_TOLERANCE)
TRAY_DEPTH = CARD_DEPTH + 2 * (WALL_THICKNESS + FIT_TOLERANCE)
CAVITY_WIDTH = CARD_WIDTH + 2 * FIT_TOLERANCE
CAVITY_DEPTH = CARD_DEPTH + 2 * FIT_TOLERANCE
CAVITY_CORNER_RADIUS = max(OUTER_CORNER_RADIUS - WALL_THICKNESS, 0.5)

NOTCH_BOTTOM_Z = FLOOR_THICKNESS + NOTCH_FLOOR_LIFT  # z of the notch lower edge
NOTCH_HEIGHT = TRAY_HEIGHT - NOTCH_BOTTOM_Z  # full wall-height opening from notch floor to top
NOTCH_CENTER_Z = NOTCH_BOTTOM_Z + NOTCH_HEIGHT / 2

OUTPUT_PATH = Path(__file__).parent / "output" / "card-tray.stl"


# ---------------------------------------------------------------------------
# Learning Mode — YOUR CONTRIBUTION lives below.
# Customize finger_notch_profile() to shape the 4 finger-access notches.
# ---------------------------------------------------------------------------
def finger_notch_profile(notch_width: float, notch_height: float) -> None:
    """Draw a U-shaped finger notch profile in the active BuildSketch.

    Flat-top / semicircular-bottom. Composed as a rectangle (upper body) unioned
    with a full circle at the bottom (only its lower half is visible after union;
    the upper half is absorbed by the rectangle). Caller's active location is
    the geometric CENTER of the notch.
    """
    r = notch_width / 2
    # Upper rectangular body — top at +h/2, bottom at center of the circle (y = r - h/2)
    with Locations((0, r / 2)):
        Rectangle(notch_width, notch_height - r)
    # Rounded bottom — full circle; top half overlaps rectangle harmlessly
    with Locations((0, -notch_height / 2 + r)):
        Circle(r)


# ---------------------------------------------------------------------------
# Tray build
# ---------------------------------------------------------------------------
with BuildPart() as tray:
    # Outer solid — RectangleRounded gives pre-rounded vertical corners
    with BuildSketch():
        RectangleRounded(TRAY_WIDTH, TRAY_DEPTH, OUTER_CORNER_RADIUS)
    extrude(amount=TRAY_HEIGHT)

    # Hollow out cavity for the card stack
    with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
        RectangleRounded(CAVITY_WIDTH, CAVITY_DEPTH, CAVITY_CORNER_RADIUS)
    extrude(amount=INNER_HEIGHT, mode=Mode.SUBTRACT)

    # Outer bed-contact fillet (first-layer adhesion) — do BEFORE notch cuts
    # so edge selection by Z-group is unambiguous.
    fillet(
        tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
        radius=BOTTOM_FILLET,
    )
    # Top-rim chamfer — done before notch cuts so only outer + cavity-inner top
    # edges are present (notch edges will be clean straight cuts after).
    chamfer(
        tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
        length=TOP_CHAMFER,
    )

    # Long-wall finger notches — front + back cut in one through-extrude along Y
    with BuildSketch(Plane.XZ):
        with Locations((0, NOTCH_CENTER_Z)):
            finger_notch_profile(NOTCH_WIDTH, NOTCH_HEIGHT)
    extrude(amount=TRAY_DEPTH / 2 + 1, both=True, mode=Mode.SUBTRACT)

    # Short-wall finger notches — left + right cut in one through-extrude along X
    with BuildSketch(Plane.YZ):
        with Locations((0, NOTCH_CENTER_Z)):
            finger_notch_profile(NOTCH_WIDTH, NOTCH_HEIGHT)
    extrude(amount=TRAY_WIDTH / 2 + 1, both=True, mode=Mode.SUBTRACT)


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
export_stl(tray.part, str(OUTPUT_PATH))
print(f"Exported: {OUTPUT_PATH}")

if show is not None:
    try:
        show(tray.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
