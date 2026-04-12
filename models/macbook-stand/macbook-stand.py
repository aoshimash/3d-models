"""Side rail for dual MacBook Pro 13-inch shelf stand.

Print 2 copies (left and right are identical).
Place one rail against each side wall of the shelf.
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

Recommended print: body wall flat on bed, 58mm print height, no supports needed.
"""

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
rail_depth = 178.0  # mm - rail depth (< max_print; MacBook overhangs front 42mm)
top_ext = 8.0  # mm - body wall extending above upper ledge top surface
fit_tol = 0.2  # mm - general sliding fit tolerance

# === Ventilation slots (cut through base foot area) ===
vent_w = 4.0  # mm - slot width
vent_pitch = 12.0  # mm - slot center-to-center spacing
vent_margin_x = 8.0  # mm - inset from body inner face and ledge edge
vent_margin_z = 6.0  # mm - inset from front and back of rail

# === Derived dimensions ===
base_h = foot_h + ledge_t  # 15 mm - total base section height
upper_z = base_h + mb_thickness + air_gap  # 73 mm - bottom of upper ledge
rail_h = upper_z + ledge_t + top_ext  # 86 mm - total rail height

# === Validation ===
assert rail_depth <= max_print, f"Rail depth {rail_depth} exceeds build volume {max_print}"
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

result = cq.Workplane("XY").moveTo(*pts[0]).polyline(pts[1:]).close().extrude(rail_depth)

# === Cut ventilation slots through foot area of base ===
# Slots run front-to-back (Z direction), only through foot area (z=0 to foot_h)
# Lower ledge surface (foot_h to base_h) stays solid for stable MacBook seating
slot_x_start = body_t + vent_margin_x
slot_x_end = body_t + ledge_w - vent_margin_x
slot_z_len = rail_depth - 2 * vent_margin_z

cx = slot_x_start
while cx + vent_w / 2 <= slot_x_end:
    result = result.cut(
        cq.Workplane("XY")
        .transformed(offset=(cx, foot_h / 2, rail_depth / 2))
        .box(vent_w, foot_h + 0.2, slot_z_len)
    )
    cx += vent_pitch

# === Export ===
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
stl_path = output_dir / "macbook-stand.stl"
result.export(str(stl_path))

try:
    show_object(result)  # type: ignore[name-defined]
except NameError:
    pass

print(f"Rail size: {body_t + ledge_w:.0f} x {rail_depth:.0f} x {rail_h:.0f} mm")
print(f"MacBook front overhang: {mb_depth - rail_depth:.0f} mm (grab point)")
print(f"USB-C side clearance: {(shelf_width - mb_width) / 2 - body_t:.0f} mm per side")
print(f"Ceiling clearance: {shelf_height - (upper_z + ledge_t + mb_thickness):.0f} mm")
print(f"Exported: {stl_path}")
