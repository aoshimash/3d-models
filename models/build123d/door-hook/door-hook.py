"""Over-the-door hook that reaches 130 mm clear of a 36 mm door.

One part: a side profile extruded 16 mm wide. Slides down over the top edge of
the door; the arm carries a hanging travel pouch (or anything with a loop or a
swivel hook) out where it hangs free of the door face.

How the load is actually held
-----------------------------
The load hangs 130 mm in front of the door, so the hook wants to tip forward.
It cannot pivot on the door's top face — as it rotates, the bridge underside
lifts off everywhere except right at the door's front top corner, so that corner
is the pivot and takes the whole vertical load. What resists the tipping is a
couple: the **bottom of the front leg** pushing into the door face, and the
**top of the back leg** pushing into the far face. The arm of that couple is the
front leg length, which is why the front leg is 105 mm and the back leg is only
40 mm — length on the back leg buys nothing, length on the front leg is the
whole mechanism.

That geometry also makes the part cheap to build. Hanging the arm off the
*bottom* of the front leg puts the load and the front-leg reaction at the same
height, so their moments very nearly cancel: cut the front leg just under the
bridge and the residual moment is ~200 N.mm, and the bridge sees under
1000 N.mm. Neither is a design driver. Everything is decided by one number —
the moment at the arm root — and that is what ARM_ROOT_DEPTH answers.

Where the load actually sits is the lip's inner face, LIP_THICKNESS back from
the tip: a strap slides outward as the arm deflects and stops there. So the
useful hang point is 121 mm out, and 130 mm is the outside of the lip.

Print orientation is a structural decision
------------------------------------------
The profile is modelled in XY and extruded along Z, which is exactly how it
prints: lying flat, silhouette on the bed, WIDTH becoming the build height.
Every bending stress in the part then runs *along* the extrusion lines inside a
layer, and no load anywhere tries to peel one layer off the next. Print it
standing up instead and the arm root becomes a layer-adhesion joint pulled
straight apart — the one orientation that fails at a fraction of this load.

It also prints without a single overhang: a prism lying on its face is its own
support, and the whole silhouette is bed contact.

Fit and the door
----------------
SLOT_CLEARANCE is 1.0 mm total on a 36.0 mm door, i.e. a snug slide-on. Measure
the door before printing — paint and veneer vary, and this is a hard dimension.
If it is tight, widening SLOT_CLEARANCE costs nothing structurally.

At 8 kg the front leg presses into the door face with ~97 N and the door's front
top corner carries the full 78 N over a few square millimetres. That will mark
soft paint. A felt pad on the front leg's lower inside face and one in the slot
corner are worth the trouble on a door you care about.

Print notes
-----------
- 172 x 113 mm footprint, 16 mm tall. That is 172 mm on a 180 mm bed — it fits,
  with room for a 3 mm brim, but nothing more. Centre it and check the plate.
- 5 perimeters, 50 % infill, 0.2 mm layers. The outer 2 mm shell is what carries
  the bending; infill below ~40 % starts to cost real section.
- Brim recommended. Not for warp — the bed contact is enormous — but a 172 mm
  span has long ends and a lifted corner here is a failed 4-hour print.
- PLA is fine indoors and stiffer than PETG. It does creep under a permanent
  load, so a bag left hanging for months will take a small set; and it softens
  in a hot sunlit room. PETG if either bothers you.
- 66 cm3 of geometry — roughly 60 g of PLA at 5 perimeters and 50 % infill.
"""

from pathlib import Path

from build123d import (
    Axis,
    BuildLine,
    BuildPart,
    BuildSketch,
    Polyline,
    chamfer,
    export_stl,
    extrude,
    fillet,
    make_face,
)

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- The specification (mm / kg) ---
DOOR_THICKNESS = 36.0  # measured door thickness
ARM_REACH = 130.0  # door front face to the outside of the tip lip
DESIGN_LOAD_KG = 8.0  # loaded pouch — sizes the arm root

