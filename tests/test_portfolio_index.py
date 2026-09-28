import json
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

        self.assertEqual(sum("flagship" in r["portfolio_roles"] for r in index["repositories"]), 10)
        self.assertEqual(sum("maintenance_focus" in r["portfolio_roles"] for r in index["repositories"]), 3)
        for edge in index["relationships"]:
            self.assertIn(edge["from"].lower(), names)
            self.assertIn(edge["to"].lower(), names)
            self.assertEqual(edge["status"], "candidate")

    def test_schema_reference_and_pillar_metadata(self):
        schema = json.loads((ROOT / "data/portfolio-index.schema.json").read_text())
        index = json.loads((ROOT / "data/portfolio-index.json").read_text())

        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(index["schema"], "data/portfolio-index.schema.json")
        self.assertTrue(all(r["pillar"] and r["evidence_source"] for r in index["repositories"]))


if __name__ == "__main__":
    unittest.main()
