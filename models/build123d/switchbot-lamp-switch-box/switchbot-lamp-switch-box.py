"""Stand-alone switch box for the SwitchBot RGBIC floor lamp — prototype Ver.0.1.

A small floor box that takes the lamp's inline controller and the spare cord
*off* the lamp. Nothing sits on the lamp base any more: the lamp keeps its own
look, the box sits wherever the cords reach, the button is pressed through a
window in the box top, and the length of cord outside the box is whatever is
not wound up inside.

Two printed parts, no fasteners:

    lid   — a cap: 2 mm top skin with the button window, pocket walls hanging
            from the skin that locate the controller, and a skirt that reaches
            down the *outside* of the body almost to the floor.
    body  — an open tray: floor, walls, two Ø12 winding posts. Its two end
            walls are slit from the top edge down to the floor so a cord can be
            laid in from above without unplugging anything.

How the cords are held (the user's "巻き付ける棒")
-------------------------------------------------
Under the controller the two posts stand 78 mm apart. Each cord leaves the
controller end, drops down the end zone and is wound around *both* posts like
an extension cord on a two-hook reel; turns stack 4 mm per turn up the posts
and then outward in layers. The turns rub on the posts and on each other, so a
pull on the cord outside the box is taken by the wraps (capstan effect), not
by the controller, and the exposed length stays where it was set. To change
it, lift the lid and wind or unwind a turn.

How the slit becomes a small hole (the user's "蓋を被せるとスリットが隠れる")
-----------------------------------------------------------------------------
Body end wall: slit SLIT_WIDTH wide from the top edge down to the floor top.
Lid skirt:     notch SLIT_WIDTH wide from its bottom edge up to HOLE_HEIGHT
               above the floor top, rounded at the top.
Each one is covered by the other wall once the lid is on; what stays open is
their overlap — a SLIT_WIDTH x HOLE_HEIGHT hole at the bottom of the end wall,
exactly where the bottom turn leaves the post. The lid comes down over a cord
already lying in the slit, because its notch is open at the bottom.

The stack (z = 0 is the floor)
------------------------------
    Z_TOP          lid skin top; the button window is a 2 mm deep well
    Z_SKIN_BOTTOM  skin underside = body wall top = controller face + FACE_CLEARANCE
    Z_FACE         controller face
    Z_LEDGE        controller underside = post tops (the posts carry the button load)
    Z_FLOOR_TOP    cavity floor; the cord exit hole starts here
    Z_SKIRT_BOTTOM lid skirt bottom edge, GROUND_CLEARANCE above the floor
    0              floor

The controller is captured on all six sides: the posts below, the skin above
(it covers everything but the button area), the pocket walls around it. The
pocket is the one proven on the Ver.0.2 base case (same clearance, same cable
notches, test piece printed and checked), only now hanging from a flat lid.

Measured vs assumed
-------------------
Controller, cable and cord figures are carried over from
switchbot-lamp-base-case (user measurements, photos and SwitchBot support
Q&A). Tags: [M] measured [P] from photos [S] spec sheet [A] assumed [D] design.
The one thing this model needs that was never measured is *where* the button
area sits on the controller face: BUTTON_AREA_OFFSET_X/Y are assumed 0
(centred). The test-pocket piece exists to check exactly that before the lid
is printed.

Print notes
-----------
- Lid prints skin-down (the exported STL is already flipped): the visible top
  is the bed face, skirt and pocket walls grow straight up, the skirt notches
  are open at the top of the print. No supports.
- Body prints as modelled, open side up. Posts and slits are vertical. No
  supports.
- PETG, 0.2 mm layers, 3 walls. Both parts are essentially all perimeter.
"""

from math import floor, pi
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
    SlotCenterToCenter,
    Torus,
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
CABLE_BEND_RADIUS = 8.0  # [A] centreline radius the Ø4 cord is asked to take (= post wrap)
CONNECTOR_DIAMETER = 10.0  # [A] barrel plugs
CONNECTOR_LENGTH = 35.0  # [A]
LAMP_PIGTAIL_LENGTH = 150.0  # [P] pole foot to barrel plug A — stays outside the box
CONTROLLER_CABLE_LAMP_SIDE = 580.0  # [S+P] controller to plug A
CONTROLLER_CABLE_ADAPTER_SIDE = 330.0  # [S+P] controller to plug B — stored entirely
CONTROLLER_SPARE_PIGTAIL = 300.0  # [P] second output with its own plug — stored entirely
ADAPTER_CORD_LENGTH = 1500.0  # [S] plug B to the AC adapter
CORD_OUTSIDE_LAMP_SIDE = 150.0  # [A] plug A to the box when the box sits beside the lamp base
CORD_OUTSIDE_OUTLET_SIDE = 500.0  # [A] box to the AC adapter at the outlet

