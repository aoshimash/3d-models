// Side rail for dual MacBook Pro 13" shelf stand (two-part with diagonal tenon).
// OpenSCAD version - rewrite of CadQuery v1 for better accuracy.
//
// Print list:
//   - Rail front x2, Rail back x2 (4 rail pieces)
//   - Bridge x8 (4 per level, 2 levels)
//
// Assembly:
//   1. Join front+back rail halves (diagonal tenon, 15-deg push)
//   2. Snap bridges onto ledges (cantilever snap-fit, push from above)
//   3. Place assembled frame in shelf (free-standing)

// ============================================================
// Parameters
// ============================================================

// --- MacBook Pro 13" ---
mb_width     = 313;   // mm - body width
mb_depth     = 220;   // mm - body depth
mb_thickness = 18;    // mm - closed-lid thickness

// --- Shelf interior ---
shelf_width  = 385;   // mm - internal width
shelf_depth  = 261;   // mm - internal depth
shelf_height = 135;   // mm - internal height

// --- Print constraints (Bambu Lab A1 Mini) ---
max_print = 180;      // mm - build volume per axis

// --- Design parameters ---
body_t       = 8;     // mm - body wall thickness
ledge_w      = 50;    // mm - ledge width (inward from body)
ledge_t      = 8;     // mm - ledge platform thickness
foot_h       = 10;    // mm - base foot height (airflow)
air_gap      = 40;    // mm - gap between MacBooks
gusset_reach = 15;    // mm - gusset extent on upper ledge underside
gusset_drop  = 20;    // mm - gusset vertical drop
rail_depth   = 258;   // mm - total rail depth (178 + 80 extension)
top_ext      = 8;     // mm - body wall above upper ledge
fit_tol      = 0.2;   // mm - general sliding fit tolerance

// --- Frame / bridge ---
inner_gap      = 230;  // mm - distance between body wall inner faces
bridge_bar_w   = 16;   // mm - bridge bar width (Z)
bridge_bar_h   = 2;    // mm - bridge bar height (recessed flush)
bridge_tab_len = 15;   // mm - tab length on each ledge (X)
bridge_tab_w   = 10;   // mm - tab width (Z, narrower than bar)
bridge_z_positions = [8, 80, 178, 250]; // Z centers

// --- Cantilever snap-fit ---
cant_t         = 1.0;  // mm - arm thickness (flex direction)
cant_clearance = 0.5;  // mm - FDM assembly clearance
hook_overhang  = 0.4;  // mm - hook protrusion
hook_h         = 1.0;  // mm - hook height
pocket_wall    = 3;    // mm - wall between pocket and ledge tip
pocket_floor   = 2;    // mm - solid floor at pocket bottom

// --- Diagonal tenon joint ---
tenon_angle     = 15;   // degrees - tilt from Z toward +X
tenon_length    = 12;   // mm - tenon length along axis
tenon_width     = 40;   // mm - tenon width (X)
tenon_taper     = 0.3;  // mm - wedge taper
tenon_tol_entry = 0.20; // mm - clearance at entry
tenon_tol_deep  = 0.10; // mm - clearance at deep end
tenon_h_base    = 10;   // mm - base tenon height
tenon_h_upper   = 6;    // mm - upper tenon height

// --- Ventilation slots ---
vent_w         = 8;    // mm - slot width (67% open)
vent_pitch     = 12;   // mm - center-to-center
vent_margin_x  = 8;    // mm - inset from edges
vent_margin_z  = 6;    // mm - inset from front/back
vent_bridge_z  = 30;   // mm - solid bridge at joint

// --- Body wall holes ---
hole_d              = 6;    // mm - hole diameter
hole_pitch          = 10;   // mm - hex grid spacing
hole_margin_y       = 3;    // mm - clearance from Y features
hole_margin_z       = 6;    // mm - clearance from Z edges
hole_tenon_clearance = 15;  // mm - clearance around joint

// --- Airflow spacer ribs ---
rib_depth  = 2.5;  // mm - protrusion from body wall
rib_width  = 3;    // mm - thickness along Z
rib_count  = 3;    // number of ribs

// ============================================================
// Derived dimensions
// ============================================================

base_h  = foot_h + ledge_t;                    // 18
upper_z = base_h + mb_thickness + air_gap;      // 76
rail_h  = upper_z + ledge_t + top_ext;          // 92
z_split = rail_depth / 2;                       // 129

bridge_span     = inner_gap - 2 * ledge_w;      // 130
bridge_total_len = bridge_span + 2 * bridge_tab_len; // 160

