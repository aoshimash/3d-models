"""Cable-store base case for the SwitchBot RGBIC floor lamp — prototype Ver.0.2.

A 220 mm matte-black disc, 24 mm tall, that sits over the lamp's own 202 mm
base, stores the spare 12 V cord in a ring channel around it, and presents the
inline controller flush in the top face, in front of the pole. Four printed
parts, no fasteners, no glue, nothing on the lamp is modified, and the lamp
never leaves the floor during assembly.

What the photos settled (Ver.0.1 → 0.2)
---------------------------------------
The controller is spliced into the cord: pole → 15 cm pigtail → barrel plug
→ controller cord (1 m end to end per SwitchBot support, roughly 58 cm on the
lamp side and 33 cm on the adapter side from the photos) → barrel plug → AC
adapter on a 1.5 m cord, plus a spare pigtail with its own plug on the
controller's two-cable end. Nothing can be
threaded, so the controller cannot be dropped into a tight window after the
cover is on — it has to be *on the base first* and the cover has to come down
over it and its cords. That rules out any step that lifts the lamp (Ver.0.1
screwed a floor plate on from underneath). So:

- No floor plate. The lamp base stays on the floor on its own anti-slip
  sheet, exactly as shipped; stability is unchanged.
- The four covers rest on the lamp base's rim and are joined to each other by
  vertical dovetails at the four seams. The two side covers carry tongues on
  both edges, the front and back covers carry the grooves: sides go on first,
  then back and front drop straight down over them. Front and back lift
  straight off again; the sides are locked under their skins until they do.
- The controller is captured by the front cover's pocket, whose end-wall
  cable notches are open at the bottom: the pocket descends over the
  controller with the cords already in place.

How the stack works
-------------------
Z = 0 is the floor. The lamp base rim top is the datum for everything above it:
the controller sits on it, and the covers sit on it through the channel rib
(r = 80) and the pocket's outer wall. So the controller face and the skin top
coincide no matter what the base thickness turns out to be — only
CONTROLLER_HEIGHT matters.

    z = 24.6  skin top = controller face      (BASE_RIM_THICKNESS + CONTROLLER_HEIGHT)
    z = 22.6  skin underside
    z = 19    top of the black pole foot (Ø38 assumed) — 3.6 mm under the skin, so
              nothing hangs from the skin inside it (no pole collar; rails shallow there).
              The Ø55 disc around it is only ~0.2 mm proud and is ignored.
    z =  8.1  lamp base rim top = controller seat = channel floor = cover seat
    z =  1    skirt bottom edge (GROUND_CLEARANCE above the floor)
    z =  0    floor

Button loads go controller → lamp base (the user's "方式A"). The covers carry
nothing but their own ~45 g each.

Why the pocket, not a sliding parting line
------------------------------------------
Every cover carries an arc of the skirt, and an arc cannot translate
tangentially around a cylinder, so covers only ever arrive vertically. A
vertical arrival cannot pass retaining lips over a controller already on the
base — but it *can* pass a lip-less pocket over it: the four pocket walls hang
from the skin to the base rim, the window is the controller outline plus
CONTROLLER_CLEARANCE, and the end walls are notched from their bottom edge for
the cords. Sideways the controller is captured over its full height; downward
by the base; upward only by gravity and the cords. No bezel, no seam across
the panel, no separate holder.

A lip reaching over the controller's rounded edge to hide the clearance line
was tried and dropped: with the face flush with the skin the lip has zero
thickness where the fillet starts, so it needs the controller recessed by
~1.2 mm and the controller loaded into the cover from below. Flush won.

Part split
----------
Front 96° (pocket), back 96° (cord exit), two 84° sides which are one part
printed twice. 96/84 keeps the front seams 7 mm clear of the pocket cavity;
4 × 90° would leave 1.5 mm of wall. Seams carry a 0.3 mm gap so printed
oversize cannot stop the ring closing.

Measured vs assumed
-------------------
Tagged on each parameter: [M] measured by the user (approximate), [P] read off
the user's photos, [S] from the SwitchBot spec sheet, [A] assumed, [D] design
choice. The spec sheet's "厚さ 1.6 cm" against the measured 4/6 mm is most
the pole socket — the rim measures 8.1 mm and the black pole foot 19 mm.

Print notes
-----------
- Covers print skin-down: the visible top is the bed face (textured PEI gives
  the matte finish for free) and every wall, rib, pad, dovetail and the skirt
  grows straight up — no supports, no bridges. The exported STLs are already
  in that orientation.
- Front/back covers are 163 × 99 mm on a 180 mm bed: fits, use a skirt not a
  wide brim.
- PETG, 0.2 mm layers, 3–4 walls, 15–20 % infill. Skin and skirt are 2 mm,
  effectively all perimeter.
"""

from math import cos, degrees, floor, pi, radians, sin, sqrt
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Color,
    Compound,
    Cylinder,
    Ellipse,
    ExportSVG,
    GeomType,
    LineType,
    Location,
    Locations,
    Mode,
    Part,
    Plane,
    Polygon,
    Rectangle,
    RectangleRounded,
    Torus,
    chamfer,
    export_step,
    export_stl,
    extrude,
    fillet,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# ===========================================================================
# Parameters   [M] measured  [P] from photos  [S] spec sheet  [A] assumed  [D] design
# ===========================================================================

# --- Existing lamp (mm) ---
BASE_DIAMETER = 202.0  # [M] base disc diameter (spec sheet: 20 cm)
BASE_RIM_THICKNESS = 8.1  # [M] thickness near the rim — the datum for controller and covers
BASE_CENTER_THICKNESS = 19.0  # [M] floor to the top of the black pole foot
BASE_HUB_DIAMETER = 38.0  # [A] diameter of that black foot — not measured, pole + margin
BASE_DISC_DIAMETER = 55.0  # [M] faint disc around the foot, ~0.2 mm proud — ignored
POLE_WIDTH = 30.5  # [M] pole ellipse, long axis (along X, tangential to the controller)
POLE_DEPTH = 26.0  # [M] pole ellipse, short axis (along Y)
LAMP_PIGTAIL_LENGTH = 150.0  # [P] pole foot to the barrel plug, lies on the base top
POLE_CORD_EXIT_BOTTOM = 3.5  # [M] cord leaves the pole foot this far above the base top
POLE_CORD_EXIT_TOP = 9.5  # [M] top edge of the cord there
LAMP_MASS_KG = 1.27  # [S]

