#!/usr/bin/env node
// Used by the visual-regression CI workflow to derive a backstop config
// pointed at a given localhost port, from the single source of truth in
// backstop.json, so the base-branch build and the PR-branch build can be
// captured on different ports and compared against each other.
const fs = require('fs');
const path = require('path');

const [, , port, bitmapsReferenceDir, bitmapsTestDir] = process.argv;

if (!port) {
  console.error(
    'Usage: backstop_config_for_port.js <port> [bitmaps_reference_dir] [bitmaps_test_dir]'
  );
  process.exit(1);
}

const configPath = path.join(__dirname, '..', 'backstop.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

config.scenarios = config.scenarios.map((scenario) => ({
  ...scenario,
  url: scenario.url.replace(/^http:\/\/localhost:\d+/, `http://localhost:${port}`),
}));

if (bitmapsReferenceDir) config.paths.bitmaps_reference = bitmapsReferenceDir;
if (bitmapsTestDir) config.paths.bitmaps_test = bitmapsTestDir;

process.stdout.write(JSON.stringify(config, null, 2));