pocket_depth   = ledge_t - pocket_floor;         // 6
pocket_x_main  = cant_t + 2 * cant_clearance;   // 2.0
pocket_x_groove = hook_overhang + cant_clearance; // 0.9
pocket_x_outer = body_t + ledge_w - pocket_wall; // 55
pocket_z       = bridge_tab_w + 2 * cant_clearance; // 11

$fn = 24; // circle resolution for hex holes

// ============================================================
// Module: Rail cross-section profile (2D)
// ============================================================

module rail_profile() {
    polygon(points=[
        [0, 0],                              // K: outer bottom
        [body_t + ledge_w, 0],               // J: base bottom outer
        [body_t + ledge_w, base_h],          // I: base top, ledge tip
        [body_t, base_h],                    // H: body at lower ledge
        [body_t, upper_z - gusset_drop],     // G: gusset end
        [body_t + gusset_reach, upper_z],    // F: gusset start
        [body_t + ledge_w, upper_z],         // E: upper ledge bottom
        [body_t + ledge_w, upper_z + ledge_t], // D: upper ledge top
        [body_t, upper_z + ledge_t],         // C: body at upper ledge
        [body_t, rail_h],                    // B: inner top
        [0, rail_h],                         // A: outer top
    ]);
}

// ============================================================
// Module: Full rail (extruded profile + all cuts)
// ============================================================

module full_rail() {
    difference() {
        union() {
            // Main rail body
            linear_extrude(height=rail_depth)
                rail_profile();

            // Airflow spacer ribs on body wall inner face
            rib_z_spacing = rail_depth / (rib_count + 1);
            for (i = [1:rib_count]) {
                translate([body_t, base_h, rib_z_spacing * i - rib_width/2])
                    cube([rib_depth, upper_z + ledge_t - base_h, rib_width]);
            }
        }

        // --- Ventilation slots (base foot area) ---
        slot_x_start = body_t + vent_margin_x;
        slot_x_end   = body_t + ledge_w - vent_margin_x;
        // Front segment
        slot_front_len = z_split - vent_bridge_z/2 - vent_margin_z;
        // Back segment
        slot_back_start = z_split + vent_bridge_z/2;
        slot_back_len = rail_depth - vent_margin_z - slot_back_start;

        for (cx = [slot_x_start : vent_pitch : slot_x_end]) {
            if (cx + vent_w/2 <= slot_x_end) {
                // Front slot
                translate([cx - vent_w/2, -0.1, vent_margin_z])
                    cube([vent_w, foot_h + 0.2, slot_front_len]);
                // Back slot
                translate([cx - vent_w/2, -0.1, slot_back_start])
                    cube([vent_w, foot_h + 0.2, slot_back_len]);
            }
        }

        // --- Body wall hex holes ---
        hex_row_spacing = hole_pitch * sqrt(3) / 2;
        hole_r = hole_d / 2;

        // Y exclusion zones
        for (row = [0 : 1 : floor((rail_h - 2*hole_margin_y) / hex_row_spacing)]) {
            y = hole_margin_y + hole_r + row * hex_row_spacing;
            // Check Y exclusions
            if (y > hole_margin_y &&
                y < rail_h - hole_margin_y &&
                !(y > base_h - hole_margin_y && y < base_h + hole_margin_y) &&
                !(y > upper_z - gusset_drop - hole_margin_y &&
                  y < upper_z + ledge_t + hole_margin_y)) {

                z_offset = (row % 2 == 1) ? hole_pitch / 2 : 0;
                for (z = [hole_margin_z + hole_r + z_offset :
                          hole_pitch :
                          rail_depth - hole_margin_z - hole_r]) {
                    // Z exclusion: tenon area
                    if (!(z > z_split - hole_tenon_clearance &&
                          z < z_split + hole_tenon_clearance)) {
                        translate([-0.1, y, z])
                            rotate([0, 90, 0])
                                cylinder(h=body_t+0.2, r=hole_r);
                    }
                }
            }
        }

        // --- Bridge pockets (snap-fit) ---
        ledge_y_tops = [base_h, upper_z + ledge_t];

        for (y_top = ledge_y_tops) {
            for (bz = bridge_z_positions) {
                y_floor = y_top - pocket_depth;

                // Bar recess (flush, open at ledge tip)
                recess_x_start = body_t + ledge_w - bridge_tab_len;
                translate([recess_x_start, y_top - bridge_bar_h, bz - bridge_bar_w/2 - cant_clearance])
                    cube([bridge_tab_len + 0.1, bridge_bar_h + 0.1,
                          bridge_bar_w + 2*cant_clearance]);

                // Main pocket (arm passage)
                translate([pocket_x_outer - pocket_x_main, y_floor,
                           bz - pocket_z/2])
                    cube([pocket_x_main, pocket_depth + 0.1, pocket_z]);

                // Hook groove on outer wall (tip side)
                groove_h = hook_h + cant_clearance;
                translate([pocket_x_outer, y_floor,
                           bz - pocket_z/2])
                    cube([pocket_x_groove, groove_h, pocket_z]);
            }
        }
    }
}

