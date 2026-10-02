#!/usr/bin/env python3
"""Create missing GitHub Pages site objects without replacing existing sites.

Authority:
  GET  /repos/{owner}/{repo}/pages
Repair:
  POST /repos/{owner}/{repo}/pages {"build_type":"workflow"}

API version: 2026-03-10

Requires PAGES_ADMIN_TOKEN with access to the listed repositories and
Pages(write) + Administration(write), or an equivalent classic-token scope.
Existing Pages sites are read and left unchanged.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

OWNER="redogit"
API_VERSION="2026-03-10"
REPOSITORIES=[
    "orbit","MauiBrickBreak","redogit","DnD","FirstNeuralNetwork",
    "conscience64","Dream-To-Action","Other-Projects-",
    "RMAL","pnp-dean","hodge","conscience64-platform",
    "games","language-carriers","archives-knowledge","portfolio",
]

token=os.environ.get("PAGES_ADMIN_TOKEN","").strip()
if not token:
    raise SystemExit("PAGES_ADMIN_TOKEN is required; do not place tokens in source or logs.")

HEADERS={
    "Accept":"application/vnd.github+json",
    "Authorization":f"Bearer {token}",
    "X-GitHub-Api-Version":API_VERSION,
    "User-Agent":"redogit-pages-bootstrap",
}

def call(repo:str, method:str="GET", body:dict|None=None):
    url=f"https://api.github.com/repos/{OWNER}/{repo}/pages"
    data=None if body is None else json.dumps(body).encode("utf-8")
    req=urllib.request.Request(url,data=data,headers=HEADERS,method=method)
    try:
        with urllib.request.urlopen(req,timeout=30) as response:
            raw=response.read()
            payload=json.loads(raw) if raw else None
            return response.status,payload
    except urllib.error.HTTPError as exc:
        raw=exc.read().decode("utf-8","replace")
        try: payload=json.loads(raw)
        except Exception: payload={"message":raw}
        return exc.code,payload

results=[]
for repo in REPOSITORIES:
    status,payload=call(repo)
    if status==200:
        results.append({
            "repository":f"{OWNER}/{repo}",
            "action":"preserved",
            "http_status":status,
            "html_url":payload.get("html_url") if isinstance(payload,dict) else None,
            "build_type":payload.get("build_type") if isinstance(payload,dict) else None,
            "source":payload.get("source") if isinstance(payload,dict) else None,
        })
        continue
    if status!=404:
        results.append({"repository":f"{OWNER}/{repo}","action":"error","http_status":status,"response":payload})
        continue

    create_status,created=call(repo,"POST",{"build_type":"workflow"})
    if create_status in (201,409):
        verify_status,verified=call(repo)
        results.append({
            "repository":f"{OWNER}/{repo}",
            "action":"created" if create_status==201 else "already-created-concurrently",
            "http_status":create_status,
            "verify_status":verify_status,
            "html_url":verified.get("html_url") if isinstance(verified,dict) else None,
            "build_type":verified.get("build_type") if isinstance(verified,dict) else None,
        })
    else:
        results.append({"repository":f"{OWNER}/{repo}","action":"error","http_status":create_status,"response":created})

summary={
    "schema":"redogit/github-pages-bootstrap/v1",
    "api_version":API_VERSION,
    "owner":OWNER,
    "results":results,
    "counts":{
        "preserved":sum(r["action"]=="preserved" for r in results),
        "created":sum(r["action"] in ("created","already-created-concurrently") for r in results),
        "errors":sum(r["action"]=="error" for r in results),
        "total":len(results),
    },
}
print(json.dumps(summary,indent=2,sort_keys=True))
sys.exit(1 if summary["counts"]["errors"] else 0)
