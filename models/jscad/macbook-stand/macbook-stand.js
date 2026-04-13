// MacBook Stand - JSCAD version
// Side rail for dual MacBook Pro 13" shelf stand
//
// Browser preview:
//   cd models/jscad && npx jscad-now macbook-stand/macbook-stand.js

const { booleans, primitives, transforms, extrusions, geometries, hulls, colors } = require('@jscad/modeling')
const { subtract, union, intersect } = booleans
const { cuboid, cylinder } = primitives
const { translate, rotate } = transforms
const { extrudeLinear } = extrusions
const { geom2 } = geometries
const { hull } = hulls
const { colorize } = colors

// ============================================================
// Parameters
// ============================================================

const mb_thickness = 18
const body_t = 8
const ledge_w = 50
const ledge_t = 8
const foot_h = 10
const air_gap = 40
const gusset_reach = 15
const gusset_drop = 20
const rail_depth = 258
const top_ext = 8

// Frame / bridge
const inner_gap = 230       // mm - between body wall inner faces
const bridge_bar_w = 16     // mm - bar width (Z), wider than tab for shoulder
const bridge_tab_w = 10     // mm - tab width (Z), fits in pocket
const bridge_tab_len = 15   // mm - tab depth into ledge (X)
const bridge_tol = 0.2      // mm - clearance per side
const pocket_floor = 2      // mm - solid floor below pocket
const shoulder_h = 2        // mm - shoulder height resting on ledge surface
const detent_w = 3          // mm - detent bump width (X)
const detent_h = 1          // mm - detent bump height (Y, protrusion)
const lip_overhang = 2      // mm - lip extends over shoulder (Z, each side)
const lip_h = 1             // mm - lip height above ledge surface (Y)
const bridge_z_positions = [8, 80, 178, 250]

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

// Tenon joint
const tenon_angle = 15
const tenon_length = 12
const tenon_width = 40
const tenon_taper = 0.3
const tenon_tol_entry = 0.20
const tenon_tol_deep = 0.10
const tenon_h_base = 10
const tenon_h_upper = 6

// ============================================================
// Derived
// ============================================================

const base_h = foot_h + ledge_t                    // 18
const upper_z = base_h + mb_thickness + air_gap    // 76
const rail_h = upper_z + ledge_t + top_ext         // 92
const z_split = rail_depth / 2                     // 129

const pocket_depth = ledge_t - pocket_floor        // 6mm
const bridge_bar_h = pocket_depth                  // 6mm total tab+shoulder height
const bridge_span = inner_gap - 2 * ledge_w        // 130mm
const bridge_total_len = bridge_span + 2 * bridge_tab_len // 160mm
const pocket_z = bridge_tab_w + 2 * bridge_tol     // 10.4mm (tab fits, bar shoulder doesn't)
const tab_depth = bridge_bar_h - shoulder_h        // 4mm - portion in pocket

const tenon_cx = (body_t + ledge_w) / 2

// ============================================================
// Rail profile (2D)
// ============================================================

function railProfile () {
  return geom2.fromPoints([
    [0, 0],
    [body_t + ledge_w, 0],
    [body_t + ledge_w, base_h],
    [body_t, base_h],
    [body_t, upper_z - gusset_drop],
    [body_t + gusset_reach, upper_z],
    [body_t + ledge_w, upper_z],
    [body_t + ledge_w, upper_z + ledge_t],
    [body_t, upper_z + ledge_t],
    [body_t, rail_h],
    [0, rail_h]
  ])
}

// ============================================================
// Vent slots
// ============================================================

function ventSlots () {
  const slots = []
  const xStart = body_t + vent_margin_x
  const xEnd = body_t + ledge_w - vent_margin_x
  const frontLen = z_split - vent_bridge_z / 2 - vent_margin_z
  const backStart = z_split + vent_bridge_z / 2
  const backLen = rail_depth - vent_margin_z - backStart

  for (let cx = xStart; cx + vent_w / 2 <= xEnd; cx += vent_pitch) {
    slots.push(translate([cx, foot_h / 2, vent_margin_z + frontLen / 2],
      cuboid({ size: [vent_w, foot_h + 0.2, frontLen] })))
    slots.push(translate([cx, foot_h / 2, backStart + backLen / 2],
      cuboid({ size: [vent_w, foot_h + 0.2, backLen] })))
  }
  return slots
}

