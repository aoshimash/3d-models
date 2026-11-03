"""Stand for the Eufy HomeVac H11 (T2521), inlet down, attachment fitted.

The vacuum stands about 470 mm tall on a 130 mm nozzle and most of its mass is high
up, so the stand has two jobs: grip the body firmly and resist tipping. Five printed
parts, no ballast and no glue: a tube, a collar on top of it, two halves of a hollow
cone around its foot, and a ring that keeps the halves closed.

How it holds
------------
The body has a step where the white barrel meets the dust cup (at the purple line).
That step lands on a flat seat in the collar, and a sleeve wraps the barrel above
it. Everything measured here was taken from the real vacuum, because an earlier
version that gripped the tapered dust cup from photo estimates did not fit at all.

Holding the barrel puts the top of the stand above the printer's Z, so the tube and
collar are separate, joined by a slip spigot.

Staying upright
---------------
Width does the work, not mass: force to tip at the top of the vacuum is total mass x
base radius / height. A hollow cone reaches Phi 200 for far less plastic than a solid
dish of the same stiffness. Phi 200 is wider than the bed, hence the two halves, which
fit when turned 45 degrees (the STL is exported that way).

The halves clamp a V bead on the tube. Without it the tube would lift straight out of
the cone and the wide footprint would do nothing. The tube's own floor also rests on
the table. Bending at the tube root is about 0.07 MPa static, so strength is not what
sizes any of this.

Assembly
--------
Stand the tube on a flat table, close both halves around it with the bead in the
groove, and drop the neck ring down the tube onto the neck. The table sets the height
and the tube aligns the halves. The foot is too wide for a ring that fits the bed, so
the ring only holds the neck; if the foot still opens, glue the two flat seams.

Fit checks (print these before the long parts)
----------------------------------------------
neck-test-tube.stl and neck-test-half.stl are a slice through the bead and groove. The
half must sit on the ring with the bead in the groove, without forcing.

The collar and joint-test.stl were already confirmed against the real vacuum.

Print notes
-----------
- tube: upright, floor on the plate, with a brim. No supports. Tall and narrow on a
  moving bed, so slow down near the top.
- cone-half (print twice): upright, foot on the plate. No supports; the inside is under
  45 degrees. Leave it where the STL puts it or it will not fit the plate. Set 6 walls
  so the 2.4 mm shell comes out solid.
- collar: upright, wide end on the plate. No supports; the bore narrows through a 45
  degree cone above the socket.
- neck-ring: flat on the plate. No supports.
"""

from math import atan2, cos, sqrt
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildLine,
    BuildPart,
    BuildSketch,
    Locations,
    Mode,
    Plane,
    Polyline,
    Pos,
    Rot,
    add,
    export_stl,
    make_face,
    revolve,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Vacuum (mm) — user-measured on the real unit ---
BARREL_DIAMETER = 66.0  # white barrel just above the purple line
DUST_CUP_DIAMETER = 61.0  # dust cup just below the purple line
TIP_TO_STEP = 205.0  # attachment tip to the purple line, attachment fitted
STEP_TO_EXHAUST = 61.0  # purple line to the lower edge of the exhaust, the sleeve limit

# --- Fit tolerances (mm) ---
SLEEVE_CLEARANCE = 0.5  # per side, barrel to sleeve — confirmed on the printed collar
DUST_CUP_CLEARANCE = 1.0  # per side, dust cup to seat bore — confirmed on the printed collar
JOINT_CLEARANCE = 0.25  # per side, spigot to socket — confirmed with joint-test.stl
NECK_CLEARANCE = 0.2  # per side, tube to cone neck and bead to groove — confirmed on test slices
RING_CLEARANCE = 0.25  # per side, cone neck to ring — same slip fit as the spigot joint
TIP_CLEARANCE = 4.0  # attachment tip to tube floor

# --- Tube and collar (mm) ---
TUBE_DIAMETER = 72.0  # outside of the tube and the collar, flush at the joint
CHAMBER_DIAMETER = 64.0  # bore of the tube, clears the dust cup and attachment
SLEEVE_HEIGHT = 30.0  # how far the sleeve climbs the barrel, well below the exhaust
FLOOR_THICKNESS = 3.0  # tube floor
JOINT_Z = 160.0  # where the collar meets the tube
SPIGOT_DIAMETER = 68.0  # outside of the tube spigot, 2 mm wall
SPIGOT_LENGTH = 15.0  # engagement into the collar
SOCKET_TOP_GAP = 0.4  # spigot end to socket roof, so the collar rests on the shoulder
RIM_CHAMFER = 1.0  # collar top, outside and lead-in
FOOT_CHAMFER = 0.6  # bottom edges, offsets elephant's foot

