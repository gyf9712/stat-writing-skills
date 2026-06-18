"""
Stdlib unittest for routing_lint.py. No external dependencies.

Run from repo root:
    python -m unittest tests.test_routing_lint

Verifies the real stat-review-routing.md passes (every owner/artifact exists)
and that a fixture with a dangling owner skill and a dangling artifact fails.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "stat-shared-references" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import routing_lint  # noqa: E402

REAL_ROUTING = ROOT / "stat-shared-references" / "stat-review-routing.md"
BAD_ROUTING = ROOT / "tests" / "fixtures" / "routing" / "bad_routing.md"


class RealRoutingTest(unittest.TestCase):
    def test_real_table_parses_rows(self):
        findings, context = routing_lint.run_lint(REAL_ROUTING)
        self.assertGreaterEqual(context["rows_checked"], 10)

    def test_real_table_clean(self):
        findings, _ = routing_lint.run_lint(REAL_ROUTING)
        self.assertEqual([f.id for f in findings], [], msg=[f.message for f in findings])

    def test_real_table_exit_zero(self):
        self.assertEqual(routing_lint.main(["--routing", str(REAL_ROUTING)]), 0)


class BadRoutingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings, cls.context = routing_lint.run_lint(BAD_ROUTING)
        cls.ids = [f.id for f in cls.findings]

    def test_dangling_owner_flagged(self):
        self.assertIn("dangling_owner_skill", self.ids)
        owners = [f.evidence.get("owner") for f in self.findings if f.id == "dangling_owner_skill"]
        self.assertIn("stat-nonexistent-skill", owners)

    def test_dangling_artifact_flagged(self):
        self.assertIn("dangling_artifact", self.ids)
        arts = [f.evidence.get("artifact") for f in self.findings if f.id == "dangling_artifact"]
        self.assertIn("NOT_A_REAL_ARTIFACT.md", arts)

    def test_em_dash_artifact_allowed(self):
        # The "— " row must NOT be flagged.
        arts = [f.evidence.get("artifact") for f in self.findings if f.id == "dangling_artifact"]
        self.assertNotIn("—", arts)

    def test_exit_code_fail(self):
        self.assertEqual(routing_lint.main(["--routing", str(BAD_ROUTING)]), 1)


if __name__ == "__main__":
    unittest.main()
