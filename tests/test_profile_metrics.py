import unittest
from datetime import datetime, timezone

from scripts.update_profile_metrics import render_domain, render_overview, slug, summarize


class ProfileMetricsTests(unittest.TestCase):
    def test_counts_only_supplied_originals_and_keeps_domain_separation(self):
        repos = [
            {"name": "commerce-incident-network", "pushed_at": "2026-09-23T00:00:00Z", "stargazers_count": 2, "forks_count": 1},
            {"name": "gpu-cloud-cost-calculator", "pushed_at": "2026-07-01T00:00:00Z", "stargazers_count": 3, "forks_count": 0},
        ]
        result = summarize(repos, datetime(2026, 9, 24, tzinfo=timezone.utc))
        self.assertEqual((result["total"], result["pushed_30d"], result["stars"], result["forks"]), (2, 1, 5, 1))
        self.assertEqual(sum(d["count"] for d in result["domains"]), 2)
        self.assertEqual({d["name"] for d in result["domains"]}, {
            "Commerce, revenue, and customer operations", "GPU, model serving, and AI economics"
        })

    def test_svg_escapes_dynamic_text(self):
        domain = {"name": "A&B <research>", "count": 1, "pushed_30d": 1, "stars": 0, "kpis": ("Metric <1>", "Cost & risk")}
        card = render_domain(domain, "2026-09-24")
        self.assertIn("A&amp;B &lt;research&gt;", card)
        self.assertIn("Metric &lt;1&gt;", card)
        self.assertNotIn("<research>", card)
        self.assertIn("LIVE GITHUB INVENTORY", render_overview({"total": 1, "pushed_30d": 1, "stars": 0, "forks": 0, "generated_at_utc": "2026-09-24"}))
        self.assertEqual(slug("AI agents: runtime, security"), "ai-agents-runtime-security")


if __name__ == "__main__":
    unittest.main()