# --- Controller (mm) ---
CONTROLLER_LENGTH = 90.5  # [M] long side, tangential
CONTROLLER_WIDTH = 34.5  # [M] short side, radial
CONTROLLER_HEIGHT = 16.5  # [M] sets the case height
CONTROLLER_CORNER_RADIUS = 4.0  # [A] plan-view corner radius of the housing
CONTROLLER_EDGE_RADIUS = 2.0  # [A] fillet on the housing's top edge (stand-in only)
BUTTON_AREA_LENGTH = 71.0  # [M] documented only — the whole face is exposed
BUTTON_AREA_WIDTH = 16.0  # [M]
CONTROLLER_CABLE_EXIT_HEIGHT = CONTROLLER_HEIGHT / 2  # [M] cables leave at mid-height
CABLE_BOOT_DIAMETER = 6.0  # [M] strain-relief boot where each cable leaves the controller
CABLE_BOOT_LENGTH = 5.0  # [M]
CABLE_PAIR_PITCH = 8.0  # [M] centre distance of the two cables on the -X end
CABLE_SLOT_MARGIN = 1.5  # [D] per side, notch wider than the boots
CABLE_SLOT_WIDTH_LEFT = CABLE_PAIR_PITCH + CABLE_BOOT_DIAMETER + 2 * CABLE_SLOT_MARGIN  # two cables
CABLE_SLOT_WIDTH_RIGHT = CABLE_BOOT_DIAMETER + 2 * CABLE_SLOT_MARGIN  # one cable
CABLE_SLOT_OFFSET_LEFT = 0.0  # [A] slot centre offset along Y from the controller centreline
CABLE_SLOT_OFFSET_RIGHT = 0.0  # [A]
CONTROLLER_CORD_TOTAL = (
    1000.0  # [S] "コントローラーの長さは 1 m" — plug to plug, controller included
)
CONTROLLER_CABLE_LAMP_SIDE = 580.0  # [S+P] the 1 m split by the photo's ratio; stored entirely
CONTROLLER_CABLE_ADAPTER_SIDE = 330.0  # [S+P] likewise; stored entirely
CONTROLLER_SPARE_PIGTAIL = 300.0  # [P] second output with its own plug, stored entirely
ADAPTER_CORD_LENGTH = 1500.0  # [S] AC adapter to its plug; stored only as far as the outlet allows

# --- Cable (mm) ---
CABLE_DIAMETER = 4.0  # [M] pole pigtail and controller cables
CABLE_DIAMETER_ADAPTER = 2.0  # [M] the adapter lead is thinner
CABLE_MIN_BEND_RADIUS = 12.0  # [A] design value used for routing checks, not a datasheet figure
CONNECTOR_DIAMETER = 10.0  # [A] barrel plugs, two of them, both stored in the channel
CONNECTOR_LENGTH = 35.0  # [A]
CABLE_PACKING_PITCH = 1.25  # [D] strand pitch / diameter assumed when estimating capacity

# --- Enclosure (mm) ---
ENCLOSURE_DIAMETER = 220.0  # [D] outer diameter
TOP_SKIN_THICKNESS = 2.0  # [D] cover top
SKIRT_THICKNESS = 2.0  # [D] cover outer wall
WALL_THICKNESS = 2.0  # [D] pocket walls, pole collar, locating pads
RIB_THICKNESS = 1.6  # [D] stiffening ribs and the channel rib
RIB_DEPTH = 8.0  # [D] height of the stiffening ribs and seam rails under the skin
RAIL_WIDTH = 6.0  # [D] seam rail, per side of the seam — the dovetails live in it
CONTROLLER_CLEARANCE = 0.5  # [D] per side, controller in its pocket (user's initial value)
CONTROLLER_PROUD = 0.0  # [D] controller face above the skin top (negative = recessed)
POLE_CLEARANCE = 2.5  # [D] per side around the pole — absorbs base centring error
BASE_CLEARANCE = 1.0  # [D] per side, lamp base inside the locating pads
PARTING_GAP = 0.3  # [D] total gap left at each radial seam
GROUND_CLEARANCE = 1.0  # [D] skirt bottom edge above the floor
CONTROLLER_RADIUS = 68.0  # [D] controller centre from the lamp axis; it sits at -Y (front)
FRONT_SECTOR_ANGLE = 96.0  # [D] front and back cover sectors; sides take the rest
CABLE_EXIT_ANGLE = 90.0  # [D] cord leaves the case here (90 = back, +Y)
EXIT_NOTCH_WIDTH = CABLE_DIAMETER + 2.0  # [D]
STRAIN_POST_DIAMETER = 6.0  # [D] capstan post beside the exit; cord bend radius = 3 + r_cable
STRAIN_POST_OFFSET = 12.0  # [D] tangential distance from the exit notch
PAD_LENGTH = 6.0  # [D] radial locating pads around the base rim, 8 of them

# --- Dovetails (mm) — vertical; plan-view trapezoid extruded over the rail height ---
DOVETAIL_ROOT_WIDTH = 6.0  # [D] tongue width (radial) at the seam face
DOVETAIL_TIP_WIDTH = 8.0  # [D] tongue width (radial) at its tip
DOVETAIL_DEPTH = 3.0  # [D] how far the tongue reaches across the seam (tangential)
DOVETAIL_SLOP = 0.15  # [D] per side; FDM sliding fit — tune with test-dovetail
DOVETAIL_INSET = 8.0  # [D] inner dovetail sits this far outside the pole-foot zone

# --- Finish (mm) ---
TOP_EDGE_CHAMFER = 0.8  # [D] top outer edge; hides elephant foot on the bed face

OUTPUT_DIR = Path(__file__).parent / "output"
DRAWING_DIR = OUTPUT_DIR / "drawings"


# ===========================================================================
# Derived geometry
# ===========================================================================
R_OUT = ENCLOSURE_DIAMETER / 2
R_SKIRT_IN = R_OUT - SKIRT_THICKNESS
BASE_R = BASE_DIAMETER / 2
HUB_R = BASE_HUB_DIAMETER / 2

