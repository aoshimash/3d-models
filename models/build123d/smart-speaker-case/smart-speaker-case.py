"""Smart-speaker case: a Ø142 cylinder with the Jabra Speak2 40 flush in the top
and a Raspberry Pi 4 B hung face-down below it.

Two printed parts, no hardware between them:

- box.stl : open-top cylinder. Four pillars from the floor carry the Pi 4
  *component side down*, so the low-profile ICE-tower cooler on its SoC hangs
  under the board with its fan facing the floor. Both USB plugs live inside
  on right-angle adapters; only the thin power cable leaves through a hole in
  the back wall at floor level.
- lid.stl : thick disc with the same diameter as the box, so the side runs
  flush from floor to top with one hairline seam. A lip left standing on the
  inside of the box wall engages an annular groove in the lid's underside.
  A round pocket in the top takes the whole height of the Jabra puck, so the
  puck's top ends up flush with the lid. The pocket floor is a ring that
  carries the puck's base, with one radial slot for the cable.

Why a cylinder, and why Ø142
----------------------------
The puck is Ø120, so a round case reads as the speaker itself, only taller.
What used to force a 160 x 134 box was not the Pi (85 x 56, diagonal 102)
but the two plugs sticking straight out of it: 60 mm for the Jabra's USB-A
adapter and 50 mm for the PSU's USB-C plug. With a right-angle adapter on
each port (user's, ~10 mm thick, cable turned 90°) each arm is 12 mm deep
and runs along the board edge instead, and the Pi plus both arms fits in a
Ø127 circle. The box interior is Ø134.8 (3.6 mm wall), leaving ~4 mm.

The Pi sits off-centre: its USB-A end toward -X, microSD end toward +X,
USB-C edge toward the back (-Y), GPIO edge toward the front. PI_CENTRE is
the one placement number; the assert below checks every protruding corner
against the wall.

The Jabra puck, as it actually is
---------------------------------
Measured by the user: a straight Ø120 band for the top 7.5 mm (buttons and
LED ring), then the side slopes inward to a Ø91.5 base, which is a flat
rubber ring. The integrated Ø3.5 cable is wound in that conical groove for
transport and leaves the cone 8 mm above the base; its plug end is
8.5 x 6.5 mm.

How the puck is held and where the cable goes
---------------------------------------------
- Sideways: the straight band is located by the Ø121.4 pocket wall (0.7 mm
  per side — 1.5 felt loose in the collar test, which printed to size).
- Vertically: the rubber ring of the base sits on the pocket floor ring,
  which reaches 8 mm in under the base rim; the opening inside is Ø75.5.
- Cable: it leaves the cone, runs down the annular gap between cone and
  pocket wall, then through a 10 mm wide radial slot in the ring (pointing
  -Y, toward the back) into the box. The slot opens into the Ø75.5 hole, so
  the plug end goes through the hole and the cable slides sideways into the
  slot. Rotate the puck so its cable exit sits over the slot.
- Removal: lift the lid off (the puck comes with it), push the puck up from
  below through the opening.

Why the Pi hangs upside down
----------------------------
The Pi carries its own CPU cooler (heat-pipe tower, 40 mm fan on top), so the
case needs no fan. Face down, the fan points at the floor plate and the
desk, with the Pi board, the lid and the puck's body between it and the four
microphones on top; flat it would blow at the lid 10 mm under the puck, and
on edge the USB-C receptacle would point up or down. Heat does not care: the
fan forces air through the fins either way, and the heat pipes' ~15 mm of
rise against gravity is nothing at a Pi's <10 W. Warm air off the fins
rises to the exhaust slots high in the wall; the fan draws fresh air through
intake slots at floor level.

How the Pi is held
------------------
At each corner hole the cooler kit stacks, from the component face outward,
a 6 mm brass standoff, the 1.5 mm bracket plate, an M2.5 nut (4.9 mm across
flats) and 2.4 mm of thread stub (all measured). Face down this stack hangs
below the board and the nut is the lowest flat surface — so the nut is what
each pillar carries: the pillar top is flat at the nut's face with a Ø3.2
hole that the thread stub drops into, locating the Pi sideways. Nothing
wider is possible: the official drawing puts the GPIO and PoE header bodies
3.6 mm and the board edge 3.5 mm from the hole centres. The pillar top sits
1 mm below the 8.5 mm GPIO header. The kit's long brass standoffs on the
solder side would hit the lid: replace them with M2.5 x 6 screws from the
solder side into the 6 mm standoffs. The Pi is held down by its own weight
and cannot lift more than ~1.5 mm before meeting the lid.

Walls (angles seen from above, +X = 0°, +Y = 90° = front)
---------------------------------------------------------
- Intake: 11 vertical slots at floor level centred on 0° (+X, microSD end).
- Exhaust: 12 vertical slots high up centred on 180° (-X, USB-A end).
- Power cable hole: 13.5 x 9 mm at floor level at -90° (back). The USB-C
  plug is pushed through it from outside during assembly, then onto the
  right-angle adapter on the receptacle; the plug body lies along the back
  edge of the board.
- Front (+90°) closed.
- The Jabra's USB-A adapter plugs into a right-angle adapter on the Pi's
  USB 3.0 stack and lies along the -X end of the board toward the back.
  Cable slack coils on the floor under the hanging board; keep it out of
  the ~40 mm square under the fan.

Flush joint
-----------
The top 4 mm of the box wall is stepped: the outer 2 mm is cut away to a
ledge, the inner 1.6 mm stays as a lip. The lid is the full Ø142; its
underside carries a 2.1 mm wide, 4.3 mm deep annular groove that the lip
enters with 0.25 mm per side (fit confirmed on a 50 mm test pair), and its
outer rim sits on the ledge. The lid cannot slide, only lift, and being
round it goes on at any angle; only the cable slot direction (toward the
back) matters.

Fit tests (all but the round joint pair already printed and passed)
--------------------------------------------------------------------
- fit-test-puck-collar.stl : 8 mm ring of the Ø121.4 pocket mouth.
- fit-test-puck-cup.stl : the pocket floor ring with the cable slot + 8 mm
  of wall; the puck must sit on the ring and the cable reach the slot.
- fit-test-pillars.stl : the four real pillars at the real pitch on a
  plate; the whole Pi assembly sits on it, nuts down.
- fit-test-joint-box.stl / fit-test-joint-lid.stl : Ø60 box and lid with
  the real wall, ledge, lip, groove and clearance — the square version of
  this pair fit perfectly; this one only adds the curvature.

Print notes
-----------
- Box: Ø142 x 59 mm, open side up, brim, no supports.
- Lid: Ø142 x 34.9 mm, pocket side up, flat on the bed, no supports. The
  rim around the pocket is solid in the model and prints as walls plus
  infill; 15 % is plenty.
- 3 walls, 0.2 mm layers.

Sources
-------
- Jabra Speak2 40 tech sheet (Rev B, 24 Apr 2023): Ø120 x 33 mm, 245 g,
  integrated USB cable ca. 80 cm. Band 7.5 mm, base Ø91.5, cable exit 8 mm
  up, cable Ø3.5, plug 8.5 x 6.5 mm measured by the user.
- Raspberry Pi 4 mechanical drawing (RP-008343): 85 x 56, holes Ø2.7 at
  3.5 mm from the edges on a 58 x 49 pitch, USB-C centre 11.2 mm from the
  microSD end, HDMI at 26 and 39.5, SoC at (32.5, 25.75), USB stacks at
  9 and 27 from the USB-C edge (Z 16.0), Ethernet at 45.75 (Z 13.5),
  GPIO header Z 8.5.
- Cooler: user's low-profile ICE-tower type; 38 mm board underside to fan
  face, 6 mm standoffs, 1.5 mm bracket, nuts 4.9 mm AF, 2.4 mm stub,
  measured. Nut height 2 mm assumed (standard M2.5).
- Right-angle USB-A and USB-C adapters: ~10 mm thick, measured by the user.
  PSU plug overmould 11.5 x 7 mm.
"""

