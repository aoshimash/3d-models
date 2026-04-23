"""Parametric drawer tray — tiles a 320 × 396 × 20 mm drawer with 2 × 3 identical trays.

Each tray is 159.5 × 131.5 × 20 mm, tiling the drawer with ~1 mm X / ~1.5 mm Y
combined clearance. Footprint fits the Bambu Lab A1 Mini bed (180 × 180 mm) with
plenty of margin.

Three variants are exported in a single run:
  - "none":     single open compartment
  - "halves":   one divider parallel to the long edge (2 compartments, ~155 × ~62 mm)
  - "quarters": cross dividers (4 compartments, ~77 × ~62 mm)

Stacking
--------
The outer bottom edge is chamfered at 45° by FOOT_CHAMFER mm. At Z=0 the footprint
shrinks to (TRAY - 2·FOOT_CHAMFER), tapering back to the full outer by Z=FOOT_CHAMFER.

The chamfer is sized so the foot at Z=0 nests into the cavity mouth of the tray
below: FOOT_CHAMFER = WALL_THICKNESS + FOOT_CLEARANCE_PER_SIDE (2.4 + 0.5 = 2.9 mm).
That gives 0.5 mm per-side lateral clearance when one tray sits on another — loose,
not rigid. Engagement depth is ~1 mm (a 45° taper widens back to full size fast),
which is enough to keep a stack from sliding apart on a desk.

Dividers are shortened by DIVIDER_TOP_GAP (2 mm) so the floor of the stacked tray
doesn't collide with divider tops when nesting. Compartments are 16 mm deep (vs.
the full 18 mm cavity) — still plenty for small desk items.

Drawer fit is unchanged: total tray height is still 20 mm (no features protrude
above the body).

Print notes
-----------
- Orientation: flat on the build plate, foot-down. The chamfer is a 45° outer
  overhang going up-and-out — printable without supports. A brim is recommended
  since the bed-contact face is ~3.4 % smaller per axis than the main body.
- Layer height: 0.2 mm (floor = 10 solid layers for rigidity).
- Infill: 10-15 % gyroid is plenty for desk use.
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


# --- Drawer constraint (mm, reference only) ---
DRAWER_INNER_WIDTH = 320.0  # X — shelf interior width
DRAWER_INNER_DEPTH = 396.0  # Y — shelf interior depth
DRAWER_INNER_HEIGHT = 20.0  # Z — shelf interior height (tray height matches)

# --- Grid layout ---
GRID_COLS = 2  # trays along X (320 / 2 ≈ 160 mm per tray)
GRID_ROWS = 3  # trays along Y (396 / 3 ≈ 132 mm per tray)
X_TOTAL_CLEARANCE = 1.0  # mm — combined X clearance across all 2 columns
Y_TOTAL_CLEARANCE = 1.5  # mm — combined Y clearance across all 3 rows

# --- Outer dimensions (mm) ---
TRAY_WIDTH = (DRAWER_INNER_WIDTH - X_TOTAL_CLEARANCE) / GRID_COLS  # 159.5
TRAY_DEPTH = (DRAWER_INNER_DEPTH - Y_TOTAL_CLEARANCE) / GRID_ROWS  # 131.5
TRAY_HEIGHT = DRAWER_INNER_HEIGHT  # 20.0 — matches drawer internal height exactly

# --- Walls & floor (mm) ---
WALL_THICKNESS = 2.4  # exterior walls: 6 perimeters at 0.4 mm nozzle
DIVIDER_THICKNESS = 2.0  # internal dividers
DIVIDER_TOP_GAP = 2.0  # gap from divider top to cavity top; leaves room for the
#                       stacked tray's floor to settle without hitting the divider
#                       (max sink due to FOOT_CHAMFER is ~1.1 mm, so 2 mm is safe)
FLOOR_THICKNESS = 2.0  # 10 solid layers at 0.2 mm

# --- Stacking foot (mm) ---
# To let the bottom of one tray nest into the cavity of another, the bottom
# outline must shrink by at least WALL_THICKNESS per side (otherwise the foot is
# still wider than the cavity inner) plus a small clearance. The chamfer is 45°
# (symmetric length), so it also sets how tall the tapered region is.
FOOT_CLEARANCE_PER_SIDE = 0.5  # mm — lateral gap between foot and cavity inner wall
FOOT_CHAMFER = WALL_THICKNESS + FOOT_CLEARANCE_PER_SIDE  # 2.9

# --- Fillets / chamfers (mm) ---
OUTER_VERTICAL_FILLET = 5.0  # softly rounded outer vertical corners
TOP_CHAMFER = 0.6  # top-rim bevel (doubles as lead-in on the cavity mouth for
#                    the foot of the tray stacked above)
INNER_FLOOR_FILLET = 0.8  # cavity floor / wall junction — kept modest because the
#                           outer wall is only ~1.5 mm thick at Z=FLOOR_THICKNESS
#                           (the foot chamfer is still tapering there)

# --- Derived dimensions ---
INNER_WIDTH = TRAY_WIDTH - 2 * WALL_THICKNESS  # 154.7
INNER_DEPTH = TRAY_DEPTH - 2 * WALL_THICKNESS  # 126.7
CAVITY_HEIGHT = TRAY_HEIGHT - FLOOR_THICKNESS  # 18.0
DIVIDER_HEIGHT = CAVITY_HEIGHT - DIVIDER_TOP_GAP  # 16.0
CAVITY_CORNER_RADIUS = max(OUTER_VERTICAL_FILLET - WALL_THICKNESS, 0.5)
FOOT_WIDTH = TRAY_WIDTH - 2 * FOOT_CHAMFER  # 153.7 — outline at Z=0 (bed contact)
FOOT_DEPTH = TRAY_DEPTH - 2 * FOOT_CHAMFER  # 125.7

OUTPUT_DIR = Path(__file__).parent / "output"
VARIANTS = ("none", "halves", "quarters")


# ---------------------------------------------------------------------------
# Learning Mode — YOUR CONTRIBUTION lives below.
# Decide which dividers to add for each variant.
# ---------------------------------------------------------------------------
def _divider_orientations(variant: str) -> list[str]:
    """Return the list of divider orientations to add for the given variant.

    Each orientation is one of:
      - "long":  divider runs parallel to the long edge (X-axis). Its length =
                 INNER_WIDTH, thickness = DIVIDER_THICKNESS in Y. It splits the
                 cavity along Y → 2 compartments of ~INNER_WIDTH × INNER_DEPTH/2.
      - "short": divider runs parallel to the short edge (Y-axis). Its length =
                 INNER_DEPTH, thickness = DIVIDER_THICKNESS in X. It splits the
                 cavity along X → 2 compartments of ~INNER_WIDTH/2 × INNER_DEPTH.

    Returning multiple orientations draws multiple dividers. They are unioned, so
    the overlap at the center (DIVIDER_THICKNESS × DIVIDER_THICKNESS column) is
    handled automatically — no special intersection logic needed.

    Variants to support (per the request):
      - "none":     no dividers → single open compartment
      - "halves":   split along the long edge → one "long" divider
      - "quarters": cross → one "long" + one "short" divider

    Raise ValueError on an unknown variant so typos surface loudly instead of
    silently producing an undivided tray.
    """
    mapping = {
        "none": [],
        "halves": ["long"],
        "quarters": ["long", "short"],
    }
    if variant not in mapping:
        raise ValueError(f"Unknown variant: {variant!r}. Expected one of {sorted(mapping)}.")
    return mapping[variant]


def build_tray(variant: str) -> BuildPart:
    """Build the tray for the given variant. Returns the BuildPart context."""
    with BuildPart() as tray:
        # --- Main outer solid (pre-rounded vertical corners) ---
        with BuildSketch():
            RectangleRounded(TRAY_WIDTH, TRAY_DEPTH, OUTER_VERTICAL_FILLET)
        extrude(amount=TRAY_HEIGHT)

        # --- Hollow the cavity from the floor upward ---
        with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
            RectangleRounded(INNER_WIDTH, INNER_DEPTH, CAVITY_CORNER_RADIUS)
        extrude(amount=CAVITY_HEIGHT, mode=Mode.SUBTRACT)

        # --- Dividers (variant-dependent). Height is CAVITY_HEIGHT minus
        #     DIVIDER_TOP_GAP so the stacked tray's floor doesn't collide with
        #     divider tops when nesting. ---
        for orientation in _divider_orientations(variant):
            with Locations(Pos(0, 0, FLOOR_THICKNESS)):
                if orientation == "long":
                    Box(
                        INNER_WIDTH,
                        DIVIDER_THICKNESS,
                        DIVIDER_HEIGHT,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
                elif orientation == "short":
                    Box(
                        DIVIDER_THICKNESS,
                        INNER_DEPTH,
                        DIVIDER_HEIGHT,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
                else:
                    raise ValueError(f"Unknown divider orientation: {orientation!r}")

        # --- Cavity floor / wall junction fillet (must go before any chamfer
        #     that shifts the Z=FLOOR_THICKNESS edge group) ---
        fillet(
            tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[1],
            radius=INNER_FLOOR_FILLET,
        )

        # --- Top rim chamfer (applies to outer top + cavity top inner — the
        #     cavity-top bevel acts as a lead-in for the stacked tray's foot) ---
        chamfer(
            tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
            length=TOP_CHAMFER,
        )

        # --- Foot chamfer on the outer bottom edge: shrinks the bed-contact
        #     footprint so the tray nests into the cavity of the tray below ---
        chamfer(
            tray.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
            length=FOOT_CHAMFER,
        )

    return tray


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
for _variant in VARIANTS:
    _tray = build_tray(_variant)
    _out = OUTPUT_DIR / f"drawer-tray-{_variant}.stl"
    export_stl(_tray.part, str(_out))
    print(f"Exported: {_out}")

if show is not None:
    try:
        show(build_tray("quarters").part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
