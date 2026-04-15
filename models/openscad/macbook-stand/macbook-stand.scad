// MacBook Stand - Full dual-MacBook design using v1 CadQuery dimensions.
// Two rails (台) connected by bridges (橋) with dovetail joints.
//
// Coordinate system:
//   X: perpendicular to rails, spans between them
//   Y: vertical (height)
//   Z: along rail length (MacBook depth direction)
//
// Structure:
//   - 2 rails with full v1 profile (base + lower ledge + gusset + upper ledge + top)
//   - Multiple bridges at 2 Y levels (lower and upper ledges)
//   - Bridges slide down into dovetail slots from above
//
// NOTE: rail_depth=258mm exceeds build volume (180mm). Splitting will be
//       addressed in a later step.

include <BOSL2/std.scad>

// ============================================================
// Parameters (v1 CadQuery dimensions)
// ============================================================

// --- MacBook Pro 13" ---
mb_width     = 313;   // mm - body width
mb_depth     = 220;   // mm - body depth
mb_thickness = 18;    // mm - closed-lid thickness

// --- Print constraints (Bambu Lab A1 Mini) ---
max_print = 180;      // mm - build volume per axis

// --- Rail cross-section ---
body_t       = 8;     // mm - body wall thickness
ledge_w      = 50;    // mm - ledge width (extending inward from body)
ledge_t      = 12;    // mm - ledge platform thickness (increased from v1 8mm
                      //   to leave floor below bridge slot for tongue support)
foot_h       = 10;    // mm - base foot height (under lower ledge)
air_gap      = 40;    // mm - vertical gap between the two MacBooks
gusset_reach = 15;    // mm - gusset extent on upper ledge underside
gusset_drop  = 20;    // mm - gusset vertical drop below upper ledge
rail_depth   = 258;   // mm - rail length (Z direction)
top_ext      = 8;     // mm - body wall extent above upper ledge
inner_gap    = 230;   // mm - distance between rail body wall inner faces

// --- Bridge dovetail (ledge joint, fits inside ledge_t) ---
dt_width   = 14;      // mm - narrow width (Z, along rail depth)
dt_depth   = 5;       // mm - taper depth (X, into rail)
dt_inset   = 4;       // mm - rectangular channel before taper
dt_angle   = 25;      // degrees - flare angle (steep for pronounced barb)


// --- Body-wall dovetail (rail front/back split joint) ---
// Two dovetails (upper + lower) on the split face, horizontal Z-slide assembly.
// Front half has tongues protruding in +Z; back half has matching slots.
bw_dt_width_narrow = 10;   // mm - narrow Y width at entry (split face)
bw_dt_depth        = 4;    // mm - taper depth (Z, into back half)
bw_dt_inset        = 3;    // mm - rectangular channel before taper
bw_dt_angle        = 14;   // degrees
bw_dt_height       = body_t;  // mm - X extent (full body wall thickness; tongue shows on outer face)
bw_dt_upper_y      = 70;   // mm - Y center of upper dovetail
bw_dt_lower_y      = 25;   // mm - Y center of lower dovetail

// --- Bridge ---
bridge_bar_width_z = dt_width;  // mm - bar width (Z) unified with tongue entry width

// --- Bridge slot floor (below dovetail slot) ---
slot_floor = 2;       // mm - ledge material below slot to support bridge tongue

// --- Body wall ventilation holes (hex grid) ---
// Punched through the body wall for airflow + material savings + print time.
hole_d               = 6;    // mm - hole diameter
hole_pitch           = 10;   // mm - hex grid center-to-center spacing
hole_margin_y        = 3;    // mm - Y clearance from ledges/gusset/edges
hole_margin_z        = 6;    // mm - Z clearance from rail front/back ends
hole_split_clearance = 15;   // mm - Z clearance around split_z (protect body-wall dovetail)

