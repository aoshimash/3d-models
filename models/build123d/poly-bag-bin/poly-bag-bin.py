"""140 mm cube waste bin with a drop-in frame that holds a poly bag.

Two parts:

- **bin** — open-top box, 140 x 140 x 137 mm, rounded vertical corners.
- **frame** — a short ring that drops into the mouth. Its 3 mm flange rests on the
  rim, so bin + frame is exactly 140 x 140 x 140 mm.

How the bag is held
-------------------
Drape the bag over the rim, drop the frame in. The bag is trapped in the fold over
the rim, under the flange; the skirt keeps the mouth pulled tight to the wall and
hides the bag edge.

Nothing here clamps. A bin liner carries almost no weight, so the frame only has
to stay put and stop the bag slipping in — and a clearance fit is what makes it
lift straight out again. The skirt runs at SKIRT_CLEARANCE per side all round,
which is loose enough to drop in one-handed but close enough that the bag cannot
billow into the gap. For a firmer hold, make SKIRT_CLEARANCE negative and it
becomes a press fit; that is a different part to live with, so it is not the
default.

Why inside rather than a collar over the outside: with no clamping force, the
direction the bag pulls decides it. Pushing rubbish down drags the bag around the
rim, which moves the outside run of it *upward* — enough to walk a resting collar
off. The same drag pulls a drop-in frame *down*, straight into the flange's seat
on the rim. Being inside also keeps the body at the full 140 mm instead of having
to shrink it to make room for a collar.

Getting it out: reach into the mouth and pinch the inside face of the skirt on two
opposite sides. There is 12 mm of vertical wall to grip and the part weighs ~40 g.

Corner radius is a bag dimension, not a styling choice
------------------------------------------------------
A bag has to wrap the outer rim to fold over it, so what has to fit is RIM_GIRTH,
and rounding the corners is what shrinks it: every millimetre of radius takes
(8 - 2*pi) = 1.72 mm off the way round. R60 asks for 457 mm — a flat bag of 229 mm
half-width just closes, so call 245 mm the smallest that is comfortable, against
543 mm (271 mm half-width) at the R10 this started with.

At R60 only 20 mm of straight wall is left per side. The radius is free up to
SIZE / 2 = 70, which is a plain cylinder and the floor of what rounding can do:
440 mm, and only 17 mm less than here. Girth is nearly spent as a lever.

What it costs is capacity, and by now that is not nothing: 2.10 L against the
2.49 L of a sharp-cornered box, 0.30 L of it given up between R30 and R60.

Print notes
-----------
- Both parts print exactly as modelled, flat on the bed, no supports.
  The frame is modelled flange-down / skirt-up (its printing orientation); it is
  used the other way up.
- ~225 g of filament for the bin, ~40 g for the frame. Walls are 2 mm, so set
  5 perimeters and 0 % infill — the parts are all perimeter anyway.
- Layer height 0.2 mm. A brim helps on the 137 mm-tall body.
- Bed: 140 mm square on the A1 Mini's 180 mm plate, and 137 mm tall against a
  180 mm Z. It fits, but nothing is spare — level the bed first.
"""

from math import pi
from pathlib import Path

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
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


# --- Overall envelope (mm) — the specification ---
SIZE = 140.0  # X/Y — outer footprint
TOTAL_HEIGHT = 140.0  # Z — bin plus the seated frame flange

# --- Bin (mm) ---
WALL_THICKNESS = 2.0  # 5 perimeters at 0.4 mm nozzle
FLOOR_THICKNESS = 2.4  # 12 layers at 0.2 mm — carries the whole load of the bag
CORNER_RADIUS = 60.0  # vertical corner rounding — sized by bag girth, see RIM_GIRTH
FLOOR_FILLET = 2.5  # inside floor-to-wall fillet — no crud trap, stiffens the base
BOTTOM_CHAMFER = 0.6  # breaks the bed-contact edge, hides elephant foot
RIM_CHAMFER = 0.8  # breaks the top rim, inside and out

# --- Frame (mm) ---
FLANGE_THICKNESS = 3.0  # rim cap — also the frame's whole contribution to height
FRAME_WALL = 4.0  # skirt thickness
SKIRT_HEIGHT = 12.0  # short: enough to hold the bag flat and to pinch when lifting
SKIRT_CLEARANCE = 0.6  # mm per side against the cavity — the slot the bag lies in
FRAME_EDGE_CHAMFER = 1.0  # breaks the flange's exposed face and the skirt tip

OUTPUT_DIR = Path(__file__).parent / "output"


# --- Derived geometry ---
BIN_HEIGHT = TOTAL_HEIGHT - FLANGE_THICKNESS
CAVITY_SIZE = SIZE - 2 * WALL_THICKNESS
CAVITY_CORNER_RADIUS = CORNER_RADIUS - WALL_THICKNESS
CAVITY_DEPTH = BIN_HEIGHT - FLOOR_THICKNESS
# Rounded corners cut area out of the square, so the capacity is not w * w * h.
CAVITY_AREA = CAVITY_SIZE**2 - (4 - pi) * CAVITY_CORNER_RADIUS**2
CAVITY_LITRES = CAVITY_AREA * CAVITY_DEPTH / 1e6

