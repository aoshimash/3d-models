"""Toothbrush stand with a drainage mesh base.

The cavity is the specification: a Phi 50 bore, 66 mm tall, which is the usual
size for a bathroom toothbrush cup. Wall thickness carries no requirement, so
INNER_DIAMETER drives the model and the outer diameter is merely a consequence
(Phi 50 bore + 2 x 2 mm wall = Phi 54 outside). Change the wall and the storage
size stays put.

Drainage
--------
Plastic cannot absorb water, so the floor is a square-grid mesh raised above the
counter by a plenum. Water falls through the mesh, crosses the plenum and exits
through notches cut around the bottom of the wall. About half the bore area is
open: the grid is trimmed by a circle rather than stopped at the last whole
square, so the outermost openings are chords and only a MESH_RIM-wide solid
ring is left against the wall.

The mesh is held up by a pillar under every rib intersection. Those pillars are
what makes this printable: without them the first mesh layer would be a single
50 mm bridge across the bore, but with them each bridge spans only one grid
pitch (~6.5 mm). The same pillars double as feet, keeping air under the mesh.

Print notes
-----------
- Orientation: upright, open end up, mesh on the build plate. No supports.
- The pillars are the only bed contact inside the bore; keep a brim off unless
  adhesion is poor (a brim between pillars is annoying to remove).
- Layer height: 0.2 mm. Set the slicer to 5 perimeters so the 2 mm wall comes
  out solid rather than as two skins around a sliver of infill.
- Infill barely matters — almost everything here is perimeter.
- Bed margin: 54 mm part on a 180 mm A1 Mini plate.
"""

from math import ceil, hypot
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Locations,
    Mode,
    Plane,
    PolarLocations,
    Pos,
    Rectangle,
    chamfer,
    export_stl,
    extrude,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Cavity (mm) — the specification; everything else is derived from it ---
INNER_DIAMETER = 50.0  # X/Y — bore, holds a family's worth of brushes
HEIGHT = 66.0  # Z — overall height, leaving 61 mm of usable depth

# --- Walls (mm) ---
WALL_THICKNESS = 2.0  # 5 perimeters at 0.4 mm nozzle — a closed tube is stiff, thin is fine

# --- Drainage mesh floor (mm) ---
PLENUM_HEIGHT = 3.0  # gap between counter and mesh underside — the water escape route
MESH_THICKNESS = 2.0  # 10 layers at 0.2 mm — stiff enough to carry brushes
GRID_PITCH = 6.5  # rib center-to-center spacing
RIB_WIDTH = 1.6  # 4 perimeters at 0.4 mm nozzle
MESH_RIM = 1.2  # solid ring at the wall — 3 perimeters, the project minimum
MIN_HOLE_BITE = 0.0  # extra guard band inside the clip circle; 0 is already sliver-free

# --- Support pillars / feet (mm) ---
PILLAR_SIZE = 2.0  # square footprint under each rib intersection
PILLAR_EDGE_CLEARANCE = 2.5  # keep pillars clear of the wall notches

# --- Wall drainage notches (mm) ---
NOTCH_COUNT = 8  # openings around the bottom of the wall
NOTCH_WIDTH = 8.0  # chord width of each opening — keeps ~60 % of the rim on the bed

# --- Edge treatment (mm) ---
TOP_CHAMFER = 0.8  # softens the rim on both the inside and outside faces

OUTPUT_PATH = Path(__file__).parent / "output" / "toothbrush-stand.stl"


# --- Derived geometry ---
INNER_RADIUS = INNER_DIAMETER / 2
OUTER_RADIUS = INNER_RADIUS + WALL_THICKNESS
MESH_BOTTOM = PLENUM_HEIGHT
MESH_TOP = MESH_BOTTOM + MESH_THICKNESS
HOLE_SIZE = GRID_PITCH - RIB_WIDTH  # square opening between ribs
CLIP_RADIUS = INNER_RADIUS - MESH_RIM  # hole pattern is trimmed to this circle


def _grid_coordinates(pitch: float, span: float) -> list[float]:
    """Symmetric 1-D grid centers covering at least `span`, centered on 0."""
    count = ceil(span / pitch) + 1
    return [(i - (count - 1) / 2) * pitch for i in range(count)]