// --- Foot ventilation slots ---
// Long slots through the foot along Z axis, providing airflow under lower
// MacBook and material savings. Split at Z=split_z with solid bridge zone.
vent_w         = 8;    // mm - slot width (X direction)
vent_pitch     = 12;   // mm - slot center-to-center spacing in X
vent_margin_x  = 8;    // mm - X clearance from body wall and ledge tip
vent_margin_z  = 6;    // mm - Z clearance from rail front/back ends
vent_bridge_z  = 30;   // mm - solid zone around split_z (protects body-wall dovetail)

// --- Airflow spacer ribs on body wall inner face ---
// Small ribs protrude inward from body wall inner face, keeping MacBook
// side faces from directly contacting the wall (preserves airflow gap
// even if MacBook shifts laterally).
rib_depth = 2.5;   // mm - protrusion from body wall inner face (+X)
rib_width = 3;     // mm - rib thickness along Z (rail depth direction)
rib_count = 3;     // number of ribs evenly spaced along Z

// --- Split & bridge positions along rail length (Z) ---
split_z            = rail_depth / 2;              // 129mm - rail front/back split
bridge_z_positions = [20, 80, 178, 238];          // 4 bridges per ledge level

// --- Fit tolerance ---
fit_tol = 0.15;       // mm - clearance per side for FDM

// ============================================================
// Derived dimensions
// ============================================================

base_h  = foot_h + ledge_t;                            // 22 (was 18 with ledge_t=8)
upper_z = base_h + mb_thickness + air_gap;             // 80 (was 76)
rail_h  = upper_z + ledge_t + top_ext;                 // 100 (was 92)

bridge_gap     = inner_gap - 2 * ledge_w;              // 130 - gap between ledge tips
dt_total_pen   = dt_inset + dt_depth;                  // 9mm tongue length
dt_width_wide  = dt_width + 2 * dt_depth * tan(dt_angle);  // ~16.5mm
dt_slide       = ledge_t - slot_floor;                 // 10mm (slot depth, leaves 2mm floor)
bridge_total_x = bridge_gap + 2 * dt_total_pen;        // ~148mm bridge total length

// Body-wall dovetail derived
bw_dt_total_pen   = bw_dt_inset + bw_dt_depth;
bw_dt_width_wide  = bw_dt_width_narrow + 2 * bw_dt_depth * tan(bw_dt_angle);
bw_dt_y_positions = [bw_dt_lower_y, bw_dt_upper_y];

// Rail X positions (left rail at X=0..58, right rail mirrored)
left_rail_outer_x = 0;
left_rail_inner_x = body_t + ledge_w;                  // 58 (left ledge tip)
right_rail_inner_x = left_rail_inner_x + bridge_gap;   // 188 (right ledge tip)
right_rail_outer_x = right_rail_inner_x + body_t + ledge_w;  // 246

// Ledge top Y positions
lower_ledge_top = base_h;               // 18
upper_ledge_top = upper_z + ledge_t;    // 84

// ============================================================
// Validation
// ============================================================

assert(bridge_total_x <= max_print,
       str("Bridge X length ", bridge_total_x, " exceeds build volume"));
assert(dt_slide <= ledge_t, "Dovetail slide exceeds ledge thickness");
assert(dt_total_pen < ledge_w, "Dovetail too deep for ledge width");
// rail_depth > max_print - splitting required for actual printing

// ============================================================
// Dovetail profiles
// ============================================================

// Female profile (2D, local XY):
//   local X = depth into rail (0 at surface, negative = deeper)
//   local Y = width along rail depth (Z in world after rotation)
module dt_female_rail_profile() {
    w1 = dt_width + 2 * fit_tol;
    w2 = dt_width_wide + 2 * fit_tol;
    polygon([
        [fit_tol, -w1/2],
        [fit_tol,  w1/2],
        [-dt_inset, w1/2],
        [-(dt_total_pen + fit_tol),  w2/2],
        [-(dt_total_pen + fit_tol), -w2/2],
        [-dt_inset, -w1/2]
    ]);
}

