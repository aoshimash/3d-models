"""Stand-alone switch box for the SwitchBot RGBIC floor lamp — prototype Ver.0.2.

A floor box that takes the lamp's inline controller and *all* of the spare
cord off the lamp. The button is pressed through a window in the top, the
cords leave through two small holes at floor level, and the length outside is
whatever is not stuffed inside.

Three printed parts, no fasteners:

    bin   — an open tray: floor, walls, a cord slit down each end wall from
            the rim to the floor, and three Ø6 pins behind each slit that the
            exiting cord weaves through.
    tray  — a plate that rests on the bin rim, with a closed-bottom well for
            the controller hanging from it into the bin. The well's end walls
            are notched from the top for the cables.
    cap   — top skin with the button window and a skirt that reaches down the
            outside of the bin almost to the floor.

What Ver.0.1 got wrong (printed, 2026-10-11)
--------------------------------------------
1. Capacity. Ver.0.1 assumed the Ø4 cord would wind neatly round two Ø12
   posts, five turns a layer. It does not: the cord, two Ø10 plugs, the
   boots and the Ø2 adapter lead stuff loosely at roughly 10 % of the space
   they are given, and the 115 cm3 under the controller was half of what the
   cords need.
2. The controller sat on the *tops* of the two posts with open space round
   them. Stuffed cord rode up onto the post tops and under the controller, so
   the lid could not close and the seat was lost. Nothing held the controller
   down until the lid was on.

Ver.0.2 fixes both: the controller sits in a well with a solid floor (cord
cannot get under it, whatever is stuffed round it), the well hangs into a
bin of ~345 cm3 free volume (6–7 % fill for every cord the lamp has, adapter
lead included), and the exposed length is held by a serpentine at each exit
instead of by winding.

How the serpentine holds the cord
---------------------------------
Behind each exit hole three Ø6 pins stand in a line PIN_PITCH apart on the
box's long axis. The cord is laid in from above (bin open, tray off) and
weaves left-right round them, so it bends about 80° at each pin. A pull from
outside is resisted by friction over ~280° of contact; pushing cord in from
outside meets the same friction. To change the exposed length, lift the cap
and the tray and move the cord through the weave by hand.

How the slit becomes a small hole
---------------------------------
Bin end wall: slit SLIT_WIDTH wide from the rim down to the floor top.
Cap skirt:    notch SLIT_WIDTH wide from its bottom edge up to HOLE_HEIGHT
              above the floor top, rounded at the top.
Each one is covered by the other wall once the cap is on; what stays open is
their overlap, a SLIT_WIDTH x HOLE_HEIGHT hole at the bottom of the end wall.
The cap comes down over a cord already lying in the slit, because its notch
is open at the bottom.

The stack (z = 0 is the floor)
------------------------------
    Z_TOP          cap skin top; the button window is a 2.5 mm deep well
    Z_PLATE_TOP    tray plate top = skin underside = controller face + FACE_CLEARANCE
    Z_FACE         controller face
    Z_RIM          bin rim = tray plate underside
    Z_SEAT         well floor = controller underside
    Z_WELL_BOTTOM  underside of the hanging well; cord space continues below it
    Z_FLOOR_TOP    bin floor; the cord exit holes start here; pins stand here
    Z_SKIRT_BOTTOM cap skirt bottom edge, GROUND_CLEARANCE above the floor
    0              floor

Button loads go finger -> controller -> well floor -> well walls -> tray
plate -> bin rim -> bin walls -> floor. The cap carries nothing.

Measured vs assumed
-------------------
Controller, cable and cord figures are carried over from
switchbot-lamp-base-case (user measurements, photos and SwitchBot support
Q&A). Tags: [M] measured [P] from photos [S] spec sheet [A] assumed [D] design.
Still not measured: where the button strip sits on the controller face
(BUTTON_AREA_OFFSET_X/Y, assumed centred). test-well + test-window check it.

Print notes
-----------
- bin: as modelled, open side up. Pins and slits are vertical. No supports.
- tray: plate-down (the exported STL is already flipped). The well walls grow
  up from the plate and its floor closes them at the top as a WELL_INNER_W
  (35.5 mm) bridge. PETG bridges that span with slight sag on the hidden
  underside; if your printer will not, add supports inside the well cavity
  only — it is an open 91.5 x 35.5 x 17 pocket and they pull straight out.
- cap: skin-down (STL already flipped). Skirt grows straight up, the skirt
  notches are open at the top of the print. No supports.
- PETG, 0.2 mm layers, 3 walls. Everything is essentially perimeter.
"""

from math import pi
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Color,
    Compound,
    Cylinder,
    ExportSVG,
    LineType,
    Location,
    Locations,
    Mode,
    Part,
    Plane,
    RectangleRounded,
    Sphere,
    Torus,
    Vector,
    add,
    chamfer,
    export_step,
    export_stl,
    extrude,
    loft,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# ===========================================================================
# Parameters   [M] measured  [P] from photos  [S] spec sheet  [A] assumed  [D] design
# ===========================================================================

# --- Controller (mm) — carried over from switchbot-lamp-base-case ---
CONTROLLER_LENGTH = 90.5  # [M] long side, along X
CONTROLLER_WIDTH = 34.5  # [M] short side, along Y
CONTROLLER_HEIGHT = 16.5  # [M]
CONTROLLER_CORNER_RADIUS = 4.0  # [A] plan-view corner radius of the housing
BUTTON_AREA_LENGTH = 71.0  # [M] the button strip on the face, along X
BUTTON_AREA_WIDTH = 16.0  # [M] along Y
BUTTON_AREA_OFFSET_X = 0.0  # [A] button strip centre relative to the housing centre — NOT measured
BUTTON_AREA_OFFSET_Y = 0.0  # [A] likewise
BUTTON_AREA_PROUD = 0.3  # [A] how far the strip stands above the face (stand-in only)
CONTROLLER_CABLE_EXIT_HEIGHT = CONTROLLER_HEIGHT / 2  # [M] cables leave at mid-height
CABLE_BOOT_DIAMETER = 6.0  # [M] strain-relief boot where each cable leaves the controller
CABLE_BOOT_LENGTH = 5.0  # [M]
CABLE_PAIR_PITCH = 8.0  # [M] centre distance of the two cables on the -X end
CABLE_SLOT_MARGIN = 1.5  # [D] per side, well notch wider than the boots
CABLE_SLOT_WIDTH_LEFT = CABLE_PAIR_PITCH + CABLE_BOOT_DIAMETER + 2 * CABLE_SLOT_MARGIN  # two cables
CABLE_SLOT_WIDTH_RIGHT = CABLE_BOOT_DIAMETER + 2 * CABLE_SLOT_MARGIN  # one cable
CABLE_SLOT_OFFSET_LEFT = 0.0  # [A] notch centre offset along Y from the controller centreline
CABLE_SLOT_OFFSET_RIGHT = 0.0  # [A]

