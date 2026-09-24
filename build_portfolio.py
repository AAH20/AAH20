#!/usr/bin/env python3
"""Build a directory of verified public, non-fork AAH20 repositories."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "data" / "public-original-repositories.json"
METRICS = ROOT / "data" / "profile-metrics.json"
OUTPUT = ROOT / "PORTFOLIO.md"

GROUPS = [
    ("Commerce, revenue, and customer operations", r"commerce|merchant|order-to-cash|payment-fraud|resolution|liveops|implementation-exchange|agent-hire|entity-continuity|vendor-assurance|trusted-community|auto.?parts|chatflux", "Shopify and merchant operations, order-to-cash reconciliation, customer support automation, and revenue assurance."),
    ("GPU, model serving, and AI economics", r"gpu|inference|nvidia|vllm|llm|runproof|worldops|tensor|kv-compress|green-inference|scale-ai|stream-fusion|neurospark|data-platform|eval-lake", "LLM inference benchmarking, GPU cost estimation, model serving, AI factory capacity, and deployment economics."),
    ("Cloud, platform engineering, and reliability", r"azure|cloud|infrastructure|kubernetes|network|devops|sre|aiops|multicloud|platform|autoprod|millionready|ghost-fork|vibeguard|otforge|fde-bounty|resilience|sap|m-a-technology", "Azure migration, Kubernetes operations, Infrastructure as Code, cloud reliability, FinOps, and platform engineering."),
    ("Marketing, audiences, and growth", r"audience|attention|growth|viral|geo-engine|creative|causal|rtb|bonding|churn|flywheel|belief|narrative|strategy|elasticity|portfolio|generative-plg|zk-cleanroom|chrono-arbitrage", "Marketing measurement, incrementality testing, synthetic audiences, recommendations, customer retention, and growth experiments."),
    ("Physical AI, robotics, and biometrics", r"physical|robot|cyborg|bio|neuro|kinetic|fleet|sky|edge-vision|chrono-twin|industrial|supply-chain|zero-shot|ieee11073", "Robot evaluation, physical AI black boxes, digital twins, biometric privacy, and industrial simulation."),
    ("AI agents: runtime, security, identity, and governance", r"agent|aegis|grc|compliance|trust|identity|mcp|effect|vuln|security|redteam|killchain|veritas|pqc|pqattest|postquantum|zero-leak|gitleaks|vdr|evidence|permissioned|graph-rag-guard|bft|kernel", "AI agent security, MCP testing, authorization, observability, evaluation, identity, and governance evidence."),
    ("Data, simulation, and decision systems", r"data|decision|swarm|context|hyper|project-atlas|due-diligence|outcome|real-time|video-template|pythondefi|metamask|cakewallet|trust-wallet", "Data engineering, simulation, decision support, business outcomes, and technical research."),
]

OVERRIDES = {
    "adversarial-nexus": "AI agents: runtime, security, identity, and governance",
    "ai-factory-revenue-twin": "GPU, model serving, and AI economics",
    "ai-ran-profitability-autopilot": "GPU, model serving, and AI economics",
    "enterprise-ai-production-control-plane": "Cloud, platform engineering, and reliability",
    "intel-pulse": "AI agents: runtime, security, identity, and governance",
    "opensearch-sovereign-vciso-control-plane": "AI agents: runtime, security, identity, and governance",
    "opentelemetry-ai-valueops-collector": "Data, simulation, and decision systems",
    "vector-index-sanitizer": "AI agents: runtime, security, identity, and governance",
    "wazuh-elastic-sovereign-vciso-control-plane": "AI agents: runtime, security, identity, and governance",
}


def group_for(name: str) -> str:
    lower = name.lower()
    if lower in OVERRIDES:
        return OVERRIDES[lower]
    for group, pattern, _ in GROUPS:
        if re.search(pattern, lower):
            return group
    return "Other original projects"


def main() -> None:
    repos = json.loads(SNAPSHOT.read_text())
    captured = json.loads(METRICS.read_text())["generated_at_utc"][:10] if METRICS.exists() else "2026-09-24"
    assert len(repos) == len({repo["name"].lower() for repo in repos})
    assert all(repo["public"] and not repo["fork"] for repo in repos)
    grouped = defaultdict(list)
    for repo in repos:
        grouped[group_for(repo["name"])].append(repo)

    lines = [
        "# Public original project directory",
        "",
        f"This directory covers **{len(repos)} public repositories created under AAH20** in the GitHub inventory refreshed on {captured}. Forks and private repositories are excluded.",
        "",
        "Browse by the problem you are trying to solve. Repository pages state their own implementation and evidence limits; a listing here is not a production-readiness claim. The category labels are navigation aids, not measured search-volume claims.",
        "",
        "[Profile and live portfolio stats](README.md#live-github-portfolio-telemetry) · [Benchmark protocols](BENCHMARKS.md)",
        "",
    ]
    for group, _, description in GROUPS:
        items = sorted(grouped.pop(group, []), key=lambda r: r["name"].lower())
        if not items:
            continue
        lines += [f"## {group}", "", f"**{len(items)} repositories.** {description}", ""]
        for repo in items:
            name = repo["name"]
            lines.append(f"- [{name}](https://github.com/AAH20/{name})")
        lines.append("")
    other = sorted(grouped.pop("Other original projects", []), key=lambda r: r["name"].lower())
    if other:
        lines += ["## Other original projects", "", f"**{len(other)} repositories.**", ""]
        lines += [f"- [{r['name']}](https://github.com/AAH20/{r['name']})" for r in other]
        lines.append("")
    assert not grouped
    OUTPUT.write_text("\n".join(lines))
    print(f"Wrote {OUTPUT} with {len(repos)} unique public originals")


if __name__ == "__main__":
    main()
