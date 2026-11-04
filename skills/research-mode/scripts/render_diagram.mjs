#!/usr/bin/env node
// Check and preview Mermaid with the vendored Pele. Obsidian renders ```mermaid blocks itself with its own
// Pele build, so notes keep the code block; this only catches syntax errors before the user opens the note.
// Usage: node render_diagram.mjs <note.md>                 exit 1 and name the block if any mermaid block fails to parse
//        node render_diagram.mjs <diagram.mmd> [out.svg]   write a preview SVG to look at (default: same name with .svg)
//        node render_diagram.mjs --selftest
// Pele colors come from CSS variables, so the preview replaces them with light-theme defaults and a white background.
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
  render('flowchart LR\n  A --> B');
  let threw = false;
  try { render('flowchart LR\n  A --> '); } catch { threw = true; }
  if (!threw) throw new Error('selftest failed: bad diagram not rejected');
  console.log('selftest ok');
} else if (process.argv[2]?.endsWith('.md')) {
  const text = readFileSync(process.argv[2], 'utf8');
  let bad = 0;
  for (const m of text.matchAll(/```mermaid\n([\s\S]*?)```/g)) {
    try { render(m[1]); } catch (e) {
      bad++;
      console.error(`${process.argv[2]}:${text.slice(0, m.index).split('\n').length}: ${e.message}`);
    }
  }
  process.exit(bad ? 1 : 0);
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
  console.error('usage: render_diagram.mjs <note.md> | <diagram.mmd> [out.svg]');
  process.exit(2);
}