Z_RIM_TOP = BASE_RIM_THICKNESS  # controller seat, channel floor, cover seat
Z_HUB_TOP = BASE_CENTER_THICKNESS
Z_CONTROLLER_TOP = Z_RIM_TOP + CONTROLLER_HEIGHT
Z_TOP = Z_CONTROLLER_TOP - CONTROLLER_PROUD  # skin top
Z_SKIN_BOTTOM = Z_TOP - TOP_SKIN_THICKNESS
Z_SKIRT_BOTTOM = GROUND_CLEARANCE
Z_POCKET_BOTTOM = Z_RIM_TOP + 0.5  # three pocket walls hover; the outer wall seats on the rim
Z_STIFFENER_BOTTOM = Z_SKIN_BOTTOM - RIB_DEPTH  # rails and ribs outside the pole-foot zone
Z_STIFFENER_BOTTOM_INNER = max(Z_STIFFENER_BOTTOM, Z_HUB_TOP + 1.0)  # over the boss
R_STIFFENER_FULL = BASE_HUB_DIAMETER / 2 + 2.0  # full-depth ribs start here
Z_COLLAR_BOTTOM = Z_HUB_TOP + CABLE_DIAMETER + 1.0  # a pole collar needs the cord to pass under
HAS_POLE_COLLAR = Z_COLLAR_BOTTOM <= Z_SKIN_BOTTOM - 3.0  # otherwise the skin edge is the hole
Z_SLOT_TOP = Z_RIM_TOP + CONTROLLER_CABLE_EXIT_HEIGHT + CABLE_BOOT_DIAMETER / 2 + 1.5
Z_EXIT_TOP = Z_RIM_TOP + CABLE_DIAMETER + 1.0
ENCLOSURE_HEIGHT = Z_TOP  # floor to skin top

# Controller pocket, centred on -Y
POCKET_CX, POCKET_CY = 0.0, -CONTROLLER_RADIUS
CAVITY_L = CONTROLLER_LENGTH + 2 * CONTROLLER_CLEARANCE
CAVITY_W = CONTROLLER_WIDTH + 2 * CONTROLLER_CLEARANCE
CAVITY_R = CONTROLLER_CORNER_RADIUS + CONTROLLER_CLEARANCE
POCKET_L = CAVITY_L + 2 * WALL_THICKNESS
POCKET_W = CAVITY_W + 2 * WALL_THICKNESS
POCKET_R = CAVITY_R + WALL_THICKNESS

# Channel
RIB_R = BASE_R - 22.0  # channel inner rib centreline — 21 mm of channel on the base rim
CHANNEL_INNER_R = RIB_R + RIB_THICKNESS / 2
CHANNEL_WIDTH_ON_BASE = BASE_R - CHANNEL_INNER_R
CHANNEL_HEIGHT = Z_SKIN_BOTTOM - Z_RIM_TOP
# The rib is removed across the front so the cords leave the pocket notches straight and the
# pole pigtail can reach the channel; the cut stays 3° inside the front cover.
RIB_CUTOUT_HALF_WIDTH = RIB_R * sin(radians(FRONT_SECTOR_ANGLE / 2 - 3.0))

# Pole cutout
# Round, so the pole's ellipse can face any way the lamp happens to be turned.
POLE_HOLE_R = max(POLE_WIDTH, POLE_DEPTH) / 2 + POLE_CLEARANCE

# Sectors (degrees, CCW from +X). Front cover is centred on 270°.
SIDE_SECTOR_ANGLE = (360.0 - 2 * FRONT_SECTOR_ANGLE) / 2
HALF_FRONT = FRONT_SECTOR_ANGLE / 2
COVER_SECTORS = {
    "front": (270 - HALF_FRONT, 270 + HALF_FRONT),
    "side-right": (270 + HALF_FRONT, 90 - HALF_FRONT + 360),
    "back": (90 - HALF_FRONT, 90 + HALF_FRONT),
    "side-left": (90 + HALF_FRONT, 270 - HALF_FRONT),
}
# At each seam the cover whose CCW edge it is carries the tongue; its neighbour the groove.
COVER_PARTING_ANGLES = [270 - HALF_FRONT, 270 + HALF_FRONT, 90 - HALF_FRONT, 90 + HALF_FRONT]
COVER_BISECTORS = [270.0, 0.0, 90.0, 180.0]
PAD_ANGLES = [22.5 + 45.0 * k for k in range(8)]
PAD_R0 = BASE_R + BASE_CLEARANCE
STRAIN_POST_R = BASE_R + 1.0 + STRAIN_POST_DIAMETER / 2
DOVETAIL_RADII = (R_STIFFENER_FULL + DOVETAIL_INSET, RIB_R - 12.0)  # centre radius, per seam
STRAIN_POST_ANGLE = CABLE_EXIT_ANGLE - degrees(STRAIN_POST_OFFSET / STRAIN_POST_R)


def polar(r: float, angle_deg: float) -> tuple[float, float]:
    a = radians(angle_deg)
    return r * cos(a), r * sin(a)


def dist_to_radial_line(x: float, y: float, angle_deg: float) -> float:
    """Perpendicular distance from (x, y) to the line through the origin at angle_deg."""
    a = radians(angle_deg)
    return abs(x * sin(a) - y * cos(a))


# ===========================================================================
# Feasibility checks — these are the Step-1 layout checks, kept live
# ===========================================================================
_cav_x, _cav_y_in = CAVITY_L / 2, -(CONTROLLER_RADIUS - CAVITY_W / 2)
_pocket_outer_corner = (POCKET_L / 2, -(CONTROLLER_RADIUS + POCKET_W / 2))
_corner_r = sqrt(_pocket_outer_corner[0] ** 2 + _pocket_outer_corner[1] ** 2)
_seam_margin = min(dist_to_radial_line(_cav_x, _cav_y_in, a) for a in COVER_SECTORS["front"])
_channel_at_corner = R_SKIRT_IN - _corner_r
STORED_CORD_M = (
    LAMP_PIGTAIL_LENGTH
    + CONTROLLER_CABLE_LAMP_SIDE
    + CONTROLLER_CABLE_ADAPTER_SIDE
    + CONTROLLER_SPARE_PIGTAIL
) / 1000

