#!/usr/bin/env python3
"""Write phase-overview.svg and phase-overview.html (diagram-design look, rstack profile) from map.data.json.
Usage: python3 export_overview.py map.data.json [out-dir]"""
import json, sys, collections
from html import escape
from pathlib import Path

D = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2] if len(sys.argv) > 2 else '.')
by = {n['id']: n for n in D['nodes']}
PH = ['explore', 'design', 'analysis', 'write', 'closed']
NOTE = {'explore': 'read the literature', 'design': 'plan the experiment', 'analysis': 'run and review', 'write': 'papers and talks', 'closed': 'after submission'}
pbs = collections.defaultdict(list)
for n in D['nodes']:
    if n['kind'] == 'playbook': pbs[n['phase']].append(n['id'])
uses = collections.defaultdict(list)
for a, b in D['edges']:
    if a in by and b in by: uses[a].append(by[b])

def plural(n):
    return '' if n == 1 else 's'

def clip(t, k=21):
    return t if len(t) <= k else t[:k - 1] + '\u2026'

def top_skills(ph, k=3):
    c = collections.Counter(n['label'] for p in pbs[ph] for n in uses[p] if n['kind'] == 'skill')
    return [f'{l}' for l, _ in c.most_common(k)]

LIGHT = dict(paper='#f4f5f3', paper2='#eceee9', ink='#1a2220', muted='#566360', soft='#5f6c68', rule='#d3d8d4', accent='#1f7a66', tint='#e3efeb')
DARK = dict(paper='#111614', paper2='#1a211f', ink='#e6ece9', muted='#9aa8a3', soft='#8b9893', rule='#2b3532', accent='#4fc3a6', tint='#16282a')
def pal(p):
    return (f".paper{{fill:{p['paper']}}} .box{{fill:{p['paper']};stroke:{p['ink']};stroke-width:1}} .acc{{fill:{p['tint']};stroke:{p['accent']};stroke-width:1.5}}"
            f" .opt{{fill:none;stroke:{p['muted']};stroke-width:1;stroke-dasharray:5 4}} .ln{{stroke:{p['muted']};stroke-width:1.2;fill:none}} .ah{{fill:{p['muted']}}}"
            f" .nm{{fill:{p['ink']}}} .sub{{fill:{p['soft']}}} .eyebrow{{fill:{p['accent']}}} .tag{{fill:{p['paper2']};stroke:{p['rule']}}}")
STYLE = ('text{font-family:Geist,"Helvetica Neue",Arial,sans-serif}.nm{font-size:15px;font-weight:600}.sub{font-family:"Geist Mono",ui-monospace,Menlo,monospace;font-size:11px}'
         '.ttl{font-family:"Instrument Serif",Georgia,serif;font-size:26px}.eyebrow{font-family:"Geist Mono",ui-monospace,monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase}'
         + pal(LIGHT) + '@media (prefers-color-scheme:dark){' + pal(DARK) + '}')

W, H, BW, GAP, X0, Y0, BH = 960, 440, 164, 20, 30, 120, 200
focal = max(PH, key=lambda p: len(pbs[p]))
g = []
for i, ph in enumerate(PH):
    x = X0 + i * (BW + GAP)
    if i: g.append(f'<line class="ln" x1="{x-GAP}" y1="{Y0+BH//2}" x2="{x-4}" y2="{Y0+BH//2}"/><polygon class="ah" points="{x-8},{Y0+BH//2-3} {x},{Y0+BH//2} {x-8},{Y0+BH//2+3}"/>')
    g.append(f'<rect class="{"acc" if ph==focal else "box"}" x="{x}" y="{Y0}" width="{BW}" height="{BH}" rx="6"/>')
    g.append(f'<rect class="tag" x="{x+12}" y="{Y0+14}" width="{len(pbs[ph]) and (86 if len(pbs[ph])>1 else 80)}" height="18" rx="2"/><text class="sub" x="{x+18}" y="{Y0+27}">{len(pbs[ph])} playbook{plural(len(pbs[ph]))}</text>')
    g.append(f'<text class="nm" x="{x+12}" y="{Y0+62}" style="text-transform:capitalize">{escape(ph)}</text>')
    g.append(f'<text class="sub" x="{x+12}" y="{Y0+80}">{escape(NOTE[ph])}</text>')
    for j, s in enumerate(top_skills(ph)):
        g.append(f'<text class="sub" x="{x+12}" y="{Y0+118+j*18}">{escape(clip(s))}</text>')
    g.append(f'<text class="sub" x="{x+12}" y="{Y0+104}" style="letter-spacing:.08em;text-transform:uppercase;font-size:9px">common skills</text>')
ay = Y0 + BH + 30
wx = X0
ww = 5 * BW + 4 * GAP
g.append(f'<rect class="opt" x="{wx}" y="{ay}" width="{ww}" height="64" rx="6"/>')
g.append(f'<text class="nm" x="{wx+16}" y="{ay+27}">Any phase</text>')
g.append(f'<text class="sub" x="{wx+16}" y="{ay+47}">{" · ".join(by[p]["label"] for p in pbs["any phase"])}</text>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="overview-title overview-desc">
<title id="overview-title">rstack phases</title>
<desc id="overview-desc">A project moves through explore, design, analysis, write and closed; four more playbooks can run in any phase.</desc>
<style>{STYLE}</style>
<rect class="paper" width="{W}" height="{H}"/>
<text class="eyebrow" x="{X0}" y="40">Overview · rstack</text>
<text class="ttl nm" x="{X0}" y="76" style="font-weight:400">A project, phase by phase</text>
{chr(10).join(g)}
</svg>'''
out.mkdir(parents=True, exist_ok=True)
(out / 'phase-overview.svg').write_text(svg)
(out / 'phase-overview.html').write_text(f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>rstack phases</title><link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Geist:wght@400;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>body{{margin:0;padding:2rem;background:{LIGHT['paper']}}}@media (prefers-color-scheme:dark){{body{{background:{DARK['paper']}}}}}.diagram-container{{width:100%;overflow-x:auto}}svg{{min-width:960px;width:100%;display:block}}</style></head>
<body><div class="diagram-container">{svg}</div></body></html>''')
print('wrote', out / 'phase-overview.svg')
