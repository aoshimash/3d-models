"""Smart-speaker case: Jabra Speak2 40 flush in the top, Raspberry Pi 4 B hung below.

Two parts, no hardware between them:

- box.stl : open-top box. Four tall standoffs carry the Pi 4 *component side
  down*, so the low-profile ICE-tower cooler on its SoC hangs under the board
  with its fan facing the floor. Both USB plugs live inside the box: the
  Jabra's USB-A adapter at the -X end of the Pi, the PSU's USB-C plug on the
  -Y side, with only the thin power cable leaving through a hole in the back
  wall at floor level.
- lid.stl : thick slab with the same footprint as the box, so the sides run
  flush from floor to top with only a hairline seam. A lip left standing on
  the inside of the box wall engages a groove in the lid's underside.
  A round pocket in its top face takes the whole height of the Jabra puck, so
  the puck's top ends up flush with the lid. The pocket floor is a ring that
  carries the puck's base, with one radial slot for the cable.

The Jabra puck, as it actually is
---------------------------------
The Speak2 40 is not a plain cylinder (Jabra's product renders, confirmed and
measured by the user): the top 7.5 mm of the side is a straight Ø120 band
carrying the buttons and LED ring, and below that the side slopes inward to a
Ø91.5 base. The base is a flat rubber ring (the central Ø51 is recessed by a
negligible 0.01 mm). The integrated Ø3.5 cable is wound in that conical
groove for transport and leaves the cone 8 mm above the base; its plug end is
8.5 x 6.5 mm.

How the puck is held and where the cable goes
---------------------------------------------
- Sideways: the straight Ø120 band is located by the Ø123 pocket wall
  (1.5 mm per side) at the mouth of the pocket. The cone below does not
  touch anything.
- Vertically: the rubber ring of the base sits on the pocket floor ring,
  which reaches RING_OVERLAP (8 mm) in under the base rim; the opening
  inside the ring is Ø75.5. The puck is held by its own 245 g; the pocket is
  32.5 mm deep so it cannot be knocked out.
- Cable: unwound from the groove, it leaves the cone and runs down the
  15.75 mm wide annular gap between cone and pocket wall, then through a
  10 mm wide radial slot in the ring (pointing -Y, toward the back of the
  box) into the box. The slot opens into the Ø75.5 hole, so the plug end is
  passed through the hole and the cable slid sideways into the slot. Rotate
  the puck so its cable exit sits over the slot; nothing is visible from
  outside.
- Removal: lift the lid off (the puck comes with it), push the puck up from
  below through the Ø75.5 opening.

Why the Pi hangs upside down
----------------------------
The Pi already carries its own CPU cooler (heat-pipe tower with a 40 mm fan on
top), so the case needs no fan of its own. What the case has to decide is
which way that fan points, because the Jabra's four microphones sit on top of
the stack and must not hear it. Flat, fan up, puts the fan 10 mm under the
lid right below the puck. On edge, fan sideways, points the USB-C receptacle
up or down and the plug no longer fits. Face down, fan toward the floor (this
design) puts the fan at the bottom of the box, pointing at the floor plate
and the desk, with the Pi board, the lid and the puck's body between it and
the mics, and costs nothing in height.

Heat: a tower cooler does not care which way is up — the fan forces the air
through the fins either way. The heat pipes work slightly against gravity but
on two short pipes with ~15 mm of rise and a Pi's <10 W that is not
measurable. Warm air off the fins rises to the exhaust slots high in the -X
wall; the fan draws fresh air through intake slots at floor level in the +X
wall, 40 mm from the fan.

Layout (box, looking down, origin at the box centre)
----------------------------------------------------
Flipping the board mirrors it: USB-C/HDMI edge faces -Y (the back), the GPIO
header faces +Y, the microSD end is at +X and the USB-A / Ethernet end at -X.
The Pi is pushed to the +Y half so the back half of the box, where the puck's
cable comes down and the power plug sits, is clear of it.

- -Y (back) wall: one 14 x 9 mm hole at floor level for the power cable. The
  USB-C plug is pushed through it from outside during assembly, then plugged
  into the receptacle, which hangs just under the board 88 mm from the wall
  (the user measured that the plug plus its bend needs 50 mm).
- -X wall: the Jabra's USB-A adapter plugs into the Pi's USB stack and runs
  toward this wall; 60 mm from the port face to the wall, as measured.
  A row of exhaust slots high up.
- +X wall: a row of intake slots at floor level, under the microSD end,
  feeding the gap under the fan.
- +Y (front) wall: closed.
- Cable storage: the back half of the floor takes the coiled Jabra cable.
  Keep it out of the ~40 mm square under the fan.
- microSD slot ends up facing *up* at the +X end: lift the lid and it is
  reachable without unscrewing anything.

Lid
---
- Pocket Ø123 x 32.5 deep; the puck stands 0.5 mm proud of the lid so its
  buttons never sit below the rim. Set PUCK_PROUD to 0 for dead flush.
- Flush joint: the top 4 mm of the box wall is stepped — the outer 2 mm is
  cut away to a ledge, the inner 1.6 mm stays as a lip. The lid is the full
  164 mm square; its underside carries a 2.1 mm wide, 4.3 mm deep groove
  that the lip enters with 0.25 mm per side, and its outer 1.7 mm rim sits
  on the ledge. Outside you see one seam line 55 mm up; the lid cannot
  slide, only lift (it is lifted by its edge, 34.9 mm tall). Being square
  with a central pocket it goes on in any of the four orientations; only
  the cable slot direction (toward the back) matters.
- The lid prints pocket-up on its flat underside; the groove is a 2.1 mm
  bridge on the bed side and needs no support.

Fits
----
- Pi: the cooler's bracket is mounted on 6 mm female-female standoffs at
  the Pi's four corner holes (PI_FOOT_H), so what lands on the pillar tops
  is the bracket, not the board. Remove the bracket-side screws and use
  M2.5 x 14..16 from the solder side instead: through the board, through the
  threaded standoff, through the bracket hole and into the Ø2.2 blind hole
  in the pillar (self-tapping; heat-set inserts if you have them). Only the
  screw heads stand above the solder side (BOARD_TOP_CLEARANCE is 4 mm).
- PI_ASSEMBLY_H (38 mm) is the user's measurement of the bare Pi + cooler,
  board solder side to the face of the fan, no base plate. The pillar
  height is derived from it so the fan ends up exactly FAN_FLOOR_GAP above
  the floor.
- Power cable hole is 13.5 x 9 mm for the measured 11.5 x 7 mm USB-C plug
  overmould (1 mm per side).

Fit tests (print these first, they are cheap)
---------------------------------------------
- fit-test-puck-collar.stl : an 8 mm tall ring of the Ø123 pocket mouth.
  Slip it over the puck's straight band from the top: it should drop on
  freely and locate the puck without rattling much.
- fit-test-puck-cup.stl : the pocket floor — the Ø75.5 ring with the
  cable slot — plus 8 mm of wall. Set the puck on it: the rubber ring of
  the base must sit on the ring, and the cable must reach the slot.
- fit-test-joint-box.stl / fit-test-joint-lid.stl : a 50 mm square box
  and lid with the real wall, ledge, lip, groove, corner radius and 0.25 mm
  clearance. The lid should drop onto the box without force, sit flush on
  all four sides and not slide. The box also carries the 13.5 x 9 mm power
  hole (push the PSU plug through) and one Ø8 pillar stub with the Ø2.2
  hole (try the M2.5 screw and the bracket).

Print notes
-----------
- Box: 164 x 164 x 59 mm, open side up, no supports. The slots and the
  cable hole are short bridges; the standoffs are plain pillars.
- Lid: 164 x 164 x 34.9 mm, pocket side up, flat on the bed, no
  supports. The rim around the pocket is a solid block in the model and
  prints as walls plus infill; 15 % is plenty.
- 164 mm on a 180 mm bed leaves room for a brim. 3 walls, 0.2 mm layers.

Preview
-------
assembly-preview.stl (do not print) carries stand-ins for every part in its
working position: the stepped puck, the Pi with its ports, header, cooler and
fan, both USB plugs and schematic runs of both cables. PREVIEW_PARTS lists
them by name for drawing scripts.

Sources
-------
- Jabra Speak2 40 tech sheet (Rev B, 24 Apr 2023): main unit Ø120 x 33 mm,
  245 g, integrated USB cable ca. 80 cm. Side profile from the product-page
  renders; band 7.5 mm, base Ø91.5, cable exit 8 mm up, cable Ø3.5 and
  plug 8.5 x 6.5 mm measured by the user.
- Raspberry Pi 4 mechanical drawing (RP-008343): 85 x 56, holes Ø2.7 at
  3.5 mm from the edges on a 58 x 49 pitch, USB-C centre 11.2 mm from the
  microSD end, HDMI at 26 and 39.5, SoC at (32.5, 25.75), USB stacks at
  9 and 27 from the USB-C edge (Z 16.0), Ethernet at 45.75 (Z 13.5),
  GPIO header Z 8.5.
- Cooler: user's own low-profile ICE-tower type, 40 mm fan on top; 38 mm
  from board underside to fan face and 6 mm corner standoffs, measured by
  the user without the plate.
- Plug clearances: 50 mm (USB-C) and 60 mm (USB-A), PSU plug overmould
  11.5 x 7 mm, measured by the user.
"""

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
    Locations,
    Mode,
    Plane,
    Pos,
    RectangleRounded,
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
PUCK_CLEARANCE = 1.5  # per side around the straight band — loose drop-in nest
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
PI_SD_OVERHANG = 2.5  # microSD card past the board edge
PI_SOC_X = 32.5
PI_SOC_Y = 25.75
PI_ASSEMBLY_H = 38.0  # board solder side to the cooler's fan face, measured (no base plate)
PI_FOOT_H = 6.0  # cooler's corner standoffs: component face to the bracket that lands on the pillar
COOLER_SIZE = 40.0  # fan / fin stack footprint, preview only
COOLER_FAN_T = 10.0  # fan frame depth, preview only