# --- Enclosure (mm) ---
WALL_THICKNESS = 2.0  # [D] body walls
FLOOR_THICKNESS = 2.0  # [D] body floor
SKIN_THICKNESS = 2.0  # [D] lid top
SKIRT_THICKNESS = 2.0  # [D] lid outer wall
POCKET_WALL_THICKNESS = 2.0  # [D] controller pocket walls hanging from the skin
CAVITY_WIDTH = 44.0  # [D] body cavity across (Y); sets how many cord layers fit beside the posts
END_ZONE = 14.0  # [D] pocket end wall to body end wall — room for the boot and the downward bend
WINDING_HEIGHT = 22.0  # [D] floor top to post top; 4 mm per Ø4 turn
POST_DIAMETER = 12.0  # [D] winding posts; Ø12 gives the cord an 8 mm centreline bend
POST_SPACING = 78.0  # [D] post centre to centre, both under the controller
CONTROLLER_CLEARANCE = 0.5  # [D] per side, controller in its pocket (checked on Ver.0.2)
FACE_CLEARANCE = 0.5  # [D] controller face to skin underside — must clear BUTTON_AREA_PROUD
POCKET_BOTTOM_CLEARANCE = 0.3  # [D] pocket wall bottom edge above the post tops
POCKET_LEAD_IN = 1.0  # [D] 45° taper on the pocket's bottom inner edge — guides the controller in
LID_CLEARANCE = 0.25  # [D] per side, lid skirt over the body wall (sliding fit)
WINDOW_MARGIN = 1.5  # [D] per side, window larger than the button strip
WINDOW_CORNER_RADIUS = 3.0  # [D]
SLIT_CLEARANCE = 0.5  # [D] per side, slit and notch wider than the Ø4 cord
HOLE_HEIGHT = 7.0  # [D] open height of the cord exit above the floor top
GROUND_CLEARANCE = 1.0  # [D] skirt bottom edge above the floor
LID_CORNER_RADIUS = 4.0  # [D] plan-view corner radius of the lid
TOP_CHAMFER = 1.0  # [D] lid top edge
NOTCH_SKIN_MARGIN = 1.8  # [D] wall left between the pocket cable notches and the skin
PACKING_MARGIN = 1.0  # [D] cord layers stop this far from the body wall

# --- Finish ---
PETG_DENSITY = 1.27  # g/cm3
PRINT_SOLID_FRACTION = 0.9  # walls dominate; infill is a rounding error

# ===========================================================================
# Derived geometry
# ===========================================================================
OUTPUT_DIR = Path(__file__).parent / "output"
DRAWING_DIR = OUTPUT_DIR / "drawings"

# Pocket (lid) — controller outline plus clearance, walls outside that.
POCKET_L = CONTROLLER_LENGTH + 2 * CONTROLLER_CLEARANCE
POCKET_W = CONTROLLER_WIDTH + 2 * CONTROLLER_CLEARANCE
POCKET_INNER_R = CONTROLLER_CORNER_RADIUS + CONTROLLER_CLEARANCE
POCKET_OUTER_L = POCKET_L + 2 * POCKET_WALL_THICKNESS
POCKET_OUTER_W = POCKET_W + 2 * POCKET_WALL_THICKNESS
POCKET_OUTER_R = POCKET_INNER_R + POCKET_WALL_THICKNESS

# Body
CAVITY_LENGTH = POCKET_OUTER_L + 2 * END_ZONE
BODY_LENGTH = CAVITY_LENGTH + 2 * WALL_THICKNESS
BODY_WIDTH = CAVITY_WIDTH + 2 * WALL_THICKNESS
LID_INNER_R = LID_CORNER_RADIUS - SKIRT_THICKNESS
BODY_CORNER_R = LID_INNER_R - LID_CLEARANCE
CAVITY_CORNER_R = 1.0

