#!/usr/bin/env python3
"""Refresh source-backed, non-fork GitHub profile metrics and SVG cards."""

from __future__ import annotations

import html
import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_portfolio import GROUPS, group_for, main as build_portfolio  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "profile"
API = "https://api.github.com/users/AAH20/repos?type=owner&per_page=100&page={}"
DOMAIN_KPIS = {
    "Commerce, revenue, and customer operations": ("Incident precision (%)", "Reviewer minutes / 100 SKUs"),
    "Cloud, platform engineering, and reliability": ("Unsafe-change escape rate (%)", "Verified rollback time (min)"),
    "GPU, model serving, and AI economics": ("p95 first-token latency (ms)", "Cost / 1M accepted tokens (USD)"),
    "Marketing, audiences, and growth": ("Incremental contribution / $ spent", "Experiment CI width (pp)"),
    "Physical AI, robotics, and biometrics": ("Missed unsafe action rate (%)", "Evidence loss rate (%)"),
    "AI agents: runtime, security, identity, and governance": ("Unauthorized action pass rate (%)", "False-denial rate (%)"),
    "Data, simulation, and decision systems": ("Data freshness lag p95 (s)", "Decision regret vs baseline (%)"),
    "Other original projects": ("Project-specific protocol", "Linked source evidence"),
}


def fetch_repositories() -> list[dict]:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "AAH20-profile-metrics"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    repos = []
    for page in range(1, 21):
        request = urllib.request.Request(API.format(page), headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError("GitHub API did not return a repository list")
        repos.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise ValueError("Repository pagination exceeded the declared bound")
    originals = [
        r for r in repos
        if r.get("owner", {}).get("login", "").lower() == "aah20"
        and not r.get("fork") and not r.get("private")
    ]
    if not originals or len({r["name"].lower() for r in originals}) != len(originals):
        raise ValueError("Empty or duplicate public-original repository inventory")
    return originals


def summarize(repos: list[dict], now: datetime) -> dict:
    cutoff = now - timedelta(days=30)
    domains: dict[str, list[dict]] = defaultdict(list)
    for repo in repos:
        domains[group_for(repo["name"])].append(repo)
    ordered = [name for name, _, _ in GROUPS] + ["Other original projects"]
    result = {
        "generated_at_utc": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": "https://api.github.com/users/AAH20/repos",
        "definitions": {
            "public_original": "Public repository owned by AAH20 with fork=false; archived repositories remain included.",
            "pushed_30d": "Repository pushed_at timestamp within the preceding 30 days; this is activity, not production adoption.",
            "stars": "Sum of current stargazers_count across public originals; not unique people or product users.",
            "forks": "Sum of current forks_count across public originals.",
        },
        "total": len(repos),
        "pushed_30d": sum(datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")) >= cutoff for r in repos),
        "stars": sum(int(r.get("stargazers_count", 0)) for r in repos),
        "forks": sum(int(r.get("forks_count", 0)) for r in repos),
        "domains": [],
    }
    for name in ordered:
        items = domains.get(name, [])
        if not items:
            continue
        result["domains"].append({
            "name": name,
            "count": len(items),
            "pushed_30d": sum(datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")) >= cutoff for r in items),
            "stars": sum(int(r.get("stargazers_count", 0)) for r in items),
            "kpis": DOMAIN_KPIS[name],
        })
    return result


def svg(width: int, height: int, content: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        '<style>text{font-family:Arial,Helvetica,sans-serif} .title{fill:#f8fafc;font-size:22px;font-weight:700}'
        '.label{fill:#cbd5e1;font-size:14px}.value{fill:#67e8f9;font-size:30px;font-weight:700}'
        '.small{fill:#a7b6c9;font-size:12px}.kpi{fill:#e2e8f0;font-size:15px}</style>'
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="#0b1629" stroke="#36516f"/>'
        f'{content}</svg>'
    )


def text(x: int, y: int, value: str, css: str) -> str:
    return f'<text x="{x}" y="{y}" class="{css}">{html.escape(str(value))}</text>'


def render_overview(summary: dict) -> str:
    parts = [text(28, 37, "PUBLIC ORIGINAL REPOSITORIES · LIVE GITHUB INVENTORY", "title")]
    for x, value, label in [
        (30, summary["total"], "public originals"),
        (270, summary["pushed_30d"], "pushed in 30 days"),
        (510, summary["stars"], "repository stars"),
        (750, summary["forks"], "repository forks"),
    ]:
        parts += [text(x, 97, value, "value"), text(x, 120, label, "label")]
    parts.append(text(28, 162, f'GitHub REST refresh: {summary["generated_at_utc"]} · Public non-forks only · Activity and attention are not adoption', "small"))
    return svg(980, 180, "".join(parts))


def render_domain(domain: dict, refreshed: str) -> str:
    k1, k2 = domain["kpis"]
    parts = [
        text(25, 37, domain["name"], "title"),
        text(27, 85, domain["count"], "value"), text(100, 83, "original repos", "label"),
        text(325, 85, domain["pushed_30d"], "value"), text(395, 83, "pushed / 30d", "label"),
        text(615, 85, domain["stars"], "value"), text(690, 83, "stars", "label"),
        text(27, 124, "Benchmark axes:", "small"),
        text(27, 148, f"{k1}  ·  {k2}", "kpi"),
        text(27, 177, f"KPI definitions, not measured outcomes · Refreshed {refreshed}", "small"),
    ]
    return svg(980, 196, "".join(parts))


def slug(name: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def write_outputs(repos: list[dict], summary: dict) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    inventory = [{"name": r["name"], "public": True, "fork": False} for r in sorted(repos, key=lambda r: r["name"].lower())]
    (ROOT / "data/public-original-repositories.json").write_text(json.dumps(inventory, indent=2) + "\n")
    (ROOT / "data/profile-metrics.json").write_text(json.dumps(summary, indent=2) + "\n")
    (ASSETS / "overview.svg").write_text(render_overview(summary))
    for domain in summary["domains"]:
        (ASSETS / f'{slug(domain["name"])}.svg').write_text(render_domain(domain, summary["generated_at_utc"]))
    build_portfolio()


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    repos = fetch_repositories()
    summary = summarize(repos, now)
    write_outputs(repos, summary)
    print(f'Updated {summary["total"]} public originals across {len(summary["domains"])} domains')