# --- Plugs (mm) ---
USBC_CLEARANCE = 50.0  # USB-C edge of the board to the back wall: plug + bend (measured)
USB_A_CLEARANCE = 60.0  # USB-A port face to the -X wall: adapter + bend (measured)
USBC_PLUG = (11.5, 30.0, 7.0)  # PSU plug overmould w, l, h — w/h measured, l preview only
USB_A_ADAPTER = (16.0, 45.0, 8.0)  # Jabra adapter w, l, h — preview only
POWER_HOLE_W = 13.5  # power cable hole: the 11.5 x 7 plug overmould must pass (1 mm per side)
POWER_HOLE_H = 9.0

# --- Box (mm) ---
OUTER = 164.0  # outer footprint, square
WALL = 3.6  # side walls — carries the rabbet
FLOOR = 3.0  # floor thickness
CORNER_R = 8.0  # vertical corner radius, outside
LIP_HEIGHT = 4.0  # how far the inner lip stands above the ledge
LEDGE_W = 2.0  # outer part of the wall cut away at the top; the lid's rim sits here
JOINT_CLEARANCE = 0.25  # per side, lip to groove
GROOVE_EXTRA = 0.3  # groove deeper than the lip so the rim, not the lip, carries the lid
EDGE_CHAMFER = 0.8  # bed-side edges, hides elephant foot

