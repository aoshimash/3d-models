"""Stand for the Eufy HomeVac H11 (T2521), inlet down, attachment fitted.

The vacuum stands about 470 mm tall on a 130 mm nozzle and most of its mass is high
up, so the stand has two jobs: grip the body firmly and keep the centre of gravity
low. Three printed parts plus ballast.

How it holds
------------
The body has a step where the white barrel meets the dust cup (at the purple line).
That step lands on a flat seat in the collar, and a sleeve wraps the barrel above
it. Everything measured here was taken from the real vacuum, because an earlier
version that gripped the tapered dust cup from photo estimates did not fit at all.

Holding the barrel puts the top of the stand above the printer's Z, so the tube
splits into a base and a collar joined by a slip spigot.

Ballast
-------
The base is a dish around the tube. Fill it from the top, then close it with the
lid. Sand gives about 650 g, steel shot about 1.9 kg. Fasten the lid with tape or
glue, or the ballast comes out if the stand ever falls over.

Fit checks (print joint-test.stl and collar.stl first)
------------------------------------------------------
Collar on the vacuum, attachment fitted:
- The attachment must pass through the collar.
- The barrel must seat on the step without rocking, and lift out freely.
- The attachment tip should stick out TIP_BELOW_COLLAR mm below the collar. Each mm
  over TIP_BELOW_COLLAR + TIP_CLEARANCE means the tip hits the base floor.
joint-test.stl into the collar: must slide in by hand and sit on its shoulder.

Print notes
-----------
- base: upright, dish on the plate. No supports. Tall and narrow, so check the first
  layer and slow down near the top.
- collar: upright, wide end on the plate. No supports; the bore narrows through a
  45 degree cone above the socket.
- lid: flat, either face down.
"""

from math import pi
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
LID_CLEARANCE = 0.25  # per side, lid to dish and tube
TIP_CLEARANCE = 4.0  # attachment tip to base floor

# --- Tube and collar (mm) ---
TUBE_DIAMETER = 72.0  # outside of the base tube and the collar, flush at the joint
CHAMBER_DIAMETER = 64.0  # bore of the base tube, clears the dust cup and attachment
SLEEVE_HEIGHT = 30.0  # how far the sleeve climbs the barrel, well below the exhaust
FLOOR_THICKNESS = 3.0  # base floor, carries the ballast
JOINT_Z = 160.0  # where the collar meets the base
SPIGOT_DIAMETER = 68.0  # outside of the base spigot, 2 mm wall
SPIGOT_LENGTH = 15.0  # engagement into the collar
SOCKET_TOP_GAP = 0.4  # spigot end to socket roof, so the collar rests on the shoulder
RIM_CHAMFER = 1.0  # collar top, outside and lead-in

# --- Dish (mm) ---
DISH_DIAMETER = 160.0  # footprint — sets the tip-over angle
DISH_HEIGHT = 35.0  # overall, lid included
DISH_WALL = 2.4  # 6 perimeters at 0.4 mm nozzle, holds back the ballast
DISH_RIM_WALL = 1.2  # outer wall around the lid
DISH_CHAMFER = 0.6  # bottom edge, offsets elephant's foot
LID_THICKNESS = 3.0  # lid sits flush with the dish rim
TUBE_LEDGE = 1.5  # ledge on the tube that carries the lid's inner edge

# --- Joint test (mm) ---
JOINT_TEST_BELOW = 5.0  # base tube kept below the shoulder, enough to hold on to

OUTPUT_DIR = Path(__file__).parent / "output"


# --- Derived geometry ---
TIP_Z = FLOOR_THICKNESS + TIP_CLEARANCE
SEAT_Z = TIP_Z + TIP_TO_STEP
TOP_Z = SEAT_Z + SLEEVE_HEIGHT
BASE_TOP_Z = JOINT_Z + SPIGOT_LENGTH
SOCKET_ROOF_Z = BASE_TOP_Z + SOCKET_TOP_GAP
TIP_BELOW_COLLAR = JOINT_Z - TIP_Z

TUBE_RADIUS = TUBE_DIAMETER / 2
CHAMBER_RADIUS = CHAMBER_DIAMETER / 2
SPIGOT_RADIUS = SPIGOT_DIAMETER / 2
SOCKET_RADIUS = SPIGOT_RADIUS + JOINT_CLEARANCE
SEAT_BORE_RADIUS = DUST_CUP_DIAMETER / 2 + DUST_CUP_CLEARANCE
SLEEVE_RADIUS = BARREL_DIAMETER / 2 + SLEEVE_CLEARANCE

