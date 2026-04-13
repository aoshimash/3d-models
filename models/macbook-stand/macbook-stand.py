"""Side rail for dual MacBook Pro 13-inch shelf stand (two-part with diagonal tenon).

Print 2 copies of each part (4 total: 2 front, 2 back).
Assembly: push the two halves together at a 15-degree angle (forward + toward wall).
The diagonal tenon locks both X and Z axes without glue.
Place one assembled rail against each side wall of the shelf.
MacBooks slide in horizontally from the front, resting on the ledges.

Cross-section (front view, one rail shown):

    A----B
    |    |
    |    C-------D     upper ledge (upper MacBook sits here)
    |    |       |
    |    |       E
    |    |     /F      gusset (structural + print-friendly overhang)
    |    |   /
    |    G
    |    |
    |    H-------I     lower ledge / base top (lower MacBook sits here)
    |    |       |
    K-----------J      base bottom (vent slots cut here)

Joint mechanism (front view, two tenons at same angle):

    ┌──┐                      ┌──┐
    │  │  upper tenon (4mm)   │  │  Y=75.5 (upper ledge)
    │  C=======D  ╱           │  │
    │  │       │╱             │  │
    │  │                      │  │
    │  │  ~65mm separation    │  │  (twist resistance)
    │  │                      │  │
    │  H=======I  ╱           │  │
    │  │       │╱             │  │
    K-----------J             │  │  Y=7.5 (base)
        base tenon (10mm)

    Both tenons tilted 15 degrees in X-Z plane (same angle).
    Assembly: single push at 15 degrees (forward + toward wall).
    Two anchor points prevent twisting around any axis.

Recommended print: body wall flat on bed, 58mm print height, no supports needed.
"""

import math
from pathlib import Path

import cadquery as cq

# === MacBook Pro 13" ===
mb_width = 313.0  # mm - body width
mb_depth = 220.0  # mm - body depth
mb_thickness = 18.0  # mm - closed-lid thickness

# === Shelf interior (3 walls + ceiling, front open) ===
shelf_width = 385.0  # mm - internal width
shelf_depth = 261.0  # mm - internal depth
shelf_height = 135.0  # mm - internal height

# === Print constraints (Bambu Lab A1 Mini) ===
max_print = 180.0  # mm - build volume per axis

# === Design parameters ===
body_t = 8.0  # mm - body wall thickness (structural spine against shelf wall)
ledge_w = 50.0  # mm - ledge extending inward from body (MacBook support)
ledge_t = 5.0  # mm - ledge platform thickness
foot_h = 10.0  # mm - base foot height (airflow channel under lower MacBook)
air_gap = 40.0  # mm - gap between MacBooks (ventilation + finger access for removal)
gusset_reach = 15.0  # mm - gusset extent along upper ledge underside
gusset_drop = 20.0  # mm - gusset vertical drop below upper ledge
rail_depth = 258.0  # mm - total rail depth (178 original + 80mm extension)
top_ext = 8.0  # mm - body wall extending above upper ledge top surface
fit_tol = 0.2  # mm - general sliding fit tolerance

# === Diagonal tenon joint parameters ===
tenon_angle = 15.0  # degrees - tenon tilt from Z axis toward +X (locks X and Z axes)
tenon_length = 12.0  # mm - tenon length along its tilted axis
tenon_width = 40.0  # mm - tenon width in X direction
tenon_taper = 0.3  # mm - groove narrows by this much from entry to deep end (wedge)
tenon_tol_entry = 0.20  # mm - clearance per side at entry (loose, easy start)
tenon_tol_deep = 0.10  # mm - clearance per side at deep end (tight, friction lock)
tenon_h_base = 10.0  # mm - base tenon height (fits in 15mm base section)
tenon_h_upper = 4.0  # mm - upper tenon height (fits in 5mm upper ledge section)

# === Ventilation slots (cut through base foot area) ===
vent_w = 4.0  # mm - slot width
vent_pitch = 12.0  # mm - slot center-to-center spacing
vent_margin_x = 8.0  # mm - inset from body inner face and ledge edge
vent_margin_z = 6.0  # mm - inset from front and back of rail

# === Derived dimensions ===
base_h = foot_h + ledge_t  # 15 mm - total base section height
upper_z = base_h + mb_thickness + air_gap  # 73 mm - bottom of upper ledge
rail_h = upper_z + ledge_t + top_ext  # 86 mm - total rail height
z_split = rail_depth / 2  # 129 mm - split point (equal halves)

# Tenon extent in global coordinates
tenon_z_extent = tenon_length * math.cos(math.radians(tenon_angle))  # Z projection
tenon_x_extent = tenon_length * math.sin(math.radians(tenon_angle))  # X projection

# === Validation ===
part_max_z = z_split + tenon_z_extent + (tenon_width / 2) * math.sin(math.radians(tenon_angle))
assert part_max_z <= max_print, f"Part depth {part_max_z:.1f} exceeds build volume {max_print}"
assert rail_h <= max_print, f"Rail height {rail_h} exceeds build volume {max_print}"
assert body_t + ledge_w <= max_print, f"Rail width {body_t + ledge_w} exceeds build volume"
assert rail_h < shelf_height, f"Rail height {rail_h} exceeds shelf height {shelf_height}"
assert upper_z - gusset_drop > base_h, "Gusset overlaps base section"

# === Build cross-section profile ===
# Coordinate system: X = width (outer wall -> ledge), Y = height (base -> top)
# Extrude along Z = depth (back -> front)