def _mesh_hole_positions() -> list[tuple[float, float]]:
    """Centers of the openings cut through the mesh floor.

    The pattern runs all the way out to CLIP_RADIUS and the squares that cross
    it are trimmed by the clip circle, so the outermost openings are chords
    rather than squares. That is deliberate — a partial opening still drains,
    and stopping at the last *whole* square would waste an annulus several
    millimetres wide.

    The one thing to avoid is a cell that merely grazes the circle and leaves a
    hair-thin opening. Keeping only cells whose *center* is inside the circle
    already rules that out: the worst case is a center sitting exactly on the
    circle, which still leaves roughly half a square, HOLE_SIZE / 2 wide. So
    MIN_HOLE_BITE exists only as a knob for a wider solid rim, and 0 is safe.
    """
    limit = CLIP_RADIUS - MIN_HOLE_BITE
    axis = _grid_coordinates(GRID_PITCH, 2 * INNER_RADIUS)
    return [(x, y) for x in axis for y in axis if hypot(x, y) <= limit]


def _pillar_positions() -> list[tuple[float, float]]:
    """Centers of the mesh support pillars — the rib intersections.

    Rib intersections sit exactly half a pitch off the hole centers, so this is
    the hole grid shifted by GRID_PITCH / 2 in both axes.
    """
    limit = INNER_RADIUS - PILLAR_EDGE_CLEARANCE
    axis = [c + GRID_PITCH / 2 for c in _grid_coordinates(GRID_PITCH, 2 * INNER_RADIUS)]
    return [(x, y) for x in axis for y in axis if hypot(x, y) <= limit]


HOLE_POSITIONS = _mesh_hole_positions()
PILLAR_POSITIONS = _pillar_positions()


with BuildPart() as stand:
    # Solid blank for the whole cup
    Cylinder(OUTER_RADIUS, HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Bore — everything above the mesh floor
    with Locations(Pos(0, 0, MESH_TOP)):
        Cylinder(
            INNER_RADIUS,
            HEIGHT - MESH_TOP,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # Plenum — the drainage gap under the mesh floor
    Cylinder(
        INNER_RADIUS,
        PLENUM_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT,
    )

    # Put the pillars back into the plenum so the mesh has something to sit on
    with Locations(*[Pos(x, y, 0) for x, y in PILLAR_POSITIONS]):
        Box(
            PILLAR_SIZE,
            PILLAR_SIZE,
            PLENUM_HEIGHT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

    # Perforate the mesh floor. Laying the pattern out in 2D first lets the clip
    # circle trim the outermost squares into chords, which pushes the openings
    # right up to a rim of constant MESH_RIM width.
    with BuildSketch(Plane.XY.offset(MESH_BOTTOM)):
        with Locations(*HOLE_POSITIONS):
            Rectangle(HOLE_SIZE, HOLE_SIZE)
        Circle(CLIP_RADIUS, mode=Mode.INTERSECT)
    extrude(amount=MESH_THICKNESS, mode=Mode.SUBTRACT)

    # Side exits: notch the wall over the full plenum height so water runs out
    # instead of pooling on the counter under the stand.
    with PolarLocations(OUTER_RADIUS, NOTCH_COUNT):
        Box(
            2 * WALL_THICKNESS + 2.0,  # overshoot both wall faces for a clean cut
            NOTCH_WIDTH,
            PLENUM_HEIGHT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # Break the top rim on both faces — comfortable to grab, hides layer lines
    chamfer(
        stand.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
        length=TOP_CHAMFER,
    )


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
export_stl(stand.part, str(OUTPUT_PATH))
print(f"Exported: {OUTPUT_PATH}")
print(f"  bore: Phi {2 * INNER_RADIUS:.1f} mm x {HEIGHT - MESH_TOP:.1f} mm deep")
print(
    f"  mesh: {len(HOLE_POSITIONS)} openings up to {HOLE_SIZE:.1f} mm "
    f"(clipped at r={CLIP_RADIUS:.1f}), {len(PILLAR_POSITIONS)} pillars"
)

if show is not None:
    try:
        show(stand.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