// ============================================================
// Module: Diagonal tenon tongue (undersized)
// ============================================================

module tenon_tongue(th) {
    tw = tenon_width - 2 * tenon_tol_entry;
    th_entry = th - 2 * tenon_tol_entry;
    tw_deep = tenon_width - tenon_taper - 2 * tenon_tol_deep;
    th_deep = th - tenon_taper - 2 * tenon_tol_deep;
    len = tenon_length - tenon_tol_entry;

    hull() {
        // Base face
        translate([-tw/2, -th_entry/2, 0])
            cube([tw, th_entry, 0.01]);
        // Tip face
        translate([-tw_deep/2, -th_deep/2, len])
            cube([tw_deep, th_deep, 0.01]);
    }
}

// ============================================================
// Module: Diagonal tenon groove (nominal)
// ============================================================

module tenon_groove(th) {
    tw_deep = tenon_width - tenon_taper;
    th_deep = th - tenon_taper;

    hull() {
        translate([-tenon_width/2, -th/2, 0])
            cube([tenon_width, th, 0.01]);
        translate([-tw_deep/2, -th_deep/2, tenon_length])
            cube([tw_deep, th_deep, 0.01]);
    }
}

// ============================================================
// Module: Rail half (front or back)
// ============================================================

module rail_half(is_front=true) {
    tenon_cx = (body_t + ledge_w) / 2;
    tenon_positions = [
        [base_h / 2, tenon_h_base],
        [upper_z + ledge_t / 2, tenon_h_upper],
    ];

    difference() {
        union() {
            // Cut rail in half
            intersection() {
                full_rail();
                if (is_front) {
                    cube([body_t + ledge_w + 10, rail_h + 10, z_split]);
                } else {
                    translate([0, 0, z_split])
                        cube([body_t + ledge_w + 10, rail_h + 10,
                              rail_depth - z_split]);
                }
            }

            // Add tongue protrusions
            for (tp = tenon_positions) {
                cy = tp[0];
                th = tp[1];
                translate([tenon_cx, cy, z_split])
                    rotate([0, -tenon_angle, 0])
                        rotate([0, 0, 0])
                            tenon_tongue(th);
            }
        }

        // Cut groove from the other half's territory
        // (only needed if this half has grooves for the mating half)
        if (!is_front) {
            for (tp = tenon_positions) {
                cy = tp[0];
                th = tp[1];
                translate([tenon_cx, cy, z_split])
                    rotate([0, -tenon_angle, 0])
                        tenon_groove(th);
            }
        }
    }
}

// ============================================================
// Module: Bridge bar with cantilever snap-fit arms
// ============================================================

module bridge() {
    arm_z = bridge_tab_w - 2 * cant_clearance;
    arm_depth = pocket_depth - cant_clearance;
    arm_inset = pocket_wall + cant_clearance;

    // Main bar
    translate([0, -bridge_bar_w/2, 0])
        cube([bridge_total_len, bridge_bar_w, bridge_bar_h]);

    // Arms at each end
    for (side = [0, 1]) {
        mirror_x = side == 0 ? 0 : 1;
        arm_x = side == 0 ? arm_inset : bridge_total_len - arm_inset - cant_t;

        // Arm body (extends into bar by 1mm overlap)
        translate([arm_x, -arm_z/2, -arm_depth])
            cube([cant_t, arm_z, arm_depth + bridge_bar_h]);

        // Hook: wedge "4" shape, facing OUTWARD (toward ledge tip)
        outer_dir = side == 0 ? -1 : 1;
        hook_x = side == 0 ? arm_x : arm_x + cant_t;

        translate([hook_x, -arm_z/2, -arm_depth])
            linear_extrude(height=arm_z) {
                // "4" shape: pointed top (ramp), flat bottom (catch)
                polygon(points=[
                    [0, 0],                              // bottom at arm face
                    [outer_dir * hook_overhang, 0],      // bottom at hook tip
                    [0, hook_h],                         // top (pointed, no overhang)
                ]);
            }
    }
}

// ============================================================
// Render selection
// ============================================================

// Uncomment the part you want to render/export:

// Front rail half
//rail_half(is_front=true);

// Back rail half
//rail_half(is_front=false);

// Bridge bar (print 8 copies)
//bridge();

// Preview: show all parts
color("SteelBlue", 0.8) rail_half(is_front=true);
color("CornflowerBlue", 0.8) rail_half(is_front=false);
color("Orange") translate([body_t + ledge_w, 0, bridge_z_positions[1]])
    bridge();