// Male profile (no tolerance) - for bridge tongue
// local X extends in +X (will be mirrored for left-side tongue)
//   local X = depth into rail (0 at bar side, positive = into rail)
//   local Y = width along rail depth
module dt_male_rail_profile() {
    polygon([
        [0, -dt_width/2],
        [0,  dt_width/2],
        [dt_inset,  dt_width/2],
        [dt_total_pen,  dt_width_wide/2],
        [dt_total_pen, -dt_width_wide/2],
        [dt_inset, -dt_width/2]
    ]);
}

// --- Middle bridge (butterfly/chigiri) profiles ---
// Bowtie shape in XY:
//   - Wide Y (= Z in world) at X=0 (entry face) AND at X=dt_total_pen (deep)
//   - Narrow Y at X=middle (waist) = bt_waist_width
// The rail halves straddle this profile. Neither half can move in Z
// because the wide wings (both at entry AND at depth) geometrically
// interfere with the narrow waist — classic butterfly lock.


// ============================================================
// Module: Rail cross-section (2D, in XY plane)
// ============================================================
// Profile matches v1 CadQuery rail shape

module rail_profile() {
    polygon(points=[
        [0, 0],                                  // K: outer bottom
        [body_t + ledge_w, 0],                   // J: base bottom, ledge tip outer
        [body_t + ledge_w, base_h],              // I: base top, lower ledge tip
        [body_t, base_h],                         // H: body at lower ledge
        [body_t, upper_z - gusset_drop],          // G: gusset bottom
        [body_t + gusset_reach, upper_z],         // F: gusset top
        [body_t + ledge_w, upper_z],              // E: upper ledge bottom tip
        [body_t + ledge_w, upper_z + ledge_t],    // D: upper ledge top tip
        [body_t, upper_z + ledge_t],              // C: body at upper ledge top
        [body_t, rail_h],                         // B: inner top
        [0, rail_h],                              // A: outer top
    ]);
}

// ============================================================
// Module: Rail with dovetail slots
// ============================================================

module rail() {
    union() {
        // Spacer ribs added AFTER all cuts (so they aren't cut by holes/vents)
        body_wall_ribs();

    difference() {
        linear_extrude(height = rail_depth)
            rail_profile();

        // Cut dovetail slots on lower ledge and upper ledge
        // Slots open at ledge top, extend downward by dt_slide (NOT all the way
        // through the ledge; leaves slot_floor mm of material below for support).
        // Slot is on inner face (X = body_t + ledge_w), cut in -X direction.
        for (bz = bridge_z_positions) {
            // Lower ledge slot
            translate([body_t + ledge_w, lower_ledge_top + 0.05, bz])
                rotate([90, 0, 0])
                    linear_extrude(height = dt_slide + fit_tol + 0.05)  // top over-cut + bottom clearance
                        dt_female_rail_profile();

            // Upper ledge slot
            translate([body_t + ledge_w, upper_ledge_top + 0.05, bz])
                rotate([90, 0, 0])
                    linear_extrude(height = dt_slide + fit_tol + 0.05)  // top over-cut + bottom clearance
                        dt_female_rail_profile();
        }

        // Body wall hex ventilation holes
        body_wall_holes();

        // Foot ventilation slots (along Z axis)
        foot_vents();
    }
    }  // close union()
}

// ============================================================
// Airflow spacer ribs on body wall inner face
// ============================================================
// Small ribs protruding from the body wall's inner face (+X side),
// keeping the MacBook side face from contacting the wall directly.
// Placed in the between-ledges Y range, evenly spaced along Z.

module body_wall_ribs() {
    rib_y_start = lower_ledge_top;                    // 22
    rib_y_end   = upper_ledge_top;                    // 92
    rib_z_spacing = rail_depth / (rib_count + 1);

    for (i = [1 : rib_count]) {
        z = rib_z_spacing * i;
        translate([body_t, rib_y_start, z - rib_width/2])
            cube([rib_depth, rib_y_end - rib_y_start, rib_width]);
    }
}

// ============================================================
// Body wall ventilation holes (hex grid)
// ============================================================
// Cylinders punched through the body wall (X direction), arranged in a
// hex grid on the YZ face. Skips structural regions (ledges, gusset,
// rail edges) and the split_z zone (protects body-wall dovetail).

