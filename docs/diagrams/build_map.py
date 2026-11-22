import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[3]
g=json.load(open('graph.json')); N=g['nodes']; E=g['edges']
PH={'explore':['literature-review','report-bootstrap'],
'design':['experimental-design','experiment-log'],
'analysis':['raw-intake','analysis-plan','analysis-run','analysis-review','hillclimb','reproduce','package-results'],
'write':['paper-preparation','paper-writing','paper-critique','presentation','peer-review'],
'closed':['reviewer-response'],
'any phase':['inquiry','protocol-wiki','project-admin','authoring-a-skill']}
MERGE={'project-docs':'project-admin','state-review':'project-admin'}
MOVING_PB=set()
MOVING_SK=set()
MOVING_TOOL=set()
EXT_SKILLS={'doc-coauthoring','deep-research','scholar-evaluation','neurokit2','lab-hardware-cad','analytical-method-validation','iso-standards-readiness'}
REMAP={'ext:citation-management':'citation-management','ext:skill-creator':'skill-creator','ext:arena':'arena','ext:swarm':'swarm','ext:hyperresearch':'xt:hyperresearch'}
EXT_TOOLS={'raw-viewer':'raw-viewer CLI and plugin','figrecipe':'tools/figrecipe (Python env)','todoist':'Todoist (MCP)','zotero-cli':'Zotero (zotero-cli, MCP)','hyperresearch':'hyperresearch CLI','obsidian':'Obsidian','beamer':'LaTeX toolchain (latexmk, BibTeX, Beamer)'}
SCRIPTS={'writing.py','number_check.py','check_layout.py','check_map.py','rstack_run.py','verify_playbook.py','raw_intake.py','sync_readme_tasks.py','check_references.py','zotero_snapshot.py','inquiry_extract.py','render_diagram.mjs','reproduce.py','check_plugin.py'}|MOVING_TOOL
nodes={}; edges=set()
def add(id,label,kind,col,status,detail='',phase=None):
    nodes[id]={'id':id,'label':label,'kind':kind,'col':col,'status':status,'detail':detail,'phase':phase}
for ph in PH: add('ph:'+ph,ph,'phase',0,'existing','')
nodes['ph:write']['status']='changed'; nodes['ph:write']['detail']='Fourth phase, replaces ready-for-publish.'
nodes['ph:analysis']['detail']='Renamed from progressing (old name kept as an alias).'
nodes['ph:closed']['detail']='Reviewer response after submission.'
nodes['ph:any phase']['detail']='Playbooks any phase bot can use.'
for ph,pbs in PH.items():
    for p in pbs:
        st='moving' if p in MOVING_PB else 'changed' if p in('experiment-log','project-admin','paper-preparation','paper-writing','paper-critique','presentation','report-bootstrap','literature-review','inquiry','experimental-design') else 'existing'
        add('pb:'+p,p,'playbook',1,st,{'experiment-log':'Records what was done as run (samples, deviations) in method/log.md of the question folder, against the frozen design.','package-results':'Last analysis playbook (was in ready-for-publish).','project-admin':'Router: Tasks advisor (reads Todoist, advises, records in docs/rstack), Docs, Exit review, phase brief, phase change. Merges project-docs, state-review and task-tracking.','protocol-wiki':'Thin: read wiki/CLAUDE.md, follow its router, write pages with doc-coauthoring.','report-bootstrap':'Renamed from proposal-synthesis. Writes 04 and 05, then opens docs/reports/<question>/ with README (intention, hypotheses, plan) and fundamental/README. Method and results come from other playbooks.','literature-review':'Thin wrapper: runs /hyperresearch on the inquiry, symlinks the final report into docs/literature-review/.','inquiry':'Wiki, interview and brainstorm before any search; then aligns the user\'s reading of chosen papers.','experimental-design':'Runs Inquiry first (wiki, interview, brainstorm, interrogate), then writes a self-contained method/design.md (no wiki links), resources.md, samples.csv in the question folder. Reads the wiki only through Inquiry.'}.get(p,''),ph)
        edges.add(('ph:'+ph,'pb:'+p))