FAN_FLOOR_GAP = 10.0  # intake clearance between the fan face and the floor
BOARD_TOP_CLEARANCE = 4.0  # solder-side pins to the lid underside
STANDOFF_DIA = 8.0  # standoff outer diameter — tall pillars, so fatter than usual
SCREW_HOLE_DIA = 2.2  # M2.5 self-tapping
SCREW_HOLE_DEPTH = 6.0  # blind, from the standoff top
CENTRE_CLEAR_Y = 10.0  # Pi's USB-C edge sits this far +Y of centre
POWER_HOLE_Z = 8.5  # power cable hole centre above the box underside

INTAKE_W = 3.0  # intake slot width (Y), +X wall at floor level
INTAKE_H = 16.0
INTAKE_PITCH = 7.0
INTAKE_COUNT = 11
INTAKE_Z0 = 5.0  # slot bottom above the box underside
INTAKE_Y_START = 0.0  # first slot centre; the row runs under the fan toward +Y

VENT_W = 3.0  # exhaust slot width (Y), -X wall near the top
VENT_H = 24.0
VENT_PITCH = 7.0
VENT_COUNT = 12
VENT_LID_GAP = 4.0  # wall left between the slot top and the rabbet ledge
VENT_Y_START = -38.5  # first slot centre; the row is centred on the wall

