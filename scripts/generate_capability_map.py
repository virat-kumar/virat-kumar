#!/usr/bin/env python3
"""Render an editable self-contained capability-map SVG for GitHub Markdown."""
from pathlib import Path
from xml.etree import ElementTree as ET

OUT=Path(__file__).resolve().parents[1]/"assets/capability-map.svg"
W,H=1180,823
BG="#0d1117"; PANEL="#151b23"; STROKE="#30363d"; WHITE="#f0f6fc"; MUTED="#a4adb9"
GROUPS=[
 ("Generative AI & Agents",44,160,350,224,"#3b82f6",[
   "Azure OpenAI / LLM solutions","RAG / GraphRAG / AI Search","Agentic workflows and MCP","LangChain / Semantic Kernel","LLMOps / fine-tuning / eval"]),
 ("Azure & Cloud Data",415,160,350,224,"#22c55e",[
   "Microsoft Azure & Fabric","Azure Databricks / SQL","PySpark / Delta Lake","Entra ID / Key Vault / APIM","SharePoint & Teams copilots"]),
 ("Machine Learning & MLOps",786,160,350,224,"#eab308",[
   "Machine learning / NLP","Transformers, BERT and NER","Multimodal AI / computer vision","MLflow / model workflows","Document intelligence / pipelines"]),
 ("Software Engineering & Architecture",44,409,535,222,"#a78bfa",[
   "Python / FastAPI / REST APIs","Software & solution architecture","TypeScript / React applications","Git, CI/CD and GitHub Actions","System design / integrations"]),
 ("Linux, Containers & Observability",601,409,535,222,"#fb7185",[
   "Ubuntu Linux / Bash / systemd","Docker / Compose / local inference","Tailscale and private networking","MCP servers / browser automation","Monitoring / telemetry / WebRTC"])
]
def add(parent,tag,attrs=None,text=None):
    el=ET.SubElement(parent,tag,attrs or {})
    if text is not None: el.text=text
    return el
def label(parent,x,y,value,size=18,bold=False,color=WHITE,align=None):
    attrs={"x":str(x),"y":str(y),"font-family":"DejaVu Sans, Arial, Helvetica, sans-serif",
           "font-size":str(size),"font-weight":"700" if bold else "400","fill":color}
    if align:attrs["text-anchor"]=align
    return add(parent,"text",attrs,value)
r=ET.Element("svg",{"xmlns":"http://www.w3.org/2000/svg","viewBox":f"0 0 {W} {H}","width":str(W),
    "height":str(H),"role":"img","aria-labelledby":"capability-title capability-description"})
add(r,"title",{"id":"capability-title"},"Virat Kumar: GenAI engineering capability map")
add(r,"desc",{"id":"capability-description"},"Five colored panels describing generative AI and agents, Azure and cloud data platforms, machine learning and MLOps, software engineering and architecture, Linux containers and observability. Programming and scripting languages include Python, SQL, Go, JavaScript, TypeScript, Bash, R and HTML/CSS.")
add(r,"rect",{"x":"1","y":"1","width":str(W-2),"height":str(H-2),"rx":"19","fill":BG,"stroke":STROKE,"stroke-width":"2"})
label(r,44,65,"Engineering capability map",34,True)
label(r,44,102,"GenAI first   /   Cloud to production   /   Software and infrastructure",18,False,MUTED)
add(r,"rect",{"x":"44","y":"126","width":"1092","height":"2","fill":"#27323e"})
for title,x,y,w,h,color,skills in GROUPS:
    add(r,"rect",{"x":str(x),"y":str(y),"width":str(w),"height":str(h),"rx":"13","fill":PANEL,
                  "stroke":STROKE,"stroke-width":"1.4"})
    add(r,"rect",{"x":str(x),"y":str(y),"width":str(w),"height":"6","rx":"3","fill":color})
    label(r,x+23,y+48,title,22,True)
    for j,skill in enumerate(skills):
        yy=y+85+j*29
        add(r,"circle",{"cx":str(x+26),"cy":str(yy-6),"r":"4.5","fill":color})
        label(r,x+41,yy,skill,17)
add(r,"rect",{"x":"44","y":"654","width":"1092","height":"130","rx":"13",
              "fill":PANEL,"stroke":STROKE,"stroke-width":"1.4"})
add(r,"rect",{"x":"44","y":"654","width":"1092","height":"6","rx":"3","fill":"#38bdf8"})
label(r,66,698,"Programming and scripting languages",23,True)
items=[("Python",114),("SQL",88),("Go",70),("JavaScript",150),
       ("TypeScript",152),("Bash / Shell",150),("R",60),("HTML / CSS",143)]
pos=66
for text,w in items:
    add(r,"rect",{"x":str(pos),"y":"717","width":str(w),"height":"44","rx":"9",
                  "fill":"#222d3d","stroke":"#355169"})
    label(r,pos+w/2,746,text,16,True,"#cbe9ff","middle")
    pos+=w+10
ET.indent(r,"  ")
OUT.write_bytes(ET.tostring(r,encoding="utf-8",xml_declaration=True))
print(f"generated {OUT.name} ({OUT.stat().st_size} bytes)")