# Skirt profile is the cavity offset inward, corners included, so the gap is the
# same all the way round instead of closing up on the corners.
SKIRT_SIZE = CAVITY_SIZE - 2 * SKIRT_CLEARANCE
SKIRT_CORNER_RADIUS = CAVITY_CORNER_RADIUS - SKIRT_CLEARANCE
OPENING_SIZE = SKIRT_SIZE - 2 * FRAME_WALL
OPENING_CORNER_RADIUS = SKIRT_CORNER_RADIUS - FRAME_WALL  # keeps the wall even round the bend
FLANGE_REACH = (SIZE - OPENING_SIZE) / 2  # how far the flange spans, rim edge to mouth

# What the bag has to wrap around: the outer rim, where it folds over. A flat bag
# needs at least half this as its flat width, and that is a hard floor with nothing
# left for the fold — allow a good margin on top.
RIM_GIRTH = 4 * (SIZE - 2 * CORNER_RADIUS) + 2 * pi * CORNER_RADIUS

assert OPENING_CORNER_RADIUS > 0, "corner radius too small for FRAME_WALL"
assert OPENING_SIZE > 0, "FRAME_WALL leaves no opening"
assert FRAME_WALL > 2 * FRAME_EDGE_CHAMFER, "chamfers meet across the skirt tip"
assert CORNER_RADIUS <= SIZE / 2, "corner radius larger than half the box"


# ---------------------------------------------------------------------------
# Bin — open-top box
# ---------------------------------------------------------------------------
with BuildPart() as bin_body:
    with BuildSketch():
        RectangleRounded(SIZE, SIZE, CORNER_RADIUS)
    extrude(amount=BIN_HEIGHT)

    with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
        RectangleRounded(CAVITY_SIZE, CAVITY_SIZE, CAVITY_CORNER_RADIUS)
    extrude(amount=CAVITY_DEPTH, mode=Mode.SUBTRACT)

    # Inside floor-to-wall fillet first: it only touches edges at z = FLOOR_THICKNESS,
    # and doing it before the bottom chamfer keeps that Z-group unambiguous.
    fillet(
        bin_body.edges().filter_by(Plane.XY).group_by(Axis.Z)[1],
        radius=FLOOR_FILLET,
    )
    chamfer(
        bin_body.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
        length=BOTTOM_CHAMFER,
    )
    # Top rim, both loops — the outer one ends up as a shadow line under the flange.
    chamfer(
        bin_body.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
        length=RIM_CHAMFER,
    )


# ---------------------------------------------------------------------------
# Frame — modelled in its printing orientation: flange on the bed, skirt up
# ---------------------------------------------------------------------------
with BuildPart() as frame:
    with BuildSketch():
        RectangleRounded(SIZE, SIZE, CORNER_RADIUS)
    extrude(amount=FLANGE_THICKNESS)

    # Straight skirt — no taper to wedge on, so it comes out the way it went in.
    with BuildSketch(Plane.XY.offset(FLANGE_THICKNESS)):
        RectangleRounded(SKIRT_SIZE, SKIRT_SIZE, SKIRT_CORNER_RADIUS)
    extrude(amount=SKIRT_HEIGHT)

    # Through-hole — the bin's actual mouth once the frame is fitted.
    with BuildSketch():
        RectangleRounded(OPENING_SIZE, OPENING_SIZE, OPENING_CORNER_RADIUS)
    extrude(amount=FLANGE_THICKNESS + SKIRT_HEIGHT, mode=Mode.SUBTRACT)

    # Flange face (on the bed here, uppermost in use) — the edges hands touch.
    chamfer(
        frame.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
        length=FRAME_EDGE_CHAMFER,
    )
    # Skirt tip — lead-in on the way into the bag.
    chamfer(
        frame.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],
        length=FRAME_EDGE_CHAMFER,
    )


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
for name, part in (("poly-bag-bin", bin_body.part), ("poly-bag-bin-frame", frame.part)):
    path = OUTPUT_DIR / f"{name}.stl"
    export_stl(part, str(path))
    print(f"Exported: {path}")

print(f"  bin:      {SIZE:.0f} x {SIZE:.0f} x {BIN_HEIGHT:.0f} mm outside")
print(
    f"  cavity:   {CAVITY_SIZE:.0f} x {CAVITY_SIZE:.0f} x {CAVITY_DEPTH:.1f} mm"
    f" ({CAVITY_LITRES:.1f} L)"
)
print(
    f"  frame:    {OPENING_SIZE:.1f} mm mouth, {SKIRT_HEIGHT:.0f} mm skirt,"
    f" {FLANGE_REACH:.1f} mm flange reach"
)
print(f"  assembled {SIZE:.0f} x {SIZE:.0f} x {TOTAL_HEIGHT:.0f} mm")
print(
    f"  bag:      needs a flat width over {RIM_GIRTH / 2:.0f} mm"
    f" (rim girth {RIM_GIRTH:.0f} mm at R{CORNER_RADIUS:.0f})"
)

if show is not None:
    try:
        show(bin_body.part, frame.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
