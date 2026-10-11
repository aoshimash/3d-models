"""Stand-alone switch box for the SwitchBot RGBIC floor lamp — prototype Ver.0.3.

A floor box that takes the lamp's inline controller and *all* of the spare
cord off the lamp. The button is pressed through a window in the top, the
cords leave through two small holes at floor level, and the length outside is
whatever is not stuffed inside.

Three printed parts, no fasteners:

    bin    — an open tray: floor, walls, a cord slit down each end wall from
             the rim to the floor, and three Ø6 pins behind each slit that the
             exiting cord weaves through.
    cap    — top skin with the button window, a skirt down the outside of the
             bin, and a pocket for the controller hanging from the skin into
             the bin. The pocket is OPEN AT THE BOTTOM: the controller goes in
             from below with every cord still attached, nothing is threaded
             through anything.
    plate  — the pocket's floor: slides into grooves in the pocket's long
             walls from the +X end, under the controller and under its cables,
             and clicks home. It closes the pocket so stuffed cord cannot get
             under the controller, and carries the button load.

Why the controller loads from below (Ver.0.2 → 0.3)
---------------------------------------------------
Ver.0.2 hung a closed-bottom well from a tray; its cords had to be threaded
plug-first through notches in the well's end walls. The user does not want to
unplug anything: on the adapter side the cord continues through the barrel
plug to the AC adapter brick, which no notch will pass. So the pocket must
accept the controller *with its cords*, which means from below, and then be
closed behind it. The sliding plate is that closure.

What Ver.0.1 got wrong (printed, 2026-10-11)
--------------------------------------------
1. Capacity. Ver.0.1 assumed the Ø4 cord would wind neatly round two Ø12
   posts, five turns a layer. It does not: cord, plugs, boots and the Ø2
   adapter lead stuff loosely at roughly 10 % of the space they are given.
2. The controller sat on the tops of two posts with open space round them.
   Stuffed cord rode up onto the post tops and under the controller, so the
   lid could not close. Hence the closed pocket floor here.

How the plate is held
---------------------
Grooves GROOVE_DEPTH deep run along the inside of both pocket long walls,
blind at the -X end, open at the +X end. The plate's edges ride in them with
PLATE_CLEARANCE. Near the +X entrance each groove ceiling carries a small
round bump; the plate has a matching scallop in each edge, so the plate slides
in over the bumps (its edge strip flexes 0.3 mm) and the bumps drop into the
scallops when it is home. Pulling it out needs the same flex. The plate's +X
end stands PLATE_PULL proud of the pocket as a finger tab.

How the serpentine holds the cord
---------------------------------
Behind each exit hole three Ø6 pins stand in a line PIN_PITCH apart on a lane
LANE_Y off the box's long axis. The cord is laid in from above and weaves
left-right round them, bending about 80° at each pin; a pull from outside is
resisted by friction over ~280° of contact. To change the exposed length, lift
the cap (controller and plate come with it) and move the cord by hand.

How the slit becomes a small hole
---------------------------------
Bin end wall: slit SLIT_WIDTH wide from the rim down to the floor top.
Cap skirt:    notch SLIT_WIDTH wide from its bottom edge up to HOLE_HEIGHT
              above the floor top, rounded at the top.
Each one is covered by the other wall once the cap is on; what stays open is
their overlap, a SLIT_WIDTH x HOLE_HEIGHT hole at the bottom of the end wall.

The stack (z = 0 is the floor)
------------------------------
    Z_TOP          cap skin top; the button window is a 2.5 mm deep well
    Z_SKIN_BOTTOM  skin underside = bin rim
    Z_FACE         controller face
    Z_SEAT         plate top = controller underside
    Z_PLATE_BOTTOM plate underside; the groove lip ends 2 mm lower
    Z_POCKET_BOTTOM bottom edge of the pocket long walls; cord space below
    Z_FLOOR_TOP    bin floor; exit holes start here; pins stand here
    Z_SKIRT_BOTTOM cap skirt bottom edge, GROUND_CLEARANCE above the floor

Button loads go finger -> controller -> plate -> grooves -> pocket walls ->
skin -> bin rim -> bin walls -> floor.

Measured vs assumed
-------------------
Controller, cable and cord figures are carried over from
switchbot-lamp-base-case (user measurements, photos and SwitchBot support
Q&A). Tags: [M] measured [P] from photos [S] spec sheet [A] assumed [D] design.
Still not measured: where the button strip sits on the controller face
(BUTTON_AREA_OFFSET_X/Y, assumed centred). test-pocket + plate check it.

Print notes
-----------
- bin: as modelled, open side up. No supports.
- cap: skin-down (STL already flipped). Skirt and pocket walls grow straight
  up; each groove is a 1 mm deep slot in a vertical wall whose 1 mm ceiling
  overhang prints fine; the bumps sit on the groove floor (in print) and
  print cleanly. No supports.
- plate: flat, as modelled. No supports.
- PETG, 0.2 mm layers, 3 walls.
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
CABLE_SLOT_MARGIN = 1.5  # [D] per side, pocket notch wider than the boots
CABLE_SLOT_WIDTH_LEFT = CABLE_PAIR_PITCH + CABLE_BOOT_DIAMETER + 2 * CABLE_SLOT_MARGIN  # two cables
CABLE_SLOT_WIDTH_RIGHT = CABLE_BOOT_DIAMETER + 2 * CABLE_SLOT_MARGIN  # one cable
CABLE_SLOT_OFFSET_LEFT = 0.0  # [A] notch centre offset along Y from the controller centreline
CABLE_SLOT_OFFSET_RIGHT = 0.0  # [A]

# --- Cords (mm) ---
CABLE_DIAMETER = 4.0  # [M] controller cords and lamp pigtail
CABLE_DIAMETER_ADAPTER = 2.0  # [M] the AC adapter lead is thinner
CABLE_BEND_RADIUS = 8.0  # [A] centreline radius the Ø4 cord takes leaving the pocket (stand-in)
CONNECTOR_DIAMETER = 10.0  # [A] barrel plugs — stowed in the bin, never threaded through anything
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
BIN_DEPTH = 37.0  # [D] floor top to rim
PIN_DIAMETER = 6.0  # [D] serpentine pins
PIN_HEIGHT = 14.0  # [D] above the floor top
PIN_COUNT = 3  # [D] per exit
PIN_PITCH = 12.0  # [D] centre to centre along X; leaves a 6 mm gap for the cord to cross
PIN_FIRST_FROM_WALL = 10.0  # [D] end wall inner face to the first pin centre
LANE_Y = 15.0  # [D] cord lane (pins and exit holes) offset from the centreline, +Y side

# --- Cap and pocket (mm) ---
SKIN_THICKNESS = 2.0  # [D] cap top
SKIRT_THICKNESS = 2.0  # [D] cap outer wall
CAP_CLEARANCE = 0.25  # [D] per side, skirt over the bin wall (sliding fit)
POCKET_WALL_THICKNESS = 2.4  # [D] pocket walls; the grooves take GROOVE_DEPTH of the long ones
POCKET_OUTER_CORNER_RADIUS = 1.5  # [D] square-ish outside so the grooves stay inside solid wall
CONTROLLER_CLEARANCE = 0.5  # [D] per side, controller in the pocket (checked on the base case)
FACE_CLEARANCE = 0.5  # [D] controller face to skin underside — must clear BUTTON_AREA_PROUD
NOTCH_SKIN_MARGIN = 1.8  # [D] wall left between the pocket cable notches and the skin
WINDOW_MARGIN = 1.5  # [D] per side, window larger than the button strip
WINDOW_CORNER_RADIUS = 3.0  # [D]
SLIT_CLEARANCE = 0.5  # [D] per side, slit and notch wider than the Ø4 cord
HOLE_HEIGHT = 7.0  # [D] open height of the cord exit above the floor top
GROUND_CLEARANCE = 1.0  # [D] skirt bottom edge above the floor
CAP_CORNER_RADIUS = 4.0  # [D] plan-view corner radius of the cap
TOP_CHAMFER = 1.0  # [D] cap top edge

# --- Plate (mm) ---
PLATE_THICKNESS = 2.0  # [D]
PLATE_CLEARANCE = 0.2  # [D] controller underside to plate top; also the fit in the groove, per side
GROOVE_DEPTH = 1.0  # [D] into each long wall
GROOVE_LIP = 2.0  # [D] wall left below the groove
GROOVE_STOP = 1.5  # [D] blind end: wall left at the -X end of each groove
PLATE_END_CLEARANCE = 0.3  # [D] plate short of the groove's blind end
PLATE_PULL = 3.0  # [D] plate stands this far out of the +X end as a finger tab
PLATE_LEAD_CHAMFER = 0.6  # [D] on the plate's leading (-X) edges
BUMP_RADIUS = 0.8  # [D] detent bump, a cylinder lying across the groove ceiling
BUMP_PROUD = 0.4  # [D] how far the bump hangs into the groove
BUMP_FROM_END = 2.5  # [D] bump centre from the pocket's +X outer face
SCALLOP_RADIUS = 1.3  # [D] matching cut in each plate edge

# --- Finish ---
PETG_DENSITY = 1.27  # g/cm3
PRINT_SOLID_FRACTION = 0.9  # walls dominate; infill is a rounding error

# ===========================================================================
# Derived geometry
# ===========================================================================
OUTPUT_DIR = Path(__file__).parent / "output"
DRAWING_DIR = OUTPUT_DIR / "drawings"

# Pocket — controller outline plus clearance, walls outside that.
POCKET_L = CONTROLLER_LENGTH + 2 * CONTROLLER_CLEARANCE
POCKET_W = CONTROLLER_WIDTH + 2 * CONTROLLER_CLEARANCE
POCKET_INNER_R = CONTROLLER_CORNER_RADIUS + CONTROLLER_CLEARANCE
POCKET_OUTER_L = POCKET_L + 2 * POCKET_WALL_THICKNESS
POCKET_OUTER_W = POCKET_W + 2 * POCKET_WALL_THICKNESS

# Bin and cap outlines
BIN_OUTER_L = BIN_LENGTH + 2 * WALL_THICKNESS
BIN_OUTER_W = BIN_WIDTH + 2 * WALL_THICKNESS
CAP_INNER_R = CAP_CORNER_RADIUS - SKIRT_THICKNESS
BIN_CORNER_R = CAP_INNER_R - CAP_CLEARANCE
BIN_CAVITY_R = 1.0
CAP_INNER_L = BIN_OUTER_L + 2 * CAP_CLEARANCE
CAP_INNER_W = BIN_OUTER_W + 2 * CAP_CLEARANCE
CAP_L = CAP_INNER_L + 2 * SKIRT_THICKNESS
CAP_W = CAP_INNER_W + 2 * SKIRT_THICKNESS

# Heights
Z_FLOOR_TOP = FLOOR_THICKNESS
Z_RIM = Z_FLOOR_TOP + BIN_DEPTH
Z_SKIN_BOTTOM = Z_RIM
Z_TOP = Z_SKIN_BOTTOM + SKIN_THICKNESS
Z_FACE = Z_SKIN_BOTTOM - FACE_CLEARANCE
Z_CONTROLLER_BOTTOM = Z_FACE - CONTROLLER_HEIGHT
Z_SEAT = Z_CONTROLLER_BOTTOM - PLATE_CLEARANCE  # plate top
Z_PLATE_BOTTOM = Z_SEAT - PLATE_THICKNESS
Z_GROOVE_TOP = Z_SEAT + PLATE_CLEARANCE / 2
Z_GROOVE_BOTTOM = Z_PLATE_BOTTOM - PLATE_CLEARANCE * 1.5
Z_POCKET_BOTTOM = Z_GROOVE_BOTTOM - GROOVE_LIP  # long walls end here
Z_END_WALL_BOTTOM = Z_CONTROLLER_BOTTOM  # end walls stop just above the plate
Z_SLOT_TOP = Z_SKIN_BOTTOM - NOTCH_SKIN_MARGIN
Z_CABLE = Z_CONTROLLER_BOTTOM + CONTROLLER_CABLE_EXIT_HEIGHT
Z_SKIRT_BOTTOM = GROUND_CLEARANCE
Z_HOLE_TOP = Z_FLOOR_TOP + HOLE_HEIGHT

# Plate and grooves
GROOVE_X0 = -POCKET_OUTER_L / 2 + GROOVE_STOP  # blind end
PLATE_X0 = GROOVE_X0 + PLATE_END_CLEARANCE
PLATE_X1 = POCKET_OUTER_L / 2 + PLATE_PULL
PLATE_LENGTH = PLATE_X1 - PLATE_X0
PLATE_WIDTH = POCKET_W + 2 * (GROOVE_DEPTH - PLATE_CLEARANCE)
BUMP_X = POCKET_OUTER_L / 2 - BUMP_FROM_END
Y_GROOVE_FACE = POCKET_W / 2  # inner face of each long wall
Y_BUMP = Y_GROOVE_FACE + GROOVE_DEPTH / 2 + 0.3  # bump cylinder centre, inside the wall

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
END_ZONE = BIN_LENGTH / 2 - POCKET_OUTER_L / 2  # pocket end wall to bin end wall

# Plug stowage stand-in: standing in the bin corners, clear of the weave and the drops.
PLUG_X = BIN_LENGTH / 2 - PIN_FIRST_FROM_WALL - CONNECTOR_DIAMETER / 2
PLUG_Y = BIN_WIDTH / 2 - 1.0 - CONNECTOR_DIAMETER / 2

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
POCKET_HANG_MM3 = POCKET_OUTER_L * POCKET_OUTER_W * (Z_RIM - Z_POCKET_BOTTOM)
PINS_MM3 = 2 * PIN_COUNT * pi * PIN_R**2 * PIN_HEIGHT
FREE_MM3 = BIN_LENGTH * BIN_WIDTH * BIN_DEPTH - POCKET_HANG_MM3 - PINS_MM3
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
assert GROOVE_DEPTH + 1.0 <= POCKET_WALL_THICKNESS, "groove leaves too little wall"
assert BUMP_PROUD < PLATE_CLEARANCE * 2.5, "bump too tall for the plate edge to flex over"
assert BUMP_RADIUS > BUMP_PROUD, "bump must be a shallow segment to ramp over"
assert SCALLOP_RADIUS >= BUMP_RADIUS + 0.4, "scallop too small for the bump"
assert BUMP_X - SCALLOP_RADIUS > PLATE_X0 + 5.0, "scallop too close to the plate's leading end"
assert Z_CABLE - CABLE_BOOT_DIAMETER / 2 - Z_SEAT >= 3.0, "plate too close to the boots"
assert Z_SLOT_TOP >= Z_CABLE + CABLE_BOOT_DIAMETER / 2 + 1.0, "pocket notch too low for the boot"
assert Z_POCKET_BOTTOM - Z_FLOOR_TOP >= 3 * CABLE_DIAMETER, "no cord space under the pocket"
assert Z_POCKET_BOTTOM > Z_FLOOR_TOP + PIN_HEIGHT + 1.0, "pocket lands on the pins"
assert POCKET_OUTER_W + 2 * 4.0 <= BIN_WIDTH, "no cord space beside the pocket"
assert END_ZONE >= X_DROP - POCKET_OUTER_L / 2 + CABLE_DIAMETER / 2 + 1.0, (
    "end zone too short for the cord to bend down"
)
assert END_ZONE >= PLATE_PULL + CABLE_DIAMETER + 2.0, "plate tab reaches the bin wall"
assert PIN_PITCH - PIN_DIAMETER >= CABLE_DIAMETER + 1.5, "cord cannot cross between the pins"
assert PIN_XS[-1] - PIN_R > POCKET_OUTER_L / 2 - 8.0, "weave runs too far under the pocket"
assert PIN_FIRST_FROM_WALL - PIN_R >= CABLE_DIAMETER + 2.0, "first pin too close to the hole"
assert LANE_Y - WEAVE_Y - CABLE_DIAMETER / 2 >= CABLE_PAIR_PITCH / 2 + CABLE_DIAMETER / 2 + 0.5, (
    "cord lane runs into the cables dropping from the pocket"
)
assert LANE_Y + WEAVE_Y + CABLE_DIAMETER / 2 + 1.0 <= PLUG_Y - CONNECTOR_DIAMETER / 2, (
    "cord lane runs into the stowed plug"
)
assert Z_HOLE_TOP + 1.0 < Z_POCKET_BOTTOM, "cord exit hole reaches the pocket"
assert SLIT_WIDTH < CONNECTOR_DIAMETER, "a plug could slip out through the slit"
assert PLUG_X - CONNECTOR_DIAMETER / 2 > X_DROP + CABLE_DIAMETER / 2 + 0.5 or (
    PLUG_Y - CONNECTOR_DIAMETER / 2 > CABLE_PAIR_PITCH / 2 + CABLE_DIAMETER / 2 + 1.0
), "plug collides with the dropping cords"
assert CONNECTOR_LENGTH <= BIN_DEPTH - 1.0, "plug too tall to stand in the bin"
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
        # Serpentine pins behind each exit, in a line on the lane.
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


def build_bumps() -> Part:
    """The two detent bumps: short cylinders lying across each groove ceiling."""
    with BuildPart() as bumps:
        for sy in (-1, 1):
            with Locations((BUMP_X, sy * Y_BUMP, Z_GROOVE_TOP + BUMP_RADIUS - BUMP_PROUD)):
                Cylinder(BUMP_RADIUS, GROOVE_DEPTH + 0.6, rotation=(90, 0, 0))
    return bumps.part


def build_cap_body() -> Part:
    with BuildPart() as c:
        with BuildSketch(Plane.XY.offset(Z_SKIRT_BOTTOM)):
            RectangleRounded(CAP_L, CAP_W, CAP_CORNER_RADIUS)
        extrude(amount=Z_TOP - Z_SKIRT_BOTTOM)
        chamfer(c.edges().group_by(Axis.Z)[-1], length=TOP_CHAMFER)
        # Hollow under the skin — the bin slides in here.
        with BuildSketch(Plane.XY.offset(Z_SKIRT_BOTTOM - 1.0)):
            RectangleRounded(CAP_INNER_L, CAP_INNER_W, CAP_INNER_R)
        extrude(amount=Z_SKIN_BOTTOM - Z_SKIRT_BOTTOM + 1.0, mode=Mode.SUBTRACT)
        # Pocket walls hanging from the skin: long walls to the groove lip, end walls shorter.
        with BuildSketch(Plane.XY.offset(Z_POCKET_BOTTOM)):
            RectangleRounded(POCKET_OUTER_L, POCKET_OUTER_W, POCKET_OUTER_CORNER_RADIUS)
            RectangleRounded(POCKET_L, POCKET_W, POCKET_INNER_R, mode=Mode.SUBTRACT)
        extrude(amount=Z_SKIN_BOTTOM - Z_POCKET_BOTTOM)
        for sx in (-1, 1):  # trim the end walls back to just above the plate
            with Locations(
                (sx * (POCKET_L / 2 + POCKET_WALL_THICKNESS / 2), 0, Z_POCKET_BOTTOM - 1)
            ):
                Box(
                    POCKET_WALL_THICKNESS + 0.02,
                    POCKET_W + 0.02,
                    Z_END_WALL_BOTTOM - Z_POCKET_BOTTOM + 1.0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
        # Grooves in the long walls: one slot across the pocket's width plus GROOVE_DEPTH into
        # each long wall, so the inner corner fillets are cleared too; blind at -X, open at +X.
        with Locations((GROOVE_X0, 0, Z_GROOVE_BOTTOM)):
            Box(
                POCKET_OUTER_L / 2 + 1.0 - GROOVE_X0,
                POCKET_W + 2 * GROOVE_DEPTH,
                Z_GROOVE_TOP - Z_GROOVE_BOTTOM,
                align=(Align.MIN, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )
        # Lead-in: the pocket mouth (its bottom edge) is wider by 1 mm per side.
        with BuildSketch(Plane.XY.offset(Z_END_WALL_BOTTOM - 0.01)):
            RectangleRounded(POCKET_L + 2.0, POCKET_W + 2.0, POCKET_INNER_R + 1.0)
        with BuildSketch(Plane.XY.offset(Z_END_WALL_BOTTOM + 1.0)):
            RectangleRounded(POCKET_L, POCKET_W, POCKET_INNER_R)
        loft(mode=Mode.SUBTRACT)
        # Cable notches in the pocket end walls, open at the bottom.
        for sx, width, offset in (
            (-1, CABLE_SLOT_WIDTH_LEFT, CABLE_SLOT_OFFSET_LEFT),
            (1, CABLE_SLOT_WIDTH_RIGHT, CABLE_SLOT_OFFSET_RIGHT),
        ):
            with Locations(
                (sx * (POCKET_L / 2 + POCKET_WALL_THICKNESS / 2), offset, Z_END_WALL_BOTTOM - 1.0)
            ):
                Box(
                    POCKET_WALL_THICKNESS + 1.0,
                    width,
                    Z_SLOT_TOP - Z_END_WALL_BOTTOM + 1.0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
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


def build_plate() -> Part:
    with BuildPart() as p:
        with Locations((PLATE_X0, 0, Z_PLATE_BOTTOM)):
            Box(
                PLATE_LENGTH,
                PLATE_WIDTH,
                PLATE_THICKNESS,
                align=(Align.MIN, Align.CENTER, Align.MIN),
            )
        lead = p.edges().filter_by(Axis.Y).group_by(Axis.X)[0]
        chamfer(lead, length=PLATE_LEAD_CHAMFER)
        # Scallops for the detent bumps, one in each edge.
        with Locations(
            (BUMP_X, -PLATE_WIDTH / 2, Z_PLATE_BOTTOM - 1),
            (BUMP_X, PLATE_WIDTH / 2, Z_PLATE_BOTTOM - 1),
        ):
            Cylinder(
                SCALLOP_RADIUS,
                PLATE_THICKNESS + 2.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )
    return p.part


def build_controller_stand_in() -> Part:
    with BuildPart() as c:
        with BuildSketch(Plane.XY.offset(Z_CONTROLLER_BOTTOM)):
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
    """Rough cord: the weave through both exits, the drops from the pocket ends,
    two loose coils under the pocket, and the two plugs standing in the corners."""
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
            z0 = Z_FLOOR_TOP + CABLE_DIAMETER + i * (CABLE_DIAMETER + 1.0)
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
cap_body = build_cap_body()
bumps = build_bumps()
cap = cap_body + bumps
plate = build_plate()
controller = build_controller_stand_in()
cords = build_cord_stand_ins()

printed: dict[str, Part] = {"bin": bin_part, "cap": cap, "plate": plate}
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

# Cap (with plate and controller) lifts straight off the bin.
_up = Location((0, 0, 30))
for name in ("cap", "plate", "controller"):
    assert overlap_volume(everything[name].moved(_up), bin_part) < 0.01, f"{name} cannot lift off"

# Plate mechanics: slides in and out along +X past the bumps' absence, stops at the blind end,
# is captured vertically by the grooves, and the bumps hold it home.
_plate_out = plate.moved(Location((25, 0, 0)))  # tab reaches the bin wall, not the skirt
_v_out = overlap_volume(_plate_out, cap_body)
assert _v_out < 0.01, f"plate does not slide out of the +X end ({_v_out:.3f} mm3)"
_plate_mid = plate.moved(Location((20, 0, 0)))
_v_mid = overlap_volume(_plate_mid, cap_body)
assert _v_mid < 0.01, f"plate binds part way along the grooves ({_v_mid:.3f} mm3)"
assert overlap_volume(plate.moved(Location((-1.0, 0, 0))), cap_body) > 0.01, (
    "no stop at the blind end"
)
assert overlap_volume(plate.moved(Location((0, 0, 0.5))), cap_body) > 0.01, "plate not held down"
assert overlap_volume(plate.moved(Location((0, 0, -0.6))), cap_body) > 0.01, "plate not held up"
assert overlap_volume(plate, bumps) < 0.01, "bumps do not sit in the scallops when home"
assert overlap_volume(plate.moved(Location((1.5, 0, 0))), bumps) > 0.01, (
    "bumps do not stop the plate"
)
assert overlap_volume(_plate_mid, bumps) > 0.01, "bumps do not ride on the plate edge while sliding"
# Sliding over a bump must only need the edge strip to flex within the groove's spare height.
assert BUMP_PROUD - PLATE_CLEARANCE / 2 <= PLATE_CLEARANCE * 1.5, (
    "bump needs more flex than the groove allows"
)

# Controller captured in every direction once the plate is home, and resting on the plate.
for dx, dy, dz, against, what in (
    (0, 0, 1.0, cap, "skin"),
    (0, 0, -1.0, plate, "plate"),
    (1.5, 0, 0, cap, "end wall +X"),
    (-1.5, 0, 0, cap, "end wall -X"),
    (0, 1.5, 0, cap, "long wall +Y"),
    (0, -1.5, 0, cap, "long wall -Y"),
):
    moved = controller.moved(Location((dx, dy, dz)))
    assert overlap_volume(moved, against) > 0.1, f"controller not captured by the {what}"
# ...and it goes in from below with the plate out: nothing of the cap is under it.
with BuildPart() as _path:  # the controller's own outline swept down out of the pocket
    with BuildSketch(Plane.XY.offset(Z_POCKET_BOTTOM - 1.0)):
        RectangleRounded(
            CONTROLLER_LENGTH + 0.2, CONTROLLER_WIDTH + 0.2, CONTROLLER_CORNER_RADIUS + 0.1
        )
    extrude(amount=Z_CONTROLLER_BOTTOM - Z_POCKET_BOTTOM + 1.0)
assert overlap_volume(_path.part, cap) < 0.01, "pocket is not open at the bottom"

# The stack: skin on the rim, skirt above the floor.
assert abs(bin_part.bounding_box().max.Z - Z_RIM) < 1e-6
assert abs(cap.bounding_box().min.Z - Z_SKIRT_BOTTOM) < 1e-6
assert abs(plate.bounding_box().max.Z - Z_SEAT) < 1e-6
assert abs(plate.bounding_box().max.X - PLATE_X1) < 1e-6

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
# 1. The pocket with a margin of skin round it, window included; print it with the plate.
#    Load the controller from below, slide the plate in: fit, click, button strip in the window.
_crop_xy = (PLATE_X1 + 4.0, POCKET_OUTER_W / 2 + 6.0)
test_pocket = cap & slab(-_crop_xy[0], _crop_xy[0], -_crop_xy[1], _crop_xy[1], -1, Z_TOP + 1)
# 2+3. One end of bin and cap, 17 mm tall, pins included: the sliding fit of the cap, the
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
    "tray.stl",
    "tray.step",
    "test-pocket.stl",
    "test-well.stl",
    "test-window.stl",
    "test-end-body.stl",
    "test-end-lid.stl",
    "drawings/part-body.svg",
    "drawings/part-lid.svg",
    "drawings/part-tray.svg",
):
    (OUTPUT_DIR / stale).unlink(missing_ok=True)


def print_oriented(part: Part, flip: bool = False) -> Part:
    p = part.rotate(Axis.X, 180) if flip else part
    bb = p.bounding_box()
    return p.moved(Location((-bb.center().X, -bb.center().Y, -bb.min.Z)))


exports = {
    "bin": (bin_part, False),
    "cap": (cap, True),
    "plate": (plate, False),
    "test-pocket": (test_pocket, True),
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
    "cap": Color(0.15, 0.15, 0.15),
    "plate": Color(0.45, 0.45, 0.45),
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
# Long section on the XZ plane through the pocket, notches, plate, pins, slits and holes.
_front_half = slab(-300, 300, 0, 300, -10, 300)
write_view("section-xz.svg", clipped(as_used, _front_half), origin=(0, -1000, 0), scale=1.5)
# Cross section on the YZ plane through the pocket centre, seen from +X.
_right_half = slab(-300, 0, -300, 300, -10, 300)
write_view("section-yz.svg", clipped(as_used, _right_half), origin=(1000, 0, 0), scale=2.5)
# Groove detail: YZ section at x=20 cropped to the pocket, seen from +X.
_groove_box = slab(
    -300, 20.0, -POCKET_OUTER_W / 2 - 4, POCKET_OUTER_W / 2 + 4, Z_POCKET_BOTTOM - 3, Z_TOP + 1
)
write_view(
    "detail-groove.svg",
    clipped([cap, plate, controller], _groove_box),
    origin=(1000, 0, 0),
    scale=5.0,
)
# Detent detail: XZ section through a groove at y = +Y_BUMP, near the +X end, seen from -Y.
_detent_box = slab(
    BUMP_X - 10.0,
    PLATE_X1 + 2.0,
    Y_GROOVE_FACE + 0.3,
    300,
    Z_POCKET_BOTTOM - 1,
    Z_SKIN_BOTTOM + 0.5,
)
write_view("detail-detent.svg", clipped([cap, plate], _detent_box), origin=(0, -1000, 0), scale=8.0)
# The weave and the exit from above, cap removed.
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
# Exploded isometric: cap up, controller below it, plate slid out to +X and lowered.
exploded = []
for name, part in everything.items():
    dx, dz = {"cap": (0, 110.0), "controller": (0, 70.0), "plate": (60.0, 45.0)}.get(name, (0, 0))
    exploded.append(part.moved(Location((dx, 0, dz))))
write_view("exploded-iso.svg", exploded, origin=(900, -900, 700))
write_view("assembled-iso.svg", as_used, origin=(900, -900, 700))
# The cap upside down with the controller dropped in and the plate half way in — the loading step.


def flipped(part: Part) -> Part:
    """The use frame turned over onto the cap's top face (skin top at z=0)."""
    return part.rotate(Axis.X, 180).moved(Location((0, 0, Z_TOP)))


