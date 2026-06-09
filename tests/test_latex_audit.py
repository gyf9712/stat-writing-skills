"""
Stdlib unittest for latex_audit.py. No external dependencies.

Run from repo root:
    python -m unittest tests.test_latex_audit

Verifies that the audit catches every check the fixture is designed to
exercise:

- JASA 12pt missing
- JASA \onehalfspacing forbidden
- JASA \doublespacing missing
- JASA geometry margin missing
- Abstract over 250 words
- Undefined \ref
- Missing citation key
- Unused bib entry
- Incomplete bib entry
- Existing image passes
- Missing image fails
- Cross-file ref main -> supplement
- Cross-file ref supplement -> main
- Compile log: undefined ref, undefined citation, overfull hbox, file not found
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "stat-shared-references" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import latex_audit  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "latex_audit"


class LatexAuditFixtureTest(unittest.TestCase):
    """Run audit on the fixture and check expected finding ids appear."""

    @classmethod
    def setUpClass(cls):
        argv = [
            "--main", str(FIXTURE / "main.tex"),
            "--supplement", str(FIXTURE / "supplement.tex"),
            "--supplement-mode", "separate-self-contained",
            "--venue", "jasa",
            "--compile", "auto",
        ]
        args = latex_audit.main.__wrapped__ if hasattr(latex_audit.main, "__wrapped__") else None
        # Easier: call run_audit directly.
        parser = _build_parser()
        ns = parser.parse_args(argv)
        cls.findings, cls.context = latex_audit.run_audit(ns)
        cls.ids = [f.id for f in cls.findings]

    def _assert_id(self, target_substring: str):
        matches = [fid for fid in self.ids if target_substring in fid]
        self.assertTrue(
            matches,
            f"expected a finding id containing {target_substring!r}; "
            f"got: {self.ids}",
        )

    def _assert_no_id(self, target_substring: str):
        matches = [fid for fid in self.ids if target_substring in fid]
        self.assertFalse(matches, f"did not expect {target_substring!r}; got {matches}")

    # Template conformance
    def test_jasa_12pt_missing(self):
        self._assert_id("venue_documentclass_missing_option_12pt")

    def test_jasa_onehalfspacing_forbidden(self):
        self._assert_id("venue_forbidden_spacing_onehalfspacing")

    def test_jasa_doublespacing_required(self):
        self._assert_id("venue_missing_required_spacing")

    def test_jasa_geometry_margin(self):
        self._assert_id("venue_geometry_margin_fail")

    def test_plain_cite_flagged(self):
        self._assert_id("venue_plain_cite_used")

    # Abstract
    def test_abstract_too_long(self):
        self._assert_id("abstract_too_long")

    # ref / label
    def test_undefined_ref(self):
        self._assert_id("undefined_ref")

    def test_cross_file_main_to_supplement(self):
        self._assert_id("cross_file_ref_main_to_supplement")

    def test_cross_file_supplement_to_main(self):
        self._assert_id("cross_file_ref_supplement_to_main")

    # cite / bib
    def test_missing_citation_key(self):
        self._assert_id("missing_citation_key")

    def test_unused_bib_entry(self):
        self._assert_id("unused_bib_entry")

    def test_incomplete_bib_entry(self):
        self._assert_id("incomplete_bib_entry")

    # images
    def test_missing_image(self):
        self._assert_id("missing_image_file")

    def test_present_image_silent_pass(self):
        # Present images should not generate a missing_image_file finding.
        # We do not test for a positive PASS finding because we do not emit one.
        present_findings = [
            f for f in self.findings
            if f.id == "missing_image_file" and "present" in str(f.evidence.get("image_path", ""))
        ]
        self.assertEqual(present_findings, [], "figures/present should not be flagged missing")

    # compile log
    def test_log_undefined_ref(self):
        self._assert_id("log_undefined_reference_specific")

    def test_log_undefined_citation(self):
        self._assert_id("log_undefined_citation_specific")

    def test_log_overfull_hbox(self):
        self._assert_id("log_overfull_hbox")

    def test_log_file_not_found(self):
        self._assert_id("log_file_not_found")

    # Provenance fields populated
    def test_provenance_populated(self):
        for key in ["script_version", "rules_version", "rules_digest", "venue", "supplement_mode"]:
            self.assertIn(key, self.context)
            self.assertTrue(self.context[key])


class ExitCodeTest(unittest.TestCase):
    """The fixture should produce exit code 1 (at least one mechanical FAIL)."""

    def test_exit_code_is_one(self):
        argv = [
            "--main", str(FIXTURE / "main.tex"),
            "--supplement", str(FIXTURE / "supplement.tex"),
            "--supplement-mode", "separate-self-contained",
            "--venue", "jasa",
            "--compile", "auto",
        ]
        code = latex_audit.main(argv)
        self.assertEqual(code, 1)


def _build_parser():
    """Mirror the argparse setup in latex_audit.main so tests can call run_audit directly."""
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--main", required=True)
    p.add_argument("--supplement", default=None)
    p.add_argument("--supplement-mode", default="none")
    p.add_argument("--venue", default="none")
    p.add_argument("--compile", default="auto")
    p.add_argument("--json-out", default=None)
    p.add_argument("--md-out", default=None)
    return p


if __name__ == "__main__":
    unittest.main()