# --- Lid (mm) ---
LID_FLOOR = 2.4  # pocket floor ring thickness
LID_TOP_FILLET = 1.0
POCKET_EDGE_CHAMFER = 0.8  # top edge of the pocket, next to the puck's rim

OUTPUT_DIR = Path(__file__).parent / "output"


# --- Derived ---
INNER = OUTER - 2 * WALL
HALF_IN = INNER / 2
COOLER_DROP = PI_ASSEMBLY_H - PI_BOARD_T  # component face down to the fan face
STANDOFF_H = FAN_FLOOR_GAP + COOLER_DROP - PI_FOOT_H  # floor top to the pillar top
PI_FACE_Z = FLOOR + STANDOFF_H + PI_FOOT_H  # component side of the board (facing down)
INNER_HEIGHT = PI_FACE_Z - FLOOR + PI_BOARD_T + BOARD_TOP_CLEARANCE  # floor top to lid underside
LID_BOTTOM_Z = FLOOR + INNER_HEIGHT
BOX_HEIGHT = LID_BOTTOM_Z + LIP_HEIGHT
LIP_THICK = WALL - LEDGE_W  # what is left of the wall beside the groove
LID_SIZE = OUTER  # flush with the box
LID_CORNER_R = CORNER_R
GROOVE_OUT = OUTER - 2 * LEDGE_W + 2 * JOINT_CLEARANCE  # groove outer boundary
GROOVE_IN = INNER - 2 * JOINT_CLEARANCE  # groove inner boundary
GROOVE_DEPTH = LIP_HEIGHT + GROOVE_EXTRA
RECESS_DEPTH = PUCK_HEIGHT - PUCK_PROUD
RECESS_DIA = PUCK_DIA + 2 * PUCK_CLEARANCE
OPENING_DIA = PUCK_BASE_DIA - 2 * RING_OVERLAP
LID_THICK = LID_FLOOR + RECESS_DEPTH
PUCK_TAPER_H = PUCK_HEIGHT - PUCK_STRAIGHT_H

# Board placement. Flipped about Y, so board-local x runs toward -X.
PI_X_USB = -HALF_IN + USB_A_CLEARANCE + PI_PORT_OVERHANG  # box X of the USB-A end
PI_X_END = PI_X_USB + PI_LENGTH  # box X of the microSD end
PI_Y0 = CENTRE_CLEAR_Y  # box Y of the USB-C edge
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

INTAKE_YS = [INTAKE_Y_START + i * INTAKE_PITCH for i in range(INTAKE_COUNT)]
VENT_Z0 = LID_BOTTOM_Z - VENT_LID_GAP - VENT_H
VENT_YS = [VENT_Y_START + i * VENT_PITCH for i in range(VENT_COUNT)]

WALL_FLAT_HALF = OUTER / 2 - CORNER_R  # flat run of each wall, outside the corner radii
SLOT_Y_IN = -(OPENING_DIA / 2 - 1.0)  # cable slot runs from the opening ...
SLOT_Y_OUT = -(RECESS_DIA / 2 + 1.0)  # ... out past the pocket wall