// ============================================================
// Body wall hex holes
// ============================================================

function bodyWallHoles () {
  const holes = []
  const rowSpacing = hole_pitch * Math.sqrt(3) / 2
  const r = hole_d / 2
  let row = 0
  for (let y = hole_margin_y + r; y <= rail_h - hole_margin_y - r; y += rowSpacing) {
    if ((y > base_h - hole_margin_y && y < base_h + hole_margin_y) ||
        (y > upper_z - gusset_drop - hole_margin_y && y < upper_z + ledge_t + hole_margin_y)) {
      row++; continue
    }
    const zo = (row % 2 === 1) ? hole_pitch / 2 : 0
    for (let z = hole_margin_z + r + zo; z <= rail_depth - hole_margin_z - r; z += hole_pitch) {
      if (z > z_split - hole_tenon_clearance && z < z_split + hole_tenon_clearance) continue
      holes.push(translate([body_t / 2, y, z],
        rotate([0, Math.PI / 2, 0], cylinder({ radius: r, height: body_t + 0.4, segments: 16 }))))
    }
    row++
  }
  return holes
}

// ============================================================
// Bridge pockets with detent recess
// ============================================================

function bridgePockets () {
  const cuts = []
  const ledgeYTops = [base_h, upper_z + ledge_t]

  for (const yTop of ledgeYTops) {
    for (const bz of bridge_z_positions) {
      // Main pocket: open at ledge tip, tab_depth deep, pocket_z wide
      // Shoulder recess: full bar width, shoulder_h deep at the top
      const pocketXCenter = body_t + ledge_w - bridge_tab_len / 2

      // Shoulder recess: 2-layer for retention lip (flush with surface)
      // Top layer: narrow opening (lip_h deep, lets tab+narrow shoulder pass)
      const shoulderRecessZ = bridge_bar_w + 2 * bridge_tol  // 16.4mm full width
      const openingZ = shoulderRecessZ - 2 * lip_overhang    // 12.4mm narrow opening
      cuts.push(translate(
        [pocketXCenter, yTop - lip_h / 2, bz],
        cuboid({ size: [bridge_tab_len + 0.1, lip_h + 0.1, openingZ] })
      ))
      // Bottom layer: full width cavity (shoulder slides in from X under the lip)
      cuts.push(translate(
        [pocketXCenter, yTop - lip_h - (shoulder_h - lip_h) / 2, bz],
        cuboid({ size: [bridge_tab_len + 0.1, shoulder_h - lip_h + 0.1, shoulderRecessZ] })
      ))

      // Tab pocket (narrow, deeper below shoulder)
      cuts.push(translate(
        [pocketXCenter, yTop - shoulder_h - tab_depth / 2, bz],
        cuboid({ size: [bridge_tab_len + 0.1, tab_depth + 0.1, pocket_z] })
      ))

      // Detent recess at inner end of pocket (1mm deeper)
      const recessX = body_t + ledge_w - bridge_tab_len + detent_w / 2
      cuts.push(translate(
        [recessX, yTop - shoulder_h - tab_depth - detent_h / 2, bz],
        cuboid({ size: [detent_w + bridge_tol, detent_h + bridge_tol, pocket_z] })
      ))
    }
  }
  return cuts
}

// ============================================================
// Airflow ribs
// ============================================================

function airflowRibs () {
  const ribs = []
  const spacing = rail_depth / (rib_count + 1)
  const h = upper_z + ledge_t - base_h
  for (let i = 1; i <= rib_count; i++) {
    ribs.push(translate([body_t + rib_depth / 2, base_h + h / 2, spacing * i],
      cuboid({ size: [rib_depth, h, rib_width] })))
  }
  return ribs
}

// ============================================================
// Full rail
// ============================================================

function fullRail () {
  let rail = extrudeLinear({ height: rail_depth }, railProfile())
  for (const rib of airflowRibs()) { rail = union(rail, rib) }
  // NOTE: bodyWallHoles() disabled for fast preview (126 cylinders = very slow)
  for (const cut of [...ventSlots(), /* ...bodyWallHoles(), */ ...bridgePockets()]) {
    rail = subtract(rail, cut)
  }
  return rail
}