# --- Cone (mm) ---
CONE_DIAMETER = 200.0  # footprint — sets the tip-over force, about 220 gf
CONE_WALL = 2.4  # shell thickness, 6 perimeters at 0.4 mm nozzle
CONE_FOOT_HEIGHT = 4.0  # vertical band at the foot, stiffens the edge
CONE_TOP_Z = 64.0  # where the shell reaches the neck — keeps the slope under 45 degrees
NECK_DIAMETER = 84.0  # outside of the neck that clamps the tube
NECK_TOP_Z = 89.0  # top of the neck

# --- Bead that keeps the tube in the cone (mm) ---
BEAD_Z = 76.0  # bead centre, mid-neck
BEAD_DEPTH = 2.5  # how far the bead stands off the tube; 45 degree flanks print unsupported

# --- Ring that keeps the cone closed (mm) ---
RING_WALL = 3.0  # radial wall, well over the minimum because it takes the hoop load
RING_HEIGHT = 25.0  # the full straight neck, bead included

# --- Test pieces (mm) ---
JOINT_TEST_BELOW = 5.0  # tube kept below the shoulder, enough to hold on to
NECK_TEST_HALF_HEIGHT = 8.0  # slice this far either side of the bead

OUTPUT_DIR = Path(__file__).parent / "output"


# --- Derived geometry ---
TIP_Z = FLOOR_THICKNESS + TIP_CLEARANCE
SEAT_Z = TIP_Z + TIP_TO_STEP
TOP_Z = SEAT_Z + SLEEVE_HEIGHT
TUBE_TOP_Z = JOINT_Z + SPIGOT_LENGTH
SOCKET_ROOF_Z = TUBE_TOP_Z + SOCKET_TOP_GAP
TIP_BELOW_COLLAR = JOINT_Z - TIP_Z

TUBE_RADIUS = TUBE_DIAMETER / 2
CHAMBER_RADIUS = CHAMBER_DIAMETER / 2
SPIGOT_RADIUS = SPIGOT_DIAMETER / 2
SOCKET_RADIUS = SPIGOT_RADIUS + JOINT_CLEARANCE
SEAT_BORE_RADIUS = DUST_CUP_DIAMETER / 2 + DUST_CUP_CLEARANCE
SLEEVE_RADIUS = BARREL_DIAMETER / 2 + SLEEVE_CLEARANCE

CONE_RADIUS = CONE_DIAMETER / 2
NECK_RADIUS = NECK_DIAMETER / 2
NECK_BORE_RADIUS = TUBE_RADIUS + NECK_CLEARANCE
GROOVE_RADIUS = TUBE_RADIUS + BEAD_DEPTH + NECK_CLEARANCE * sqrt(2)
GROOVE_HALF_HEIGHT = GROOVE_RADIUS - NECK_BORE_RADIUS

# The inner shell runs parallel to the outer one, so step in along the radius by the
# wall thickness projected onto the slope.
CONE_SLOPE = (CONE_RADIUS - NECK_RADIUS) / (CONE_TOP_Z - CONE_FOOT_HEIGHT)
CONE_RADIAL_WALL = CONE_WALL / cos(atan2(CONE_RADIUS - NECK_RADIUS, CONE_TOP_Z - CONE_FOOT_HEIGHT))
FOOT_INNER_RADIUS = CONE_RADIUS - CONE_RADIAL_WALL
SHELL_MEETS_BORE_Z = CONE_FOOT_HEIGHT + (FOOT_INNER_RADIUS - NECK_BORE_RADIUS) / CONE_SLOPE

RING_BORE_RADIUS = NECK_RADIUS + RING_CLEARANCE
RING_OUTER_RADIUS = RING_BORE_RADIUS + RING_WALL


def _revolved(points, arc=360):
    """Revolve a closed half profile (radius on X, height on Z) around the Z axis."""
    with BuildPart() as part:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*points, close=True)
            make_face()
        revolve(axis=Axis.Z, revolution_arc=arc)
    return part.part


def _slice(shape, bottom_z, top_z, width):
    """Keep only the part of a shape between two heights, moved down to sit on Z=0."""
    with BuildPart() as piece:
        add(shape)
        with Locations((0, 0, bottom_z)):
            Box(
                width,
                width,
                top_z - bottom_z,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.INTERSECT,
            )
    return Pos(0, 0, -bottom_z) * piece.part


def build_tube():
    """Floor, tube, retaining bead and spigot."""
    return _revolved(
        [
            (0, 0),
            (TUBE_RADIUS - FOOT_CHAMFER, 0),
            (TUBE_RADIUS, FOOT_CHAMFER),
            (TUBE_RADIUS, BEAD_Z - BEAD_DEPTH),
            (TUBE_RADIUS + BEAD_DEPTH, BEAD_Z),
            (TUBE_RADIUS, BEAD_Z + BEAD_DEPTH),
            (TUBE_RADIUS, JOINT_Z),
            (SPIGOT_RADIUS, JOINT_Z),
            (SPIGOT_RADIUS, TUBE_TOP_Z),
            (CHAMBER_RADIUS, TUBE_TOP_Z),
            (CHAMBER_RADIUS, FLOOR_THICKNESS),
            (0, FLOOR_THICKNESS),
        ]
    )