# Lid
LID_INNER_LENGTH = BODY_LENGTH + 2 * LID_CLEARANCE
LID_INNER_WIDTH = BODY_WIDTH + 2 * LID_CLEARANCE
LID_LENGTH = LID_INNER_LENGTH + 2 * SKIRT_THICKNESS
LID_WIDTH = LID_INNER_WIDTH + 2 * SKIRT_THICKNESS

# Heights
Z_FLOOR_TOP = FLOOR_THICKNESS
Z_LEDGE = Z_FLOOR_TOP + WINDING_HEIGHT  # post tops = controller underside
Z_FACE = Z_LEDGE + CONTROLLER_HEIGHT
Z_SKIN_BOTTOM = Z_FACE + FACE_CLEARANCE  # = body wall top
BODY_HEIGHT = Z_SKIN_BOTTOM
Z_TOP = Z_SKIN_BOTTOM + SKIN_THICKNESS
Z_SKIRT_BOTTOM = GROUND_CLEARANCE
Z_POCKET_BOTTOM = Z_LEDGE + POCKET_BOTTOM_CLEARANCE
Z_SLOT_TOP = Z_SKIN_BOTTOM - NOTCH_SKIN_MARGIN
Z_CABLE = Z_LEDGE + CONTROLLER_CABLE_EXIT_HEIGHT
Z_HOLE_TOP = Z_FLOOR_TOP + HOLE_HEIGHT

# Posts and cord exit
POST_R = POST_DIAMETER / 2
POST_X = POST_SPACING / 2
SLIT_WIDTH = CABLE_DIAMETER + 2 * SLIT_CLEARANCE
WINDOW_L = BUTTON_AREA_LENGTH + 2 * WINDOW_MARGIN
WINDOW_W = BUTTON_AREA_WIDTH + 2 * WINDOW_MARGIN
X_BODY_WALL = CAVITY_LENGTH / 2 + WALL_THICKNESS / 2  # end wall centreline
X_SKIRT_END = LID_INNER_LENGTH / 2 + SKIRT_THICKNESS / 2  # lid end wall centreline

# Where the cord goes after the boot: straight to the boot tip, then a quarter bend down.
X_BOOT_TIP = CONTROLLER_LENGTH / 2 + CABLE_BOOT_LENGTH
X_DROP = X_BOOT_TIP + CABLE_BEND_RADIUS  # centreline of the vertical run in the end zone
Z_BEND_CENTRE = Z_CABLE - CABLE_BEND_RADIUS

# Cord capacity — turns around both posts, 4 mm per turn up the posts, then layers outward.
TURNS_PER_LAYER = floor(WINDING_HEIGHT / CABLE_DIAMETER)
MAX_LAYERS = floor((CAVITY_WIDTH / 2 - POST_R - PACKING_MARGIN) / CABLE_DIAMETER)


def turn_length(layer: int) -> float:
    """Length of one turn in the given layer (1 = against the posts)."""
    r = POST_R + (layer - 0.5) * CABLE_DIAMETER
    return 2 * POST_SPACING + 2 * pi * r


CAPACITY_MM = sum(TURNS_PER_LAYER * turn_length(k) for k in range(1, MAX_LAYERS + 1))
CAPACITY_COMFORTABLE_MM = sum(TURNS_PER_LAYER * turn_length(k) for k in range(1, MAX_LAYERS))
# Ø2 cord takes half the post height per turn, so it counts half.
STORED_MM = (
    (CONTROLLER_CABLE_LAMP_SIDE - CORD_OUTSIDE_LAMP_SIDE)
    + CONTROLLER_SPARE_PIGTAIL
    + CONTROLLER_CABLE_ADAPTER_SIDE
    + (ADAPTER_CORD_LENGTH - CORD_OUTSIDE_OUTLET_SIDE) * (CABLE_DIAMETER_ADAPTER / CABLE_DIAMETER)
)
WORST_CASE_MM = STORED_MM + CORD_OUTSIDE_OUTLET_SIDE * (CABLE_DIAMETER_ADAPTER / CABLE_DIAMETER)