assert OUTER <= 180.0 and BOX_HEIGHT <= 180.0, "box does not fit the A1 Mini bed"
assert FAN_FACE_Z - FLOOR >= 8.0, "fan too close to the floor to breathe"
assert PI_X_END + PI_SD_OVERHANG < HALF_IN - 2.0, "microSD card hits the +X wall"
assert PI_Y0 + HALF_IN >= USBC_CLEARANCE, "no room for the USB-C plug"
assert PI_Y0 + PI_WIDTH < HALF_IN - 4.0, "GPIO edge too close to the front wall"
assert PI_Y0 > SLOT_Y_IN + 6.0, "puck cable would drop onto the Pi, not behind it"
assert OPENING_DIA >= 60.0, "opening too small to push the puck out"
assert PUCK_BASE_DIA < RECESS_DIA - 2 * 4.0, "base too close to the pocket wall for the cable"
assert PUCK_STRAIGHT_H < RECESS_DEPTH, "straight band must be inside the pocket"
assert min(INTAKE_YS) - INTAKE_W / 2 > -WALL_FLAT_HALF, "intake runs into the corner radius"
assert max(INTAKE_YS) + INTAKE_W / 2 < WALL_FLAT_HALF, "intake runs into the corner radius"
assert min(VENT_YS) - VENT_W / 2 > -WALL_FLAT_HALF, "vents run into the corner radius"
assert max(VENT_YS) + VENT_W / 2 < WALL_FLAT_HALF, "vents run into the corner radius"
assert VENT_Z0 > FAN_FACE_Z, "exhaust slots should sit above the fan, not beside it"
assert POWER_HOLE_Z - POWER_HOLE_H / 2 > FLOOR, "power cable hole breaks into the floor"
assert abs(USBC_X) + POWER_HOLE_W / 2 < WALL_FLAT_HALF, "power hole runs into the corner radius"
assert LIP_THICK >= 1.2, "lip thinner than three perimeters"
assert GROOVE_OUT < OUTER - 2.0, "lid rim outside the groove too thin"
assert SCREW_HOLE_DEPTH < STANDOFF_H, "screw hole runs out of the standoff"


# ---------------------------------------------------------------------------
# Box
# ---------------------------------------------------------------------------
with BuildPart() as box_builder:
    with BuildSketch():
        RectangleRounded(OUTER, OUTER, CORNER_R)
    extrude(amount=BOX_HEIGHT)
    chamfer(box_builder.faces().sort_by(Axis.Z)[0].edges(), length=EDGE_CHAMFER)

    # Cavity, up to the wall top
    with BuildSketch(Plane.XY.offset(FLOOR)):
        RectangleRounded(INNER, INNER, CORNER_R - WALL)
    extrude(amount=BOX_HEIGHT - FLOOR, mode=Mode.SUBTRACT)

    # Ledge: cut the outer part of the wall away at the top, leaving the inner lip
    with BuildSketch(Plane.XY.offset(LID_BOTTOM_Z)):
        RectangleRounded(OUTER + 2, OUTER + 2, CORNER_R + 1)
        RectangleRounded(
            OUTER - 2 * LEDGE_W, OUTER - 2 * LEDGE_W, CORNER_R - LEDGE_W, mode=Mode.SUBTRACT
        )
    extrude(amount=LIP_HEIGHT + 1, mode=Mode.SUBTRACT)

    # Pi standoffs (tall pillars) with blind screw holes from the top
    with BuildSketch(Plane.XY.offset(FLOOR)):
        with Locations(*PI_HOLES):
            Circle(radius=STANDOFF_DIA / 2)
    extrude(amount=STANDOFF_H)
    with BuildSketch(Plane.XY.offset(FLOOR + STANDOFF_H)):
        with Locations(*PI_HOLES):
            Circle(radius=SCREW_HOLE_DIA / 2)
    extrude(amount=-SCREW_HOLE_DEPTH, mode=Mode.SUBTRACT)

    # Intake slots in the +X wall, at floor level near the fan
    for iy in INTAKE_YS:
        with Locations(Pos(OUTER / 2 - WALL / 2, iy, INTAKE_Z0 + INTAKE_H / 2)):
            Box(WALL + 2, INTAKE_W, INTAKE_H, mode=Mode.SUBTRACT)

    # Exhaust slots in the -X wall, up near the lid
    for vy in VENT_YS:
        with Locations(Pos(-OUTER / 2 + WALL / 2, vy, VENT_Z0 + VENT_H / 2)):
            Box(WALL + 2, VENT_W, VENT_H, mode=Mode.SUBTRACT)

    # Power cable hole in the -Y wall, at floor level below the receptacle
    with Locations(Pos(USBC_X, -OUTER / 2 + WALL / 2, POWER_HOLE_Z)):
        Box(POWER_HOLE_W, WALL + 2, POWER_HOLE_H, mode=Mode.SUBTRACT)