# --- Cords (mm) ---
CABLE_DIAMETER = 4.0  # [M] controller cords and lamp pigtail
CABLE_DIAMETER_ADAPTER = 2.0  # [M] the AC adapter lead is thinner
CABLE_BEND_RADIUS = 8.0  # [A] centreline radius the Ø4 cord takes leaving the well (stand-in)
CONNECTOR_DIAMETER = 10.0  # [A] barrel plugs
CONNECTOR_LENGTH = 35.0  # [A]
CONTROLLER_CABLE_LAMP_SIDE = 580.0  # [S+P] controller to plug A
CONTROLLER_CABLE_ADAPTER_SIDE = 330.0  # [S+P] controller to plug B — stored entirely
CONTROLLER_SPARE_PIGTAIL = 300.0  # [P] second output with its own plug — stored entirely
ADAPTER_CORD_LENGTH = 1500.0  # [S] plug B to the AC adapter
CORD_OUTSIDE_LAMP_SIDE = 150.0  # [A] plug A to the box when the box sits beside the lamp base
CORD_OUTSIDE_OUTLET_SIDE = 500.0  # [A] box to the AC adapter at the outlet
PACKING_FRACTION = 0.08  # [A] solid cord volume / free volume for cord stuffed in loosely

# --- Bin (mm) ---
WALL_THICKNESS = 2.0  # [D] bin walls
FLOOR_THICKNESS = 2.0  # [D] bin floor
BIN_LENGTH = 156.0  # [D] interior, along X
BIN_WIDTH = 74.0  # [D] interior, along Y
BIN_DEPTH = 36.0  # [D] floor top to rim
PIN_DIAMETER = 6.0  # [D] serpentine pins
PIN_HEIGHT = 14.0  # [D] above the floor top
PIN_COUNT = 3  # [D] per exit
PIN_PITCH = 12.0  # [D] centre to centre along X; leaves a 6 mm gap for the cord to cross
PIN_FIRST_FROM_WALL = 10.0  # [D] end wall inner face to the first pin centre
LANE_Y = 15.0  # [D] cord lane (pins and exit holes) offset from the centreline, +Y side

# --- Tray (mm) ---
PLATE_THICKNESS = 2.5  # [D] tray plate on the bin rim
WELL_WALL_THICKNESS = 2.0  # [D]
WELL_FLOOR_THICKNESS = 3.0  # [D] the bridged floor under the controller
WELL_LEAD_IN = 1.0  # [D] 45° taper round the well mouth
LIP_THICKNESS = 1.6  # [D] locating lip under the plate, inside the bin walls
LIP_HEIGHT = 4.0  # [D]
LIP_CLEARANCE = 0.25  # [D] per side, lip inside the bin walls
PLATE_EDGE_INSET = 0.1  # [D] per side, plate edge inside the bin's outer face
CONTROLLER_CLEARANCE = 0.5  # [D] per side, controller in the well (checked on Ver.0.2 base case)
FACE_CLEARANCE = 0.5  # [D] controller face to skin underside — must clear BUTTON_AREA_PROUD
NOTCH_BOTTOM_MARGIN = 1.5  # [D] well notch bottom below the boot

# --- Cap (mm) ---
SKIN_THICKNESS = 2.0  # [D] cap top
SKIRT_THICKNESS = 2.0  # [D] cap outer wall
CAP_CLEARANCE = 0.25  # [D] per side, skirt over the bin wall (sliding fit)
WINDOW_MARGIN = 1.5  # [D] per side, window larger than the button strip
WINDOW_CORNER_RADIUS = 3.0  # [D]
SLIT_CLEARANCE = 0.5  # [D] per side, slit and notch wider than the Ø4 cord
HOLE_HEIGHT = 7.0  # [D] open height of the cord exit above the floor top
GROUND_CLEARANCE = 1.0  # [D] skirt bottom edge above the floor
CAP_CORNER_RADIUS = 4.0  # [D] plan-view corner radius of the cap
TOP_CHAMFER = 1.0  # [D] cap top edge

# --- Finish ---
PETG_DENSITY = 1.27  # g/cm3
PRINT_SOLID_FRACTION = 0.9  # walls dominate; infill is a rounding error

# ===========================================================================
# Derived geometry
# ===========================================================================
OUTPUT_DIR = Path(__file__).parent / "output"
DRAWING_DIR = OUTPUT_DIR / "drawings"

# Well — controller outline plus clearance, walls outside that.
WELL_INNER_L = CONTROLLER_LENGTH + 2 * CONTROLLER_CLEARANCE
WELL_INNER_W = CONTROLLER_WIDTH + 2 * CONTROLLER_CLEARANCE
WELL_INNER_R = CONTROLLER_CORNER_RADIUS + CONTROLLER_CLEARANCE
WELL_OUTER_L = WELL_INNER_L + 2 * WELL_WALL_THICKNESS
WELL_OUTER_W = WELL_INNER_W + 2 * WELL_WALL_THICKNESS
WELL_OUTER_R = WELL_INNER_R + WELL_WALL_THICKNESS