module body_wall_holes() {
    hex_row_spacing = hole_pitch * sqrt(3) / 2;
    hole_r = hole_d / 2;

    // Penetrating Y range: only the body wall between lower ledge top and
    // the gusset/upper-ledge region. Outside of this range, the body wall's
    // inner face (X=body_t) is backed by ledge/gusset/foot material, so a hole
    // would be blind (no through-airflow, no material savings).
    y_pen_min = base_h + hole_margin_y;                          // above lower ledge
    y_pen_max = upper_z - gusset_drop - hole_margin_y;           // below gusset

    // Number of rows fitting in penetrating Y span
    n_rows = floor((y_pen_max - y_pen_min) / hex_row_spacing);

    for (row = [0 : n_rows]) {
        y = y_pen_min + hole_r + row * hex_row_spacing;

        if (y + hole_r <= y_pen_max) {
            z_offset = (row % 2 == 1) ? hole_pitch / 2 : 0;
            z_start  = hole_margin_z + hole_r + z_offset;
            z_end    = rail_depth - hole_margin_z - hole_r;

            for (z = [z_start : hole_pitch : z_end]) {
                // Skip zone around split_z (protect body-wall dovetail)
                z_ok = !(z > split_z - hole_split_clearance
                         && z < split_z + hole_split_clearance);
                if (z_ok) {
                    translate([-0.1, y, z])
                        rotate([0, 90, 0])
                            cylinder(h = body_t + 0.2, r = hole_r, $fn = 24);
                }
            }
        }
    }
}

// ============================================================
// Foot ventilation slots (long slots along Z, through foot)
// ============================================================
// Cuts airflow slots through the foot (Y = 0 to foot_h) running along Z.
// Skipped in a zone around Z=split_z to keep that region solid for the
// body-wall dovetail joint. Also keeps margins from body wall / ledge tip
// (so X walls aren't breached) and rail front/back ends.

module foot_vents() {
    x_start = body_t + vent_margin_x;
    x_end   = body_t + ledge_w - vent_margin_x;

    front_z_min = vent_margin_z;
    front_z_max = split_z - vent_bridge_z / 2;
    back_z_min  = split_z + vent_bridge_z / 2;
    back_z_max  = rail_depth - vent_margin_z;

    for (cx = [x_start + vent_w/2 : vent_pitch : x_end - vent_w/2]) {
        if (front_z_max > front_z_min)
            _foot_vent_shape(cx, front_z_min, front_z_max);
        if (back_z_max > back_z_min)
            _foot_vent_shape(cx, back_z_min, back_z_max);
    }
}

// Foot vent with 45° self-supporting top (trapezoid cross-section in XY).
// When printed in orientation A (body-wall outer face X=0 on bed, world X
// is print vertical), the vent's ceiling closes gradually from world Y=10
// side (supported by lower ledge) toward Y=0 side (unsupported), at 45°.
// No bridging needed.
//
// XY polygon:                            Y=10 ┌─────┐
//   rectangle + triangular slope extension       │     │\
//                                                │rect │ \  slope (45°)
//                                                │     │  \
//                                           Y=0  └─────┴───\
//                                                X=16  X=24 X=34
module _foot_vent_shape(cx, z_min, z_max) {
    translate([0, 0, z_min])
        linear_extrude(height = z_max - z_min)
            polygon([
                [cx - vent_w/2,             -0.1],           // bottom-left
                [cx + vent_w/2 + foot_h,    -0.1],           // bottom-right (extended for slope)
                [cx + vent_w/2,              foot_h + 0.1],  // top-right (slope apex)
                [cx - vent_w/2,              foot_h + 0.1]   // top-left
            ]);
}

// ============================================================
// Body-wall dovetail: tongue/slot for rail front/back split
// ============================================================
// Two dovetails (upper + lower) on the body wall at Z=split_z.
// Front half has tongues (male), back half has slots (female).
// Assembly: push front half in +Z direction into back half (horizontal slide).

