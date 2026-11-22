import re, json, yaml
from pathlib import Path
R=Path(__file__).resolve().parents[3]
NAME=re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
def toks(t): return {x for x in re.findall(r"`([^`\n]+)`",t) if NAME.match(x) and len(x)>2}
def scripts(t): return set(re.findall(r"\b([a-z][a-z0-9_]+\.(?:py|sh|mjs))\b",t))
out={"nodes":{},"edges":[]}
def node(id,kind,stack,**k):
    n=out["nodes"].setdefault(id,{"id":id,"kind":kind,"stacks":[]}); 
    if stack not in n["stacks"]: n["stacks"].append(stack)
    n.update(k); return n
def edge(a,b,t): out["edges"].append([a,b,t])
for stack,root,mode in [("rstack",R/"rstack","research-mode")]:
    sk=root/"skills"
    bundled={p.name for p in sk.iterdir() if p.is_dir()}
    man=yaml.safe_load((sk/mode/"references/skills-manifest.yaml").read_text()) if (sk/mode/"references/skills-manifest.yaml").exists() else {}
    ext={e["name"] for e in (man or {}).get("externals",[])}
    for b in bundled:
        kind="principle" if b.startswith("principle-") else "mode" if b==mode else "skill"
        node(b,kind,stack)
    for e in ext: node("ext:"+e,"external",stack,label=e)
    pbs=sorted((sk/mode/"playbooks").glob("*.md"))
    for pb in pbs:
        pid="pb:"+pb.stem; node(pid,"playbook",stack,label=pb.stem,lines=len(pb.read_text().splitlines()))
        t=pb.read_text()
        for tk in toks(t):
            if tk in bundled and tk!=mode: edge(pid,tk,"uses")
            elif tk in ext: edge(pid,"ext:"+tk,"uses")
        for s in scripts(t): node("tool:"+s,"tool",stack,label=s); edge(pid,"tool:"+s,"runs")
        if "`critic`" in t or "critic agent" in t.lower(): node("agent:critic@"+stack,"agent",stack,label="critic"); edge(pid,"agent:critic@"+stack,"calls")
        edge("mode:"+mode,pid,"routes")
    node("mode:"+mode,"mode",stack,label=mode)
    for b in bundled:
        f=sk/b/"SKILL.md"
        if f.exists() and b!=mode:
            for tk in toks(f.read_text()):
                if tk in bundled and tk!=b and tk!=mode: edge(b,tk,"mentions")
    for s in (sk/mode/"scripts").glob("*.py"): node("tool:"+s.name,"tool",stack,label=s.name)
    for s in sk.glob("*/scripts/*.py"): node("tool:"+s.name,"tool",stack,label=s.name,owner=s.parents[1].name); edge(s.parents[1].name,"tool:"+s.name,"runs")
# states
t=(R/"rstack/skills/research-mode/SKILL.md").read_text()
rows=re.findall(r"^\| (explore|design|progressing|ready-for-publish|closed) \| [^|]* \| ([^|]*) \|",t,re.M)
stems=[p.stem for p in (R/"rstack/skills/research-mode/playbooks").glob("*.md")]
for st,pbs in rows:
    node("state:"+st,"state","rstack",label=st)
    for title in [x.strip() for x in pbs.split(",")]:
        w=set(re.findall(r"[a-z]+",title.lower()))
        for s in stems:
            if set(s.split("-"))<=w and len(set(s.split("-")))>=1 and s.split("-")==re.findall(r"[a-z]+",title.lower()): edge("state:"+st,"pb:"+s,"allows")
# overlaps
dups=sorted(n for n,v in out["nodes"].items() if len(v["stacks"])>1)
out["overlap"]=dups
seen=set(); out["edges"]=[e for e in out["edges"] if not (tuple(e) in seen or seen.add(tuple(e)))]
json.dump(out,open(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'graph.json','w'),indent=0)
from collections import Counter
print(Counter(v["kind"] for v in out["nodes"].values()), len(out["edges"]))
print("overlap",dups)
