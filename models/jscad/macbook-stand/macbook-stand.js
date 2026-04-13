// MacBook Stand - JSCAD version
// Side rail for dual MacBook Pro 13" shelf stand
//
// Usage:
//   node macbook-stand.js
//
// Outputs STL files to output/ directory.

const { booleans, primitives, transforms, extrusions, geometries } = require('@jscad/modeling')
const { subtract, union, intersect } = booleans
const { cuboid, cylinder } = primitives
const { translate, rotate, mirror } = transforms
const { extrudeLinear } = extrusions
const { geom2, path2 } = geometries
const { serialize } = require('@jscad/stl-serializer')
const fs = require('fs')
const path = require('path')

// ============================================================
// Parameters
// ============================================================

// MacBook Pro 13"
const mb_width = 313       // mm - body width
const mb_depth = 220       // mm - body depth
const mb_thickness = 18    // mm - closed-lid thickness

// Shelf interior
const shelf_width = 385
const shelf_depth = 261
const shelf_height = 135

// Print constraints (Bambu Lab A1 Mini)
const max_print = 180

// Design parameters
const body_t = 8           // mm - body wall thickness
const ledge_w = 50         // mm - ledge width
const ledge_t = 8          // mm - ledge thickness
const foot_h = 10          // mm - base foot height
const air_gap = 40         // mm - gap between MacBooks
const gusset_reach = 15
const gusset_drop = 20
const rail_depth = 258     // mm - total rail depth
const top_ext = 8

// Frame / bridge
const inner_gap = 230      // mm - between body wall inner faces
const bridge_bar_w = 16
const bridge_bar_h = 2     // mm - recessed flush
const bridge_tab_len = 15
const bridge_tab_w = 10
const bridge_z_positions = [8, 80, 178, 250]

// Cantilever snap-fit
const cant_t = 1.0
const cant_clearance = 0.5
const hook_overhang = 0.4
const hook_h = 1.0
const pocket_wall = 3
const pocket_floor = 2

// Ventilation
const vent_w = 8
const vent_pitch = 12
const vent_margin_x = 8
const vent_margin_z = 6
const vent_bridge_z = 30

// Body wall holes
const hole_d = 6
const hole_pitch = 10
const hole_margin_y = 3
const hole_margin_z = 6
const hole_tenon_clearance = 15

// Airflow ribs
const rib_depth = 2.5
const rib_width = 3
const rib_count = 3

// Derived
const base_h = foot_h + ledge_t           // 18
const upper_z = base_h + mb_thickness + air_gap  // 76
const rail_h = upper_z + ledge_t + top_ext       // 92
const z_split = rail_depth / 2                   // 129
const pocket_depth = ledge_t - pocket_floor      // 6
const bridge_span = inner_gap - 2 * ledge_w     // 130
const bridge_total_len = bridge_span + 2 * bridge_tab_len // 160

// ============================================================
// Helper: export geometry to STL file
// ============================================================

function exportSTL (geometry, filename) {
  const outputDir = path.join(__dirname, 'output')
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true })

  const rawData = serialize({ binary: true }, geometry)
  const buffer = Buffer.concat(rawData.map(d => Buffer.from(d)))
  const filepath = path.join(outputDir, filename)
  fs.writeFileSync(filepath, buffer)
  console.log(`Exported: ${filepath} (${(buffer.length / 1024).toFixed(1)} KB)`)
}

// ============================================================
// Rail cross-section profile (2D polygon)
// ============================================================

function railProfile () {
  const points = [
    [0, 0],                                  // K
    [body_t + ledge_w, 0],                   // J
    [body_t + ledge_w, base_h],              // I
    [body_t, base_h],                        // H
    [body_t, upper_z - gusset_drop],         // G
    [body_t + gusset_reach, upper_z],        // F
    [body_t + ledge_w, upper_z],             // E
    [body_t + ledge_w, upper_z + ledge_t],   // D
    [body_t, upper_z + ledge_t],             // C
    [body_t, rail_h],                        // B
    [0, rail_h]                              // A
  ]
  return geom2.fromPoints(points)
}

// ============================================================
// Full rail body (extruded profile)
// ============================================================

function railBody () {
  const profile = railProfile()
  return extrudeLinear({ height: rail_depth }, profile)
}

// ============================================================
// Bridge bar with cantilever snap-fit
// ============================================================

function bridge () {
  const arm_z = bridge_tab_w - 2 * cant_clearance
  const arm_depth = pocket_depth - cant_clearance
  const arm_inset = pocket_wall + cant_clearance

  // Main bar
  let result = cuboid({
    size: [bridge_total_len, bridge_bar_w, bridge_bar_h],
    center: [bridge_total_len / 2, 0, bridge_bar_h / 2]
  })

  // Arms + hooks at each end
  for (let side = 0; side < 2; side++) {
    const arm_x = side === 0
      ? arm_inset
      : bridge_total_len - arm_inset - cant_t
    const dir = side === 0 ? -1 : 1 // outward direction

    // Arm body (extends 1mm into bar for solid union)
    const arm = cuboid({
      size: [cant_t, arm_z, arm_depth + bridge_bar_h],
      center: [arm_x + cant_t / 2, 0, -(arm_depth - bridge_bar_h) / 2]
    })
    result = union(result, arm)

    // Hook: "4" wedge shape (pointed top, flat bottom catch)
    const outer_x = side === 0 ? arm_x : arm_x + cant_t
    const hook_points = [
      [0, 0],                        // bottom at arm face
      [dir * hook_overhang, 0],      // bottom at hook tip
      [0, hook_h]                    // top (pointed)
    ]
    const hook2d = geom2.fromPoints(hook_points)
    let hook = extrudeLinear({ height: arm_z }, hook2d)
    // Position: at arm outer face, at bottom of arm
    hook = translate([outer_x, -arm_z / 2, -arm_depth], hook)
    result = union(result, hook)
  }

  return result
}

// ============================================================
// Main: generate and export
// ============================================================

console.log('=== MacBook Stand (JSCAD) ===')
console.log(`Rail: ${body_t + ledge_w} x ${rail_depth} x ${rail_h} mm`)
console.log(`Bridge: ${bridge_total_len} mm (span ${bridge_span} + tabs ${bridge_tab_len}x2)`)
console.log(`Bridge positions: [${bridge_z_positions}]`)

// Generate bridge
const bridgeGeom = bridge()
exportSTL(bridgeGeom, 'macbook-stand-bridge.stl')

// Generate rail body (full, no splits yet - test)
const railGeom = railBody()
exportSTL(railGeom, 'macbook-stand-rail-test.stl')

console.log('Done.')