// 2D profile (local XY):
//   local X = depth (Z in world) - into back half
//   local Y = width (Y in world)
module bw_dt_profile_2d(tol = 0) {
    w1 = bw_dt_width_narrow + 2 * tol;
    w2 = bw_dt_width_wide   + 2 * tol;
    polygon([
        [-tol,                    -w1/2],
        [-tol,                     w1/2],
        [bw_dt_inset,              w1/2],
        [bw_dt_total_pen + tol,    w2/2],
        [bw_dt_total_pen + tol,   -w2/2],
        [bw_dt_inset,             -w1/2]
    ]);
}

// Single body-wall tongue (male), extends from split_z in +Z
// Positioned at Y=y_center, X within body wall
module bw_tongue_single(y_center) {
    translate([body_t, y_center, split_z])
        rotate([0, -90, 0])   // local X → world Z, local Y → world Y, extrude → world -X
            linear_extrude(height = bw_dt_height)
                bw_dt_profile_2d();
}

// Single body-wall slot (female with clearance)
module bw_slot_single(y_center) {
    translate([body_t + fit_tol, y_center, split_z])
        rotate([0, -90, 0])
            linear_extrude(height = bw_dt_height + 2 * fit_tol)
                bw_dt_profile_2d(tol = fit_tol);
}

module bw_tongues_all() {
    for (y = bw_dt_y_positions) bw_tongue_single(y);
}

module bw_slots_all() {
    for (y = bw_dt_y_positions) bw_slot_single(y);
}

// ============================================================
// Rail front/back halves (split at Z = split_z)
// ============================================================

module rail_front_half() {
    union() {
        // Front portion (Z = 0 to split_z)
        intersection() {
            rail();
            translate([-1, -1, -1])
                cube([body_t + ledge_w + 2, rail_h + 2, split_z + 1]);
        }
        // Body-wall tongues extending into back half
        bw_tongues_all();
    }
}

module rail_back_half() {
    difference() {
        // Back portion (Z = split_z to rail_depth)
        intersection() {
            rail();
            translate([-1, -1, split_z])
                cube([body_t + ledge_w + 2, rail_h + 2, rail_depth - split_z + 1]);
        }
        // Body-wall slots
        bw_slots_all();
    }
}

// ============================================================
// Module: Bridge
// ============================================================
// Bar at ledge level, tongues extending into rails at both X ends.
// Cross-section (XZ) of tongue is the dovetail trapezoid.

module bridge() {
    // In local coords:
    //   X: spans between rails (0 = left ledge tip, bridge_gap = right ledge tip)
    //   Y: vertical, 0 = bottom, dt_slide = top (= ledge_t height)
    //   Z: along rail depth, centered at 0

    // Main bar (spans the gap)
    translate([0, 0, -bridge_bar_width_z/2])
        cube([bridge_gap, dt_slide, bridge_bar_width_z]);

    // Right tongue (extends in +X from X=bridge_gap into right rail)
    translate([bridge_gap, 0, 0])
        rotate([90, 0, 0])
            translate([0, 0, -dt_slide])
                linear_extrude(height = dt_slide)
                    dt_male_rail_profile();

    // Left tongue (extends in -X from X=0 into left rail) - mirrored
    translate([0, 0, 0])
        mirror([1, 0, 0])
            rotate([90, 0, 0])
                translate([0, 0, -dt_slide])
                    linear_extrude(height = dt_slide)
                        dt_male_rail_profile();
}

// ============================================================
// Preview mode settings
// ============================================================

show_colors = true;   // Color-code features within each part
show_split  = true;   // Show rail as front/back halves (with split joint)
split_exploded_gap = 0; // mm - Z gap for exploded view (0 = flush)

// --- Rail (台) feature colors ---
c_foot        = "LightGray";
c_lower_ledge = "Gold";
c_body_wall   = "SteelBlue";
c_gusset      = "Tomato";
c_upper_ledge = "Goldenrod";
c_top_ext     = "CornflowerBlue";