assert CONTROLLER_RADIUS - CAVITY_W / 2 - WALL_THICKNESS >= HUB_R + 2.0, (
    "pocket inner wall overlaps the base hub — the controller would rock on the step"
)
assert CONTROLLER_RADIUS + POCKET_W / 2 <= BASE_R - 1.0, "pocket outer wall misses the base rim"
assert _corner_r + 2.0 < R_SKIRT_IN, "controller pocket hits the skirt"
assert _channel_at_corner >= CABLE_DIAMETER + 1.0, "no cable passage past the pocket corners"
assert _seam_margin >= WALL_THICKNESS + 2.0, "front cover seams cut into the controller pocket"
assert POLE_HOLE_R < R_STIFFENER_FULL < RIB_R, "pole cutout reaches the rib zone"
assert RIB_CUTOUT_HALF_WIDTH > POCKET_L / 2 + 2.0, "channel rib would plug the pocket notches"
assert Z_HUB_TOP + 1.5 <= Z_SKIN_BOTTOM, "the pole foot hits the skin"
assert Z_RIM_TOP + POLE_CORD_EXIT_TOP + 1.0 <= Z_SKIN_BOTTOM, (
    "the pole cord cannot pass under the skin — recess the controller (CONTROLLER_PROUD < 0)"
)
assert Z_SLOT_TOP <= Z_SKIN_BOTTOM - 1.5, "cable notch would cut through the skin"
assert Z_SLOT_TOP - Z_RIM_TOP >= CONTROLLER_CABLE_EXIT_HEIGHT + CABLE_BOOT_DIAMETER / 2 + 1.0
assert STRAIN_POST_R + STRAIN_POST_DIAMETER / 2 <= R_SKIRT_IN + 1.0
assert STRAIN_POST_R - STRAIN_POST_DIAMETER / 2 >= BASE_R + 0.5, "strain post lands on the base"
assert PAD_R0 + PAD_LENGTH <= R_SKIRT_IN + 0.5, "locating pads poke through the skirt"
assert CONNECTOR_DIAMETER <= min(CHANNEL_WIDTH_ON_BASE, CHANNEL_HEIGHT) - 2.0, (
    "barrel plugs do not fit the channel"
)
assert DOVETAIL_DEPTH + DOVETAIL_SLOP + 1.5 <= RAIL_WIDTH, "groove breaks through the rail"
assert all(
    r + DOVETAIL_TIP_WIDTH / 2 + 1 < RIB_R - RIB_THICKNESS
    and r - DOVETAIL_TIP_WIDTH / 2 > R_STIFFENER_FULL + 1
    for r in DOVETAIL_RADII
), "a dovetail runs into the pole-foot zone or the channel rib"

# Cable capacity: strands that fit side by side on the base-rim part of the channel.
_pitch = CABLE_DIAMETER * CABLE_PACKING_PITCH
_strands_wide = floor(CHANNEL_WIDTH_ON_BASE / _pitch)
_strands_high = floor(CHANNEL_HEIGHT / _pitch)
_loop_length = 2 * pi * (CHANNEL_INNER_R + CHANNEL_WIDTH_ON_BASE / 2)
# Outside the base rim the channel drops to the floor: one more column of strands.
_gap_width = R_SKIRT_IN - BASE_R - BASE_CLEARANCE
_gap_strands = floor(_gap_width / _pitch) * floor((Z_SKIN_BOTTOM - Z_SKIRT_BOTTOM) / _pitch)
_gap_loop_length = 2 * pi * (BASE_R + _gap_width / 2)
# The front sector is the controller's; loops close around it only past the pocket corners.
_capacity_mm = (_strands_wide * _strands_high * _loop_length + _gap_strands * _gap_loop_length) * (
    1 - FRONT_SECTOR_ANGLE / 360
)
CABLE_CAPACITY_M = _capacity_mm / 1000
CABLE_CAPACITY_COMFORTABLE_M = CABLE_CAPACITY_M * 0.6
WORST_CASE_CORD_M = STORED_CORD_M + ADAPTER_CORD_LENGTH / 1000  # outlet right beside the lamp
assert (
    CONTROLLER_CABLE_LAMP_SIDE + CONTROLLER_CABLE_ADAPTER_SIDE + CONTROLLER_LENGTH
    <= CONTROLLER_CORD_TOTAL + 50
), "controller cord segments exceed the official 1 m"
assert STORED_CORD_M < CABLE_CAPACITY_COMFORTABLE_M, "the fixed-length cords alone fill the channel"
assert WORST_CASE_CORD_M < CABLE_CAPACITY_M, "whole cord incl. the adapter lead does not fit packed"


# ===========================================================================
# Builders
# ===========================================================================
def sector_prism(a0: float, a1: float, half_gap: float, reach: float = 400.0) -> Part:
    """Tall prism over angles a0→a1 (CCW), each radial face pulled inward by half_gap."""
    mid = radians((a0 + a1) / 2)
    half = radians((a1 - a0) / 2)
    apex_r = half_gap / sin(half)
    apex = (apex_r * cos(mid), apex_r * sin(mid))
    p0 = (apex[0] + reach * cos(radians(a0)), apex[1] + reach * sin(radians(a0)))
    p1 = (apex[0] + reach * cos(radians(a1)), apex[1] + reach * sin(radians(a1)))
    far = (apex[0] + 1.5 * reach * cos(mid), apex[1] + 1.5 * reach * sin(mid))
    with BuildPart() as prism:
        with BuildSketch(Plane.XY.offset(-50)):
            Polygon(apex, p0, far, p1, align=None)
        extrude(amount=150)
    return prism.part


def radial_box(r0: float, r1: float, width: float, z0: float, z1: float, angle: float) -> None:
    """Inside a BuildPart: box from radius r0 to r1 along the ray at `angle`, z0..z1."""
    x, y = polar(r0, angle)
    with Locations((x, y, z0)):
        Box(
            r1 - r0,
            width,
            z1 - z0,
            rotation=(0, 0, angle),
            align=(Align.MIN, Align.CENTER, Align.MIN),
        )