# Bin, tray, cap outlines
BIN_OUTER_L = BIN_LENGTH + 2 * WALL_THICKNESS
BIN_OUTER_W = BIN_WIDTH + 2 * WALL_THICKNESS
CAP_INNER_R = CAP_CORNER_RADIUS - SKIRT_THICKNESS
BIN_CORNER_R = CAP_INNER_R - CAP_CLEARANCE
BIN_CAVITY_R = 1.0
CAP_INNER_L = BIN_OUTER_L + 2 * CAP_CLEARANCE
CAP_INNER_W = BIN_OUTER_W + 2 * CAP_CLEARANCE
CAP_L = CAP_INNER_L + 2 * SKIRT_THICKNESS
CAP_W = CAP_INNER_W + 2 * SKIRT_THICKNESS
PLATE_L = BIN_OUTER_L - 2 * PLATE_EDGE_INSET
PLATE_W = BIN_OUTER_W - 2 * PLATE_EDGE_INSET
PLATE_R = max(BIN_CORNER_R - PLATE_EDGE_INSET, 0.5)
LIP_OUTER_L = BIN_LENGTH - 2 * LIP_CLEARANCE
LIP_OUTER_W = BIN_WIDTH - 2 * LIP_CLEARANCE

# Heights
Z_FLOOR_TOP = FLOOR_THICKNESS
Z_RIM = Z_FLOOR_TOP + BIN_DEPTH
Z_PLATE_TOP = Z_RIM + PLATE_THICKNESS
Z_SKIN_BOTTOM = Z_PLATE_TOP
Z_TOP = Z_SKIN_BOTTOM + SKIN_THICKNESS
Z_FACE = Z_PLATE_TOP - FACE_CLEARANCE
Z_SEAT = Z_FACE - CONTROLLER_HEIGHT
Z_WELL_BOTTOM = Z_SEAT - WELL_FLOOR_THICKNESS
Z_CABLE = Z_SEAT + CONTROLLER_CABLE_EXIT_HEIGHT
Z_NOTCH_BOTTOM = Z_CABLE - CABLE_BOOT_DIAMETER / 2 - NOTCH_BOTTOM_MARGIN
Z_LIP_BOTTOM = Z_RIM - LIP_HEIGHT
Z_SKIRT_BOTTOM = GROUND_CLEARANCE
Z_HOLE_TOP = Z_FLOOR_TOP + HOLE_HEIGHT

# Cord exit, pins and the weave
SLIT_WIDTH = CABLE_DIAMETER + 2 * SLIT_CLEARANCE
WINDOW_L = BUTTON_AREA_LENGTH + 2 * WINDOW_MARGIN
WINDOW_W = BUTTON_AREA_WIDTH + 2 * WINDOW_MARGIN
X_BIN_WALL = BIN_LENGTH / 2 + WALL_THICKNESS / 2  # end wall centreline
X_SKIRT_END = CAP_INNER_L / 2 + SKIRT_THICKNESS / 2  # cap end wall centreline
PIN_R = PIN_DIAMETER / 2
PIN_XS = [BIN_LENGTH / 2 - PIN_FIRST_FROM_WALL - k * PIN_PITCH for k in range(PIN_COUNT)]
WEAVE_Y = PIN_R + CABLE_DIAMETER / 2 + 0.3  # cord centreline beside a pin, stand-in only
Z_CORD_FLOOR = Z_FLOOR_TOP + CABLE_DIAMETER / 2

# Where the cord goes after the boot: straight to the boot tip, then a quarter bend down.
X_BOOT_TIP = CONTROLLER_LENGTH / 2 + CABLE_BOOT_LENGTH
X_DROP = X_BOOT_TIP + CABLE_BEND_RADIUS  # centreline of the vertical run in the end zone
Z_BEND_CENTRE = Z_CABLE - CABLE_BEND_RADIUS
END_ZONE = BIN_LENGTH / 2 - WELL_OUTER_L / 2  # well end wall to bin end wall

# Plug stowage stand-in: standing in the bin corners, clear of the weave, the drops and the lip.
PLUG_X = BIN_LENGTH / 2 - PIN_FIRST_FROM_WALL - CONNECTOR_DIAMETER / 2
PLUG_Y = LIP_OUTER_W / 2 - LIP_THICKNESS - 1.0 - CONNECTOR_DIAMETER / 2

# Capacity: loose stuffing, solid cord volume against the free volume of the bin.
CORD_SOLID_MM3 = (
    pi
    * (CABLE_DIAMETER / 2) ** 2
    * (
        (CONTROLLER_CABLE_LAMP_SIDE - CORD_OUTSIDE_LAMP_SIDE)
        + CONTROLLER_SPARE_PIGTAIL
        + CONTROLLER_CABLE_ADAPTER_SIDE
    )
    + pi * (CABLE_DIAMETER_ADAPTER / 2) ** 2 * (ADAPTER_CORD_LENGTH - CORD_OUTSIDE_OUTLET_SIDE)
    + 2 * pi * (CONNECTOR_DIAMETER / 2) ** 2 * CONNECTOR_LENGTH
)
WELL_HANG_MM3 = WELL_OUTER_L * WELL_OUTER_W * (Z_RIM - Z_WELL_BOTTOM)
PINS_MM3 = 2 * PIN_COUNT * pi * PIN_R**2 * PIN_HEIGHT
LIP_MM3 = 2 * (LIP_OUTER_L + LIP_OUTER_W) * LIP_THICKNESS * LIP_HEIGHT
FREE_MM3 = BIN_LENGTH * BIN_WIDTH * BIN_DEPTH - WELL_HANG_MM3 - PINS_MM3 - LIP_MM3
FILL_FRACTION = CORD_SOLID_MM3 / FREE_MM3