from math import cos, hypot, radians, sin
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Compound,
    Cone,
    Cylinder,
    GeomType,
    Location,
    Locations,
    Mode,
    Plane,
    Pos,
    Solid,
    Sphere,
    Vector,
    chamfer,
    export_stl,
    extrude,
    fillet,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Jabra Speak2 40 (mm) ---
PUCK_DIA = 120.0  # top rim / straight band diameter (tech sheet)
PUCK_HEIGHT = 33.0  # overall height (tech sheet)
PUCK_STRAIGHT_H = 7.5  # straight band below the top rim (measured)
PUCK_BASE_DIA = 91.5  # bottom of the cone (measured); base is a flat rubber ring
PUCK_CABLE_EXIT_Z = 8.0  # cable leaves the cone this far above the base (measured)
PUCK_CLEARANCE = 0.7  # per side around the straight band; 1.5 felt loose in the collar test
PUCK_PROUD = 0.5  # how far the puck's top stands above the lid (0 = dead flush)
RING_OVERLAP = 8.0  # pocket floor ring reaches this far in under the base rim
CABLE_SLOT_W = 10.0  # radial slot in the ring for the puck's Ø3.5 cable (toward -Y)
CABLE_DIA = 3.5  # Jabra cable (measured); used for the PSU cable stand-in too

# --- Raspberry Pi 4 B (mm, board-local: x from the microSD end, y from the USB-C edge) ---
PI_LENGTH = 85.0
PI_WIDTH = 56.0
PI_BOARD_T = 1.5
PI_HOLE_INSET = 3.5
PI_HOLE_PITCH_X = 58.0
PI_HOLE_PITCH_Y = 49.0
PI_USBC_X = 11.2  # USB-C receptacle centre (3.5 + 7.7)
PI_USBC_HEIGHT = 3.2
PI_HDMI_XS = (26.0, 39.5)  # micro HDMI centres, preview only
PI_USB_YS = (9.0, 27.0)  # USB 2.0 / 3.0 stack centres, preview only
PI_USB_STACK_H = 16.0
PI_ETH_Y = 45.75  # Ethernet jack centre, preview only
PI_ETH_H = 13.5
PI_GPIO_X0 = 7.1  # header start, preview only
PI_GPIO_Y = 51.2  # header centre line, preview only
PI_GPIO_H = 8.5
PI_PORT_OVERHANG = 3.0  # USB-A stacks past the board edge
PI_USBC_OVERHANG = 1.3  # USB-C receptacle past the board edge
PI_SD_OVERHANG = 2.5  # microSD card past the board edge
PI_SOC_X = 32.5
PI_SOC_Y = 25.75
PI_ASSEMBLY_H = 38.0  # board solder side to the cooler's fan face, measured (no base plate)
PI_STANDOFF_H = 6.0  # cooler kit's brass standoff on the component side (measured)
BRACKET_T = 1.5  # cooler bracket plate on top of the standoff (measured)
NUT_AF = 4.9  # M2.5 nut across flats (measured)
NUT_H = 2.0  # M2.5 nut height — standard value, not measured
THREAD_STUB = 2.4  # standoff thread showing beyond the nut (measured)
SCREW_HEAD_H = 2.5  # M2.5 pan head on the solder side, preview only
COOLER_SIZE = 40.0  # fan / fin stack footprint, preview only
COOLER_FAN_T = 10.0  # fan frame depth, preview only