def dovetail_prism(
    seam_angle: float, r_centre: float, grow: float, z0: float, z1: float, direction: int
) -> Part:
    """Vertical dovetail across the seam at `seam_angle`, pointing CCW (+1) or CW (-1).

    Plan-view trapezoid in the seam's frame (u = radial along the seam, n = normal in the
    pointing direction): DOVETAIL_ROOT_WIDTH wide at the seam, DOVETAIL_TIP_WIDTH wide
    DOVETAIL_DEPTH across it, plus a 1 mm stub back into the owner so a tongue fuses with its
    rail. `grow` pads every face — that is what turns the tongue into the groove.
    """
    a = radians(seam_angle)
    u = (cos(a), sin(a))
    n = (-direction * sin(a), direction * cos(a))
    half_root = DOVETAIL_ROOT_WIDTH / 2 + grow
    half_tip = DOVETAIL_TIP_WIDTH / 2 + grow
    depth = DOVETAIL_DEPTH + grow

    def pt(along: float, across: float) -> tuple[float, float]:
        return (along * u[0] + across * n[0], along * u[1] + across * n[1])

    with BuildPart() as prism:
        with BuildSketch(Plane.XY.offset(z0)):
            Polygon(
                pt(r_centre - half_root, -1.0),
                pt(r_centre + half_root, -1.0),
                pt(r_centre + half_root, 0.0),
                pt(r_centre + half_tip, depth),
                pt(r_centre - half_tip, depth),
                pt(r_centre - half_root, 0.0),
                align=None,
            )
        extrude(amount=z1 - z0)
    return prism.part


