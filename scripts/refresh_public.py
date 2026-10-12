#!/usr/bin/env python3
"""Update only the public-repository feed in the GitHub profile README.

Source: GitHub public user-repositories API. Never lists private repositories.
The separately curated GitHub pinned projects are not changed by this script.
"""
import argparse
import html
import json
import os
from pathlib import Path
import re
import urllib.request

ACCOUNT = "virat-kumar"
START = "<!-- LATEST_PUBLIC_START -->"
END = "<!-- LATEST_PUBLIC_END -->"
ROOT = Path(__file__).resolve().parents[1]

def fetch_public():
    url = f"https://api.github.com/users/{ACCOUNT}/repos?type=owner&per_page=100&sort=pushed&direction=desc"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "virat-kumar-public-profile"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
        records = json.load(response)
    if not isinstance(records, list):
        raise ValueError("GitHub did not return a public repository list")
    records = [r for r in records
        if r.get("private") is False
        and r.get("owner", {}).get("login", "").lower() == ACCOUNT
        and r.get("name", "").lower() != ACCOUNT
        and r.get("html_url", "").startswith(f"https://github.com/{ACCOUNT}/")]
    records.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    return records[:3]

def markdown(records):
    rows = ["| Latest public repositories | Last updated (UTC) | What it contains |",
            "|---|---|---|"]
    for repo in records:
        name = html.escape(repo["name"])
        url = repo["html_url"]
        when = (repo.get("pushed_at") or "")[:10] or "Unknown"
        note = (repo.get("description") or "Public source repository").strip()
        note = re.sub(r"\s+", " ", note)
        note = html.escape(note.replace("|", "/"))[:115]
        if repo.get("fork"):
            note += " (fork)"
        rows.append(f"| [{name}]({url}) | {when} | {note} |")
    return "\n".join(rows)

def refresh(path, records, check=False):
    original = path.read_text(encoding="utf-8")
    if original.count(START) != 1 or original.count(END) != 1:
        raise ValueError("Missing or duplicate README refresh markers")
    before, tail = original.split(START, 1)
    _, after = tail.split(END, 1)
    desired = before + START + "\n" + markdown(records) + "\n" + END + after
    if check:
        if desired != original:
            raise SystemExit("README latest-public section is stale")
        print("PASS latest public section current")
        return
    if desired != original:
        path.write_text(desired, encoding="utf-8")
        print("Updated latest-public section")
    else:
        print("No changes to latest-public section")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    refresh(ROOT / "README.md", fetch_public(), args.check)