# Plug stowage: standing upright in the end zone corners, beside the dropping cords.
PLUG_X = POCKET_OUTER_L / 2 + 0.75 + CONNECTOR_DIAMETER / 2
PLUG_Y = CAVITY_WIDTH / 2 - PACKING_MARGIN - CONNECTOR_DIAMETER / 2

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
assert POST_X + POST_R <= CONTROLLER_LENGTH / 2, "posts must sit under the controller"
assert POST_X + POST_R < POCKET_L / 2, "post top meets the pocket end wall"
assert POST_X - POST_R > 0, "posts overlap"
assert POCKET_OUTER_W + 2 * 1.0 <= CAVITY_WIDTH, "pocket walls hit the body walls"
assert X_DROP + CABLE_DIAMETER / 2 + 1.0 <= CAVITY_LENGTH / 2, (
    "end zone too short for the cord to bend down"
)
assert PLUG_X + CONNECTOR_DIAMETER / 2 + 0.5 <= CAVITY_LENGTH / 2, "plug does not fit the end zone"
assert (
    PLUG_Y - CONNECTOR_DIAMETER / 2
    >= max(CABLE_SLOT_WIDTH_LEFT / 2, CABLE_PAIR_PITCH / 2 + CABLE_DIAMETER / 2) + 1.0
), "plug collides with the dropping cords"
assert CONNECTOR_LENGTH <= BODY_HEIGHT - Z_FLOOR_TOP - 1.0, "plug too tall to stand in the end zone"
assert Z_SLOT_TOP >= Z_CABLE + CABLE_BOOT_DIAMETER / 2 + 1.0, "pocket notch too low for the boot"
assert Z_HOLE_TOP + 1.0 < Z_LEDGE, "cord exit hole reaches the controller zone"
assert SLIT_WIDTH < CONNECTOR_DIAMETER, "a plug could slip out through the slit"
assert MAX_LAYERS >= 2, "cavity too narrow for a second cord layer"
assert STORED_MM <= CAPACITY_COMFORTABLE_MM, "cords to store need the outermost layer"
assert WORST_CASE_MM <= CAPACITY_MM, "even the whole adapter lead would not fit"
assert LID_LENGTH <= 180 and LID_WIDTH <= 180 and Z_TOP <= 180, "lid does not fit the A1 Mini bed"


