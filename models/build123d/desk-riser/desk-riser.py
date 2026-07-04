"""Desk-leg riser — lifts a desk by 100 mm.

One riser sits under each of the four desk legs (print 4 copies).
Each leg ends in a 34 mm diameter cylindrical foot that drops into a
recessed socket on top of the riser, so the desk cannot slide off.

The body is a truncated cone: an 80 mm footprint at the floor tapering
to 48 mm at the top. Tip-over resistance scales with base radius
(F_tip = load x base_radius / height), so the wide base is what keeps
the riser upright when the desk is pushed sideways.
Because the leg sinks SOCKET_DEPTH into the riser, the overall height
is RAISE_HEIGHT + SOCKET_DEPTH so the effective lift is exactly 100 mm.

Print notes
-----------
- Orientation: base down, socket opening up. The outer wall tapers
  inward going up, so there are no overhangs — no supports needed.
- All 4 copies fit on one A1 Mini plate (2 x 2 of 80 mm circles = 160 mm
  square, inside the 180 mm bed).
- Load is pure compression; 4-5 perimeters + 25-30 % infill is plenty
  for furniture weight.
- Layer height: 0.2 mm.

Fit test
--------
desk-riser-fit-test.stl is the top 15 mm of the exact same body
(socket + 5 mm floor), sliced off with a plane. Print it first to
verify the socket fits the leg, tune FIT_TOLERANCE if needed, then
print the 4 full risers.

desk-riser-tolerance-gauge.stl holds four gauge rings with per-side
clearances of 0.6 / 0.8 / 1.0 / 1.2 mm (0.2 and 0.4 both failed on
real prints). Notch count on the outer wall identifies the ring:
1 notch = 0.6 mm ... 4 notches = 1.2 mm. Set FIT_TOLERANCE to the
smallest clearance whose ring drops fully onto the leg.

Measured result: the 4-notch (1.2 mm) ring was the one that seated
fully — FIT_TOLERANCE is set from that sweep.
"""

import math
from pathlib import Path