# ===========================================================================
# Layout checks
# ===========================================================================
assert BUTTON_AREA_PROUD < FACE_CLEARANCE, "button strip would touch the skin"
assert abs(BUTTON_AREA_OFFSET_X) + WINDOW_L / 2 <= CONTROLLER_LENGTH / 2 - 1.0, (
    "window runs off the controller face (X)"
)
assert abs(BUTTON_AREA_OFFSET_Y) + WINDOW_W / 2 <= CONTROLLER_WIDTH / 2 - 1.0, (
    "window runs off the controller face (Y)"
)
assert Z_WELL_BOTTOM - Z_FLOOR_TOP >= 3 * CABLE_DIAMETER, "no cord space under the well"
assert Z_WELL_BOTTOM > Z_FLOOR_TOP + PIN_HEIGHT + 1.0, "well lands on the pins"
assert WELL_OUTER_W + 2 * 4.0 <= BIN_WIDTH, "no cord space beside the well"
assert END_ZONE >= X_DROP - WELL_OUTER_L / 2 + CABLE_DIAMETER / 2 + 1.0, (
    "end zone too short for the cord to bend down"
)
assert PIN_PITCH - PIN_DIAMETER >= CABLE_DIAMETER + 1.5, "cord cannot cross between the pins"
assert PIN_XS[-1] - PIN_R > WELL_OUTER_L / 2 - 8.0, "weave runs too far under the well"
assert PIN_FIRST_FROM_WALL - PIN_R >= CABLE_DIAMETER + 2.0, "first pin too close to the hole"
assert LANE_Y - WEAVE_Y - CABLE_DIAMETER / 2 >= CABLE_PAIR_PITCH / 2 + CABLE_DIAMETER / 2 + 0.5, (
    "cord lane runs into the cables dropping from the well"
)
assert LANE_Y + WEAVE_Y + CABLE_DIAMETER / 2 + 1.0 <= PLUG_Y - CONNECTOR_DIAMETER / 2, (
    "cord lane runs into the stowed plug"
)
assert Z_NOTCH_BOTTOM > Z_SEAT, "well notch cuts into the floor"
assert Z_HOLE_TOP + 1.0 < Z_WELL_BOTTOM, "cord exit hole reaches the well"
assert SLIT_WIDTH < CONNECTOR_DIAMETER, "a plug could slip out through the slit"
assert PLUG_X - CONNECTOR_DIAMETER / 2 > X_DROP + CABLE_DIAMETER / 2 + 0.5 or (
    PLUG_Y - CONNECTOR_DIAMETER / 2 > CABLE_PAIR_PITCH / 2 + CABLE_DIAMETER / 2 + 1.0
), "plug collides with the dropping cords"
assert CONNECTOR_LENGTH <= Z_LIP_BOTTOM - Z_FLOOR_TOP - 1.0 or (
    PLUG_Y + CONNECTOR_DIAMETER / 2 < LIP_OUTER_W / 2 - LIP_THICKNESS
), "plug hits the tray lip"
assert FILL_FRACTION <= PACKING_FRACTION, (
    f"cords need {CORD_SOLID_MM3 / PACKING_FRACTION / 1000:.0f} cm3, bin has {FREE_MM3 / 1000:.0f}"
)
assert CAP_L <= 180 and CAP_W <= 180 and Z_TOP <= 180, "cap does not fit the A1 Mini bed"