// ============================================================
// Tenon shapes
// ============================================================

function tenonShape (tw, th, twD, thD, len) {
  return hull(
    cuboid({ size: [tw, th, 0.01] }),
    translate([0, 0, len], cuboid({ size: [twD, thD, 0.01] }))
  )
}
function tenonTongue (th) {
  return tenonShape(
    tenon_width - 2 * tenon_tol_entry, th - 2 * tenon_tol_entry,
    tenon_width - tenon_taper - 2 * tenon_tol_deep, th - tenon_taper - 2 * tenon_tol_deep,
    tenon_length - tenon_tol_entry)
}
function tenonGroove (th) {
  return tenonShape(tenon_width, th, tenon_width - tenon_taper, th - tenon_taper, tenon_length)
}

// ============================================================
// Rail half (split with tenon)
// ============================================================

const tenon_positions = [
  { cy: base_h / 2, th: tenon_h_base },
  { cy: upper_z + ledge_t / 2, th: tenon_h_upper }
]

function railHalf (isFront) {
  const rail = fullRail()
  const aRad = tenon_angle * Math.PI / 180
  const w = body_t + ledge_w

  const box = isFront
    ? translate([w / 2, rail_h / 2, z_split / 2], cuboid({ size: [w + 4, rail_h + 4, z_split] }))
    : translate([w / 2, rail_h / 2, z_split + (rail_depth - z_split) / 2],
      cuboid({ size: [w + 4, rail_h + 4, rail_depth - z_split] }))

  let half = intersect(rail, box)

  for (const { cy, th } of tenon_positions) {
    const shape = isFront ? tenonTongue(th) : tenonGroove(th)
    const placed = translate([tenon_cx, cy, z_split], rotate([0, -aRad, 0], shape))
    half = isFront ? union(half, placed) : subtract(half, placed)
  }
  return half
}

// ============================================================
// Bridge bar (stepped profile with detent)
// ============================================================

function bridgeBar () {
  // Center section: full width, full height (spans the gap)
  const centerLen = bridge_total_len - 2 * bridge_tab_len
  const center = translate(
    [bridge_total_len / 2, 0, bridge_bar_h / 2],
    cuboid({ size: [centerLen, bridge_bar_w, bridge_bar_h] })
  )

  const tabs = []
  for (let side = 0; side < 2; side++) {
    const tabX = side === 0 ? bridge_tab_len / 2 : bridge_total_len - bridge_tab_len / 2

    // Tab: narrow, full height (fits in pocket)
    tabs.push(translate([tabX, 0, bridge_bar_h / 2],
      cuboid({ size: [bridge_tab_len, bridge_tab_w - 2 * bridge_tol, bridge_bar_h] })))

    // Shoulder: wide, only shoulder_h tall, at the top
    tabs.push(translate([tabX, 0, bridge_bar_h - shoulder_h / 2],
      cuboid({ size: [bridge_tab_len, bridge_bar_w, shoulder_h] })))

    // Detent bump: at bridge TIP (deepest into pocket), protrudes BELOW tab
    const bumpX = side === 0
      ? detent_w / 2
      : bridge_total_len - detent_w / 2
    tabs.push(translate([bumpX, 0, -detent_h / 2],
      cuboid({ size: [detent_w, bridge_tab_w - 2 * bridge_tol, detent_h] })))
  }

  return union(center, ...tabs)
}

// ============================================================
// JSCAD main
// ============================================================

const main = () => {
  const front = railHalf(true)
  const back = railHalf(false)
  const bridge = bridgeBar()

  const gap = 10
  return [
    colorize([0.4, 0.6, 0.8, 0.9], translate([0, 0, -gap / 2], front)),
    colorize([0.5, 0.7, 0.9, 0.9], translate([0, 0, gap / 2], back)),
    colorize([1.0, 0.6, 0.2, 1.0],
      translate([body_t + ledge_w + 20, 0, bridge_z_positions[1]], bridge))
  ]
}

module.exports = { main }