// --- Bridge (橋) feature colors ---
c_bar         = "LimeGreen";      // central rectangular bar
c_inset       = "HotPink";        // rectangular channel portion of tongue
c_taper       = "MediumPurple";   // dovetail taper portion of tongue

// ============================================================
// Module: Rail with color-coded features
// ============================================================
// Splits the rail into named regions using bounding-box intersections.
// Each region is rendered in its own color for easy identification.

// Bounding boxes for each feature (XY regions, full Z)
// Intersected with the full rail to extract that feature's volume.

module _bb(x1, y1, x2, y2) {
    translate([x1, y1, -1])
        cube([x2 - x1, y2 - y1, rail_depth + 2]);
}

module rail_feature_FOOT()        { _bb(0,                  0,                  body_t + ledge_w, foot_h); }
module rail_feature_LOWER_LEDGE() { _bb(body_t,             foot_h,             body_t + ledge_w, base_h); }
module rail_feature_BODY_WALL()   { _bb(0,                  foot_h,             body_t,           upper_z + ledge_t); }
module rail_feature_GUSSET()      { _bb(body_t,             upper_z - gusset_drop, body_t + gusset_reach, upper_z); }
module rail_feature_UPPER_LEDGE() { _bb(body_t,             upper_z,            body_t + ledge_w, upper_z + ledge_t); }
module rail_feature_TOP_EXT()     { _bb(0,                  upper_z + ledge_t,  body_t,           rail_h); }

// Helper: render a rail-like object with feature colors
module _apply_rail_colors(rail_module_name) {
    if (show_colors) {
        if (rail_module_name == "front") {
            color(c_foot)        intersection() { rail_front_half(); rail_feature_FOOT(); }
            color(c_lower_ledge) intersection() { rail_front_half(); rail_feature_LOWER_LEDGE(); }
            color(c_body_wall)   intersection() { rail_front_half(); rail_feature_BODY_WALL(); }
            color(c_gusset)      intersection() { rail_front_half(); rail_feature_GUSSET(); }
            color(c_upper_ledge) intersection() { rail_front_half(); rail_feature_UPPER_LEDGE(); }
            color(c_top_ext)     intersection() { rail_front_half(); rail_feature_TOP_EXT(); }
        } else if (rail_module_name == "back") {
            color(c_foot)        intersection() { rail_back_half(); rail_feature_FOOT(); }
            color(c_lower_ledge) intersection() { rail_back_half(); rail_feature_LOWER_LEDGE(); }
            color(c_body_wall)   intersection() { rail_back_half(); rail_feature_BODY_WALL(); }
            color(c_gusset)      intersection() { rail_back_half(); rail_feature_GUSSET(); }
            color(c_upper_ledge) intersection() { rail_back_half(); rail_feature_UPPER_LEDGE(); }
            color(c_top_ext)     intersection() { rail_back_half(); rail_feature_TOP_EXT(); }
        } else {
            color(c_foot)        intersection() { rail(); rail_feature_FOOT(); }
            color(c_lower_ledge) intersection() { rail(); rail_feature_LOWER_LEDGE(); }
            color(c_body_wall)   intersection() { rail(); rail_feature_BODY_WALL(); }
            color(c_gusset)      intersection() { rail(); rail_feature_GUSSET(); }
            color(c_upper_ledge) intersection() { rail(); rail_feature_UPPER_LEDGE(); }
            color(c_top_ext)     intersection() { rail(); rail_feature_TOP_EXT(); }
        }
    } else {
        if      (rail_module_name == "front") rail_front_half();
        else if (rail_module_name == "back")  rail_back_half();
        else                                  rail();
    }
}

module rail_colored() {
    if (show_split) {
        // Front half (in place)
        _apply_rail_colors("front");
        // Back half (optionally shifted for exploded view)
        translate([0, 0, split_exploded_gap])
            _apply_rail_colors("back");
    } else {
        _apply_rail_colors("full");
    }
}

// ============================================================
// Module: Bridge with color-coded features
// ============================================================
// BAR: central rectangular bar
// INSET_L/R: rectangular channel portions of tongues
// TAPER_L/R: dovetail taper portions of tongues

