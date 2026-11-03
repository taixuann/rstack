#!/usr/bin/env node
// Render Mermaid text to a self-contained SVG with the vendored pele.
// Usage: node render_diagram.mjs <diagram.mmd> [out.svg]   (default out: same name with .svg)
//        node render_diagram.mjs --selftest
// Pele colors come from CSS variables, which an <img>-embedded SVG cannot inherit, so the
// variables are replaced by their light-theme defaults and a white background is added.
import { readFileSync, writeFileSync } from 'node:fs';
import { render } from '../vendor/pele/pele.js';

export function toSvg(text) {
  let { svg } = render(text);
  const vars = {};
  for (const m of svg.matchAll(/--(_\w+):var\(--pele-[\w-]+,([^)]+)\)/g)) vars[m[1]] = m[2];
  svg = svg.replace(/--_\w+:var\(--pele-[\w-]+,[^)]+\);?/g, '');
  svg = svg.replace(/var\(--(_\w+)\)/g, (_, k) => vars[k] ?? 'inherit');
  svg = svg.replace(/var\(--pele-[\w-]+,([^)]+)\)/g, '$1');
  if (/var\(--/.test(svg)) throw new Error('unresolved CSS variable left in SVG');
  return svg.replace(/^(<svg[^>]*>)/, '$1<rect width="100%" height="100%" fill="#fff"/>');
}

if (process.argv[2] === '--selftest') {
  const svg = toSvg('flowchart LR\n  A[Heart] --> B[Cell]');
  if (!svg.includes('<svg') || /var\(--/.test(svg) || !svg.includes('fill="#fff"')) throw new Error('selftest failed');
  console.log('selftest ok');
} else if (process.argv[2]) {
  const out = process.argv[3] ?? process.argv[2].replace(/\.mmd$/, '') + '.svg';
  try {
    writeFileSync(out, toSvg(readFileSync(process.argv[2], 'utf8')));
    console.log(out);
  } catch (e) {
    console.error(`${process.argv[2]}: ${e.message}`);
    process.exit(1);
  }
} else {
  console.error('usage: render_diagram.mjs <diagram.mmd> [out.svg]');
  process.exit(2);
}