from build123d import (
    Align,
    Axis,
    BuildPart,
    Compound,
    Cone,
    Cylinder,
    Keep,
    Location,
    Locations,
    Mode,
    Part,
    Plane,
    SortBy,
    chamfer,
    export_stl,
    split,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Desk leg (measured) ---
LEG_DIAMETER = 34.0  # mm - nominal leg foot diameter (user-measured, ~cm precision)
FIT_TOLERANCE = 1.2  # mm - clearance per side, settled by the gauge-ring sweep:
#                      the 4-notch (1.2 mm) ring was the smallest that seated
#                      fully on the real leg; 0.2 / 0.4 / smaller rings did not

# --- Riser body (mm) ---
RAISE_HEIGHT = 100.0  # effective lift: floor to socket floor
SOCKET_DEPTH = 10.0  # recess depth — enough to keep the foot captive
TOTAL_HEIGHT = RAISE_HEIGHT + SOCKET_DEPTH  # overall riser height (110)
BASE_DIAMETER = 80.0  # floor footprint — wide for tip-over stability
TOP_DIAMETER = 48.0  # top face — leaves a thick wall around the socket

SOCKET_DIAMETER = LEG_DIAMETER + 2 * FIT_TOLERANCE  # socket bore (36.4)

# --- Edge treatment (mm) ---
SOCKET_LEAD_IN = 1.5  # chamfer at the socket rim, guides the leg in
BOTTOM_CHAMFER = 0.5  # counteracts first-layer elephant foot

# --- Fit-test piece (mm) ---
FIT_TEST_FLOOR = 5.0  # material kept under the socket in the test print
FIT_TEST_CUT_Z = TOTAL_HEIGHT - SOCKET_DEPTH - FIT_TEST_FLOOR  # slice plane (95)

# --- Tolerance gauge rings (mm) ---
GAUGE_CLEARANCES = [0.6, 0.8, 1.0, 1.2]  # per-side candidates; ring i+1 notches
GAUGE_WALL = 5.0  # wall around the largest gauge bore
GAUGE_FLOOR = 2.0  # thin floor under each gauge socket
GAUGE_OUTER = LEG_DIAMETER + 2 * GAUGE_CLEARANCES[-1] + 2 * GAUGE_WALL  # 46.4
GAUGE_HEIGHT = GAUGE_FLOOR + SOCKET_DEPTH  # 12
GAUGE_PITCH = 50.0  # 2x2 grid spacing between ring centres
NOTCH_DIAMETER = 3.0  # ID groove bitten into the outer wall
NOTCH_SPACING_DEG = 12.0  # angular gap between adjacent notches

# --- Sanity checks ---
assert TOTAL_HEIGHT <= 180.0, "Exceeds A1 Mini build Z (180 mm)"
assert (TOP_DIAMETER - SOCKET_DIAMETER) / 2 >= 1.2, "Socket wall too thin"
assert SOCKET_LEAD_IN < (TOP_DIAMETER - SOCKET_DIAMETER) / 2
assert 0 < FIT_TEST_CUT_Z < TOTAL_HEIGHT - SOCKET_DEPTH

OUTPUT_DIR = Path(__file__).parent / "output"


def build_riser() -> BuildPart:
    """Build the single riser shape."""
    with BuildPart() as riser:
        # --- Tapered body ---
        Cone(
            bottom_radius=BASE_DIAMETER / 2,
            top_radius=TOP_DIAMETER / 2,
            height=TOTAL_HEIGHT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

        # --- Leg socket (subtract, blind hole from the top face) ---
        with Locations((0, 0, TOTAL_HEIGHT)):
            Cylinder(
                radius=SOCKET_DIAMETER / 2,
                height=SOCKET_DEPTH,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
                mode=Mode.SUBTRACT,
            )

        # --- Socket lead-in chamfer ---
        # The top face holds two circular edges: the outer rim and the
        # socket rim. The socket rim is the smaller radius.
        top_edges = riser.edges().group_by(Axis.Z)[-1]
        socket_rim = top_edges.sort_by(SortBy.RADIUS)[0]
        chamfer(socket_rim, length=SOCKET_LEAD_IN)

        # --- Bottom edge chamfer (elephant-foot compensation) ---
        bottom_rim = riser.edges().group_by(Axis.Z)[0]
        chamfer(bottom_rim, length=BOTTOM_CHAMFER)

    return riser


def build_fit_test(riser: BuildPart) -> Part:
    """Slice the socket end off the full riser and drop it onto Z=0.

    Splitting the finished body (rather than remodelling a short stub)
    guarantees the test print shares the exact socket geometry —
    tolerance, lead-in chamfer and outer taper included.
    """
    top = split(
        objects=riser.part,
        bisect_by=Plane.XY.offset(FIT_TEST_CUT_Z),
        keep=Keep.TOP,
    )
    return top.moved(Location((0, 0, -FIT_TEST_CUT_Z)))


def build_gauge_ring(clearance: float, notches: int) -> Part:
    """One gauge ring: the riser's socket geometry at a candidate clearance.

    The bore, depth and lead-in chamfer match the real riser socket, so
    whichever ring drops fully onto the leg is exactly how the final
    print will fit. Vertical notch grooves on the outer wall identify
    the ring (1 notch = smallest clearance).
    """
    bore = LEG_DIAMETER + 2 * clearance
    with BuildPart() as ring:
        Cylinder(
            radius=GAUGE_OUTER / 2,
            height=GAUGE_HEIGHT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        with Locations((0, 0, GAUGE_HEIGHT)):
            Cylinder(
                radius=bore / 2,
                height=SOCKET_DEPTH,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
                mode=Mode.SUBTRACT,
            )
        top_edges = ring.edges().group_by(Axis.Z)[-1]
        chamfer(top_edges.sort_by(SortBy.RADIUS)[0], length=SOCKET_LEAD_IN)
        # ID notches: vertical grooves centred on the outer surface
        notch_locs = []
        for i in range(notches):
            angle = math.radians(i * NOTCH_SPACING_DEG)
            notch_locs.append(
                (
                    GAUGE_OUTER / 2 * math.cos(angle),
                    GAUGE_OUTER / 2 * math.sin(angle),
                    GAUGE_HEIGHT / 2,
                )
            )
        with Locations(*notch_locs):
            Cylinder(
                radius=NOTCH_DIAMETER / 2,
                height=GAUGE_HEIGHT,
                mode=Mode.SUBTRACT,
            )
    return ring.part


def build_gauge() -> Compound:
    """All gauge rings arranged in a 2 x 2 grid for a single print."""
    rings = []
    for i, clearance in enumerate(GAUGE_CLEARANCES):
        col, row = i % 2, i // 2
        offset = (
            (col - 0.5) * GAUGE_PITCH,
            (row - 0.5) * GAUGE_PITCH,
            0,
        )
        rings.append(build_gauge_ring(clearance, i + 1).moved(Location(offset)))
    return Compound(children=rings)


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
riser_part = build_riser()
export_stl(riser_part.part, str(OUTPUT_DIR / "desk-riser.stl"))
print(f"Exported: {OUTPUT_DIR / 'desk-riser.stl'}")
fit_test_part = build_fit_test(riser_part)
export_stl(fit_test_part, str(OUTPUT_DIR / "desk-riser-fit-test.stl"))
print(f"Exported: {OUTPUT_DIR / 'desk-riser-fit-test.stl'}")
gauge_part = build_gauge()
export_stl(gauge_part, str(OUTPUT_DIR / "desk-riser-tolerance-gauge.stl"))
print(f"Exported: {OUTPUT_DIR / 'desk-riser-tolerance-gauge.stl'}")

if show is not None:
    try:
        show(riser_part.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