# --- Straddle over the door top (mm) ---
SLOT_CLEARANCE = 1.0  # total slop across the slot — snug slide-on fit
BRIDGE_THICKNESS = 8.0  # material over the door's top edge
BACK_LEG_THICKNESS = 5.0  # far side of the door — carries the couple, not bending
BACK_LEG_LENGTH = 40.0  # only has to reach past the top corner and stay put
FRONT_LEG_THICKNESS = 10.0  # sized for stiffness, not stress
FRONT_LEG_LENGTH = 105.0  # the couple arm — the single most useful dimension here

# --- Arm (mm) ---
WIDTH = 16.0  # extrusion depth = print height; also the strap's bearing width
ARM_ROOT_DEPTH = 26.0  # section at the front leg, where the moment peaks
ARM_TIP_DEPTH = 12.0  # section at the tip, where it does not
LIP_THICKNESS = 9.0  # upturn at the tip — the strap rests against its inner face
LIP_HEIGHT = 22.0  # above the arm's top surface

# --- Detailing (mm) ---
ARM_ROOT_FILLET = 8.0  # inside corner of the hook — the one real stress riser
LIP_ROOT_FILLET = 5.0  # inside corner at the lip
ARM_UNDER_FILLET = 5.0  # arm underside into the front leg's bottom face
DOOR_CORNER_FILLET = 3.0  # slot corners — relief, and stops the part biting the door
DOOR_CONTACT_FILLET = 3.0  # front leg's bottom inside edge, which presses the door
LEAD_IN_FILLET = 2.0  # back leg tip — guides the hook onto the door; both corners
OUTER_FILLET = 4.0  # exposed convex corners
EDGE_CHAMFER = 0.8  # breaks both flat faces, hides elephant foot on the bed side

OUTPUT_DIR = Path(__file__).parent / "output"


# --- Derived geometry ---
SLOT_WIDTH = DOOR_THICKNESS + SLOT_CLEARANCE
BACK_X = -(SLOT_WIDTH + BACK_LEG_THICKNESS)  # outside face of the back leg
ARM_TOP_Y = -(FRONT_LEG_LENGTH - ARM_ROOT_DEPTH)  # the surface a strap sits on
ARM_TIP_BOTTOM_Y = ARM_TOP_Y - ARM_TIP_DEPTH
LIP_INNER_X = ARM_REACH - LIP_THICKNESS
HANG_X = LIP_INNER_X  # where a strap actually ends up

# --- Load path, for the printed summary ---
LOAD_N = DESIGN_LOAD_KG * 9.81
# Tipping about the door's front top corner, resisted by the front-leg/back-leg
# couple over FRONT_LEG_LENGTH. This is the force squeezing the door.
SQUEEZE_N = LOAD_N * HANG_X / FRONT_LEG_LENGTH
ROOT_MOMENT = LOAD_N * (HANG_X - FRONT_LEG_THICKNESS)
ROOT_MODULUS = WIDTH * ARM_ROOT_DEPTH**2 / 6
ROOT_STRESS = ROOT_MOMENT / ROOT_MODULUS
PROFILE_LENGTH = ARM_REACH - BACK_X
PROFILE_HEIGHT = BRIDGE_THICKNESS + FRONT_LEG_LENGTH

assert ARM_ROOT_DEPTH < FRONT_LEG_LENGTH, "arm root deeper than the leg it hangs from"
assert ARM_TIP_DEPTH < ARM_ROOT_DEPTH, "arm must taper toward the tip"
assert LIP_INNER_X > FRONT_LEG_THICKNESS + ARM_ROOT_FILLET, "no usable hook opening"
assert ARM_ROOT_FILLET < ARM_ROOT_DEPTH, "root fillet eats the root section"
# Both lead-ins land on the back leg's 5 mm end face and have to share it.
assert 2 * LEAD_IN_FILLET < BACK_LEG_THICKNESS, "lead-in fillets overrun the back leg tip"
assert PROFILE_LENGTH <= 180.0, "profile does not fit the A1 Mini bed"
assert ROOT_STRESS < 20.0, "arm root over the working stress for printed PLA"