# ===========================================================================
# Parts
# ===========================================================================
def build_body() -> Part:
    with BuildPart() as body:
        with BuildSketch(Plane.XY):
            RectangleRounded(BODY_LENGTH, BODY_WIDTH, BODY_CORNER_R)
        extrude(amount=BODY_HEIGHT)
        with BuildSketch(Plane.XY.offset(Z_FLOOR_TOP)):
            RectangleRounded(CAVITY_LENGTH, CAVITY_WIDTH, CAVITY_CORNER_R)
        extrude(amount=BODY_HEIGHT - Z_FLOOR_TOP + 1.0, mode=Mode.SUBTRACT)
        # Winding posts, floor to controller underside.
        with Locations((-POST_X, 0, Z_FLOOR_TOP), (POST_X, 0, Z_FLOOR_TOP)):
            Cylinder(POST_R, WINDING_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Cord slits: both end walls, top edge down to the floor top.
        for sx in (-1, 1):
            with Locations((sx * X_BODY_WALL, 0, Z_FLOOR_TOP)):
                Box(
                    WALL_THICKNESS + 2.0,
                    SLIT_WIDTH,
                    BODY_HEIGHT - Z_FLOOR_TOP + 1.0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
    return body.part


def build_lid() -> Part:
    with BuildPart() as lid:
        with BuildSketch(Plane.XY.offset(Z_SKIRT_BOTTOM)):
            RectangleRounded(LID_LENGTH, LID_WIDTH, LID_CORNER_RADIUS)
        extrude(amount=Z_TOP - Z_SKIRT_BOTTOM)
        chamfer(lid.edges().group_by(Axis.Z)[-1], length=TOP_CHAMFER)
        # Hollow under the skin — the body slides in here.
        with BuildSketch(Plane.XY.offset(Z_SKIRT_BOTTOM - 1.0)):
            RectangleRounded(LID_INNER_LENGTH, LID_INNER_WIDTH, LID_INNER_R)
        extrude(amount=Z_SKIN_BOTTOM - Z_SKIRT_BOTTOM + 1.0, mode=Mode.SUBTRACT)
        # Pocket walls hanging from the skin around the controller.
        with BuildSketch(Plane.XY.offset(Z_POCKET_BOTTOM)):
            RectangleRounded(POCKET_OUTER_L, POCKET_OUTER_W, POCKET_OUTER_R)
            RectangleRounded(POCKET_L, POCKET_W, POCKET_INNER_R, mode=Mode.SUBTRACT)
        extrude(amount=Z_SKIN_BOTTOM - Z_POCKET_BOTTOM)
        # Lead-in: the pocket mouth is POCKET_LEAD_IN wider per side at its bottom edge.
        with BuildSketch(Plane.XY.offset(Z_POCKET_BOTTOM - 0.01)):
            RectangleRounded(
                POCKET_L + 2 * POCKET_LEAD_IN,
                POCKET_W + 2 * POCKET_LEAD_IN,
                POCKET_INNER_R + POCKET_LEAD_IN,
            )
        with BuildSketch(Plane.XY.offset(Z_POCKET_BOTTOM + POCKET_LEAD_IN)):
            RectangleRounded(POCKET_L, POCKET_W, POCKET_INNER_R)
        loft(mode=Mode.SUBTRACT)
        # Cable notches in the pocket end walls, open at the bottom.
        for sx, width, offset in (
            (-1, CABLE_SLOT_WIDTH_LEFT, CABLE_SLOT_OFFSET_LEFT),
            (1, CABLE_SLOT_WIDTH_RIGHT, CABLE_SLOT_OFFSET_RIGHT),
        ):
            with Locations(
                (sx * (POCKET_L / 2 + POCKET_WALL_THICKNESS / 2), offset, Z_POCKET_BOTTOM - 1.0)
            ):
                Box(
                    POCKET_WALL_THICKNESS + 1.0,
                    width,
                    Z_SLOT_TOP - Z_POCKET_BOTTOM + 1.0,
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
            with Locations((sx * X_SKIRT_END, 0, Z_SKIRT_BOTTOM - 1.0)):
                Box(
                    SKIRT_THICKNESS + 2.0,
                    SLIT_WIDTH,
                    Z_HOLE_TOP - SLIT_WIDTH / 2 - Z_SKIRT_BOTTOM + 1.0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
            with Locations((sx * X_SKIRT_END, 0, Z_HOLE_TOP - SLIT_WIDTH / 2)):
                Cylinder(
                    SLIT_WIDTH / 2, SKIRT_THICKNESS + 2.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT
                )
    return lid.part


def build_controller_stand_in() -> Part:
    with BuildPart() as c:
        with BuildSketch(Plane.XY.offset(Z_LEDGE)):
            RectangleRounded(CONTROLLER_LENGTH, CONTROLLER_WIDTH, CONTROLLER_CORNER_RADIUS)
        extrude(amount=CONTROLLER_HEIGHT)
        with BuildSketch(Plane.XY.offset(Z_FACE)):
            with Locations((BUTTON_AREA_OFFSET_X, BUTTON_AREA_OFFSET_Y)):
                RectangleRounded(BUTTON_AREA_LENGTH, BUTTON_AREA_WIDTH, 2.0)
        extrude(amount=BUTTON_AREA_PROUD)
        # Boots: two on the -X end, one on the +X end.
        boots = [(-1, CABLE_SLOT_OFFSET_LEFT - CABLE_PAIR_PITCH / 2)]
        boots += [(-1, CABLE_SLOT_OFFSET_LEFT + CABLE_PAIR_PITCH / 2)]
        boots += [(1, CABLE_SLOT_OFFSET_RIGHT)]
        for sx, y in boots:
            with Locations((sx * CONTROLLER_LENGTH / 2, y, Z_CABLE)):
                Cylinder(
                    CABLE_BOOT_DIAMETER / 2,
                    CABLE_BOOT_LENGTH,
                    rotation=(0, 90, 0),
                    align=(Align.CENTER, Align.CENTER, Align.MIN if sx > 0 else Align.MAX),
                )
    return c.part


def build_cord_stand_ins() -> dict[str, Part]:
    """Rough cord: three turns on the posts, a second layer of two, the two exit
    runs through the holes, and the drops from the controller ends."""
    parts: dict[str, Part] = {}
    with BuildPart() as turns:
        for layer, count in ((1, 3), (2, 2)):
            r_in = POST_R + (layer - 1) * CABLE_DIAMETER
            for i in range(count):
                with BuildSketch(Plane.XY.offset(Z_FLOOR_TOP + i * CABLE_DIAMETER)):
                    SlotCenterToCenter(POST_SPACING, 2 * (r_in + CABLE_DIAMETER))
                    SlotCenterToCenter(POST_SPACING, 2 * r_in, mode=Mode.SUBTRACT)
                extrude(amount=CABLE_DIAMETER)
    parts["cord-turns"] = turns.part
    with BuildPart() as exits:
        for sx in (-1, 1):
            with Locations(
                (sx * (POST_X + POST_R + 2 * CABLE_DIAMETER), 0, Z_FLOOR_TOP + CABLE_DIAMETER / 2)
            ):
                Cylinder(
                    CABLE_DIAMETER / 2,
                    LID_LENGTH / 2 + 15.0 - (POST_X + POST_R + 2 * CABLE_DIAMETER),
                    rotation=(0, 90, 0),
                    align=(Align.CENTER, Align.CENTER, Align.MIN if sx > 0 else Align.MAX),
                )
    parts["cord-exits"] = exits.part
    with BuildPart() as drops:
        for sx, y in (
            (-1, CABLE_SLOT_OFFSET_LEFT - CABLE_PAIR_PITCH / 2),
            (-1, CABLE_SLOT_OFFSET_LEFT + CABLE_PAIR_PITCH / 2),
            (1, CABLE_SLOT_OFFSET_RIGHT),
        ):
            # Quarter bend from the boot tip down, then a straight drop to the turns.
            # Built in the +X/+Z quadrant about its own centre, mirrored for the -X end.
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
                    Z_BEND_CENTRE - (Z_FLOOR_TOP + 3 * CABLE_DIAMETER),
                    align=(Align.CENTER, Align.CENTER, Align.MAX),
                )
    parts["cord-drops"] = drops.part
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
body = build_body()
lid = build_lid()
controller = build_controller_stand_in()
cords = build_cord_stand_ins()

printed: dict[str, Part] = {"body": body, "lid": lid}
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


# The bend stand-in must really start at the boot tip and end at the drop line.
_bend_bb = cords["cord-drops"].bounding_box()
assert abs(_bend_bb.max.X - (X_DROP + CABLE_DIAMETER / 2)) < 0.01, "bend stand-in misplaced"
assert abs(_bend_bb.min.X + (X_DROP + CABLE_DIAMETER / 2)) < 0.01, "bend stand-in misplaced (-X)"
assert abs(_bend_bb.max.Z - (Z_CABLE + CABLE_DIAMETER / 2)) < 0.01, "bend stand-in misplaced (z)"

# Nothing printed may hit anything, and the controller may not hit the cords.
interferences = []
pairs = [(a, b) for a in printed for b in everything if a < b or b in stand_ins]
pairs += [("controller", c) for c in cords]
seen = set()
for a, b in pairs:
    if a == b or (b, a) in seen:
        continue
    seen.add((a, b))
    v = overlap_volume(everything[a], everything[b])
    if v > 0.01:
        interferences.append((a, b, round(v, 2)))
assert not interferences, f"parts interfere: {interferences}"

# Lid lifts straight off; controller is captured in every direction once it is on.
assert overlap_volume(lid.moved(Location((0, 0, 30))), body) < 0.01, "lid cannot lift off"
assert overlap_volume(lid.moved(Location((0, 0, 30))), controller) < 0.01, (
    "lid lifts into the controller"
)
for dx, dy, dz in ((0, 0, 1.0), (1.5, 0, 0), (-1.5, 0, 0), (0, 1.5, 0), (0, -1.5, 0)):
    moved = controller.moved(Location((dx, dy, dz)))
    assert overlap_volume(moved, lid) > 0.1, f"controller not captured when moved {(dx, dy, dz)}"
assert overlap_volume(controller.moved(Location((0, 0, -1.0))), body) > 0.1, (
    "controller does not rest on the posts"
)

# The skin seats on the body wall top, nothing else touches first.
assert abs(body.bounding_box().max.Z - Z_SKIN_BOTTOM) < 1e-6
assert abs(lid.bounding_box().min.Z - Z_SKIRT_BOTTOM) < 1e-6

# Cord exit, both ends. Probes are X-rays through both walls: the hole must be clear of
# body *and* lid, the slit above the hole must be blanked by the skirt, the body slit must
# be open to the top edge so a cord can be laid in, and neither cut may be wider than designed.
_w = SLIT_WIDTH / 2 - 0.1
for sx in (-1, 1):
    x0, x1 = sorted((sx * (CAVITY_LENGTH / 2 - 1.0), sx * (LID_LENGTH / 2 + 1.0)))
    hole = slab(x0, x1, -_w, _w, Z_FLOOR_TOP + 0.1, Z_HOLE_TOP - SLIT_WIDTH / 2) + Cylinder(
        _w, x1 - x0, rotation=(0, 90, 0)
    ).moved(Location(((x0 + x1) / 2, 0, Z_HOLE_TOP - SLIT_WIDTH / 2)))
    assert overlap_volume(hole, body) < 0.01, f"body blocks the cord hole at x={sx}"
    assert overlap_volume(hole, lid) < 0.01, f"lid blocks the cord hole at x={sx}"
    above = slab(x0, x1, -_w, _w, Z_HOLE_TOP + 0.2, BODY_HEIGHT - 0.2)
    _skirt_fill = SKIRT_THICKNESS * 2 * _w * (BODY_HEIGHT - 0.2 - Z_HOLE_TOP - 0.2)
    assert overlap_volume(above, lid) > 0.98 * _skirt_fill, (
        f"skirt does not blank the slit above the hole at x={sx}"
    )
    assert overlap_volume(above, body) < 0.01, f"body slit is not open to the top edge at x={sx}"
    beside = slab(x0, x1, SLIT_WIDTH / 2 + 0.1, SLIT_WIDTH / 2 + 1.0, Z_FLOOR_TOP + 0.5, Z_HOLE_TOP)
    _both_fill = (WALL_THICKNESS + SKIRT_THICKNESS) * 0.9 * (Z_HOLE_TOP - Z_FLOOR_TOP - 0.5)
    assert overlap_volume(beside, body + lid) > 0.98 * _both_fill, (
        f"cord hole wider than designed at x={sx}"
    )

# Print-bed fit.
for name, part in printed.items():
    bb = part.bounding_box()
    assert max(bb.size.X, bb.size.Y, bb.size.Z) <= 180.0, f"{name} does not fit the bed"


# ===========================================================================
# Test pieces
# ===========================================================================
# 1. The lid's pocket and window only — does the controller drop in, is the button
#    strip centred in the window?  Prints skin-down like the lid.
_pocket_crop = slab(
    -(POCKET_OUTER_L / 2 + 6.0),
    POCKET_OUTER_L / 2 + 6.0,
    -(POCKET_OUTER_W / 2 + 4.0),
    POCKET_OUTER_W / 2 + 4.0,
    Z_POCKET_BOTTOM - 1.0,
    Z_TOP + 1.0,
)
test_pocket = lid & _pocket_crop
# 2. One end of body and lid, 14 mm tall: the sliding fit of the cap and the cord
#    hole formed by slit + notch. Align the two top edges to see the hole.
_end_crop = slab(
    CAVITY_LENGTH / 2 - 12.0,
    LID_LENGTH / 2 + 1.0,
    -LID_WIDTH / 2 - 1,
    LID_WIDTH / 2 + 1,
    -1.0,
    14.0,
)
test_end_body = body & _end_crop
test_end_lid = lid & _end_crop


# ===========================================================================
# Export
# ===========================================================================
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DRAWING_DIR.mkdir(parents=True, exist_ok=True)


def print_oriented(part: Part, flip: bool = False) -> Part:
    p = part.rotate(Axis.X, 180) if flip else part
    bb = p.bounding_box()
    return p.moved(Location((-bb.center().X, -bb.center().Y, -bb.min.Z)))


exports = {
    "body": (body, False),
    "lid": (lid, True),
    "test-pocket": (test_pocket, True),
    "test-end-body": (test_end_body, False),
    "test-end-lid": (test_end_lid, False),
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
    "body": Color(0.25, 0.25, 0.25),
    "lid": Color(0.15, 0.15, 0.15),
    "controller": Color(0.9, 0.9, 0.9),
    "cord-turns": Color(0.1, 0.3, 0.8),
    "cord-exits": Color(0.1, 0.3, 0.8),
    "cord-drops": Color(0.1, 0.3, 0.8),
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
# Long section on the XZ plane through the posts, slits and holes, seen from -Y.
_front_half = slab(-300, 300, 0, 300, -10, 300)
write_view("section-xz.svg", clipped(as_used, _front_half), origin=(0, -1000, 0), scale=2.0)
# Cross section on the YZ plane through a post, seen from +X.
_right_half = slab(-300, POST_X, -300, 300, -10, 300)
write_view("section-yz.svg", clipped(as_used, _right_half), origin=(1000, 0, 0), scale=3.0)
# The cord exit, from outside: hole = notch ∩ slit.
_end_detail = slab(CAVITY_LENGTH / 2 - 5.0, 300, -12, 12, -1, 20)
write_view("detail-exit.svg", clipped([body, lid], _end_detail), origin=(1000, 0, 0), scale=5.0)
# Exploded isometric: lid up, controller half-way.
exploded = []
for name, part in everything.items():
    dz = {"lid": 90.0, "controller": 45.0}.get(name, 0.0)
    exploded.append(part.moved(Location((0, 0, dz))))
write_view("exploded-iso.svg", exploded, origin=(900, -900, 700))
write_view("assembled-iso.svg", as_used, origin=(900, -900, 700))
for name, (part, flip) in exports.items():
    if not name.startswith("test"):
        write_view(f"part-{name}.svg", [print_oriented(part, flip)], origin=(700, -900, 800))
write_view(
    "test-pieces.svg",
    [
        print_oriented(test_pocket, True).moved(Location((0, 45, 0))),
        print_oriented(test_end_body).moved(Location((-25, -35, 0))),
        print_oriented(test_end_lid).moved(Location((25, -35, 0))),
    ],
    origin=(700, -900, 800),
)


# ===========================================================================
# Report
# ===========================================================================
def grams(part: Part) -> float:
    return part.volume / 1000 * PETG_DENSITY * PRINT_SOLID_FRACTION


print("Exported to", OUTPUT_DIR)
print(f"  box outside:    {LID_LENGTH:.1f} x {LID_WIDTH:.1f} x {Z_TOP:.1f} mm, 2 printed parts")
print(
    f"  body:           {BODY_LENGTH:.1f} x {BODY_WIDTH:.1f} x {BODY_HEIGHT:.1f} mm, "
    f"cavity {CAVITY_LENGTH:.1f} x {CAVITY_WIDTH:.1f}"
)
print(
    f"  stack:          floor top z={Z_FLOOR_TOP:.1f}, post top z={Z_LEDGE:.1f}, "
    f"face z={Z_FACE:.1f}, skin z={Z_SKIN_BOTTOM:.1f}..{Z_TOP:.1f}"
)
print(
    f"  window:         {WINDOW_L:.1f} x {WINDOW_W:.1f} mm at "
    f"({BUTTON_AREA_OFFSET_X:+.1f}, {BUTTON_AREA_OFFSET_Y:+.1f})"
)
print(
    f"  pocket:         {POCKET_L:.1f} x {POCKET_W:.1f}, walls to z={Z_POCKET_BOTTOM:.1f}, "
    f"notches to z={Z_SLOT_TOP:.1f}"
)
print(f"  posts:          Ø{POST_DIAMETER:.0f} at x=±{POST_X:.0f}, {WINDING_HEIGHT:.0f} tall")
print(
    f"  cord exit:      {SLIT_WIDTH:.1f} wide x {HOLE_HEIGHT:.1f} high at "
    f"z={Z_FLOOR_TOP:.0f}..{Z_HOLE_TOP:.0f}, both ends"
)
print(
    f"  end zone:       {END_ZONE:.1f} mm; cord drops at x=±{X_DROP:.1f} "
    f"(bend R{CABLE_BEND_RADIUS:.0f})"
)
print(
    f"  cord capacity:  {TURNS_PER_LAYER} turns/layer x {MAX_LAYERS} layers "
    f"-> ~{CAPACITY_MM / 1000:.2f} m packed, "
    f"~{CAPACITY_COMFORTABLE_MM / 1000:.2f} m without the outer layer"
)
print(
    f"  cord to store:  ~{STORED_MM / 1000:.2f} m (Ø4-equivalent; Ø2 counted half), "
    f"worst case {WORST_CASE_MM / 1000:.2f} m"
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
