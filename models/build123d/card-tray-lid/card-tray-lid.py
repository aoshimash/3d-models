"""Parametric lid for the card-tray — OVERLAPPING (shoebox) style.

A deep-skirt lid that drops over the tray from above and fully conceals the
tray sides, including the four U-shaped finger notches. Think shoebox lid.
A center through-hole in the top plate lets a fingertip hook into the tray
cavity and lift the lid straight up.

Dimension contract (must match card-tray.py) — if you change the tray, update
the ``TRAY_*`` constants below.

Assembled footprint in the drawer
---------------------------------
- Tray body: 96 × 60 × 22 mm
- Lid outer (with 2 mm skirt walls + 0.3 mm fit clearance per side): ~101 × 65 × 24 mm
- Drawer clearance: 30 mm - 24 mm = 6 mm head-room (lid top is 6 mm below the shelf)

Removal workflow
----------------
Because the skirt runs the full tray height, the lid cannot be lifted off
while the tray sits inside a 30 mm drawer (the skirt needs 22 mm of vertical
clearance to clear the tray). Pull the tray out of the drawer first, then
lift the lid off by hooking a finger through the top hole.

Print notes
-----------
- Orientation: INVERTED for printing. Top plate on the bed, skirt walls rise
  upward (z+). No overhangs. The script already builds the geometry in this
  print-optimal orientation — import the STL and print flat.
- Finger-hole ceiling bridge length = 25 mm, trivially bridgeable at 0.2 mm
  layer height.
"""

from pathlib import Path

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    Circle,
    Mode,
    Plane,
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


# --- Reference: tray dimensions (KEEP IN SYNC with card-tray.py) ---
TRAY_OUTER_WIDTH = 96.0  # mm — tray outer X
TRAY_OUTER_DEPTH = 60.0  # mm — tray outer Y
TRAY_OUTER_CORNER_RADIUS = 3.0  # mm — tray outer vertical corner radius
TRAY_HEIGHT = 22.0  # mm — tray outer Z (= full skirt coverage target)
SHELF_INNER_HEIGHT = 30.0  # mm — drawer constraint (sanity assertion only)

# --- Lid geometry ---
LID_TOP_THICKNESS = 2.0  # mm — ceiling above the tray
SKIRT_THICKNESS = 2.0  # mm — skirt wall thickness (matches tray wall for consistency)
SKIRT_CLEARANCE = 0.3  # mm — per-side gap between skirt inner face and tray outer face
SKIRT_HEIGHT = TRAY_HEIGHT  # mm — full tray height → side notches completely hidden

# --- Grip: through-hole in the lid center ---
GRIP_HOLE_DIAMETER = 25.0  # mm — fingertip enters here to hook & lift

# --- Cosmetic ---
EDGE_FILLET = 0.6  # mm — outer top-plate edge (print first-layer + finger-feel)
SKIRT_TIP_CHAMFER = 0.4  # mm — open end of the skirt (eases slide-on over tray)


# --- Derived ---
LID_OUTER_WIDTH = TRAY_OUTER_WIDTH + 2 * (SKIRT_THICKNESS + SKIRT_CLEARANCE)
LID_OUTER_DEPTH = TRAY_OUTER_DEPTH + 2 * (SKIRT_THICKNESS + SKIRT_CLEARANCE)
LID_OUTER_CORNER_RADIUS = TRAY_OUTER_CORNER_RADIUS + SKIRT_THICKNESS + SKIRT_CLEARANCE

SKIRT_INNER_WIDTH = TRAY_OUTER_WIDTH + 2 * SKIRT_CLEARANCE
SKIRT_INNER_DEPTH = TRAY_OUTER_DEPTH + 2 * SKIRT_CLEARANCE
SKIRT_INNER_CORNER_RADIUS = TRAY_OUTER_CORNER_RADIUS + SKIRT_CLEARANCE

STACK_HEIGHT = TRAY_HEIGHT + LID_TOP_THICKNESS  # skirt is lateral, doesn't add Z
assert STACK_HEIGHT <= SHELF_INNER_HEIGHT, (
    f"Tray + lid stack ({STACK_HEIGHT} mm) exceeds SHELF_INNER_HEIGHT ({SHELF_INNER_HEIGHT} mm)"
)

OUTPUT_PATH = Path(__file__).parent / "output" / "card-tray-lid.stl"


# ---------------------------------------------------------------------------
# Build — in print orientation: top plate on bed (z=0), skirt walls rising +Z.
# (In-use orientation is this, flipped 180°.)
# ---------------------------------------------------------------------------
with BuildPart() as lid:
    # Top plate — full lid footprint, the lid's in-use TOP (in-print BOTTOM on bed)
    with BuildSketch():
        RectangleRounded(LID_OUTER_WIDTH, LID_OUTER_DEPTH, LID_OUTER_CORNER_RADIUS)
    extrude(amount=LID_TOP_THICKNESS)

    # Skirt — annular ring sketched on top of the top plate, extruded upward.
    # A single BuildSketch with outer minus inner gives a hollow frame profile.
    with BuildSketch(Plane.XY.offset(LID_TOP_THICKNESS)):
        RectangleRounded(LID_OUTER_WIDTH, LID_OUTER_DEPTH, LID_OUTER_CORNER_RADIUS)
        RectangleRounded(
            SKIRT_INNER_WIDTH,
            SKIRT_INNER_DEPTH,
            SKIRT_INNER_CORNER_RADIUS,
            mode=Mode.SUBTRACT,
        )
    extrude(amount=SKIRT_HEIGHT)

    # Finger-access through-hole — cuts only the top plate; the skirt interior
    # below is already open so a finger can reach into the tray cavity and hook
    # up on the ring of top-plate surrounding the hole.
    with BuildSketch():
        Circle(GRIP_HOLE_DIAMETER / 2)
    extrude(amount=LID_TOP_THICKNESS, mode=Mode.SUBTRACT)

    # Fillet the in-print bed ring (outer top plate perimeter + finger-hole entry)
    # — improves first-layer adhesion AND gives a friendly rounded edge on the
    # lid's visible top surface in use.
    fillet(
        lid.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
        radius=EDGE_FILLET,
    )
    # Chamfer the open skirt edge (in-print top = in-use bottom): lead-in for
    # dropping the lid over the tray.
    chamfer(
        lid.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
        length=SKIRT_TIP_CHAMFER,
    )


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
export_stl(lid.part, str(OUTPUT_PATH))
print(f"Exported: {OUTPUT_PATH}")

if show is not None:
    try:
        show(lid.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
