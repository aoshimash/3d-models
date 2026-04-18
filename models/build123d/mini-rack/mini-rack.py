"""Two-tier mini rack — hardware-free (printed tapered press-fit pegs).

Plan B variant: no bolts, no nuts, no tools. Post ends have tapered round pegs
that press-fit into matching straight holes in the shelves. Tip is slip-fit for
easy entry; base has interference for friction grip. Assembly is effectively
permanent after full insertion.

Components
----------
- shelf.stl : thick plate with 4 corner through-holes (print 2x)
- post.stl  : hollow square post with tapered pegs on each end (print 4x)
- assembly-preview.stl : full rack for visualization only (do NOT print)

Assembly
--------
1. Lay a shelf flat, tapered-tip-first insert 4 posts into corner holes.
2. Press each post fully home (use a flat surface + hand pressure, or tap with
   a soft mallet on the upper post shoulder).
3. Align the second shelf on top of the 4 upward-facing pegs.
4. Press the second shelf down evenly until it seats on the post shoulders.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Compound,
    Cone,
    Cylinder,
    Locations,
    Mode,
    Pos,
    RectangleRounded,
    export_stl,
    extrude,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Shelf parameters (mm) ---
SHELF_WIDTH = 120.0  # X/Y size (square)
SHELF_THICKNESS = 6.0  # thick enough to fully receive the tapered peg
SHELF_CORNER_FILLET = 6.0  # outer corner rounding

# --- Post parameters (mm) ---
POST_SECTION = 14.0  # outer square side
POST_WALL = 2.2  # wall thickness
POST_BODY_HEIGHT = 70.0  # square body length (between shelf shoulders)
POST_RIB_THICKNESS = 1.2  # internal cross rib thickness

# --- Shoulder (flat disc that seats on the shelf face) ---
SHOULDER_DIA = POST_SECTION  # same as post section — acts as transition to round peg
SHOULDER_HEIGHT = 2.0  # flat seat between body and peg base

# --- Press-fit peg parameters (THE CRITICAL FIT) ---
PEG_LENGTH = SHELF_THICKNESS  # peg equals shelf thickness → buried flush with far face
PEG_BASE_DIA = 9.2  # at shoulder (larger — interference with hole)
PEG_TIP_DIA = 8.6  # at tip (smaller — slip-fit entry)
SHELF_HOLE_DIA = 9.0  # straight through-hole in shelf

# Interference summary (per diameter, not per side):
#   at tip:  9.0 - 8.6 = +0.4 mm slip (easy entry)
#   at base: 9.2 - 9.0 = -0.2 mm interference (press fit, ~0.1 mm per side)
# A1 Mini typical FDM tolerance is +/-0.15 mm; tune PEG_BASE_DIA if fit is wrong.

# --- Layout ---
POST_INSET = 10.0  # post center measured from shelf edge
_half = SHELF_WIDTH / 2 - POST_INSET
POST_POSITIONS: list[tuple[float, float]] = [
    (-_half, -_half),
    (_half, -_half),
    (-_half, _half),
    (_half, _half),
]

OUTPUT_DIR = Path(__file__).parent / "output"


# ---------------------------------------------------------------------------
# Shelf: flat rounded-corner plate with 4 corner holes
# ---------------------------------------------------------------------------
with BuildPart() as shelf_builder:
    with BuildSketch() as sk:
        RectangleRounded(SHELF_WIDTH, SHELF_WIDTH, SHELF_CORNER_FILLET)
        with Locations(*[Pos(x, y) for x, y in POST_POSITIONS]):
            Circle(radius=SHELF_HOLE_DIA / 2, mode=Mode.SUBTRACT)
    extrude(amount=SHELF_THICKNESS)

shelf_part = shelf_builder.part


# ---------------------------------------------------------------------------
# Post: hollow square tube + cross rib + shoulders + tapered pegs (both ends)
# ---------------------------------------------------------------------------
with BuildPart() as post_builder:
    # Square hollow body (centered on origin vertically)
    Box(
        POST_SECTION,
        POST_SECTION,
        POST_BODY_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    _inner = POST_SECTION - 2 * POST_WALL
    Box(
        _inner,
        _inner,
        POST_BODY_HEIGHT + 1,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
        mode=Mode.SUBTRACT,
    )
    # Cross ribs inside
    Box(
        POST_SECTION,
        POST_RIB_THICKNESS,
        POST_BODY_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    Box(
        POST_RIB_THICKNESS,
        POST_SECTION,
        POST_BODY_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )

    # Shoulders (flat discs at each end of body)
    for z_sign in (-1, 1):
        z_center = z_sign * (POST_BODY_HEIGHT / 2 + SHOULDER_HEIGHT / 2)
        with Locations(Pos(0, 0, z_center)):
            Cylinder(
                radius=SHOULDER_DIA / 2,
                height=SHOULDER_HEIGHT,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            )

    # Tapered pegs (Cone from base to tip)
    # Top peg:    base at z = +(H/2 + SHOULDER_HEIGHT), tip at +(... + PEG_LENGTH)
    # Bottom peg: base at z = -(H/2 + SHOULDER_HEIGHT), tip at -(... + PEG_LENGTH)
    shoulder_outer_z = POST_BODY_HEIGHT / 2 + SHOULDER_HEIGHT
    # Top peg: base_radius at bottom of cone, tip_radius at top
    with Locations(Pos(0, 0, shoulder_outer_z)):
        Cone(
            bottom_radius=PEG_BASE_DIA / 2,
            top_radius=PEG_TIP_DIA / 2,
            height=PEG_LENGTH,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
    # Bottom peg: mirrored — base at shoulder (top of cone), tip pointing down
    with Locations(Pos(0, 0, -shoulder_outer_z)):
        Cone(
            bottom_radius=PEG_TIP_DIA / 2,
            top_radius=PEG_BASE_DIA / 2,
            height=PEG_LENGTH,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        )

post_part = post_builder.part


# ---------------------------------------------------------------------------
# Assembly preview (visualization only)
# ---------------------------------------------------------------------------
# Geometry of assembled stack (z = 0 is underside of bottom shelf):
#   bottom shelf : z = 0 .. SHELF_THICKNESS
#   lower peg    : tip at z = 0 (buried in shelf), shoulder top at z = SHELF_THICKNESS
#   post body    : z = SHELF_THICKNESS + SHOULDER_HEIGHT .. ... + POST_BODY_HEIGHT
#   upper peg    : extends above post body by SHOULDER_HEIGHT + PEG_LENGTH
#   top shelf    : sits on upper shoulder face, pegs buried inside
bottom_shelf = Pos(0, 0, 0) * shelf_part
post_center_z = PEG_LENGTH + SHOULDER_HEIGHT + POST_BODY_HEIGHT / 2
posts_in_assembly = [Pos(x, y, post_center_z) * post_part for x, y in POST_POSITIONS]
top_shoulder_face_z = post_center_z + POST_BODY_HEIGHT / 2 + SHOULDER_HEIGHT
top_shelf = Pos(0, 0, top_shoulder_face_z) * shelf_part

assembly = Compound(label="mini-rack", children=[bottom_shelf, top_shelf, *posts_in_assembly])


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
export_stl(shelf_part, str(OUTPUT_DIR / "shelf.stl"))
export_stl(post_part, str(OUTPUT_DIR / "post.stl"))
export_stl(assembly, str(OUTPUT_DIR / "assembly-preview.stl"))
print(f"Exported shelf / post / assembly-preview to: {OUTPUT_DIR}")


if show is not None:
    try:
        show(assembly)
    except Exception as e:
        print(f"(ocp_vscode viewer not connected: {e})")