pts = [
    (0, rail_h),  # A: outer top
    (body_t, rail_h),  # B: inner top
    (body_t, upper_z + ledge_t),  # C: body at upper ledge top
    (body_t + ledge_w, upper_z + ledge_t),  # D: upper ledge tip, top
    (body_t + ledge_w, upper_z),  # E: upper ledge tip, bottom
    (body_t + gusset_reach, upper_z),  # F: gusset start on ledge underside
    (body_t, upper_z - gusset_drop),  # G: gusset end on body
    (body_t, base_h),  # H: body at base top / lower ledge surface
    (body_t + ledge_w, base_h),  # I: base top, ledge tip
    (body_t + ledge_w, 0),  # J: base bottom, outer edge
    (0, 0),  # K: outer bottom
]

full_rail = cq.Workplane("XY").moveTo(*pts[0]).polyline(pts[1:]).close().extrude(rail_depth)

# === Cut ventilation slots through foot area of base ===
slot_x_start = body_t + vent_margin_x
slot_x_end = body_t + ledge_w - vent_margin_x
slot_z_len = rail_depth - 2 * vent_margin_z

cx = slot_x_start
while cx + vent_w / 2 <= slot_x_end:
    full_rail = full_rail.cut(
        cq.Workplane("XY")
        .transformed(offset=(cx, foot_h / 2, rail_depth / 2))
        .box(vent_w, foot_h + 0.2, slot_z_len)
    )
    cx += vent_pitch

# === Diagonal tenon joint ===
# Two tenons: one in the base section, one in the upper ledge section.
# Both tilted 15 degrees from Z toward +X (same angle = single assembly motion).
# Separated by ~65mm vertically for maximum twist resistance.
# Lock: diagonal geometry prevents pure X or Z separation (primary forces).
# Wedge: groove tapers more than tongue, creating progressive tightening.
# Y axis: constrained by rectangular cross-section of tenon/groove.

margin = 2.0  # mm - bounding box overshoot for clean boolean ops
bb_w = body_t + ledge_w + 2 * margin
bb_h = rail_h + 2 * margin
bb_cx = (body_t + ledge_w) / 2
bb_cy = rail_h / 2

# Tenon X center (shared): middle of the full-width sections
tenon_cx = (body_t + ledge_w) / 2

# Tenon positions: base section and upper ledge section
tenon_positions = [
    (tenon_cy_base := base_h / 2, tenon_h_base),  # Y=7.5, h=10
    (tenon_cy_upper := upper_z + ledge_t / 2, tenon_h_upper),  # Y=75.5, h=4
]


def make_tenon_pair(cy, th):
    """Create tongue (undersized) and groove (nominal) for one tenon position."""
    tongue = (
        cq.Workplane("XY")
        .transformed(offset=(tenon_cx, cy, z_split), rotate=(0, tenon_angle, 0))
        .rect(tenon_width - 2 * tenon_tol_entry, th - 2 * tenon_tol_entry)
        .workplane(offset=tenon_length - tenon_tol_entry)
        .rect(
            tenon_width - tenon_taper - 2 * tenon_tol_deep,
            th - tenon_taper - 2 * tenon_tol_deep,
        )
        .loft()
    )
    groove = (
        cq.Workplane("XY")
        .transformed(offset=(tenon_cx, cy, z_split), rotate=(0, tenon_angle, 0))
        .rect(tenon_width, th)
        .workplane(offset=tenon_length)
        .rect(tenon_width - tenon_taper, th - tenon_taper)
        .loft()
    )
    return tongue, groove


# === Split rail into two parts ===
front_box = (
    cq.Workplane("XY").transformed(offset=(bb_cx, bb_cy, z_split / 2)).box(bb_w, bb_h, z_split)
)
back_box = (
    cq.Workplane("XY")
    .transformed(offset=(bb_cx, bb_cy, z_split + (rail_depth - z_split) / 2))
    .box(bb_w, bb_h, rail_depth - z_split)
)

front_cutter = front_box
back_cutter = back_box

for cy, th in tenon_positions:
    tongue, groove = make_tenon_pair(cy, th)
    front_cutter = front_cutter.union(tongue)
    back_cutter = back_cutter.cut(groove)

# Part A: front half + tongue protrusions
part_front = full_rail.intersect(front_cutter)

# Part B: back half - groove pockets
part_back = full_rail.intersect(back_cutter)

# === Export ===
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

front_path = output_dir / "macbook-stand-front.stl"
back_path = output_dir / "macbook-stand-back.stl"
part_front.export(str(front_path))
part_back.export(str(back_path))

try:
    show_object(part_front, name="front")  # type: ignore[name-defined]
    show_object(part_back, name="back")  # type: ignore[name-defined]
except NameError:
    pass

print(f"Total rail: {body_t + ledge_w:.0f} x {rail_depth:.0f} x {rail_h:.0f} mm")
print(f"Split at Z={z_split:.0f} mm")
print(f"Base tenon: {tenon_width:.0f}x{tenon_h_base:.0f} mm at Y={tenon_cy_base:.1f}")
print(f"Upper tenon: {tenon_width:.0f}x{tenon_h_upper:.0f} mm at Y={tenon_cy_upper:.1f}")
print(f"Tenon L={tenon_length:.0f} mm, angle={tenon_angle:.0f} deg")
print(f"Tenon taper: {tenon_taper:.1f} mm (progressive wedge)")
print(f"Clearance: {tenon_tol_entry:.2f} mm (entry) -> {tenon_tol_deep:.2f} mm (deep)")
print(f"Each part max depth: {part_max_z:.0f} mm (limit: {max_print:.0f} mm)")
print(f"MacBook front overhang: {mb_depth - rail_depth:.0f} mm (grab point)")
print(f"USB-C side clearance: {(shelf_width - mb_width) / 2 - body_t:.0f} mm per side")
print(f"Ceiling clearance: {shelf_height - (upper_z + ledge_t + mb_thickness):.0f} mm")
print(f"Exported: {front_path}")
print(f"Exported: {back_path}")