# --- Plugs on right-angle adapters (mm) ---
L_ADAPTER_DEPTH = 12.0  # right-angle adapter beyond the port face (~10 measured) + room
USB_A_ADAPTER = (8.0, 45.0, 16.0)  # Jabra adapter x, y, z when lying along the board end
USBC_PLUG = (30.0, 11.5, 7.0)  # PSU plug body x, y, z when lying along the board edge
POWER_HOLE_W = 13.5  # power cable hole: the 11.5 x 7 plug overmould must pass (1 mm per side)
POWER_HOLE_H = 9.0

# --- Box (mm) ---
OUTER_DIA = 142.0  # outer diameter — Pi + both right-angle arms need Ø127 inside
WALL = 3.6  # side wall — carries the ledge and lip
FLOOR = 3.0  # floor thickness
LIP_HEIGHT = 4.0  # how far the inner lip stands above the ledge
LEDGE_W = 2.0  # outer part of the wall cut away at the top; the lid's rim sits here
JOINT_CLEARANCE = 0.25  # per side, lip to groove (fit confirmed)
GROOVE_EXTRA = 0.3  # groove deeper than the lip so the rim, not the lip, carries the lid
EDGE_CHAMFER = 0.8  # bed-side edge of the box, hides elephant foot

FAN_FLOOR_GAP = 10.0  # intake clearance between the fan face and the floor
BOARD_TOP_CLEARANCE = 4.0  # solder-side screw heads to the lid underside
STANDOFF_DIA = 8.0  # pillar diameter: covers the nut, passes under the GPIO header
STUB_HOLE_DIA = 3.2  # hole in the pillar top for the M2.5 thread stub
STUB_HOLE_EXTRA = 1.0  # hole deeper than the stub so the nut, not the stub, lands
PI_CENTRE = (6.5, 8.5)  # board centre in the box; balances the four protruding corners
KEEPOUT_MARGIN = 2.0  # any protruding part to the inner wall

INTAKE_ANGLE = 0.0  # degrees; row centred on +X, the microSD end
INTAKE_COUNT = 11
INTAKE_PITCH_DEG = 6.5
INTAKE_W = 3.0  # slot width along the wall
INTAKE_H = 16.0
INTAKE_Z0 = 5.0  # slot bottom above the box underside

VENT_ANGLE = 180.0  # degrees; exhaust row centred on -X, the USB-A end
VENT_COUNT = 12
VENT_PITCH_DEG = 6.5
VENT_W = 3.0
VENT_H = 24.0
VENT_LID_GAP = 4.0  # wall left between the slot top and the ledge

POWER_ANGLE = -90.0  # degrees; the back
POWER_HOLE_Z = 8.5  # power cable hole centre above the box underside

# --- Lid (mm) ---
LID_FLOOR = 2.4  # pocket floor ring thickness
LID_TOP_FILLET = 1.0
POCKET_EDGE_CHAMFER = 0.8  # top edge of the pocket, next to the puck's rim

OUTPUT_DIR = Path(__file__).parent / "output"


# --- Derived ---
R_OUT = OUTER_DIA / 2
R_IN = R_OUT - WALL
COOLER_DROP = PI_ASSEMBLY_H - PI_BOARD_T  # component face down to the fan face
PI_FOOT_H = PI_STANDOFF_H + BRACKET_T + NUT_H  # component face down to the nut face
STUB_HOLE_DEPTH = THREAD_STUB + STUB_HOLE_EXTRA
STANDOFF_H = FAN_FLOOR_GAP + COOLER_DROP - PI_FOOT_H  # floor top to the pillar top
PI_FACE_Z = FLOOR + STANDOFF_H + PI_FOOT_H  # component side of the board (facing down)
INNER_HEIGHT = PI_FACE_Z - FLOOR + PI_BOARD_T + BOARD_TOP_CLEARANCE  # floor top to lid underside
LID_BOTTOM_Z = FLOOR + INNER_HEIGHT
BOX_HEIGHT = LID_BOTTOM_Z + LIP_HEIGHT
LIP_THICK = WALL - LEDGE_W
GROOVE_R_OUT = R_OUT - LEDGE_W + JOINT_CLEARANCE
GROOVE_R_IN = R_IN - JOINT_CLEARANCE
GROOVE_DEPTH = LIP_HEIGHT + GROOVE_EXTRA
RECESS_DEPTH = PUCK_HEIGHT - PUCK_PROUD
RECESS_DIA = PUCK_DIA + 2 * PUCK_CLEARANCE
OPENING_DIA = PUCK_BASE_DIA - 2 * RING_OVERLAP
LID_THICK = LID_FLOOR + RECESS_DEPTH
PUCK_TAPER_H = PUCK_HEIGHT - PUCK_STRAIGHT_H