def build_cover_ring() -> Part:
    """The complete 360° cover; sectors are cut from it afterwards."""
    with BuildPart() as cover:
        # Skin
        with Locations((0, 0, Z_SKIN_BOTTOM)):
            Cylinder(R_OUT, TOP_SKIN_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Skirt
        with BuildSketch(Plane.XY.offset(Z_SKIRT_BOTTOM)):
            Circle(R_OUT)
            Circle(R_SKIRT_IN, mode=Mode.SUBTRACT)
        extrude(amount=Z_SKIN_BOTTOM - Z_SKIRT_BOTTOM)
        # Locating pads: radial fins just outside the base rim, down to the skirt's bottom edge
        for a in PAD_ANGLES:
            radial_box(
                PAD_R0, PAD_R0 + PAD_LENGTH, WALL_THICKNESS, Z_SKIRT_BOTTOM, Z_SKIN_BOTTOM, a
            )
        # Channel rib: the inner wall of the cable ring and the covers' seat on the base rim.
        # Cut away across the front.
        with BuildSketch(Plane.XY.offset(Z_RIM_TOP)):
            Circle(RIB_R + RIB_THICKNESS / 2)
            Circle(RIB_R - RIB_THICKNESS / 2, mode=Mode.SUBTRACT)
            Rectangle(
                2 * RIB_CUTOUT_HALF_WIDTH,
                R_OUT,
                align=(Align.CENTER, Align.MAX),
                mode=Mode.SUBTRACT,
            )
        extrude(amount=Z_SKIN_BOTTOM - Z_RIM_TOP)
        # Pole collar — only when the pole foot leaves room for it and the cord under it
        if HAS_POLE_COLLAR:
            with BuildSketch(Plane.XY.offset(Z_COLLAR_BOTTOM)):
                Circle(POLE_HOLE_R + WALL_THICKNESS)
            extrude(amount=Z_SKIN_BOTTOM - Z_COLLAR_BOTTOM)
        # Rails straddling each radial seam (halved by the split), and bisector ribs.
        # Shallow over the pole foot, full depth from R_STIFFENER_FULL out to the channel rib.
        for a in COVER_PARTING_ANGLES:
            radial_box(
                10.0, R_STIFFENER_FULL, 2 * RAIL_WIDTH, Z_STIFFENER_BOTTOM_INNER, Z_SKIN_BOTTOM, a
            )
            radial_box(
                R_STIFFENER_FULL, RIB_R, 2 * RAIL_WIDTH, Z_STIFFENER_BOTTOM, Z_SKIN_BOTTOM, a
            )
        for a in COVER_BISECTORS:
            if a == 270.0:
                continue  # the pocket is there
            radial_box(
                10.0, R_STIFFENER_FULL, RIB_THICKNESS, Z_STIFFENER_BOTTOM_INNER, Z_SKIN_BOTTOM, a
            )
            radial_box(R_STIFFENER_FULL, RIB_R, RIB_THICKNESS, Z_STIFFENER_BOTTOM, Z_SKIN_BOTTOM, a)
        # Controller pocket walls; the outer wall also seats on the base rim
        with BuildSketch(Plane.XY.offset(Z_POCKET_BOTTOM)):
            with Locations((POCKET_CX, POCKET_CY)):
                RectangleRounded(POCKET_L, POCKET_W, POCKET_R)
        extrude(amount=Z_SKIN_BOTTOM - Z_POCKET_BOTTOM)
        with Locations((POCKET_CX, POCKET_CY - CAVITY_W / 2 - WALL_THICKNESS / 2, Z_RIM_TOP)):
            Box(
                CAVITY_L - 2 * POCKET_R,
                WALL_THICKNESS,
                Z_POCKET_BOTTOM - Z_RIM_TOP + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        # Strain-relief post beside the cord exit: a round post webbed into the skirt
        px, py = polar(STRAIN_POST_R, STRAIN_POST_ANGLE)
        with Locations((px, py, Z_SKIRT_BOTTOM)):
            Cylinder(
                STRAIN_POST_DIAMETER / 2,
                Z_SKIN_BOTTOM - Z_SKIRT_BOTTOM,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        radial_box(
            STRAIN_POST_R,
            R_OUT - 0.5,
            WALL_THICKNESS,
            Z_SKIRT_BOTTOM,
            Z_SKIN_BOTTOM,
            STRAIN_POST_ANGLE,
        )

        # --- Subtractions ---
        # Pole cutout through everything
        with BuildSketch(Plane.XY.offset(-10)):
            Circle(POLE_HOLE_R)
        extrude(amount=Z_TOP + 20, mode=Mode.SUBTRACT)
        # Controller cavity + window
        with BuildSketch(Plane.XY.offset(Z_RIM_TOP - 1)):
            with Locations((POCKET_CX, POCKET_CY)):
                RectangleRounded(CAVITY_L, CAVITY_W, CAVITY_R)
        extrude(amount=Z_TOP - Z_RIM_TOP + 2, mode=Mode.SUBTRACT)
        # Cable notches in the pocket end walls, open at the bottom
        for sign, width, offset in (
            (-1, CABLE_SLOT_WIDTH_LEFT, CABLE_SLOT_OFFSET_LEFT),
            (+1, CABLE_SLOT_WIDTH_RIGHT, CABLE_SLOT_OFFSET_RIGHT),
        ):
            cx = POCKET_CX + sign * (CAVITY_L / 2 + WALL_THICKNESS / 2)
            with Locations((cx, POCKET_CY + offset, Z_RIM_TOP - 1)):
                Box(
                    WALL_THICKNESS + 2,
                    width,
                    Z_SLOT_TOP - Z_RIM_TOP + 1,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
        # Cord exit notch in the skirt, rounded top, open at the bottom edge
        ex, ey = polar(R_OUT - SKIRT_THICKNESS / 2, CABLE_EXIT_ANGLE)
        with Locations((ex, ey, Z_SKIRT_BOTTOM - 1)):
            Box(
                SKIRT_THICKNESS + 2,
                EXIT_NOTCH_WIDTH,
                Z_EXIT_TOP - EXIT_NOTCH_WIDTH / 2 - Z_SKIRT_BOTTOM + 1,
                rotation=(0, 0, CABLE_EXIT_ANGLE),
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )
        with Locations((ex, ey, Z_EXIT_TOP - EXIT_NOTCH_WIDTH / 2)):
            Cylinder(
                EXIT_NOTCH_WIDTH / 2,
                SKIRT_THICKNESS + 2,
                rotation=(0, 90, CABLE_EXIT_ANGLE),
                mode=Mode.SUBTRACT,
            )
        # Top outer edge
        top_face = cover.faces().sort_by(Axis.Z)[-1]
        top_outer = [
            e for e in top_face.edges().filter_by(GeomType.CIRCLE) if abs(e.radius - R_OUT) < 1e-3
        ]
        chamfer(top_outer, length=TOP_EDGE_CHAMFER)
    return cover.part


def add_dovetails(sector: Part, a0: float, a1: float, tongues: bool) -> Part:
    """Tongues on both edges (side covers) or grooves on both edges (front and back).

    A tongue sits under its neighbour's skin, so the tongue owner must already be in place
    when the groove owner drops on. Sides first, then front and back.
    """
    z0, z1 = Z_STIFFENER_BOTTOM, Z_SKIN_BOTTOM
    for r in DOVETAIL_RADII:
        if tongues:
            sector = sector + dovetail_prism(a0, r, 0.0, z0, z1 - 0.3, direction=-1)
            sector = sector + dovetail_prism(a1, r, 0.0, z0, z1 - 0.3, direction=+1)
        else:
            sector = sector - dovetail_prism(a0, r, DOVETAIL_SLOP, z0 - 1, z1, direction=+1)
            sector = sector - dovetail_prism(a1, r, DOVETAIL_SLOP, z0 - 1, z1, direction=-1)
    return sector


def build_lamp_stand_in() -> tuple[Part, Part]:
    """Lamp base (disc + hub) and a stub of the pole, for the assembly and the drawings."""
    with BuildPart() as base:
        Cylinder(BASE_R, BASE_RIM_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, Z_RIM_TOP)):
            Cylinder(
                HUB_R,
                BASE_CENTER_THICKNESS - BASE_RIM_THICKNESS,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
    with BuildPart() as pole:
        with BuildSketch(Plane.XY.offset(Z_HUB_TOP)):
            Ellipse(POLE_WIDTH / 2, POLE_DEPTH / 2)
        extrude(amount=60)
    return base.part, pole.part


def build_controller_stand_in() -> Part:
    with BuildPart() as ctl:
        with BuildSketch(Plane.XY.offset(Z_RIM_TOP)):
            with Locations((POCKET_CX, POCKET_CY)):
                RectangleRounded(CONTROLLER_LENGTH, CONTROLLER_WIDTH, CONTROLLER_CORNER_RADIUS)
        extrude(amount=CONTROLLER_HEIGHT)
        fillet(ctl.faces().sort_by(Axis.Z)[-1].edges(), radius=CONTROLLER_EDGE_RADIUS)
        with BuildSketch(Plane.XY.offset(Z_CONTROLLER_TOP - 0.3)):
            with Locations((POCKET_CX, POCKET_CY)):
                RectangleRounded(BUTTON_AREA_LENGTH, BUTTON_AREA_WIDTH, 2.0)
        extrude(amount=0.3, mode=Mode.SUBTRACT)
    return ctl.part


def build_cable_stand_in() -> Part:
    """One stored loop lying on the base rim, round the back — shows the channel in section."""
    r = CHANNEL_INNER_R + CHANNEL_WIDTH_ON_BASE / 2
    loop = Torus(r, CABLE_DIAMETER / 2, major_angle=360 - FRONT_SECTOR_ANGLE - 10)
    loop = loop.moved(
        Location((0, 0, Z_RIM_TOP + CABLE_DIAMETER / 2), (0, 0, 270 + HALF_FRONT + 5))
    )
    return Part() + loop


# ===========================================================================
# Build
# ===========================================================================
cover_ring = build_cover_ring()
half_gap = PARTING_GAP / 2

covers: dict[str, Part] = {}
for name, (a0, a1) in COVER_SECTORS.items():
    sector = cover_ring & sector_prism(a0, a1, half_gap)
    covers[name] = add_dovetails(sector, a0, a1, tongues=name.startswith("side"))

lamp_base, pole = build_lamp_stand_in()
controller = build_controller_stand_in()
cable_loop = build_cable_stand_in()

# Unique printed parts. The two side covers are one part: rotating side-right by 180° about Z
# gives side-left exactly (pocket and exit are not in them, dovetail handedness is preserved).
unique_parts: dict[str, Part] = {
    "cover-front": covers["front"],
    "cover-back": covers["back"],
    "cover-side": covers["side-right"],
}


def shape_volume(shape) -> float:
    """Volume of a Shape, a ShapeList, or None — booleans return any of them."""
    if shape is None:
        return 0.0
    if isinstance(shape, (list, tuple)):
        return sum(shape_volume(s) for s in shape)
    try:
        return shape.volume
    except Exception:
        return 0.0


_side_mirror = covers["side-right"].rotate(Axis.Z, 180)
_side_diff = shape_volume(_side_mirror - covers["side-left"]) + shape_volume(
    covers["side-left"] - _side_mirror
)
assert _side_diff < 1.0, f"side covers are not interchangeable (diff {_side_diff:.2f} mm3)"


# ===========================================================================
# Verification
# ===========================================================================
def report_bbox(name: str, part: Part) -> tuple[float, float, float]:
    bb = part.bounding_box()
    size = (bb.size.X, bb.size.Y, bb.size.Z)
    assert max(size) <= 180.0, f"{name} does not fit the A1 Mini bed: {size}"
    return size


def overlap_volume(a: Part, b: Part) -> float:
    try:
        return shape_volume(a & b)
    except Exception:  # OCCT may throw on disjoint shapes
        return 0.0


printed = {
    "cover-front": covers["front"],
    "cover-back": covers["back"],
    "cover-side-right": covers["side-right"],
    "cover-side-left": covers["side-left"],
}
stand_ins = {
    "lamp-base": lamp_base,
    "pole": pole,
    "controller": controller,
    "cable-loop": cable_loop,
}
everything = {**printed, **stand_ins}
names = list(everything)
interferences = []
for i, n1 in enumerate(names):
    for n2 in names[i + 1 :]:
        v = overlap_volume(everything[n1], everything[n2])
        if v > 0.01:
            interferences.append((n1, n2, v))
assert not interferences, f"parts interfere: {interferences}"
# Dovetail mechanics at the back|side-right seam: pulling the covers apart must collide,
# the groove owner (back) must lift straight off, the tongue owner must be locked under it.
_seam = COVER_SECTORS["back"][0]
_n = (-sin(radians(_seam)), cos(radians(_seam)))  # from side-right into back
_pulled = covers["side-right"].moved(Location((-_n[0], -_n[1], 0)))
assert overlap_volume(_pulled, covers["back"]) > 1.0, "dovetail does not hold the seam closed"
_lifted_back = covers["back"].moved(Location((0, 0, 5)))
assert overlap_volume(_lifted_back, covers["side-right"]) < 0.01, "back cover cannot lift off"
_lifted_side = covers["side-right"].moved(Location((0, 0, 5)))
assert overlap_volume(_lifted_side, covers["back"]) > 1.0, "side cover is not locked by the back"
# Every cover must actually seat on the base rim (rib or pocket wall touching z = Z_RIM_TOP).
for name, part in printed.items():
    assert abs(part.bounding_box().min.Z - Z_SKIRT_BOTTOM) < 1e-6, f"{name} skirt bottom off"
    seat = part & Box(300, 300, 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, Z_RIM_TOP))
    )
    assert shape_volume(seat) > 1.0, f"{name} has no seat on the base rim"


# ===========================================================================
# Export
# ===========================================================================
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DRAWING_DIR.mkdir(parents=True, exist_ok=True)
for stale in OUTPUT_DIR.glob("floor-quadrant.*"):
    stale.unlink()
for stale in ("test-boss.stl", "test-floor.stl", "drawings/part-floor-quadrant.svg"):
    (OUTPUT_DIR / stale).unlink(missing_ok=True)


def print_oriented(part: Part, flip: bool = True) -> Part:
    """Flip covers skin-down and sit every part on z=0, centred on the bed."""
    p = part.rotate(Axis.X, 180) if flip else part
    bb = p.bounding_box()
    return p.moved(Location((-bb.center().X, -bb.center().Y, -bb.min.Z)))


sizes = {}
for name, part in unique_parts.items():
    oriented = print_oriented(part)
    sizes[name] = report_bbox(name, oriented)
    export_stl(oriented, str(OUTPUT_DIR / f"{name}.stl"))
    export_step(oriented, str(OUTPUT_DIR / f"{name}.step"))

# Test pieces: print these before the full set.
# 1. The pocket, cut out of the front cover — checks the controller fit and the cable notches.
_pocket_box = Box(
    POCKET_L + 16, POCKET_W + 16, 100, align=(Align.CENTER, Align.CENTER, Align.MIN)
).moved(Location((POCKET_CX, POCKET_CY, -5)))
test_pocket = print_oriented(covers["front"] & _pocket_box)
export_stl(test_pocket, str(OUTPUT_DIR / "test-pocket.stl"))
# 2. One dovetail pair — back|side-right seam, inner dovetail: side-right = tongue, back = groove.
_seam = COVER_SECTORS["back"][0]
_dx, _dy = polar(DOVETAIL_RADII[0], _seam)
_dove_box = Box(26, 26, 100, rotation=(0, 0, _seam), align=(Align.CENTER, Align.CENTER, Align.MIN))
_dove_box = _dove_box.moved(Location((_dx, _dy, -5)))
test_dovetail_tongue = print_oriented(covers["side-right"] & _dove_box)
test_dovetail_groove = print_oriented(covers["back"] & _dove_box)
export_stl(test_dovetail_tongue, str(OUTPUT_DIR / "test-dovetail-tongue.stl"))
export_stl(test_dovetail_groove, str(OUTPUT_DIR / "test-dovetail-groove.stl"))

# Assembly, in the as-used orientation, with the lamp stand-ins.
ASSEMBLY_COLORS = {
    "cover-front": Color(0.18, 0.18, 0.18),
    "cover-back": Color(0.22, 0.22, 0.22),
    "cover-side-right": Color(0.26, 0.26, 0.26),
    "cover-side-left": Color(0.26, 0.26, 0.26),
    "lamp-base": Color(0.05, 0.05, 0.05),
    "pole": Color(0.95, 0.95, 0.95),
    "controller": Color(0.1, 0.1, 0.12),
    "cable-loop": Color(0.6, 0.1, 0.1),
}
assembly_children = []
for name, part in everything.items():
    p = Part() + part
    p.label = name
    p.color = ASSEMBLY_COLORS[name]
    assembly_children.append(p)
assembly = Compound(children=assembly_children, label="switchbot-lamp-base-case")
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
# Section on the YZ plane through the pole, pocket (front) and cord exit (back), seen from +X.
_half_x = Part() + Box(600, 600, 600).moved(Location((-300, 0, 0)))
write_view("section-yz.svg", clipped(as_used, _half_x), origin=(1000, 0, 0), scale=2.0)
# Pocket detail: same section, cropped to the controller.
_detail_box = Part() + Box(1, POCKET_W + 30, 60, align=(Align.MAX, Align.CENTER, Align.MIN)).moved(
    Location((0, POCKET_CY, -5))
)
write_view("section-pocket.svg", clipped(as_used, _detail_box), origin=(1000, 0, 0), scale=5.0)
# Plan section at mid-height: channel, rib, pocket walls, pads, rails and dovetails.
_below = Part() + Box(600, 600, 600, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(
    Location((0, 0, Z_RIM_TOP + 8.0))
)
write_view("section-plan.svg", clipped(as_used, _below), origin=(0, 0, 1000), up=(0, 1, 0))
# Dovetail detail: the test pair, in print orientation, from above.
write_view(
    "detail-dovetail.svg",
    [
        test_dovetail_tongue.moved(Location((-16, 0, 0))),
        test_dovetail_groove.moved(Location((16, 0, 0))),
    ],
    origin=(0, 0, 1000),
    up=(0, 1, 0),
    scale=4.0,
)
# Exploded isometric: covers lifted, controller lifted further.
exploded = []
for name, part in everything.items():
    dz = 60.0 if name.startswith("cover") else 0.0
    if name == "controller":
        dz = 100.0
    exploded.append(part.moved(Location((0, 0, dz))))
write_view("exploded-iso.svg", exploded, origin=(900, -900, 700))
write_view("assembled-iso.svg", as_used, origin=(900, -900, 700))
for name in unique_parts:
    write_view(f"part-{name}.svg", [print_oriented(unique_parts[name])], origin=(700, -900, 800))


# ===========================================================================
# Report
# ===========================================================================
print("Exported to", OUTPUT_DIR)
print(
    f"  enclosure:      Ø{ENCLOSURE_DIAMETER:.0f} x {ENCLOSURE_HEIGHT:.0f} mm, "
    "4 printed parts, no fasteners"
)
print(
    f"  controller:     seat z={Z_RIM_TOP:.1f}, face z={Z_CONTROLLER_TOP:.1f}, "
    f"skin top z={Z_TOP:.1f}"
)
print(f"  pocket window:  {CAVITY_L:.1f} x {CAVITY_W:.1f} mm, walls to z={Z_POCKET_BOTTOM:.1f}")
_notches = f"left {CABLE_SLOT_WIDTH_LEFT:.0f} / right {CABLE_SLOT_WIDTH_RIGHT:.0f} mm wide"
print(
    f"  cable notches:  {_notches}, open from the rim up to z={Z_SLOT_TOP:.1f} "
    f"({Z_SKIN_BOTTOM - Z_SLOT_TOP:.1f} mm of wall left)"
)
print(
    f"  pole foot:      top z={Z_HUB_TOP:.1f}, {Z_SKIN_BOTTOM - Z_HUB_TOP:.1f} mm under the skin; "
    f"pole collar {'kept' if HAS_POLE_COLLAR else 'omitted'}; "
    f"ribs full depth from r={R_STIFFENER_FULL:.0f}"
)
print(f"  seam margin:    {_seam_margin:.1f} mm from the cavity to the nearest front seam")
print(
    f"  pole hole:      round Ø{2 * POLE_HOLE_R:.1f}; pole cord passes "
    f"{Z_SKIN_BOTTOM - Z_RIM_TOP - POLE_CORD_EXIT_TOP:.1f} mm under the skin"
)
print(
    f"  channel:        r {CHANNEL_INNER_R:.1f}..{BASE_R:.0f} on the base "
    f"({CHANNEL_WIDTH_ON_BASE:.1f} wide), {CHANNEL_HEIGHT:.0f} high; "
    f"{_channel_at_corner:.1f} mm past the pocket corners"
)
print(
    f"  cable capacity: {_strands_wide} x {_strands_high} strands -> "
    f"~{CABLE_CAPACITY_M:.1f} m packed, ~{CABLE_CAPACITY_COMFORTABLE_M:.1f} m laid loosely"
)
_adapter_m = ADAPTER_CORD_LENGTH / 1000
print(
    f"  cord to store:  fixed {STORED_CORD_M:.2f} m; "
    f"with the whole {_adapter_m:.1f} m adapter lead inside {WORST_CASE_CORD_M:.2f} m"
)
print(
    f"  sectors:        front/back {FRONT_SECTOR_ANGLE:.0f}°, sides {SIDE_SECTOR_ANGLE:.0f}°, "
    f"seams at {', '.join(f'{a:.0f}°' for a in sorted(a % 360 for a in COVER_PARTING_ANGLES))}"
)
_dove = f"{DOVETAIL_ROOT_WIDTH:.0f}->{DOVETAIL_TIP_WIDTH:.0f} x {DOVETAIL_DEPTH:.0f} mm"
print(
    f"  dovetails:      {_dove}, {Z_SKIN_BOTTOM - Z_STIFFENER_BOTTOM:.0f} tall, "
    f"slop {DOVETAIL_SLOP} per side, at r = {', '.join(f'{r:.0f}' for r in DOVETAIL_RADII)} "
    "on every seam"
)
print("  printed parts (print orientation, bed is 180 x 180):")
total_cm3 = 0.0
for name, (sx, sy, sz) in sizes.items():
    vol = unique_parts[name].volume / 1000
    count = 2 if name == "cover-side" else 1
    total_cm3 += vol * count
    grams = vol * 1.27 * 0.9
    size = f"{sx:6.1f} x {sy:6.1f} x {sz:5.1f} mm"
    print(f"    {name:12s} x{count}  {size}   {vol:5.1f} cm3  ~{grams:4.0f} g PETG each")
print(f"  whole set:      {total_cm3:.0f} cm3 solid, ~{total_cm3 * 1.27 * 0.9:.0f} g PETG")
print("  interference check between all parts and stand-ins: none; every cover seats on the rim")

if show is not None:
    try:
        show(assembly)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