_loading = [flipped(cap), flipped(controller), flipped(plate.moved(Location((50.0, 0, 0))))]
write_view("loading-iso.svg", _loading, origin=(900, -900, 700))
for name, (part, flip) in exports.items():
    if not name.startswith("test"):
        write_view(f"part-{name}.svg", [print_oriented(part, flip)], origin=(700, -900, 800))
write_view(
    "test-pieces.svg",
    [
        print_oriented(test_pocket, True).moved(Location((0, 50, 0))),
        print_oriented(plate).moved(Location((0, -5, 0))),
        print_oriented(test_end_bin).moved(Location((-40, -65, 0))),
        print_oriented(test_end_cap).moved(Location((40, -65, 0))),
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
    f"  stack:          plate z={Z_PLATE_BOTTOM:.1f}..{Z_SEAT:.1f}, controller to z={Z_FACE:.1f}, "
    f"skin z={Z_SKIN_BOTTOM:.1f}..{Z_TOP:.1f}; pocket bottom z={Z_POCKET_BOTTOM:.1f}"
)
print(
    f"  window:         {WINDOW_L:.1f} x {WINDOW_W:.1f} mm at "
    f"({BUTTON_AREA_OFFSET_X:+.1f}, {BUTTON_AREA_OFFSET_Y:+.1f})"
)
print(
    f"  pocket:         {POCKET_L:.1f} x {POCKET_W:.1f}, walls {POCKET_WALL_THICKNESS:.1f}; "
    f"notches left {CABLE_SLOT_WIDTH_LEFT:.0f} / right {CABLE_SLOT_WIDTH_RIGHT:.0f} wide, "
    f"open at the bottom to z={Z_SLOT_TOP:.1f}"
)
print(
    f"  plate:          {PLATE_LENGTH:.1f} x {PLATE_WIDTH:.1f} x {PLATE_THICKNESS:.1f}, "
    f"grooves {GROOVE_DEPTH:.1f} deep x {Z_GROOVE_TOP - Z_GROOVE_BOTTOM:.1f} high, "
    f"bumps Ø{2 * BUMP_RADIUS:.1f} proud {BUMP_PROUD:.1f} at x={BUMP_X:.1f}, tab {PLATE_PULL:.0f}"
)
print(
    f"  cord exit:      {SLIT_WIDTH:.1f} wide x {HOLE_HEIGHT:.1f} high at "
    f"z={Z_FLOOR_TOP:.0f}..{Z_HOLE_TOP:.0f}, both ends, lane y={LANE_Y:.0f}"
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
