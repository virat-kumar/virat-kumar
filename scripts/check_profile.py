#!/usr/bin/env python3
"""Static privacy, factual-history and visual coverage checks for the public profile."""
from pathlib import Path
import re
from xml.etree import ElementTree
ROOT=Path(__file__).resolve().parents[1]
readme=(ROOT/"README.md").read_text()
svg=ROOT/"assets/capability-map.svg"
root=ElementTree.parse(svg).getroot()
for term in ["Generative AI", "Azure OpenAI", "Azure AI Search", "Databricks",
             "Microsoft Fabric", "LangChain", "Semantic Kernel", "Docker",
             "Linux", "Software Engineering", "Architecture", "Python", "Go",
             "TypeScript", "Bash", "R"]:
    assert term.lower() in (readme+" "+svg.read_text()).lower(),term
assert "Boston Consulting Group" in readme and "concluded in August 2026" in readme
assert "Boston Consulting Group" not in readme.split("### About me")[0]
assert readme.count("<!-- LATEST_PUBLIC_START -->")==1
assert readme.count("<!-- LATEST_PUBLIC_END -->")==1
assert "assets/hero.svg" in readme
assert svg.stat().st_size > 4000
assert "capability" in root.find("{http://www.w3.org/2000/svg}title").text.lower()
for private in ["/home/virat/",".env","PRIVATE KEY","tailac2e85","Marquis at Waterview"]:
    assert private not in readme, f"Unexpected potentially sensitive reference: {private}"
links=re.findall(r"\]\((https://github.com/virat-kumar/[^)]+)\)",readme)
assert len(links)>=8
print(f"PASS: privacy, dated BCG history, capabilities, SVG and {len(links)} links")