text={}
for d in [R/'rstack/skills/research-mode/playbooks']:
    for f in d.glob('*.md'):
        if True:
            k=MERGE.get(f.stem,f.stem); text[k]=text.get(k,'')+f.read_text()
skills_dir={p.name for p in (R/'rstack/skills').iterdir() if p.is_dir()}|MOVING_SK
for a,b,t in E:
    if not a.startswith('pb:') or t not in('uses','runs','calls'): continue
    p=MERGE.get(a[3:],a[3:]); a='pb:'+p
    if 'pb:'+p not in nodes: continue
    b=REMAP.get(b,b)
    if b.startswith('principle-'): continue
    if b.startswith('ext:'):
        n=b[4:]
        if n in EXT_SKILLS:
            nodes.setdefault('xs:'+n,{'id':'xs:'+n,'label':n,'kind':'external skill','col':3,'status':'external','detail':'Install globally (a skill from another source).','phase':None}); edges.add((a,'xs:'+n))
        continue
    if b.startswith('tool:'):
        s=b[5:]
        if s in SCRIPTS:
            st='moving' if s in MOVING_TOOL else 'existing'
            nodes.setdefault('sc:'+s,{'id':'sc:'+s,'label':s,'kind':'script','col':4,'status':st,'detail':'','phase':None}); edges.add((a,'sc:'+s))
        continue
    if b.startswith('agent:'):
        nodes.setdefault('ag:critic',{'id':'ag:critic','label':'critic (agent)','kind':'agent','col':4,'status':'existing','detail':'One agent, six modes: source analysis, analysis run, reader, evidence, referee, prose.','phase':None}); edges.add((a,'ag:critic')); continue
    if b=='xt:hyperresearch': continue
    if b in skills_dir:
        st='moving' if b in MOVING_SK else 'existing'
        nodes.setdefault('sk:'+b,{'id':'sk:'+b,'label':b,'kind':'skill','col':2,'status':st,'detail':'','phase':None}); edges.add((a,'sk:'+b))
# external tools by text mention
for p,t in text.items():
    if 'pb:'+p not in nodes: continue
    for k,lab in EXT_TOOLS.items():
        if k=='openalex': continue
        if re.search(k,t,re.I):
            nodes.setdefault('xt:'+k,{'id':'xt:'+k,'label':lab,'kind':'external tool','col':3,'status':'external','detail':'Install separately (not a skill).','phase':None}); edges.add(('pb:'+p,'xt:'+k))
# project-docs holds a catalogue table of skills per state; that is not use, so keep only real links
KEEP_PA={'sk:interrogate','sc:check_references.py'}
edges={e for e in edges if e[0]!='pb:project-admin' or e[1] in KEEP_PA}
for k in ('literature-review','inquiry'):
    edges.add(('pb:'+k,'sk:obsidian-notes'))
# obsidian-writing becomes a skill
nodes['sk:obsidian-notes']={'id':'sk:obsidian-notes','label':'obsidian-notes','kind':'skill','col':2,'status':'changed','detail':'Was the obsidian-writing playbook. Style for notes the user reads and comments on in Obsidian. Its place-it step moves into layout.md. Linked from literature-review and inquiry, which write paper READMEs, alignments and cross-paper notes.','phase':None}
for k,t in text.items():
    if 'pb:'+k in nodes and re.search('obsidian',t,re.I) and k!='authoring-a-skill': edges.add(('pb:'+k,'sk:obsidian-notes'))
for sc in ('check_references.py','render_diagram.mjs'):
    if 'sc:'+sc in nodes: edges.add(('sk:obsidian-notes','sc:'+sc))
