import json
import sys
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))
from update_profile_metrics import FLAGSHIP_REPOSITORIES
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PortfolioIndexTests(unittest.TestCase):
    def test_index_matches_public_original_inventory(self):
        inventory = json.loads((ROOT / "data/public-original-repositories.json").read_text())
        index = json.loads((ROOT / "data/portfolio-index.json").read_text())
        names = {item["name"].lower() for item in index["repositories"]}

        self.assertEqual(index["portfolio_count"], len(inventory))
        self.assertEqual(names, {item["name"].lower() for item in inventory})
        self.assertTrue(all(item["public"] and not item["fork"] for item in inventory))

    def test_portfolio_roles_and_relationships(self):
        index = json.loads((ROOT / "data/portfolio-index.json").read_text())
        names = {item["name"].lower() for item in index["repositories"]}

        # Derived, not hardcoded. This previously asserted exactly 10, so when a
        # flagship repository was deliberately withdrawn from public view (export
        # control) the scheduled run failed with "AssertionError: 9 != 10" and the
        # message named no cause. The invariant that actually matters is: the
        # flagship role is exactly the declared flagship set, restricted to the
        # repositories that are publicly present. Adding a flagship without tagging
        # it still fails; withdrawing one no longer does.
        declared = {name.lower() for name in FLAGSHIP_REPOSITORIES}
        indexed = {r["name"].lower() for r in index["repositories"]}
        tagged = {r["name"].lower() for r in index["repositories"] if "flagship" in r["portfolio_roles"]}
        self.assertEqual(
            tagged,
            declared & indexed,
            "flagship roles in the index must equal the declared set restricted to "
            "publicly present repositories; a declared flagship is either missing its "
            "role or a non-flagship is tagged",
        )
        self.assertEqual(sum("maintenance_focus" in r["portfolio_roles"] for r in index["repositories"]), 3)
        for edge in index["relationships"]:
            self.assertIn(edge["from"].lower(), names)
            self.assertIn(edge["to"].lower(), names)
            self.assertIn(edge["status"], {"candidate", "implemented"})
            self.assertTrue(edge["evidence"])

    def test_apex_links_and_positioning(self):
        index=json.loads((ROOT/"data/portfolio-index.json").read_text())
        emitted={edge["from"] for edge in index["relationships"] if edge["status"]=="implemented" and edge["to"]=="Apex_PerfAtlas"}
        self.assertEqual(emitted,{"Apex_ULL","Apex_Tick","Apex_ContractForge"})
        for entry in index["repositories"]:
            if entry["name"] in {"Apex_ULL","Apex_Tick","Apex_PerfAtlas","Apex_ContractForge"}:
                self.assertEqual(entry["pillar"],"Low-latency systems and silicon acceleration")
                self.assertEqual(entry["portfolio_roles"],["catalog"])

    def test_schema_reference_and_pillar_metadata(self):
        schema = json.loads((ROOT / "data/portfolio-index.schema.json").read_text())
        index = json.loads((ROOT / "data/portfolio-index.json").read_text())

        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(index["schema"], "data/portfolio-index.schema.json")
        self.assertTrue(all(r["pillar"] and r["evidence_source"] for r in index["repositories"]))


if __name__ == "__main__":
    unittest.main()