box_part = box_builder.part


# ---------------------------------------------------------------------------
# Lid
# ---------------------------------------------------------------------------
with BuildPart() as lid_builder:
    with BuildSketch():
        RectangleRounded(LID_SIZE, LID_SIZE, LID_CORNER_R)
    extrude(amount=LID_THICK)
    fillet(lid_builder.faces().sort_by(Axis.Z)[-1].edges(), radius=LID_TOP_FILLET)

    # Groove in the underside for the box's lip
    with BuildSketch(Plane.XY.offset(-1)):
        RectangleRounded(GROOVE_OUT, GROOVE_OUT, CORNER_R - LEDGE_W + JOINT_CLEARANCE)
        RectangleRounded(
            GROOVE_IN, GROOVE_IN, CORNER_R - WALL - JOINT_CLEARANCE, mode=Mode.SUBTRACT
        )
    extrude(amount=1 + GROOVE_DEPTH, mode=Mode.SUBTRACT)

    # Puck pocket, full puck height less what stands proud
    with Locations(Pos(0, 0, LID_THICK)):
        Cylinder(
            radius=RECESS_DIA / 2,
            height=RECESS_DEPTH,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
            mode=Mode.SUBTRACT,
        )
    pocket_rim = (
        lid_builder.edges()
        .filter_by(GeomType.CIRCLE)
        .filter_by(lambda e: abs(e.radius - RECESS_DIA / 2) < 0.01)
        .sort_by(Axis.Z)[-1]
    )
    chamfer(pocket_rim, length=POCKET_EDGE_CHAMFER)

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
            PI_USBC_X - 4.5, PI_USBC_X + 4.5, -1.3, 7.5, PI_FACE_Z - PI_USBC_HEIGHT, PI_FACE_Z
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
            -PI_SD_OVERHANG, 12.5, 20.5, 31.5, PI_FACE_Z + PI_BOARD_T, PI_FACE_Z + PI_BOARD_T + 1.0
        ),
    ]
)
cooler_feet = Compound(
    children=[
        Pos(x, y, PI_FACE_Z - PI_FOOT_H)
        * Cylinder(radius=2.5, height=PI_FOOT_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        for x, y in PI_HOLES
    ]
)
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

# PSU plug in the receptacle, cable down and out through the back wall
usbc_plug = Pos(USBC_X, PI_Y0 - 1.3, USBC_Z) * Box(
    USBC_PLUG[0], USBC_PLUG[1], USBC_PLUG[2], align=(Align.CENTER, Align.MAX, Align.CENTER)
)
usbc_tail = PI_Y0 - 1.3 - USBC_PLUG[1]
power_cable = _cable(
    [
        (USBC_X, usbc_tail, USBC_Z),
        (USBC_X, usbc_tail - 14.0, USBC_Z - 6.0),
        (USBC_X, -HALF_IN + 8.0, POWER_HOLE_Z),
        (USBC_X, -OUTER / 2 - 20.0, POWER_HOLE_Z),
    ],
    CABLE_DIA / 2,
)

# Jabra adapter in the upper port of the USB 3.0 stack, cable looping through
# the back half of the floor and up through the lid slot into the puck's cone
usb_a_y = PI_Y0 + PI_USB_YS[1]
usb_a_z = PI_FACE_Z - 4.5
usb_a_face = PI_X_USB - PI_PORT_OVERHANG
usb_a_adapter = Pos(usb_a_face, usb_a_y, usb_a_z) * Box(
    USB_A_ADAPTER[1],
    USB_A_ADAPTER[0],
    USB_A_ADAPTER[2],
    align=(Align.MAX, Align.CENTER, Align.CENTER),
)
cable_exit = (0.0, -(PUCK_BASE_DIA / 2 + 1.0), puck_z + PUCK_CABLE_EXIT_Z)
JABRA_CABLE_PATH = [
    (usb_a_face - USB_A_ADAPTER[1], usb_a_y, usb_a_z),
    (usb_a_face - USB_A_ADAPTER[1] - 8.0, usb_a_y, usb_a_z - 8.0),
    (-HALF_IN + 6.0, usb_a_y - 10.0, FLOOR + 12.0),
    (-HALF_IN + 6.0, -HALF_IN + 20.0, FLOOR + 6.0),
    (-30.0, -HALF_IN + 6.0, FLOOR + 6.0),
    (30.0, -HALF_IN + 6.0, FLOOR + 6.0),
    (40.0, -40.0, FLOOR + 8.0),
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
    ("usbc_plug", usbc_plug),
    ("power_cable", power_cable),
    ("usb_a_adapter", usb_a_adapter),
    ("jabra_cable", jabra_cable),
]
assembly = Compound(label="smart-speaker-case", children=[shape for _, shape in PREVIEW_PARTS])


# ---------------------------------------------------------------------------
# Fit-test pieces
# ---------------------------------------------------------------------------
TEST_WALL = 3.0  # wall of the two puck test pieces
TEST_COLLAR_H = 8.0  # collar: the pocket mouth, slips over the straight band
TEST_CUP_WALL_H = 8.0  # cup: short wall above the floor ring
TEST_RABBET_OUTER = 50.0  # mini box / lid pair, real wall, lip and corner radius
TEST_RABBET_H = 20.0  # mini box wall height including the lip
TEST_RABBET_FLOOR = 2.0
TEST_PILLAR_H = 8.0  # pillar stub in the mini box
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
    collar_rim = (
        collar_builder.edges()
        .filter_by(GeomType.CIRCLE)
        .filter_by(lambda e: abs(e.radius - RECESS_DIA / 2) < 0.01)
        .sort_by(Axis.Z)[-1]
    )
    chamfer(collar_rim, length=POCKET_EDGE_CHAMFER)
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
    with BuildSketch():
        RectangleRounded(TEST_RABBET_OUTER, TEST_RABBET_OUTER, CORNER_R)
    extrude(amount=TEST_RABBET_H)
    chamfer(test_box_builder.faces().sort_by(Axis.Z)[0].edges(), length=EDGE_CHAMFER)
    with BuildSketch(Plane.XY.offset(TEST_RABBET_FLOOR)):
        RectangleRounded(
            TEST_RABBET_OUTER - 2 * WALL, TEST_RABBET_OUTER - 2 * WALL, CORNER_R - WALL
        )
    extrude(amount=TEST_RABBET_H - TEST_RABBET_FLOOR, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(TEST_RABBET_H - LIP_HEIGHT)):
        RectangleRounded(TEST_RABBET_OUTER + 2, TEST_RABBET_OUTER + 2, CORNER_R + 1)
        RectangleRounded(
            TEST_RABBET_OUTER - 2 * LEDGE_W,
            TEST_RABBET_OUTER - 2 * LEDGE_W,
            CORNER_R - LEDGE_W,
            mode=Mode.SUBTRACT,
        )
    extrude(amount=LIP_HEIGHT + 1, mode=Mode.SUBTRACT)
    # the real power-cable hole, in the -Y wall
    with Locations(Pos(0, -TEST_RABBET_OUTER / 2 + WALL / 2, POWER_HOLE_Z)):
        Box(POWER_HOLE_W, WALL + 2, POWER_HOLE_H, mode=Mode.SUBTRACT)
    # one pillar stub with the M2.5 hole
    with Locations(Pos(0, 0, TEST_RABBET_FLOOR)):
        Cylinder(
            radius=STANDOFF_DIA / 2,
            height=TEST_PILLAR_H,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
    with Locations(Pos(0, 0, TEST_RABBET_FLOOR + TEST_PILLAR_H - SCREW_HOLE_DEPTH)):
        Cylinder(
            radius=SCREW_HOLE_DIA / 2,
            height=SCREW_HOLE_DEPTH + 1,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )
test_box = test_box_builder.part

with BuildPart() as test_lid_builder:
    with BuildSketch():
        RectangleRounded(TEST_RABBET_OUTER, TEST_RABBET_OUTER, CORNER_R)
    extrude(amount=TEST_LID_THICK)
    fillet(test_lid_builder.faces().sort_by(Axis.Z)[-1].edges(), radius=LID_TOP_FILLET)
    test_groove_out = TEST_RABBET_OUTER - 2 * LEDGE_W + 2 * JOINT_CLEARANCE
    test_groove_in = TEST_RABBET_OUTER - 2 * WALL - 2 * JOINT_CLEARANCE
    with BuildSketch(Plane.XY.offset(-1)):
        RectangleRounded(test_groove_out, test_groove_out, CORNER_R - LEDGE_W + JOINT_CLEARANCE)
        RectangleRounded(
            test_groove_in, test_groove_in, CORNER_R - WALL - JOINT_CLEARANCE, mode=Mode.SUBTRACT
        )
    extrude(amount=1 + GROOVE_DEPTH, mode=Mode.SUBTRACT)
test_lid = test_lid_builder.part

assert POWER_HOLE_Z + POWER_HOLE_H / 2 < TEST_RABBET_H - LIP_HEIGHT - 2.0, "test hole hits the lip"
assert TEST_RABBET_FLOOR + TEST_PILLAR_H < TEST_RABBET_H - LIP_HEIGHT, "test pillar hits the lid"


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
    print(f"Exported box / lid / assembly-preview / 4 fit tests to: {OUTPUT_DIR}")

    box_cm3 = box_part.volume / 1000
    lid_cm3 = lid_part.volume / 1000
    total_h = max(puck_z + PUCK_HEIGHT, LID_BOTTOM_Z + LID_THICK)
    usbc_room = PI_Y0 + HALF_IN
    usb_a_room = usb_a_face + HALF_IN
    print(f"  box:        {OUTER:.0f} x {OUTER:.0f} x {BOX_HEIGHT:.0f} mm, {box_cm3:.0f} cm3")
    print(f"  lid:        {LID_SIZE:.1f} x {LID_SIZE:.1f} x {LID_THICK:.1f} mm, {lid_cm3:.0f} cm3")
    print(
        f"  assembled:  {OUTER:.0f} x {OUTER:.0f} x {total_h:.1f} mm, puck {PUCK_PROUD:.1f} proud"
    )
    print(f"  puck nest:  Ø{RECESS_DIA:.1f} x {RECESS_DEPTH:.1f} deep, ring to Ø{OPENING_DIA:.0f}")
    print(
        f"  Pi:         x {PI_X_USB:.1f} .. {PI_X_END:.1f}, y {PI_Y0:.1f} .. {PI_Y0 + PI_WIDTH:.1f}"
    )
    print(f"  pillars:    {STANDOFF_H:.1f} mm tall, fan face at z={FAN_FACE_Z:.1f}")
    screw = PI_BOARD_T + PI_FOOT_H + 1.5 + SCREW_HOLE_DEPTH - 1.0
    print(f"  Pi screws:  M2.5 x ~{screw:.0f} mm from the solder side, through the standoffs")
    tests = [test_collar, test_cup, test_box, test_lid]
    print(f"  fit tests:  {', '.join(f'{t.volume / 1000:.0f} cm3' for t in tests)} solid")
    print(f"  plug room:  USB-C {usbc_room:.1f} mm, USB-A {usb_a_room:.1f} mm")
    hole = f"{POWER_HOLE_W:.1f} x {POWER_HOLE_H:.1f} mm"
    print(f"  power hole: x={USBC_X:.1f}, z={POWER_HOLE_Z:.1f}, {hole}")

    if show is not None:
        try:
            show(assembly)
        except Exception as e:  # viewer not running is fine
            print(f"(ocp_vscode viewer not connected: {e})")