DISH_RADIUS = DISH_DIAMETER / 2
TROUGH_OUTER_RADIUS = DISH_RADIUS - DISH_WALL
TROUGH_INNER_RADIUS = TUBE_RADIUS + TUBE_LEDGE
LID_SEAT_Z = DISH_HEIGHT - LID_THICKNESS
LID_OUTER_RADIUS = DISH_RADIUS - DISH_RIM_WALL - LID_CLEARANCE
LID_INNER_RADIUS = TUBE_RADIUS + LID_CLEARANCE
BALLAST_VOLUME = (
    pi * (TROUGH_OUTER_RADIUS**2 - TROUGH_INNER_RADIUS**2) * (LID_SEAT_Z - FLOOR_THICKNESS)
)


def _revolved(points):
    """Revolve a closed half profile (radius on X, height on Z) around the Z axis."""
    with BuildPart() as part:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*points, close=True)
            make_face()
        revolve(axis=Axis.Z)
    return part.part


def build_base():
    """Dish, lid seat, tube and spigot."""
    return _revolved(
        [
            (0, 0),
            (DISH_RADIUS - DISH_CHAMFER, 0),
            (DISH_RADIUS, DISH_CHAMFER),
            (DISH_RADIUS, DISH_HEIGHT),
            (DISH_RADIUS - DISH_RIM_WALL, DISH_HEIGHT),
            (DISH_RADIUS - DISH_RIM_WALL, LID_SEAT_Z),
            (TROUGH_OUTER_RADIUS, LID_SEAT_Z),
            (TROUGH_OUTER_RADIUS, FLOOR_THICKNESS),
            (TROUGH_INNER_RADIUS, FLOOR_THICKNESS),
            (TROUGH_INNER_RADIUS, LID_SEAT_Z),
            (TUBE_RADIUS, LID_SEAT_Z),
            (TUBE_RADIUS, JOINT_Z),
            (SPIGOT_RADIUS, JOINT_Z),
            (SPIGOT_RADIUS, BASE_TOP_Z),
            (CHAMBER_RADIUS, BASE_TOP_Z),
            (CHAMBER_RADIUS, FLOOR_THICKNESS),
            (0, FLOOR_THICKNESS),
        ]
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


def build_lid():
    """Flat ring closing the ballast dish."""
    return _revolved(
        [
            (LID_INNER_RADIUS, 0),
            (LID_OUTER_RADIUS, 0),
            (LID_OUTER_RADIUS, LID_THICKNESS),
            (LID_INNER_RADIUS, LID_THICKNESS),
        ]
    )


def build_joint_test(base):
    """Top of the base tube only, to try the spigot in the collar."""
    bottom_z = JOINT_Z - JOINT_TEST_BELOW
    with BuildPart() as test:
        add(base)
        with Locations((0, 0, bottom_z)):
            Box(
                TUBE_DIAMETER + 1,
                TUBE_DIAMETER + 1,
                BASE_TOP_Z - bottom_z,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.INTERSECT,
            )
    return Pos(0, 0, -bottom_z) * test.part


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    base = build_base()
    collar = build_collar()
    lid = build_lid()
    joint_test = build_joint_test(base)
    export_stl(base, str(OUTPUT_DIR / "base.stl"))
    export_stl(collar, str(OUTPUT_DIR / "collar.stl"))
    export_stl(lid, str(OUTPUT_DIR / "lid.stl"))
    export_stl(joint_test, str(OUTPUT_DIR / "joint-test.stl"))
    print(f"stacked height {TOP_Z:.1f}, base {BASE_TOP_Z:.1f}, collar {TOP_Z - JOINT_Z:.1f}")
    print(f"sleeve {SLEEVE_HEIGHT:.1f} of {STEP_TO_EXHAUST:.1f} available below the exhaust")
    print(f"tip below collar {TIP_BELOW_COLLAR:.1f}, ballast {BALLAST_VOLUME / 1000:.0f} cm3")
    if show is not None:
        show(base, Pos(0, 0, JOINT_Z) * collar, Pos(0, 0, LID_SEAT_Z) * lid)