# workspace folders and new items
nodes['wf:wiki']={'id':'wf:wiki','label':'wiki/ (workspace folder)','kind':'workspace folder','col':3,'status':'external','detail':'Reusable protocol knowledge, own git repo and router wiki/CLAUDE.md. Only protocol-wiki writes it; design reads it.','phase':None}
nodes['wf:tools']={'id':'wf:tools','label':'tools/ (workspace folder)','kind':'workspace folder','col':3,'status':'external','detail':'Installed tools: figrecipe, paperflow, xps-fitting-workbench, RamanAnalyzer, labview. Needs tools/README.md: tool, entry command, which playbook uses it.','phase':None}
for k,t in text.items():
    if 'pb:'+k not in nodes: continue
    if re.search(r'\bwiki/',t): edges.add(('pb:'+k,'wf:wiki'))
    if re.search(r'\btools/',t): edges.add(('pb:'+k,'wf:tools'))
nodes['sc:layout.md']={'id':'sc:layout.md','label':'layout.md (folder table)','kind':'reference','col':4,'status':'changed','detail':'One table: path, what it holds, which playbook writes it, read-only or not. A report folder holds fundamental/, method/, results/ and the evidence files. Every playbook opens with Reads / Writes taken from it.','phase':None}
nodes['sc:check_layout.py']={'id':'sc:check_layout.py','label':'check_layout.py','kind':'script','col':4,'status':'changed','detail':'Flags unknown folders in a project, such as a stray manuscripts/.','phase':None}
edges.add(('pb:project-admin','sc:layout.md')); edges.add(('pb:project-admin','sc:check_layout.py'))
nodes['sc:check_map.py']={'id':'sc:check_map.py','label':'check_map.py','kind':'script','col':4,'status':'changed','detail':'Offline check that tasks.md and the Todoist map agree (no nested tasks, every open task has a map row).','phase':None}
edges.add(('pb:project-admin','sc:check_map.py'))
nodes['sk:setup-research']={'id':'sk:setup-research','label':'setup-research','kind':'skill','col':2,'status':'changed','detail':'Now reports missing external skills and tools from the manifest and tools/README.md.','phase':None}
edges.add(('pb:project-admin','sk:setup-research'))
# verifier (hook) ties to four playbooks
add('sc:verify_playbook.py','verify_playbook.py','script',4,'existing','Stop hook that checks each playbook\'s Done-when list.') if 'sc:verify_playbook.py' not in nodes else None
if 'sc:number_check.py' in nodes: nodes['sc:number_check.py']['detail']='Checks numbers, units and citation keys against the report.'
for n in nodes.values():
    if n['id'].startswith('xs:') and not any(b==n['id'] for a,b in edges): n['detail']='Optional domain skill, named in the per-state skill table of project-admin. Install only if the project needs it.'
# order: playbooks fixed, others by barycenter
order=[p for ph in PH for p in PH[ph]]
y={}
for i,p in enumerate(order): y['pb:'+p]=i
for ph in PH:
    ys=[y['pb:'+p] for p in PH[ph]]; y['ph:'+ph]=sum(ys)/len(ys)
adj={}
for a,b in edges: adj.setdefault(b,[]).append(a)
for c in (2,3,4):
    items=[n for n in nodes.values() if n['col']==c]
    for n in items:
        ps=[y[a] for a in adj.get(n['id'],[]) if a.startswith('pb:')]
        n['bary']=sum(ps)/len(ps) if ps else 99
    items.sort(key=lambda n:(n['kind']!='external skill' if c==3 else 0,n['bary'],n['label']))
    for i,n in enumerate(items): y[n['id']]=i
out={'nodes':list(nodes.values()),'edges':[list(e) for e in edges],'order':y}
import collections
print(collections.Counter((n['col'],n['status']) for n in nodes.values()),len(edges))
json.dump(out,open('map.data.json','w'),indent=1)
html=open(Path(__file__).with_name('map_template.html')).read().replace('/*DATA*/',json.dumps(out,separators=(',',':')))
open('map2.html','w').write(html)
