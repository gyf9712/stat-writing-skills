"""
Stdlib unittest for review_regression.py. No external dependencies.

Run from repo root:
    python -m unittest tests.test_review_regression

Verifies that a silently-dropped canonical concern (CS2) is flagged and drives a
nonzero exit, while a review that dispositions every prior canonical ID is clean.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "stat-shared-references" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import review_regression  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "review_regression"
PRIOR = FIXTURE / "prior.md"


class DropTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings, cls.context = review_regression.run_check(PRIOR, FIXTURE / "current_drop.md")
        cls.dropped = [f for f in cls.findings if f.status == "DROPPED"]

    def test_prior_ids_extracted(self):
        # CS1, CS2, TR1, PW3, thm:main should all be detected in the prior review.
        for cid in ("CS1", "CS2", "TR1", "PW3", "thm:main"):
            self.assertIn(cid, self.context["prior_ids"])

    def test_cs2_and_pw3_dropped(self):
        dropped_ids = {f.evidence["id"] for f in self.dropped}
        self.assertIn("CS2", dropped_ids)
        self.assertIn("PW3", dropped_ids)

    def test_carried_ids_not_dropped(self):
        dropped_ids = {f.evidence["id"] for f in self.dropped}
        self.assertNotIn("CS1", dropped_ids)
        self.assertNotIn("TR1", dropped_ids)
        self.assertNotIn("thm:main", dropped_ids)

    def test_exit_code_fail(self):
        self.assertEqual(
            review_regression.main(["--prior", str(PRIOR), "--current", str(FIXTURE / "current_drop.md")]),
            1,
        )


class CleanTest(unittest.TestCase):
    def test_no_drops(self):
        findings, _ = review_regression.run_check(PRIOR, FIXTURE / "current_clean.md")
        dropped = [f for f in findings if f.status == "DROPPED"]
        self.assertEqual(dropped, [], msg=[f.evidence for f in dropped])

    def test_exit_code_clean(self):
        self.assertEqual(
            review_regression.main(["--prior", str(PRIOR), "--current", str(FIXTURE / "current_clean.md")]),
            0,
        )


if __name__ == "__main__":
    unittest.main()