# Board placement. Flipped about Y, so board-local x runs toward -X.
PI_X_USB = PI_CENTRE[0] - PI_LENGTH / 2  # box X of the USB-A end
PI_X_END = PI_CENTRE[0] + PI_LENGTH / 2  # box X of the microSD end
PI_Y0 = PI_CENTRE[1] - PI_WIDTH / 2  # box Y of the USB-C edge
PI_HOLES = [
    (PI_X_END - PI_HOLE_INSET - dx, PI_Y0 + PI_HOLE_INSET + dy)
    for dx in (0.0, PI_HOLE_PITCH_X)
    for dy in (0.0, PI_HOLE_PITCH_Y)
]
USBC_X = PI_X_END - PI_USBC_X
USBC_Z = PI_FACE_Z - PI_USBC_HEIGHT / 2  # receptacle hangs under the board
COOLER_X = PI_X_END - PI_SOC_X
COOLER_Y = PI_Y0 + PI_SOC_Y
FAN_FACE_Z = PI_FACE_Z - (PI_ASSEMBLY_H - PI_BOARD_T)

# Arms on the right-angle adapters (box coordinates)
USB_A_FACE = PI_X_USB - PI_PORT_OVERHANG  # USB-A port face
USB_A_Y = PI_Y0 + PI_USB_YS[1]  # USB 3.0 stack, the one the adapter goes on
USB_A_Z = PI_FACE_Z - 4.5  # upper port of the stack
USB_A_ARM_X = (USB_A_FACE - L_ADAPTER_DEPTH, USB_A_FACE)  # adapter + Jabra plug live here
USB_A_ARM_Y = (USB_A_Y + 8.0 - USB_A_ADAPTER[1], USB_A_Y + 8.0)  # runs toward the back
USBC_EDGE = PI_Y0 - PI_USBC_OVERHANG
USBC_ARM_Y = (USBC_EDGE - L_ADAPTER_DEPTH, USBC_EDGE)
USBC_ARM_X = (USBC_X - 6.0 - USBC_PLUG[0], USBC_X + 6.0)  # plug body runs toward -X
USBC_CABLE_Y = USBC_EDGE - L_ADAPTER_DEPTH / 2

INTAKE_ANGLES = [
    INTAKE_ANGLE + (i - (INTAKE_COUNT - 1) / 2) * INTAKE_PITCH_DEG for i in range(INTAKE_COUNT)
]
VENT_ANGLES = [VENT_ANGLE + (i - (VENT_COUNT - 1) / 2) * VENT_PITCH_DEG for i in range(VENT_COUNT)]
VENT_Z0 = LID_BOTTOM_Z - VENT_LID_GAP - VENT_H

SLOT_Y_IN = -(OPENING_DIA / 2 - 1.0)  # cable slot runs from the opening ...
SLOT_Y_OUT = -(RECESS_DIA / 2 + 1.0)  # ... out past the pocket wall

# Everything that sticks out, checked against the inner wall
KEEPOUT_POINTS = [
    (PI_X_END + PI_SD_OVERHANG, PI_Y0),
    (PI_X_END + PI_SD_OVERHANG, PI_Y0 + PI_WIDTH),
    (PI_X_USB, PI_Y0 + PI_WIDTH),
    (USB_A_ARM_X[0], USB_A_ARM_Y[0]),
    (USB_A_ARM_X[0], USB_A_ARM_Y[1]),
    (USBC_ARM_X[0], USBC_ARM_Y[0]),
    (USBC_ARM_X[1], USBC_ARM_Y[0]),
]
KEEPOUT_R = max(hypot(x, y) for x, y in KEEPOUT_POINTS)

assert OUTER_DIA <= 180.0 and BOX_HEIGHT <= 180.0, "does not fit the A1 Mini bed"
assert KEEPOUT_R < R_IN - KEEPOUT_MARGIN, f"Pi or a plug reaches the wall ({KEEPOUT_R:.1f} mm)"
assert all(hypot(x, y) + STANDOFF_DIA / 2 < R_IN for x, y in PI_HOLES), "pillar in the wall"
assert FAN_FACE_Z - FLOOR >= 8.0, "fan too close to the floor to breathe"
assert USBC_CABLE_Y - USBC_PLUG[1] / 2 > SLOT_Y_IN + 2.0, "PSU plug body reaches the cable drop"
assert OPENING_DIA >= 60.0, "opening too small to push the puck out"
assert PUCK_BASE_DIA < RECESS_DIA - 2 * 4.0, "base too close to the pocket wall for the cable"
assert PUCK_STRAIGHT_H < RECESS_DEPTH, "straight band must be inside the pocket"
assert SLOT_Y_OUT > -GROOVE_R_IN + 1.0, "cable slot reaches the lid groove"
assert R_OUT - GROOVE_R_OUT >= 1.5, "lid rim outside the groove too thin"
assert LIP_THICK >= 1.2, "lip thinner than three perimeters"
assert VENT_Z0 > FAN_FACE_Z, "exhaust slots should sit above the fan, not beside it"
assert POWER_HOLE_Z - POWER_HOLE_H / 2 > FLOOR, "power cable hole breaks into the floor"
assert STUB_HOLE_DEPTH < STANDOFF_H, "stub hole runs out of the pillar"
assert STANDOFF_DIA >= NUT_AF / 0.866 + 1.0, "pillar top narrower than the nut"
assert PI_FOOT_H > PI_GPIO_H + 0.5, "pillar top would hit the GPIO header"


def _wall_cut(angle_deg: float, z: float, width: float, height: float) -> Location:
    """Location of a radial cutter through the wall at this angle and height."""
    r = R_OUT - WALL / 2
    a = radians(angle_deg)
    return Location((r * cos(a), r * sin(a), z), (0, 0, angle_deg))


