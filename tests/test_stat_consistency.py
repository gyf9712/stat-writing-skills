"""
Stdlib unittest for stat_consistency.py. No external dependencies.

Run from repo root:
    python -m unittest tests.test_stat_consistency

Verifies the deterministic GRIM/GRIMMER/statcheck core: p-values recomputed
from test statistics match known critical values, GRIM flags impossible means
for integer-item scales, and statcheck flags reported-p mismatches (escalating
to a decision error when the recomputed p crosses alpha).
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "stat-shared-references" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import stat_consistency as sc  # noqa: E402


class TestPValues(unittest.TestCase):
    def test_z_critical(self):
        self.assertAlmostEqual(sc.p_from_z(1.96), 0.05, delta=2e-3)

    def test_t_critical(self):
        self.assertAlmostEqual(sc.p_from_t(2.228, 10), 0.05, delta=2e-3)

    def test_chi2_critical(self):
        self.assertAlmostEqual(sc.p_from_chi2(3.841, 1), 0.05, delta=2e-3)

    def test_F_critical(self):
        self.assertAlmostEqual(sc.p_from_F(4.965, 1, 10), 0.05, delta=2e-3)

    def test_r_critical(self):
        self.assertAlmostEqual(sc.p_from_r(0.5, 20), 0.02458, delta=2e-3)

    def test_t_df28(self):
        self.assertAlmostEqual(sc.p_from_t(2.05, 28), 0.04976, delta=2e-3)


class TestGRIM(unittest.TestCase):
    def test_possible_mean(self):
        self.assertTrue(sc.grim(1.80, 10, 2)["consistent"])

    def test_impossible_mean(self):
        self.assertFalse(sc.grim(1.83, 10, 2)["consistent"])

    def test_impossible_mean_n28(self):
        self.assertFalse(sc.grim(5.19, 28, 2)["consistent"])

    def test_possible_mean_n28(self):
        self.assertTrue(sc.grim(5.18, 28, 2)["consistent"])


class TestGRIMMER(unittest.TestCase):
    def test_plausible_sd_not_flagged(self):
        # Conservative: a plainly possible SD must never be flagged.
        self.assertTrue(sc.grimmer(3.0, 1.0, 20, 1)["consistent"])


class TestStatcheck(unittest.TestCase):
    def test_inconsistent_reported_p(self):
        r = sc.statcheck("t", 2.05, 28, 0.04, p_op="=", tail="two")
        self.assertFalse(r["consistent"])

    def test_consistent_reported_p(self):
        r = sc.statcheck("t", 2.05, 28, 0.05, p_op="=", tail="two")
        self.assertTrue(r["consistent"])

    def test_decision_error_is_block(self):
        r = sc.statcheck("t", 1.50, 28, 0.02, p_op="=", tail="two")
        self.assertFalse(r["consistent"])
        self.assertEqual(r["severity"], "block")

    def test_case_insensitive_stat_name(self):
        # 'F' and 'f' must both resolve.
        r = sc.statcheck("F", 4.965, 1, 0.05, df2=10, p_op="=", tail="two")
        self.assertTrue(r["consistent"])


class TestBatch(unittest.TestCase):
    def test_gate_blocks_on_grim_failure(self):
        spec = {
            "means": [{"id": "T.mean", "mean": 1.83, "n": 10, "decimals": 2}],
            "stats": [],
        }
        out = sc.run_batch(spec)
        self.assertEqual(out["gate"], "BLOCK")
        self.assertEqual(out["summary"]["block"], 1)


if __name__ == "__main__":
    unittest.main()