def build_cone_half():
    """One half of the hollow cone, with its seam faces on the XZ plane."""
    return _revolved(
        [
            (FOOT_INNER_RADIUS, 0),
            (CONE_RADIUS - FOOT_CHAMFER, 0),
            (CONE_RADIUS, FOOT_CHAMFER),
            (CONE_RADIUS, CONE_FOOT_HEIGHT),
            (NECK_RADIUS, CONE_TOP_Z),
            (NECK_RADIUS, NECK_TOP_Z - RIM_CHAMFER),
            (NECK_RADIUS - RIM_CHAMFER, NECK_TOP_Z),
            (NECK_BORE_RADIUS, NECK_TOP_Z),
            (NECK_BORE_RADIUS, BEAD_Z + GROOVE_HALF_HEIGHT),
            (GROOVE_RADIUS, BEAD_Z),
            (NECK_BORE_RADIUS, BEAD_Z - GROOVE_HALF_HEIGHT),
            (NECK_BORE_RADIUS, SHELL_MEETS_BORE_Z),
            (FOOT_INNER_RADIUS, CONE_FOOT_HEIGHT),
        ],
        arc=180,
    )


def build_collar():
    """Socket, seat and sleeve, moved down to sit on Z=0."""
    collar = _revolved(
        [
            (SOCKET_RADIUS, JOINT_Z),
            (TUBE_RADIUS, JOINT_Z),
            (TUBE_RADIUS, TOP_Z - RIM_CHAMFER),
            (TUBE_RADIUS - RIM_CHAMFER, TOP_Z),
            (SLEEVE_RADIUS + RIM_CHAMFER, TOP_Z),
            (SLEEVE_RADIUS, TOP_Z - RIM_CHAMFER),
            (SLEEVE_RADIUS, SEAT_Z),
            (SEAT_BORE_RADIUS, SEAT_Z),
            (SEAT_BORE_RADIUS, SOCKET_ROOF_Z + SOCKET_RADIUS - SEAT_BORE_RADIUS),  # 45 degrees
            (SOCKET_RADIUS, SOCKET_ROOF_Z),
        ]
    )
    return Pos(0, 0, -JOINT_Z) * collar


def build_neck_ring():
    """Plain ring that drops over the neck, chamfered inside as a lead-in at both ends."""
    return _revolved(
        [
            (RING_BORE_RADIUS + FOOT_CHAMFER, 0),
            (RING_OUTER_RADIUS - FOOT_CHAMFER, 0),
            (RING_OUTER_RADIUS, FOOT_CHAMFER),
            (RING_OUTER_RADIUS, RING_HEIGHT - RIM_CHAMFER),
            (RING_OUTER_RADIUS - RIM_CHAMFER, RING_HEIGHT),
            (RING_BORE_RADIUS + RIM_CHAMFER, RING_HEIGHT),
            (RING_BORE_RADIUS, RING_HEIGHT - RIM_CHAMFER),
            (RING_BORE_RADIUS, FOOT_CHAMFER),
        ]
    )


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    tube = build_tube()
    cone_half = build_cone_half()
    collar = build_collar()
    neck_ring = build_neck_ring()
    joint_test = _slice(tube, JOINT_Z - JOINT_TEST_BELOW, TUBE_TOP_Z, TUBE_DIAMETER + 1)
    neck_low, neck_high = BEAD_Z - NECK_TEST_HALF_HEIGHT, BEAD_Z + NECK_TEST_HALF_HEIGHT
    neck_test_tube = _slice(tube, neck_low, neck_high, TUBE_DIAMETER + 10)
    neck_test_half = _slice(cone_half, neck_low, neck_high, NECK_DIAMETER + 1)

    export_stl(tube, str(OUTPUT_DIR / "tube.stl"))
    export_stl(Rot(Z=-45) * cone_half, str(OUTPUT_DIR / "cone-half.stl"))  # fits the bed turned
    export_stl(collar, str(OUTPUT_DIR / "collar.stl"))
    export_stl(neck_ring, str(OUTPUT_DIR / "neck-ring.stl"))
    export_stl(joint_test, str(OUTPUT_DIR / "joint-test.stl"))
    export_stl(neck_test_tube, str(OUTPUT_DIR / "neck-test-tube.stl"))
    export_stl(neck_test_half, str(OUTPUT_DIR / "neck-test-half.stl"))

    print(f"stacked height {TOP_Z:.1f}, tube {TUBE_TOP_Z:.1f}, collar {TOP_Z - JOINT_Z:.1f}")
    print(f"sleeve {SLEEVE_HEIGHT:.1f} of {STEP_TO_EXHAUST:.1f} available below the exhaust")
    print(f"tip below collar {TIP_BELOW_COLLAR:.1f}")
    if show is not None:
        show(tube, cone_half, Pos(0, 0, JOINT_Z) * collar)
