#!/usr/bin/env python3
"""Write playbook-map.svg (and .png if rsvg-convert exists) from map.data.json.
Usage: python3 export_map.py [map.data.json] [out-dir]   (map.data.json is written by build2.py)"""
import json, sys, shutil, subprocess
from html import escape
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else 'map.data.json')
out = Path(sys.argv[2] if len(sys.argv) > 2 else '.')
D = json.loads(src.read_text())
by = {n['id']: n for n in D['nodes']}
uses = {}
for a, b in D['edges']:
    if a in by and b in by: uses.setdefault(a, []).append(by[b])

PH = ['explore', 'design', 'analysis', 'write', 'closed', 'any phase']
NOTE = {'explore': 'find and read the literature', 'design': 'plan the experiment', 'analysis': 'run and review the analysis',
        'write': 'papers, talks, review', 'closed': 'after submission', 'any phase': 'usable at any time'}
TINT = {'explore': 'a', 'design': 'b', 'analysis': 'c', 'write': 'd', 'closed': 'e', 'any phase': 'f'}
KC = {'skill': 'sk', 'external skill': 'ex', 'external tool': 'ex', 'script': 'sc', 'reference': 'rf', 'workspace folder': 'rf', 'agent': 'ag'}
W, PAD, LBL, GAP, CW = 1200, 24, 150, 12, 0
CHAR, CH_H, CH_PAD = 6.6, 20, 8          # chip: ~6.6px per char at 11.5px, shortcut: monospace-ish estimate, check the PNG after font changes
COLS = 3
CW = (W - 2 * PAD - LBL - 16 - GAP * (COLS - 1)) / COLS

def chips(pb, width):
    """Flow chips into rows of at most `width`; returns list of (x, y, w, node)."""
    items = sorted(uses.get(pb['id'], []), key=lambda n: (n['col'], n['label']))
    x = y = 0; res = []
    for n in items:
        w = len(n['label']) * CHAR + 2 * CH_PAD
        if x and x + w > width: x = 0; y += CH_H + 4
        res.append((x, y, w, n)); x += w + 4
    return res, (y + CH_H if items else 0)


LIGHT = dict(bg='#f6f7f5', fg='#1a2220', mut='#566360', card='#ffffff', line='#d3d8d4', sk='#6b5ba8', sc='#667370', ag='#b8456b', ex='#2f6fb0', rf='#a06a1c', chg='#d9731f', pb='#1f7a66',
             a='#e6f0ea', b='#e7edf5', c='#efe9f4', d='#f5eee1', e='#f2e7e7', f='#e9ebe9')
DARK = dict(bg='#111614', fg='#e6ece9', mut='#9aa8a3', card='#1a211f', line='#2b3532', sk='#a99bea', sc='#93a09b', ag='#ee86a8', ex='#74aef0', rf='#e0a95a', chg='#f0975a', pb='#4fc3a6',
            a='#17231f', b='#171f29', c='#201a28', d='#272015', e='#271a1a', f='#1c211f')
def palette(p):
    return (f".bg{{fill:{p['bg']}}} text{{fill:{p['fg']}}} .mut{{fill:{p['mut']}}} .card{{fill:{p['card']};stroke:{p['line']}}} .chg{{fill:{p['chg']}}}"
            + ''.join(f".band.{k}{{fill:{p[k]}}}" for k in 'abcdef')
            + ''.join(f".chip.{k}{{color:{p[k]};fill:{p[k]}}} .chip.{k} rect{{stroke:{p[k]};fill:none}} .chip.{k} text{{fill:{p[k]}}}" for k in ('sk','sc','ag','ex','rf','pb')))
STYLE = ('text{font-family:Inter,"Helvetica Neue",Arial,sans-serif}.title{font-size:22px;font-weight:600}.mut{font-size:12px}.ph{font-size:15px;font-weight:600;text-transform:capitalize}'
         '.pb{font-size:13.5px;font-weight:600}.chip text{font-size:11.5px}' + palette(LIGHT) + '@media (prefers-color-scheme:dark){' + palette(DARK) + '}')

parts = []; y = 96
for ph in PH:
    pbs = sorted([n for n in D['nodes'] if n['kind'] == 'playbook' and n['phase'] == ph], key=lambda n: D['order'][n['id']])
    cells = []
    for pb in pbs:
        ch, h = chips(pb, CW - 20)
        cells.append((pb, ch, 40 + h + 10))
    rows = [cells[i:i + COLS] for i in range(0, len(cells), COLS)]
    rh = [max(c[2] for c in r) for r in rows]
    bh = sum(rh) + GAP * (len(rows) - 1) + 24
    g = [f'<g transform="translate({PAD},{y})">',
         f'<rect class="band {TINT[ph]}" width="{W-2*PAD}" height="{bh}" rx="10"/>',
         f'<text class="ph" x="16" y="34">{escape(ph)}</text><text class="mut" x="16" y="54">{escape(NOTE[ph])}</text>']
    yy = 12
    for r, h in zip(rows, rh):
        for i, (pb, ch, _) in enumerate(r):
            cx = LBL + 16 + i * (CW + GAP)
            g.append(f'<rect class="card" x="{cx}" y="{yy}" width="{CW}" height="{h}" rx="6"/>')
            g.append(f'<text class="pb" x="{cx+10}" y="{yy+20}">{escape(pb["label"])}</text>')
            if pb['status'] == 'changed': g.append(f'<circle class="chg" cx="{cx+CW-12}" cy="{yy+15}" r="3.5"/>')
            for (x, cy, w, n) in ch:
                g.append(f'<g class="chip {KC[n["kind"]]}" transform="translate({cx+10+x},{yy+32+cy})"><rect width="{w:.0f}" height="{CH_H}" rx="4"/>'
                         f'<text x="{CH_PAD}" y="14">{escape(n["label"])}</text></g>')
        yy += h + GAP
    g.append('</g>'); parts.append('\n'.join(g)); y += bh + 12
H = y + 44
legend = [('pb', 'playbook'), ('sk', 'skill'), ('sc', 'script / reference'), ('ag', 'agent'), ('ex', 'outside rstack')]
lg = ''.join(f'<g class="chip {c}" transform="translate({PAD+i*150},{H-30})"><rect width="12" height="12" rx="3"/><text class="mut" x="18" y="10">{t}</text></g>' for i, (c, t) in enumerate(legend))
lg += f'<circle class="chg" cx="{PAD+5*150+6}" cy="{H-24}" r="4"/><text class="mut" x="{PAD+5*150+16}" y="{H-20}">changed in this plan</text>'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="rstack playbooks by phase, with the skills, scripts and tools each one uses">
<style>{STYLE}</style>
<rect class="bg" width="{W}" height="{H}"/>
<text class="title" x="{PAD}" y="42">rstack playbook map</text>
<text class="mut" x="{PAD}" y="64">Playbooks by project phase. Chips show the skills, scripts, agent and outside tools each playbook calls.</text>
{chr(10).join(parts)}
{lg}
</svg>'''
out.mkdir(parents=True, exist_ok=True)
(out / 'playbook-map.svg').write_text(svg)
if shutil.which('rsvg-convert'):
    subprocess.run(['rsvg-convert', '-w', '2400', '-b', '#f6f7f5', str(out / 'playbook-map.svg'), '-o', str(out / 'playbook-map.png')], check=True)
print('wrote', out / 'playbook-map.svg', f'{W}x{H}')