# ---------------------------------------------------------------------------
# Box
# ---------------------------------------------------------------------------
with BuildPart() as box_builder:
    Cylinder(radius=R_OUT, height=BOX_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
    chamfer(box_builder.faces().sort_by(Axis.Z)[0].edges(), length=EDGE_CHAMFER)

    # Cavity, up to the wall top
    with Locations(Pos(0, 0, FLOOR)):
        Cylinder(
            radius=R_IN,
            height=BOX_HEIGHT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # Ledge: cut the outer part of the wall away at the top, leaving the inner lip
    with BuildSketch(Plane.XY.offset(LID_BOTTOM_Z)):
        Circle(radius=R_OUT + 1)
        Circle(radius=R_OUT - LEDGE_W, mode=Mode.SUBTRACT)
    extrude(amount=LIP_HEIGHT + 1, mode=Mode.SUBTRACT)

    # Pi pillars: the cooler's corner nuts land on the flat tops, the thread
    # stubs drop into the holes
    with BuildSketch(Plane.XY.offset(FLOOR)):
        with Locations(*PI_HOLES):
            Circle(radius=STANDOFF_DIA / 2)
    extrude(amount=STANDOFF_H)
    with BuildSketch(Plane.XY.offset(FLOOR + STANDOFF_H)):
        with Locations(*PI_HOLES):
            Circle(radius=STUB_HOLE_DIA / 2)
    extrude(amount=-STUB_HOLE_DEPTH, mode=Mode.SUBTRACT)

    # Intake slots at floor level, exhaust slots up near the lid, power hole
    for ang in INTAKE_ANGLES:
        with Locations(_wall_cut(ang, INTAKE_Z0 + INTAKE_H / 2, INTAKE_W, INTAKE_H)):
            Box(WALL + 2, INTAKE_W, INTAKE_H, mode=Mode.SUBTRACT)
    for ang in VENT_ANGLES:
        with Locations(_wall_cut(ang, VENT_Z0 + VENT_H / 2, VENT_W, VENT_H)):
            Box(WALL + 2, VENT_W, VENT_H, mode=Mode.SUBTRACT)
    with Locations(_wall_cut(POWER_ANGLE, POWER_HOLE_Z, POWER_HOLE_W, POWER_HOLE_H)):
        Box(WALL + 2, POWER_HOLE_W, POWER_HOLE_H, mode=Mode.SUBTRACT)

box_part = box_builder.part


# ---------------------------------------------------------------------------
# Lid
# ---------------------------------------------------------------------------
def _rim_edge(builder: BuildPart, radius: float):
    """Topmost circular edge of this radius."""
    return (
        builder.edges()
        .filter_by(GeomType.CIRCLE)
        .filter_by(lambda e: abs(e.radius - radius) < 0.01)
        .sort_by(Axis.Z)[-1]
    )


with BuildPart() as lid_builder:
    Cylinder(radius=R_OUT, height=LID_THICK, align=(Align.CENTER, Align.CENTER, Align.MIN))
    fillet(_rim_edge(lid_builder, R_OUT), radius=LID_TOP_FILLET)

    # Annular groove in the underside for the box's lip
    with BuildSketch(Plane.XY.offset(-1)):
        Circle(radius=GROOVE_R_OUT)
        Circle(radius=GROOVE_R_IN, mode=Mode.SUBTRACT)
    extrude(amount=1 + GROOVE_DEPTH, mode=Mode.SUBTRACT)

    # Puck pocket, full puck height less what stands proud
    with Locations(Pos(0, 0, LID_THICK)):
        Cylinder(
            radius=RECESS_DIA / 2,
            height=RECESS_DEPTH,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
            mode=Mode.SUBTRACT,
        )
    chamfer(_rim_edge(lid_builder, RECESS_DIA / 2), length=POCKET_EDGE_CHAMFER)

    # Opening inside the floor ring: push-out access
    Cylinder(
        radius=OPENING_DIA / 2,
        height=LID_FLOOR + 2,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
        mode=Mode.SUBTRACT,
    )
    # Radial cable slot through the ring, toward the back of the box
    with Locations(Pos(0, (SLOT_Y_IN + SLOT_Y_OUT) / 2, LID_FLOOR / 2)):
        Box(CABLE_SLOT_W, SLOT_Y_IN - SLOT_Y_OUT, LID_FLOOR + 2, mode=Mode.SUBTRACT)

lid_part = lid_builder.part


# ---------------------------------------------------------------------------
# Preview stand-ins (visualisation only), all in the box frame
# ---------------------------------------------------------------------------
def _cable(points: list[tuple[float, float, float]], radius: float) -> Compound:
    """Schematic cable: straight tubes between the points, balls at the joints."""
    pieces = []
    pts = [Vector(*p) for p in points]
    for a, b in zip(pts, pts[1:]):
        d = b - a
        pieces.append(Solid.make_cylinder(radius, d.length, Plane(origin=a, z_dir=d)))
        pieces.append(Pos(b.X, b.Y, b.Z) * Sphere(radius))
    return Compound(children=pieces)


def _board_box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> Box:
    """Axis-aligned box from board-local x/y ranges, hanging below the board."""
    # board-local x runs toward -X (board is mirrored), y runs toward +Y
    bx0, bx1 = PI_X_END - x1, PI_X_END - x0
    return Pos(bx0, PI_Y0 + y0, z0) * Box(
        bx1 - bx0, y1 - y0, z1 - z0, align=(Align.MIN, Align.MIN, Align.MIN)
    )


def _span_box(xs: tuple, ys: tuple, zs: tuple) -> Box:
    """Axis-aligned box from (min, max) ranges in the box frame."""
    return Pos(xs[0], ys[0], zs[0]) * Box(
        xs[1] - xs[0], ys[1] - ys[0], zs[1] - zs[0], align=(Align.MIN, Align.MIN, Align.MIN)
    )


puck_z = LID_BOTTOM_Z + LID_FLOOR
puck_band = Pos(0, 0, puck_z + PUCK_TAPER_H) * Cylinder(
    radius=PUCK_DIA / 2, height=PUCK_STRAIGHT_H, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
puck_cone = Pos(0, 0, puck_z) * Cone(
    bottom_radius=PUCK_BASE_DIA / 2,
    top_radius=PUCK_DIA / 2,
    height=PUCK_TAPER_H,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
puck = puck_band + puck_cone

pi_board = Pos(PI_X_USB, PI_Y0, PI_FACE_Z) * Box(
    PI_LENGTH, PI_WIDTH, PI_BOARD_T, align=(Align.MIN, Align.MIN, Align.MIN)
)
pi_ports = Compound(
    children=[
        # USB 2.0 / 3.0 double stacks, 13 wide, past the USB end by 3
        *[
            _board_box(
                PI_LENGTH - 14.5,
                PI_LENGTH + PI_PORT_OVERHANG,
                y - 6.5,
                y + 6.5,
                PI_FACE_Z - PI_USB_STACK_H,
                PI_FACE_Z,
            )
            for y in PI_USB_YS
        ],
        # Ethernet jack
        _board_box(
            PI_LENGTH - 19.5,
            PI_LENGTH + 2.0,
            PI_ETH_Y - 8.0,
            PI_ETH_Y + 8.0,
            PI_FACE_Z - PI_ETH_H,
            PI_FACE_Z,
        ),
        # USB-C power receptacle, 9 wide, past the edge by 1.3
        _board_box(
            PI_USBC_X - 4.5,
            PI_USBC_X + 4.5,
            -PI_USBC_OVERHANG,
            7.5,
            PI_FACE_Z - PI_USBC_HEIGHT,
            PI_FACE_Z,
        ),
        # micro HDMI x2
        *[_board_box(x - 3.5, x + 3.5, -1.0, 6.5, PI_FACE_Z - 3.0, PI_FACE_Z) for x in PI_HDMI_XS],
        # GPIO header, 2 x 20
        _board_box(
            PI_GPIO_X0,
            PI_GPIO_X0 + 50.8,
            PI_GPIO_Y - 2.55,
            PI_GPIO_Y + 2.55,
            PI_FACE_Z - PI_GPIO_H,
            PI_FACE_Z,
        ),
        # microSD card on the solder side (now on top), past the end by 2.5
        _board_box(
            -PI_SD_OVERHANG,
            12.5,
            20.5,
            31.5,
            PI_FACE_Z + PI_BOARD_T,
            PI_FACE_Z + PI_BOARD_T + 1.0,
        ),
    ]
)


def _corner_stack(x: float, y: float) -> list:
    """Cooler mounting stack at one corner hole, board face down: standoff,
    bracket pad, nut, thread stub below; screw head above the solder side."""
    down = Align.MAX  # grows downward from the given z
    return [
        Pos(x, y, PI_FACE_Z)
        * Cylinder(radius=2.75, height=PI_STANDOFF_H, align=(Align.CENTER, Align.CENTER, down)),
        Pos(x, y, PI_FACE_Z - PI_STANDOFF_H)
        * Cylinder(radius=4.5, height=BRACKET_T, align=(Align.CENTER, Align.CENTER, down)),
        Pos(x, y, PI_FACE_Z - PI_STANDOFF_H - BRACKET_T)
        * Cylinder(radius=NUT_AF / 1.732, height=NUT_H, align=(Align.CENTER, Align.CENTER, down)),
        Pos(x, y, PI_FACE_Z - PI_FOOT_H)
        * Cylinder(radius=1.25, height=THREAD_STUB, align=(Align.CENTER, Align.CENTER, down)),
        Pos(x, y, PI_FACE_Z + PI_BOARD_T)
        * Cylinder(radius=2.25, height=SCREW_HEAD_H, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    ]


cooler_feet = Compound(children=[s for x, y in PI_HOLES for s in _corner_stack(x, y)])
cooler_fins = Pos(COOLER_X, COOLER_Y, FAN_FACE_Z + COOLER_FAN_T) * Box(
    COOLER_SIZE,
    COOLER_SIZE,
    PI_FACE_Z - FAN_FACE_Z - COOLER_FAN_T,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
cooler_fan = Pos(COOLER_X, COOLER_Y, FAN_FACE_Z) * Box(
    COOLER_SIZE, COOLER_SIZE, COOLER_FAN_T, align=(Align.CENTER, Align.CENTER, Align.MIN)
) - Pos(COOLER_X, COOLER_Y, FAN_FACE_Z) * Cylinder(
    radius=COOLER_SIZE / 2 - 1.5,
    height=COOLER_FAN_T - 2,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

# Right-angle USB-C adapter on the receptacle, PSU plug lying along the back edge,
# cable down and out through the back wall
usbc_adapter = _span_box((USBC_X - 6.0, USBC_X + 6.0), USBC_ARM_Y, (USBC_Z - 4.0, USBC_Z + 4.0))
usbc_plug = _span_box(
    (USBC_ARM_X[0], USBC_X - 6.0),
    (USBC_CABLE_Y - USBC_PLUG[1] / 2, USBC_CABLE_Y + USBC_PLUG[1] / 2),
    (USBC_Z - USBC_PLUG[2] / 2, USBC_Z + USBC_PLUG[2] / 2),
)
POWER_CABLE_PATH = [
    (USBC_ARM_X[0], USBC_CABLE_Y, USBC_Z),
    (USBC_ARM_X[0] - 8.0, USBC_CABLE_Y - 8.0, USBC_Z - 8.0),
    (0.0, -R_IN + 6.0, POWER_HOLE_Z),
    (0.0, -R_OUT - 20.0, POWER_HOLE_Z),
]
power_cable = _cable(POWER_CABLE_PATH, CABLE_DIA / 2)

# Right-angle USB-A adapter on the USB 3.0 stack, Jabra adapter lying along the
# board end toward the back, cable looping over the floor and up into the puck
usb_a_l_adapter = _span_box(
    USB_A_ARM_X, (USB_A_Y - 8.0, USB_A_Y + 8.0), (USB_A_Z - 8.0, USB_A_Z + 8.0)
)
usb_a_adapter = _span_box(
    (USB_A_ARM_X[0] + 2.0, USB_A_ARM_X[0] + 2.0 + USB_A_ADAPTER[0]),
    (USB_A_ARM_Y[0], USB_A_Y - 8.0),
    (USB_A_Z - USB_A_ADAPTER[2] / 2, USB_A_Z + USB_A_ADAPTER[2] / 2),
)
cable_exit = (0.0, -(PUCK_BASE_DIA / 2 + 1.0), puck_z + PUCK_CABLE_EXIT_Z)
_arm_x = USB_A_ARM_X[0] + 2.0 + USB_A_ADAPTER[0] / 2
JABRA_CABLE_PATH = [
    (_arm_x, USB_A_ARM_Y[0], USB_A_Z),
    (_arm_x, USB_A_ARM_Y[0] - 8.0, USB_A_Z - 10.0),
    (_arm_x + 10.0, -R_IN + 12.0, FLOOR + 8.0),
    (-12.0, -R_IN + 7.0, FLOOR + 6.0),
    (14.0, -R_IN + 7.0, FLOOR + 6.0),
    (24.0, -40.0, FLOOR + 8.0),
    (0.0, -(RECESS_DIA / 2 - 5.0), FLOOR + 14.0),
    (0.0, -(RECESS_DIA / 2 - 5.0), puck_z - 2.0),
    cable_exit,
]
jabra_cable = _cable(JABRA_CABLE_PATH, CABLE_DIA / 2)

lid_in_place = Pos(0, 0, LID_BOTTOM_Z) * lid_part

PREVIEW_PARTS: list[tuple[str, object]] = [
    ("box", box_part),
    ("lid", lid_in_place),
    ("puck", puck),
    ("pi_board", pi_board),
    ("pi_ports", pi_ports),
    ("cooler_feet", cooler_feet),
    ("cooler_fins", cooler_fins),
    ("cooler_fan", cooler_fan),
    ("usbc_plug", usbc_adapter + usbc_plug),
    ("power_cable", power_cable),
    ("usb_a_adapter", usb_a_l_adapter + usb_a_adapter),
    ("jabra_cable", jabra_cable),
]
assembly = Compound(label="smart-speaker-case", children=[shape for _, shape in PREVIEW_PARTS])


# ---------------------------------------------------------------------------
# Fit-test pieces
# ---------------------------------------------------------------------------
TEST_WALL = 3.0  # wall of the two puck test pieces
TEST_COLLAR_H = 8.0  # collar: the pocket mouth, slips over the straight band
TEST_CUP_WALL_H = 8.0  # cup: short wall above the floor ring
TEST_JOINT_DIA = 60.0  # mini round box / lid pair, real wall, ledge, lip and groove
TEST_JOINT_H = 20.0  # mini box wall height including the lip
TEST_JOINT_FLOOR = 2.0
TEST_LID_THICK = 8.0

with BuildPart() as collar_builder:
    Cylinder(
        radius=RECESS_DIA / 2 + TEST_WALL,
        height=TEST_COLLAR_H,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    with Locations(Pos(0, 0, -1)):
        Cylinder(
            radius=RECESS_DIA / 2,
            height=TEST_COLLAR_H + 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )
    chamfer(_rim_edge(collar_builder, RECESS_DIA / 2), length=POCKET_EDGE_CHAMFER)
test_collar = collar_builder.part

with BuildPart() as cup_builder:
    Cylinder(
        radius=RECESS_DIA / 2 + TEST_WALL,
        height=LID_FLOOR + TEST_CUP_WALL_H,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    with Locations(Pos(0, 0, LID_FLOOR)):
        Cylinder(
            radius=RECESS_DIA / 2,
            height=TEST_CUP_WALL_H + 1,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )
    with Locations(Pos(0, 0, -1)):
        Cylinder(
            radius=OPENING_DIA / 2,
            height=LID_FLOOR + 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )
    with Locations(Pos(0, (SLOT_Y_IN + SLOT_Y_OUT) / 2, LID_FLOOR / 2)):
        Box(CABLE_SLOT_W, SLOT_Y_IN - SLOT_Y_OUT, LID_FLOOR + 2, mode=Mode.SUBTRACT)
test_cup = cup_builder.part

with BuildPart() as test_box_builder:
    r = TEST_JOINT_DIA / 2
    Cylinder(radius=r, height=TEST_JOINT_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    chamfer(test_box_builder.faces().sort_by(Axis.Z)[0].edges(), length=EDGE_CHAMFER)
    with Locations(Pos(0, 0, TEST_JOINT_FLOOR)):
        Cylinder(
            radius=r - WALL,
            height=TEST_JOINT_H,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )
    with BuildSketch(Plane.XY.offset(TEST_JOINT_H - LIP_HEIGHT)):
        Circle(radius=r + 1)
        Circle(radius=r - LEDGE_W, mode=Mode.SUBTRACT)
    extrude(amount=LIP_HEIGHT + 1, mode=Mode.SUBTRACT)
test_box = test_box_builder.part

with BuildPart() as test_lid_builder:
    r = TEST_JOINT_DIA / 2
    Cylinder(radius=r, height=TEST_LID_THICK, align=(Align.CENTER, Align.CENTER, Align.MIN))
    fillet(_rim_edge(test_lid_builder, r), radius=LID_TOP_FILLET)
    with BuildSketch(Plane.XY.offset(-1)):
        Circle(radius=r - LEDGE_W + JOINT_CLEARANCE)
        Circle(radius=r - WALL - JOINT_CLEARANCE, mode=Mode.SUBTRACT)
    extrude(amount=1 + GROOVE_DEPTH, mode=Mode.SUBTRACT)
test_lid = test_lid_builder.part

# Pillar jig: the real pillars at the real pitch on a thin plate
TEST_JIG_PLATE_T = 2.0
TEST_JIG_MARGIN = 6.0  # plate beyond the pillar centres
with BuildPart() as jig_builder:
    Box(
        PI_HOLE_PITCH_X + 2 * TEST_JIG_MARGIN,
        PI_HOLE_PITCH_Y + 2 * TEST_JIG_MARGIN,
        TEST_JIG_PLATE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    jig_holes = [
        (sx * PI_HOLE_PITCH_X / 2, sy * PI_HOLE_PITCH_Y / 2) for sx in (-1, 1) for sy in (-1, 1)
    ]
    with BuildSketch(Plane.XY.offset(TEST_JIG_PLATE_T)):
        with Locations(*jig_holes):
            Circle(radius=STANDOFF_DIA / 2)
    extrude(amount=STANDOFF_H)
    with BuildSketch(Plane.XY.offset(TEST_JIG_PLATE_T + STANDOFF_H)):
        with Locations(*jig_holes):
            Circle(radius=STUB_HOLE_DIA / 2)
    extrude(amount=-STUB_HOLE_DEPTH, mode=Mode.SUBTRACT)
test_jig = jig_builder.part


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    export_stl(box_part, str(OUTPUT_DIR / "box.stl"))
    export_stl(lid_part, str(OUTPUT_DIR / "lid.stl"))
    export_stl(
        assembly, str(OUTPUT_DIR / "assembly-preview.stl"), tolerance=0.3, angular_tolerance=0.4
    )
    export_stl(test_collar, str(OUTPUT_DIR / "fit-test-puck-collar.stl"))
    export_stl(test_cup, str(OUTPUT_DIR / "fit-test-puck-cup.stl"))
    export_stl(test_box, str(OUTPUT_DIR / "fit-test-joint-box.stl"))
    export_stl(test_lid, str(OUTPUT_DIR / "fit-test-joint-lid.stl"))
    export_stl(test_jig, str(OUTPUT_DIR / "fit-test-pillars.stl"))
    print(f"Exported box / lid / assembly-preview / 5 fit tests to: {OUTPUT_DIR}")

    box_cm3 = box_part.volume / 1000
    lid_cm3 = lid_part.volume / 1000
    total_h = max(puck_z + PUCK_HEIGHT, LID_BOTTOM_Z + LID_THICK)
    print(f"  box:        Ø{OUTER_DIA:.0f} x {BOX_HEIGHT:.0f} mm, {box_cm3:.0f} cm3")
    print(f"  lid:        Ø{OUTER_DIA:.0f} x {LID_THICK:.1f} mm, {lid_cm3:.0f} cm3")
    print(f"  assembled:  Ø{OUTER_DIA:.0f} x {total_h:.1f} mm, puck {PUCK_PROUD:.1f} proud")
    print(f"  puck nest:  Ø{RECESS_DIA:.1f} x {RECESS_DEPTH:.1f} deep, ring to Ø{OPENING_DIA:.0f}")
    print(
        f"  Pi:         x {PI_X_USB:.1f} .. {PI_X_END:.1f}, y {PI_Y0:.1f} .. {PI_Y0 + PI_WIDTH:.1f}"
    )
    print(f"  keep-out:   farthest corner at r={KEEPOUT_R:.1f}, wall at r={R_IN:.1f}")
    print(f"  pillars:    {STANDOFF_H:.1f} mm tall, fan face at z={FAN_FACE_Z:.1f}")
    print(f"  Pi rests:   on its 4 nuts, {PI_FOOT_H:.1f} mm below the board face")
    print("  Pi screws:  4 x M2.5 x 6 from the solder side (replace the long brass standoffs)")
    tests = [test_collar, test_cup, test_box, test_lid, test_jig]
    print(f"  fit tests:  {', '.join(f'{t.volume / 1000:.0f} cm3' for t in tests)} solid")
    hole = f"{POWER_HOLE_W:.1f} x {POWER_HOLE_H:.1f} mm"
    print(f"  power hole: at {POWER_ANGLE:.0f} deg, z={POWER_HOLE_Z:.1f}, {hole}")

    if show is not None:
        try:
            show(assembly)
        except Exception as e:  # viewer not running is fine
            print(f"(ocp_vscode viewer not connected: {e})")