# ===========================================================================
# Parts
# ===========================================================================
def build_bin() -> Part:
    with BuildPart() as b:
        with BuildSketch(Plane.XY):
            RectangleRounded(BIN_OUTER_L, BIN_OUTER_W, BIN_CORNER_R)
        extrude(amount=Z_RIM)
        with BuildSketch(Plane.XY.offset(Z_FLOOR_TOP)):
            RectangleRounded(BIN_LENGTH, BIN_WIDTH, BIN_CAVITY_R)
        extrude(amount=BIN_DEPTH + 1.0, mode=Mode.SUBTRACT)
        # Serpentine pins behind each exit, in a line on the long axis.
        with Locations(*[(sx * x, LANE_Y, Z_FLOOR_TOP) for sx in (-1, 1) for x in PIN_XS]):
            Cylinder(PIN_R, PIN_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Cord slits: both end walls, rim down to the floor top.
        for sx in (-1, 1):
            with Locations((sx * X_BIN_WALL, LANE_Y, Z_FLOOR_TOP)):
                Box(
                    WALL_THICKNESS + 2.0,
                    SLIT_WIDTH,
                    BIN_DEPTH + 1.0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
    return b.part


def build_tray() -> Part:
    with BuildPart() as t:
        # Plate on the rim.
        with BuildSketch(Plane.XY.offset(Z_RIM)):
            RectangleRounded(PLATE_L, PLATE_W, PLATE_R)
        extrude(amount=PLATE_THICKNESS)
        # Locating lip under the plate, inside the bin walls.
        with BuildSketch(Plane.XY.offset(Z_LIP_BOTTOM)):
            RectangleRounded(LIP_OUTER_L, LIP_OUTER_W, max(BIN_CAVITY_R - LIP_CLEARANCE, 0.5))
            RectangleRounded(
                LIP_OUTER_L - 2 * LIP_THICKNESS,
                LIP_OUTER_W - 2 * LIP_THICKNESS,
                0.5,
                mode=Mode.SUBTRACT,
            )
        extrude(amount=LIP_HEIGHT)
        # The well: outer block hanging from the plate, cavity from the plate top down to the seat.
        with BuildSketch(Plane.XY.offset(Z_WELL_BOTTOM)):
            RectangleRounded(WELL_OUTER_L, WELL_OUTER_W, WELL_OUTER_R)
        extrude(amount=Z_RIM - Z_WELL_BOTTOM)
        with BuildSketch(Plane.XY.offset(Z_SEAT)):
            RectangleRounded(WELL_INNER_L, WELL_INNER_W, WELL_INNER_R)
        extrude(amount=Z_PLATE_TOP - Z_SEAT + 1.0, mode=Mode.SUBTRACT)
        # Lead-in round the mouth.
        with BuildSketch(Plane.XY.offset(Z_PLATE_TOP + 0.01)):
            RectangleRounded(
                WELL_INNER_L + 2 * WELL_LEAD_IN,
                WELL_INNER_W + 2 * WELL_LEAD_IN,
                WELL_INNER_R + WELL_LEAD_IN,
            )
        with BuildSketch(Plane.XY.offset(Z_PLATE_TOP - WELL_LEAD_IN)):
            RectangleRounded(WELL_INNER_L, WELL_INNER_W, WELL_INNER_R)
        loft(mode=Mode.SUBTRACT)
        # Cable notches through the well end walls and the plate, open at the top.
        for sx, width, offset in (
            (-1, CABLE_SLOT_WIDTH_LEFT, CABLE_SLOT_OFFSET_LEFT),
            (1, CABLE_SLOT_WIDTH_RIGHT, CABLE_SLOT_OFFSET_RIGHT),
        ):
            with Locations(
                (sx * (WELL_INNER_L / 2 + WELL_WALL_THICKNESS / 2), offset, Z_NOTCH_BOTTOM)
            ):
                Box(
                    WELL_WALL_THICKNESS + 1.0,
                    width,
                    Z_PLATE_TOP - Z_NOTCH_BOTTOM + 1.0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
    return t.part


def build_cap() -> Part:
    with BuildPart() as c:
        with BuildSketch(Plane.XY.offset(Z_SKIRT_BOTTOM)):
            RectangleRounded(CAP_L, CAP_W, CAP_CORNER_RADIUS)
        extrude(amount=Z_TOP - Z_SKIRT_BOTTOM)
        chamfer(c.edges().group_by(Axis.Z)[-1], length=TOP_CHAMFER)
        # Hollow under the skin — bin and tray slide in here.
        with BuildSketch(Plane.XY.offset(Z_SKIRT_BOTTOM - 1.0)):
            RectangleRounded(CAP_INNER_L, CAP_INNER_W, CAP_INNER_R)
        extrude(amount=Z_SKIN_BOTTOM - Z_SKIRT_BOTTOM + 1.0, mode=Mode.SUBTRACT)
        # Button window through the skin.
        with BuildSketch(Plane.XY.offset(Z_SKIN_BOTTOM - 1.0)):
            with Locations((BUTTON_AREA_OFFSET_X, BUTTON_AREA_OFFSET_Y)):
                RectangleRounded(WINDOW_L, WINDOW_W, WINDOW_CORNER_RADIUS)
        extrude(amount=SKIN_THICKNESS + 2.0, mode=Mode.SUBTRACT)
        # Cord notches in the skirt bottom edge, rounded at the top.
        for sx in (-1, 1):
            with Locations((sx * X_SKIRT_END, LANE_Y, Z_SKIRT_BOTTOM - 1.0)):
                Box(
                    SKIRT_THICKNESS + 2.0,
                    SLIT_WIDTH,
                    Z_HOLE_TOP - SLIT_WIDTH / 2 - Z_SKIRT_BOTTOM + 1.0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
            with Locations((sx * X_SKIRT_END, LANE_Y, Z_HOLE_TOP - SLIT_WIDTH / 2)):
                Cylinder(
                    SLIT_WIDTH / 2, SKIRT_THICKNESS + 2.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT
                )
    return c.part


def build_controller_stand_in() -> Part:
    with BuildPart() as c:
        with BuildSketch(Plane.XY.offset(Z_SEAT)):
            RectangleRounded(CONTROLLER_LENGTH, CONTROLLER_WIDTH, CONTROLLER_CORNER_RADIUS)
        extrude(amount=CONTROLLER_HEIGHT)
        with BuildSketch(Plane.XY.offset(Z_FACE)):
            with Locations((BUTTON_AREA_OFFSET_X, BUTTON_AREA_OFFSET_Y)):
                RectangleRounded(BUTTON_AREA_LENGTH, BUTTON_AREA_WIDTH, 2.0)
        extrude(amount=BUTTON_AREA_PROUD)
        # Boots: two on the -X end, one on the +X end.
        for sx, y in (
            (-1, CABLE_SLOT_OFFSET_LEFT - CABLE_PAIR_PITCH / 2),
            (-1, CABLE_SLOT_OFFSET_LEFT + CABLE_PAIR_PITCH / 2),
            (1, CABLE_SLOT_OFFSET_RIGHT),
        ):
            with Locations((sx * CONTROLLER_LENGTH / 2, y, Z_CABLE)):
                Cylinder(
                    CABLE_BOOT_DIAMETER / 2,
                    CABLE_BOOT_LENGTH,
                    rotation=(0, 90, 0),
                    align=(Align.CENTER, Align.CENTER, Align.MIN if sx > 0 else Align.MAX),
                )
    return c.part


def segment(p0: tuple, p1: tuple, diameter: float) -> Part:
    """A cylinder from p0 to p1."""
    v = Vector(*p1) - Vector(*p0)
    with BuildPart(Plane(origin=Vector(*p0), z_dir=v)) as s:
        Cylinder(diameter / 2, v.length, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return s.part


def weave_points(sx: int) -> list[tuple[float, float, float]]:
    """Cord centreline through one exit: outside -> hole -> round the pins -> free."""
    z = Z_CORD_FLOOR
    pts = [(CAP_L / 2 + 15.0, 0.0, z), (BIN_LENGTH / 2 - CABLE_DIAMETER, 0.0, z)]
    for k, x in enumerate(PIN_XS):
        side = WEAVE_Y if k % 2 == 0 else -WEAVE_Y
        pts.append((x + PIN_R, side, z))
        pts.append((x - PIN_R, side, z))
    pts.append((PIN_XS[-1] - PIN_R - 5.0, 0.0, z))
    return [(sx * x, LANE_Y + y, z) for x, y, z in pts]


def build_cord_stand_ins() -> dict[str, Part]:
    """Rough cord: the weave through both exits, the drops from the well ends,
    two loose coils under the well, and the two plugs standing in the corners."""
    parts: dict[str, Part] = {}
    with BuildPart() as weave:
        for sx in (-1, 1):
            pts = weave_points(sx)
            for p0, p1 in zip(pts, pts[1:]):
                add(segment(p0, p1, CABLE_DIAMETER))
            for p in pts[1:-1]:
                with Locations(p):
                    Sphere(CABLE_DIAMETER / 2)
    parts["cord-weave"] = weave.part
    with BuildPart() as drops:
        for sx, y in (
            (-1, CABLE_SLOT_OFFSET_LEFT - CABLE_PAIR_PITCH / 2),
            (-1, CABLE_SLOT_OFFSET_LEFT + CABLE_PAIR_PITCH / 2),
            (1, CABLE_SLOT_OFFSET_RIGHT),
        ):
            bend = Torus(
                CABLE_BEND_RADIUS,
                CABLE_DIAMETER / 2,
                major_angle=90,
                rotation=(90, 0, 0),
                align=None,
                mode=Mode.PRIVATE,
            )
            if sx < 0:
                bend = bend.mirror(Plane.YZ)
            add(bend.moved(Location((sx * X_BOOT_TIP, y, Z_BEND_CENTRE))))
            with Locations((sx * X_DROP, y, Z_BEND_CENTRE)):
                Cylinder(
                    CABLE_DIAMETER / 2,
                    Z_BEND_CENTRE - (Z_FLOOR_TOP + 2 * CABLE_DIAMETER),
                    align=(Align.CENTER, Align.CENTER, Align.MAX),
                )
    parts["cord-drops"] = drops.part
    with BuildPart() as coils:
        for i, (lx, ly) in enumerate(((70.0, 28.0), (60.0, 24.0))):
            z0 = Z_FLOOR_TOP + 2 * CABLE_DIAMETER + i * (CABLE_DIAMETER + 1.0)
            with BuildSketch(Plane.XY.offset(z0)):
                RectangleRounded(lx, ly, 8.0)
                RectangleRounded(
                    lx - 2 * CABLE_DIAMETER, ly - 2 * CABLE_DIAMETER, 4.0, mode=Mode.SUBTRACT
                )
            extrude(amount=CABLE_DIAMETER)
    parts["cord-coils"] = coils.part
    with BuildPart() as plugs:
        for sx in (-1, 1):
            with Locations((sx * PLUG_X, sx * PLUG_Y, Z_FLOOR_TOP)):
                Cylinder(
                    CONNECTOR_DIAMETER / 2,
                    CONNECTOR_LENGTH,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )
    parts["plugs"] = plugs.part
    return parts


# ===========================================================================
# Build
# ===========================================================================
bin_part = build_bin()
tray = build_tray()
cap = build_cap()
controller = build_controller_stand_in()
cords = build_cord_stand_ins()

printed: dict[str, Part] = {"bin": bin_part, "tray": tray, "cap": cap}
stand_ins: dict[str, Part] = {"controller": controller, **cords}
everything = {**printed, **stand_ins}


# ===========================================================================
# Verification
# ===========================================================================
def shape_volume(shape) -> float:
    if shape is None:
        return 0.0
    if isinstance(shape, (list, tuple)):
        return sum(shape_volume(s) for s in shape)
    try:
        return shape.volume
    except Exception:
        return 0.0


def overlap_volume(a: Part, b: Part) -> float:
    try:
        return shape_volume(a & b)
    except Exception:  # OCCT may throw on disjoint shapes
        return 0.0


def slab(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> Part:
    return Part() + Box(x1 - x0, y1 - y0, z1 - z0, align=Align.MIN).moved(Location((x0, y0, z0)))


# The bend stand-ins must really start at the boot tips and end on the drop lines.
_bend_bb = cords["cord-drops"].bounding_box()
assert abs(_bend_bb.max.X - (X_DROP + CABLE_DIAMETER / 2)) < 0.01, "bend stand-in misplaced"
assert abs(_bend_bb.min.X + (X_DROP + CABLE_DIAMETER / 2)) < 0.01, "bend stand-in misplaced (-X)"
assert abs(_bend_bb.max.Z - (Z_CABLE + CABLE_DIAMETER / 2)) < 0.01, "bend stand-in misplaced (z)"

# Nothing printed may hit anything, and the controller may not hit the cords.
interferences = []
checked = set()
for a in printed:
    for b in everything:
        if a != b and (b, a) not in checked:
            checked.add((a, b))
            v = overlap_volume(everything[a], everything[b])
            if v > 0.01:
                interferences.append((a, b, round(v, 2)))
for b in cords:
    v = overlap_volume(controller, cords[b])
    if v > 0.01:
        interferences.append(("controller", b, round(v, 2)))
assert not interferences, f"parts interfere: {interferences}"

# Cap and tray lift straight off; the controller is captured in every direction once closed.
_up = Location((0, 0, 30))
assert overlap_volume(cap.moved(_up), bin_part) < 0.01, "cap cannot lift off the bin"
assert overlap_volume(cap.moved(_up), tray) < 0.01, "cap cannot lift off the tray"
assert overlap_volume(cap.moved(_up), controller) < 0.01, "cap lifts into the controller"
assert overlap_volume(tray.moved(_up), bin_part) < 0.01, "tray cannot lift off the bin"
for dx, dy, dz, against, what in (
    (0, 0, 1.0, cap, "skin"),
    (0, 0, -1.0, tray, "well floor"),
    (1.5, 0, 0, tray, "well wall +X"),
    (-1.5, 0, 0, tray, "well wall -X"),
    (0, 1.5, 0, tray, "well wall +Y"),
    (0, -1.5, 0, tray, "well wall -Y"),
):
    moved = controller.moved(Location((dx, dy, dz)))
    assert overlap_volume(moved, against) > 0.1, f"controller not captured by the {what}"

# The stack: skin on the plate, plate on the rim, skirt above the floor.
assert abs(bin_part.bounding_box().max.Z - Z_RIM) < 1e-6
assert abs(tray.bounding_box().max.Z - Z_PLATE_TOP) < 1e-6
assert abs(tray.bounding_box().min.Z - Z_WELL_BOTTOM) < 1e-6
assert abs(cap.bounding_box().min.Z - Z_SKIRT_BOTTOM) < 1e-6
_seat = tray & slab(-50, 50, -20, 20, Z_SEAT - 0.2, Z_SEAT)
assert shape_volume(_seat) > 0.95 * WELL_OUTER_L * WELL_OUTER_W * 0.2, "well floor is not solid"

# Cord exit, both ends. Probes are X-rays through both walls: the hole must be clear of
# bin *and* cap, the slit above the hole must be blanked by the skirt, the bin slit must
# be open to the rim so a cord can be laid in, and neither cut may be wider than designed.
_w = SLIT_WIDTH / 2 - 0.1
for sx in (-1, 1):
    x0, x1 = sorted((sx * (BIN_LENGTH / 2 - 1.0), sx * (CAP_L / 2 + 1.0)))
    hole = slab(
        x0, x1, LANE_Y - _w, LANE_Y + _w, Z_FLOOR_TOP + 0.1, Z_HOLE_TOP - SLIT_WIDTH / 2
    ) + Cylinder(_w, x1 - x0, rotation=(0, 90, 0)).moved(
        Location(((x0 + x1) / 2, LANE_Y, Z_HOLE_TOP - SLIT_WIDTH / 2))
    )
    assert overlap_volume(hole, bin_part) < 0.01, f"bin blocks the cord hole at x={sx}"
    assert overlap_volume(hole, cap) < 0.01, f"cap blocks the cord hole at x={sx}"
    above = slab(x0, x1, LANE_Y - _w, LANE_Y + _w, Z_HOLE_TOP + 0.2, Z_RIM - 0.2)
    _skirt_fill = SKIRT_THICKNESS * 2 * _w * (Z_RIM - 0.2 - Z_HOLE_TOP - 0.2)
    assert overlap_volume(above, cap) > 0.98 * _skirt_fill, (
        f"skirt does not blank the slit above the hole at x={sx}"
    )
    assert overlap_volume(above, bin_part) < 0.01, f"bin slit is not open to the rim at x={sx}"
    beside = slab(
        x0,
        x1,
        LANE_Y + SLIT_WIDTH / 2 + 0.1,
        LANE_Y + SLIT_WIDTH / 2 + 1.0,
        Z_FLOOR_TOP + 0.5,
        Z_HOLE_TOP,
    )
    _both_fill = (WALL_THICKNESS + SKIRT_THICKNESS) * 0.9 * (Z_HOLE_TOP - Z_FLOOR_TOP - 0.5)
    assert overlap_volume(beside, bin_part + cap) > 0.98 * _both_fill, (
        f"cord hole wider than designed at x={sx}"
    )

# Print-bed fit.
for name, part in printed.items():
    bb = part.bounding_box()
    assert max(bb.size.X, bb.size.Y, bb.size.Z) <= 180.0, f"{name} does not fit the bed"


# ===========================================================================
# Test pieces
# ===========================================================================
# 1+2. The well with a margin of plate, and the same outline of cap skin with the window.
#      Stack them edge to edge over the controller: does it drop in, is the button strip
#      centred in the window, does the bridged well floor print?  Both print face-down.
_crop_xy = (WELL_OUTER_L / 2 + 6.0, WELL_OUTER_W / 2 + 6.0)
test_well = tray & slab(-_crop_xy[0], _crop_xy[0], -_crop_xy[1], _crop_xy[1], -1, Z_TOP + 1)
test_window = cap & slab(
    -_crop_xy[0], _crop_xy[0], -_crop_xy[1], _crop_xy[1], Z_SKIN_BOTTOM - 0.5, Z_TOP + 1
)
# 3+4. One end of bin and cap, 17 mm tall, pins included: the sliding fit of the cap, the
#      cord hole formed by slit + notch, and the weave. Align the two top edges.
_end_crop = slab(
    PIN_XS[1] - PIN_R - 2.0, CAP_L / 2 + 1.0, -CAP_W / 2 - 1, CAP_W / 2 + 1, -1.0, 17.0
)
test_end_bin = bin_part & _end_crop
test_end_cap = cap & _end_crop


# ===========================================================================
# Export
# ===========================================================================
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DRAWING_DIR.mkdir(parents=True, exist_ok=True)
for stale in (
    "body.stl",
    "body.step",
    "lid.stl",
    "lid.step",
    "test-pocket.stl",
    "test-end-body.stl",
    "test-end-lid.stl",
    "drawings/part-body.svg",
    "drawings/part-lid.svg",
):
    (OUTPUT_DIR / stale).unlink(missing_ok=True)


def print_oriented(part: Part, flip: bool = False) -> Part:
    p = part.rotate(Axis.X, 180) if flip else part
    bb = p.bounding_box()
    return p.moved(Location((-bb.center().X, -bb.center().Y, -bb.min.Z)))


exports = {
    "bin": (bin_part, False),
    "tray": (tray, True),
    "cap": (cap, True),
    "test-well": (test_well, True),
    "test-window": (test_window, True),
    "test-end-bin": (test_end_bin, False),
    "test-end-cap": (test_end_cap, False),
}
sizes: dict[str, tuple[float, float, float]] = {}
for name, (part, flip) in exports.items():
    oriented = print_oriented(part, flip)
    bb = oriented.bounding_box()
    sizes[name] = (bb.size.X, bb.size.Y, bb.size.Z)
    export_stl(oriented, str(OUTPUT_DIR / f"{name}.stl"))
    if not name.startswith("test"):
        export_step(oriented, str(OUTPUT_DIR / f"{name}.step"))

colors = {
    "bin": Color(0.25, 0.25, 0.25),
    "tray": Color(0.45, 0.45, 0.45),
    "cap": Color(0.15, 0.15, 0.15),
    "controller": Color(0.9, 0.9, 0.9),
    "cord-weave": Color(0.1, 0.3, 0.8),
    "cord-drops": Color(0.1, 0.3, 0.8),
    "cord-coils": Color(0.1, 0.3, 0.8),
    "plugs": Color(0.8, 0.5, 0.1),
}
assembly = Compound(
    children=[
        Compound(children=[part], label=name, color=colors[name])
        for name, part in everything.items()
    ]
)
export_step(assembly, str(OUTPUT_DIR / "assembly.step"))


# ===========================================================================
# Drawings (SVG)
# ===========================================================================
def write_view(
    filename: str,
    shapes: list,
    origin: tuple[float, float, float],
    up: tuple[float, float, float] = (0, 0, 1),
    scale: float = 1.0,
    hidden: bool = False,
):
    compound = Compound(children=[Part() + s for s in shapes])
    visible, hidden_edges = compound.project_to_viewport(origin, viewport_up=up, look_at=(0, 0, 0))
    exporter = ExportSVG(scale=scale, margin=5, line_weight=0.25)
    exporter.add_layer("visible", line_color=(0, 0, 0), line_weight=0.3)
    exporter.add_shape(visible, layer="visible")
    if hidden:
        exporter.add_layer(
            "hidden", line_color=(120, 120, 120), line_weight=0.15, line_type=LineType.DASHED
        )
        exporter.add_shape(hidden_edges, layer="hidden")
    exporter.write(str(DRAWING_DIR / filename))


def clipped(shapes: list, box: Part) -> list:
    out = []
    for s in shapes:
        hit = s & box
        if shape_volume(hit) > 0.01:
            out.append(hit)
    return out


as_used = list(everything.values())
write_view("top.svg", as_used, origin=(0, 0, 1000), up=(0, 1, 0))
write_view("front.svg", as_used, origin=(0, -1000, 0))
write_view("end.svg", as_used, origin=(1000, 0, 0))
# Long section on the XZ plane through the well, notches, pins, slits and holes, seen from -Y.
_front_half = slab(-300, 300, 0, 300, -10, 300)
write_view("section-xz.svg", clipped(as_used, _front_half), origin=(0, -1000, 0), scale=1.5)
# Cross section on the YZ plane through the well centre, seen from +X.
_right_half = slab(-300, 0, -300, 300, -10, 300)
write_view("section-yz.svg", clipped(as_used, _right_half), origin=(1000, 0, 0), scale=2.5)
# The weave and the exit from above, cap and tray removed, controller removed.
_lane = slab(PIN_XS[-1] - 12.0, 300, -12, LANE_Y + 12, -1, 300)
write_view(
    "detail-weave.svg",
    clipped([bin_part, cords["cord-weave"], cords["cord-drops"]], _lane),
    origin=(0, 0, 1000),
    up=(0, 1, 0),
    scale=4.0,
)
# The cord exit, from outside: hole = notch ∩ slit.
_end_detail = slab(BIN_LENGTH / 2 - 5.0, 300, LANE_Y - 12, LANE_Y + 12, -1, 20)
write_view("detail-exit.svg", clipped([bin_part, cap], _end_detail), origin=(1000, 0, 0), scale=5.0)
# Exploded isometric: cap up, tray + controller half-way.
exploded = []
for name, part in everything.items():
    dz = {"cap": 110.0, "tray": 50.0, "controller": 75.0}.get(name, 0.0)
    exploded.append(part.moved(Location((0, 0, dz))))
write_view("exploded-iso.svg", exploded, origin=(900, -900, 700))
write_view("assembled-iso.svg", as_used, origin=(900, -900, 700))
for name, (part, flip) in exports.items():
    if not name.startswith("test"):
        write_view(f"part-{name}.svg", [print_oriented(part, flip)], origin=(700, -900, 800))
write_view(
    "test-pieces.svg",
    [
        print_oriented(test_well, True).moved(Location((0, 50, 0))),
        print_oriented(test_window, True).moved(Location((0, -10, 0))),
        print_oriented(test_end_bin).moved(Location((-40, -70, 0))),
        print_oriented(test_end_cap).moved(Location((40, -70, 0))),
    ],
    origin=(700, -900, 800),
)


# ===========================================================================
# Report
# ===========================================================================
def grams(part: Part) -> float:
    return part.volume / 1000 * PETG_DENSITY * PRINT_SOLID_FRACTION


print("Exported to", OUTPUT_DIR)
print(f"  box outside:    {CAP_L:.1f} x {CAP_W:.1f} x {Z_TOP:.1f} mm, 3 printed parts")
print(
    f"  bin:            interior {BIN_LENGTH:.0f} x {BIN_WIDTH:.0f} x {BIN_DEPTH:.0f}, "
    f"rim z={Z_RIM:.1f}"
)
print(
    f"  stack:          seat z={Z_SEAT:.1f}, face z={Z_FACE:.1f}, plate z={Z_RIM:.1f}.."
    f"{Z_PLATE_TOP:.1f}, skin to z={Z_TOP:.1f}; well bottom z={Z_WELL_BOTTOM:.1f}"
)
print(
    f"  window:         {WINDOW_L:.1f} x {WINDOW_W:.1f} mm at "
    f"({BUTTON_AREA_OFFSET_X:+.1f}, {BUTTON_AREA_OFFSET_Y:+.1f})"
)
print(
    f"  well:           {WELL_INNER_L:.1f} x {WELL_INNER_W:.1f}, floor {WELL_FLOOR_THICKNESS:.0f} "
    f"(bridge {WELL_INNER_W:.1f} mm), notches down to z={Z_NOTCH_BOTTOM:.2f}"
)
print(
    f"  cord exit:      {SLIT_WIDTH:.1f} wide x {HOLE_HEIGHT:.1f} high at "
    f"z={Z_FLOOR_TOP:.0f}..{Z_HOLE_TOP:.0f}, both ends"
)
print(
    f"  serpentine:     {PIN_COUNT} x Ø{PIN_DIAMETER:.0f} pins at x=±"
    f"{', ±'.join(f'{x:.0f}' for x in PIN_XS)}, {PIN_HEIGHT:.0f} tall"
)
print(
    f"  end zone:       {END_ZONE:.2f} mm; cord drops at x=±{X_DROP:.2f} "
    f"(bend R{CABLE_BEND_RADIUS:.0f})"
)
print(
    f"  cord volume:    solid {CORD_SOLID_MM3 / 1000:.1f} cm3 in {FREE_MM3 / 1000:.0f} cm3 free "
    f"-> {100 * FILL_FRACTION:.1f} % fill (limit {100 * PACKING_FRACTION:.0f} %)"
)
for name in printed:
    sx, sy, sz = sizes[name]
    print(
        f"  {name:<14}  {sx:.1f} x {sy:.1f} x {sz:.1f} mm, "
        f"{printed[name].volume / 1000:.1f} cm3, ~{grams(printed[name]):.0f} g"
    )
for name in exports:
    if name.startswith("test"):
        sx, sy, sz = sizes[name]
        print(f"  {name:<14}  {sx:.1f} x {sy:.1f} x {sz:.1f} mm")

if show is not None:
    try:
        show(assembly)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
