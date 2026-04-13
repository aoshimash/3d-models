// CLI exporter for macbook-stand
// Usage: node macbook-stand/export.js [part]
//   node macbook-stand/export.js          → all parts
//   node macbook-stand/export.js front    → front rail only
//   node macbook-stand/export.js back     → back rail only
//   node macbook-stand/export.js bridge   → bridge only

const { serialize } = require('@jscad/stl-serializer')
const fs = require('fs')
const path = require('path')

// Re-use the same model code
const modelPath = path.join(__dirname, 'macbook-stand.js')
delete require.cache[require.resolve(modelPath)]
const model = require(modelPath)

// Access internal functions by temporarily patching module.exports
// For now, call main() and extract parts
const parts = model.main()

function exportSTL (geometry, filename) {
  const outputDir = path.join(__dirname, 'output')
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true })
  const rawData = serialize({ binary: true }, geometry)
  const buffer = Buffer.concat(rawData.map(d => Buffer.from(d)))
  const filepath = path.join(outputDir, filename)
  fs.writeFileSync(filepath, buffer)
  console.log(`  ${filename} (${(buffer.length / 1024).toFixed(1)} KB)`)
}

const partArg = process.argv[2]

console.log('Exporting MacBook Stand STLs...')

if (!partArg || partArg === 'front') {
  exportSTL(parts[0], 'macbook-stand-front.stl')
}
if (!partArg || partArg === 'back') {
  exportSTL(parts[1], 'macbook-stand-back.stl')
}
if (!partArg || partArg === 'bridge') {
  exportSTL(parts[2], 'macbook-stand-bridge.stl')
}

console.log('Done.')