# ---------------------------------------------------------------------------
# Side profile — clockwise from the back leg's bottom outside corner.
# X runs away from the door, Y is up, the door's top front corner is the origin.
# ---------------------------------------------------------------------------
PROFILE = [
    (BACK_X, -BACK_LEG_LENGTH),  # back leg, bottom outside
    (BACK_X, BRIDGE_THICKNESS),  # up the back face
    (FRONT_LEG_THICKNESS, BRIDGE_THICKNESS),  # across the top of the bridge
    (FRONT_LEG_THICKNESS, ARM_TOP_Y),  # down the front leg's outside face
    (LIP_INNER_X, ARM_TOP_Y),  # along the arm's top surface
    (LIP_INNER_X, ARM_TOP_Y + LIP_HEIGHT),  # up the inside of the lip
    (ARM_REACH, ARM_TOP_Y + LIP_HEIGHT),  # over the top of the lip
    (ARM_REACH, ARM_TIP_BOTTOM_Y),  # down the outside of the lip
    (FRONT_LEG_THICKNESS, -FRONT_LEG_LENGTH),  # tapered underside, back to the root
    (0.0, -FRONT_LEG_LENGTH),  # front leg, bottom face
    (0.0, 0.0),  # up the door's front face
    (-SLOT_WIDTH, 0.0),  # across the slot ceiling
    (-SLOT_WIDTH, -BACK_LEG_LENGTH),  # down the back leg's inside face
]

# (vertex, radius) — keyed on the point above, so the two lists stay readable.
PROFILE_FILLETS = [
    (PROFILE[0], LEAD_IN_FILLET),
    (PROFILE[1], OUTER_FILLET),
    (PROFILE[2], OUTER_FILLET),
    (PROFILE[3], ARM_ROOT_FILLET),
    (PROFILE[4], LIP_ROOT_FILLET),
    (PROFILE[5], 2.0),
    (PROFILE[6], OUTER_FILLET),
    (PROFILE[7], OUTER_FILLET),
    (PROFILE[8], ARM_UNDER_FILLET),
    (PROFILE[9], DOOR_CONTACT_FILLET),
    (PROFILE[10], DOOR_CORNER_FILLET),
    (PROFILE[11], DOOR_CORNER_FILLET),
    (PROFILE[12], LEAD_IN_FILLET),
]


with BuildPart() as hook:
    with BuildSketch() as profile:
        with BuildLine():
            Polyline(*PROFILE, close=True)
        make_face()
        # One at a time: each fillet consumes its corner, so the surviving
        # vertices have to be re-selected against the current sketch.
        for (px, py), radius in PROFILE_FILLETS:
            fillet(profile.vertices().sort_by_distance((px, py, 0))[0], radius=radius)

    extrude(amount=WIDTH)

    # Both flat faces — the bed side and the top side of the printed prism.
    chamfer(hook.faces().filter_by(Axis.Z).edges(), length=EDGE_CHAMFER)


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
path = OUTPUT_DIR / "door-hook.stl"
export_stl(hook.part, str(path))
print(f"Exported: {path}")

print(f"  door slot:  {SLOT_WIDTH:.1f} mm for a {DOOR_THICKNESS:.1f} mm door")
print(f"  reach:      {ARM_REACH:.0f} mm to the tip, {HANG_X:.0f} mm to the hang point")
print(f"  opening:    {HANG_X - FRONT_LEG_THICKNESS:.0f} mm long, {LIP_HEIGHT:.0f} mm lip")
print(f"  footprint:  {PROFILE_LENGTH:.0f} x {PROFILE_HEIGHT:.0f} x {WIDTH:.0f} mm")
print(f"  at {DESIGN_LOAD_KG:.0f} kg ({LOAD_N:.0f} N):")
print(f"    squeeze on the door   {SQUEEZE_N:.0f} N")
print(f"    arm root moment       {ROOT_MOMENT:.0f} N.mm")
print(f"    arm root bending      {ROOT_STRESS:.1f} MPa (working limit ~20 for PLA)")
print(f"    volume                {hook.part.volume / 1000:.0f} cm3 solid")

if show is not None:
    try:
        show(hook.part)
    except Exception as e:  # viewer not running is fine
        print(f"(ocp_vscode viewer not connected: {e})")