// Male profile for a single segment (0 to segment_len in X, with specified widths)
module dt_male_segment_profile(seg_len, w_start, w_end) {
    polygon([
        [0,        -w_start/2],
        [0,         w_start/2],
        [seg_len,   w_end/2],
        [seg_len,  -w_end/2]
    ]);
}

module bridge_colored() {
    // BAR (central rectangular bar) - LimeGreen
    color(show_colors ? c_bar : undef)
        translate([0, 0, -bridge_bar_width_z/2])
            cube([bridge_gap, dt_slide, bridge_bar_width_z]);

    // Right INSET (rectangular channel, X = bridge_gap to bridge_gap+dt_inset)
    color(show_colors ? c_inset : undef)
        translate([bridge_gap, 0, -dt_width/2])
            cube([dt_inset, dt_slide, dt_width]);

    // Right TAPER (dovetail taper, X = bridge_gap+dt_inset to bridge_gap+dt_total_pen)
    color(show_colors ? c_taper : undef)
        translate([bridge_gap + dt_inset, 0, 0])
            rotate([90, 0, 0])
                translate([0, 0, -dt_slide])
                    linear_extrude(height = dt_slide)
                        dt_male_segment_profile(dt_depth, dt_width, dt_width_wide);

    // Left INSET (rectangular channel, X = -dt_inset to 0)
    color(show_colors ? c_inset : undef)
        translate([-dt_inset, 0, -dt_width/2])
            cube([dt_inset, dt_slide, dt_width]);

    // Left TAPER (dovetail taper, X = -dt_total_pen to -dt_inset)
    color(show_colors ? c_taper : undef)
        translate([-dt_inset, 0, 0])
            mirror([1, 0, 0])
                rotate([90, 0, 0])
                    translate([0, 0, -dt_slide])
                        linear_extrude(height = dt_slide)
                            dt_male_segment_profile(dt_depth, dt_width, dt_width_wide);
}


// ============================================================
// Part selector: choose what to render / export
// ============================================================
// Valid values:
//   "preview"    - full color-coded assembly (default, for OpenSCAD GUI)
//   "rail_front" - printable: one front half of a rail (print 2, identical)
//   "rail_back"  - printable: one back half of a rail (print 2, identical)
//   "bridge"     - printable: one bridge (print 8, identical)
//
// CLI example:
//   openscad -D 'part="bridge"' -o output/bridge.stl macbook-stand.scad

part = "preview";

if (part == "preview") {
    // Left rail (RAIL-L)
    rail_colored();

    // Right rail (RAIL-R, mirrored)
    translate([right_rail_outer_x, 0, 0])
        mirror([1, 0, 0])
            rail_colored();

    // Bridges
    for (bz = bridge_z_positions) {
        translate([left_rail_inner_x, lower_ledge_top - dt_slide, bz])
            bridge_colored();
        translate([left_rail_inner_x, upper_ledge_top - dt_slide, bz])
            bridge_colored();
    }
} else if (part == "rail_front") {
    rail_front_half();
} else if (part == "rail_back") {
    // Shift to origin so STL starts at Z=0 for printing
    translate([0, 0, -split_z])
        rail_back_half();
} else if (part == "bridge") {
    // Orient bridge flat on the bed: bar's Y=0 face on the build plate
    bridge();
} else {
    assert(false, str("Unknown part: '", part, "'"));
}

// === Info ===
echo(str("Stand size: ", right_rail_outer_x, " x ", rail_h, " x ", rail_depth, " mm"));
echo(str("Inner gap (between body walls): ", inner_gap, " mm"));
echo(str("Bridge gap (between ledge tips): ", bridge_gap, " mm"));
echo(str("Bridge total X length: ", bridge_total_x, " mm"));
echo(str("Bridges: ", len(bridge_z_positions), " per level x 2 levels = ",
     len(bridge_z_positions) * 2, " total"));
echo(str("Dovetail: narrow=", dt_width, " wide=", dt_width_wide,
     " slide=", dt_slide, " mm"));
