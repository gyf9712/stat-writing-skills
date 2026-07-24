#!/usr/bin/env python3
"""Deterministic statistical-consistency core for ccf-integrity-auditor.

Ported (conceptually) from ARIS integrity-forensics' deterministic
GRIM/GRIMMER/statcheck core. Pure-Python, zero dependencies, so it runs as a
mechanical pre-pass before the semantic claim-evidence audit.

What it does, and only what it does:

  GRIM      Given a reported mean, sample size, and decimal precision for an
            integer-item scale, decide whether that mean is arithmetically
            achievable at all. (Brown & Heathers, 2017.)

  GRIMMER   Conservative granularity check on a reported SD given mean and n:
            flags only when NO integer sum-of-squares can reproduce the SD's
            rounding interval, i.e. a clear impossibility. (Anaya, 2016;
            deliberately under-powered here to avoid false positives.)

  statcheck Recompute the p-value from a reported test statistic + df and
            compare against the reported p. Flags inconsistencies and, more
            severely, "decision errors" where the recomputed p lands on the
            other side of alpha from what was reported. (Nuijten et al., 2016.)

This tool NEVER repairs anything. It reports arithmetic facts. Every flag it
raises is a deterministic contradiction, not a judgment call, and feeds the
"Numeric consistency findings" section of the skill's output contract.

Usage:
  stat_consistency.py --selftest
  stat_consistency.py --json INPUT.json        # structured batch (see SCHEMA below)
  stat_consistency.py --grim MEAN N DECIMALS [--items K]
  stat_consistency.py --statcheck STAT VALUE df1 [df2] --p REPORTED [--tail two|one]

INPUT.json SCHEMA:
  {
    "means":  [{"id": "T1.mean", "mean": 1.83, "n": 10, "decimals": 2, "items": 1,
                "sd": 0.79}],        # sd optional -> also runs GRIMMER
    "stats":  [{"id": "t.p1", "stat": "t", "value": 2.05, "df1": 28,
                "p": 0.04, "p_op": "=", "tail": "two"}]
  }
  stat is one of: t, F, chi2, r, z. df2 only for F. r uses df1 = n (sample size).
"""
from __future__ import annotations

import argparse
import json
import math
import sys

# ---------------------------------------------------------------------------
# Special functions (Numerical Recipes style, pure Python)
# ---------------------------------------------------------------------------

def _gammln(x: float) -> float:
    cof = [76.18009172947146, -86.50532032941677, 24.01409824083091,
           -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]
    y = x
    tmp = x + 5.5
    tmp -= (x + 0.5) * math.log(tmp)
    ser = 1.000000000190015
    for c in cof:
        y += 1.0
        ser += c / y
    return -tmp + math.log(2.5066282746310005 * ser / x)


def _gser(a: float, x: float) -> float:
    if x <= 0:
        return 0.0
    gln = _gammln(a)
    ap = a
    total = 1.0 / a
    delta = total
    for _ in range(2000):
        ap += 1.0
        delta *= x / ap
        total += delta
        if abs(delta) < abs(total) * 1e-16:
            break
    return total * math.exp(-x + a * math.log(x) - gln)


def _gcf(a: float, x: float) -> float:
    gln = _gammln(a)
    fpmin = 1e-300
    b = x + 1.0 - a
    c = 1.0 / fpmin
    d = 1.0 / b
    h = d
    for i in range(1, 2000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < fpmin:
            d = fpmin
        c = b + an / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


def gammp(a: float, x: float) -> float:
    """Regularized lower incomplete gamma P(a, x)."""
    if x < 0 or a <= 0:
        raise ValueError("gammp domain")
    if x < a + 1.0:
        return _gser(a, x)
    return 1.0 - _gcf(a, x)


def gammq(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a, x) = 1 - P(a, x)."""
    return 1.0 - gammp(a, x)


def _betacf(a: float, b: float, x: float) -> float:
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, 500):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            break
    return h


def betai(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(_gammln(a + b) - _gammln(a) - _gammln(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


# ---------------------------------------------------------------------------
# p-values from test statistics
# ---------------------------------------------------------------------------

def p_from_z(z: float) -> float:
    """Two-tailed p for a standard-normal z."""
    return math.erfc(abs(z) / math.sqrt(2.0))


def p_from_t(t: float, df: float) -> float:
    """Two-tailed p for Student t."""
    x = df / (df + t * t)
    return betai(df / 2.0, 0.5, x)


def p_from_chi2(chi2: float, df: float) -> float:
    """Upper-tail p for chi-square (inherently one-tailed)."""
    return gammq(df / 2.0, chi2 / 2.0)


def p_from_F(f: float, df1: float, df2: float) -> float:
    """Upper-tail p for F (inherently one-tailed)."""
    x = df2 / (df2 + df1 * f)
    return betai(df2 / 2.0, df1 / 2.0, x)


def p_from_r(r: float, n: float) -> float:
    """Two-tailed p for a Pearson correlation from sample size n."""
    df = n - 2.0
    if df <= 0 or abs(r) >= 1.0:
        return float("nan")
    t = r * math.sqrt(df / (1.0 - r * r))
    return p_from_t(t, df)


# ---------------------------------------------------------------------------
# GRIM / GRIMMER
# ---------------------------------------------------------------------------

def grim(mean: float, n: int, decimals: int, items: int = 1) -> dict:
    """Is `mean` reachable as (integer total) / (n*items) at `decimals`?"""
    N = n * items
    unit = 10.0 ** (-decimals)
    half = unit / 2.0
    target = mean * N
    lo = int(math.floor(target)) - 2
    hi = int(math.ceil(target)) + 2
    for total in range(lo, hi + 1):
        recon = total / N
        if abs(recon - mean) < half - 1e-12 or abs(abs(recon - mean) - half) < 1e-12:
            return {"consistent": True, "n_eff": N}
    return {"consistent": False, "n_eff": N,
            "detail": f"no integer total over {N} rounds to {mean} at {decimals}dp"}


def grimmer(mean: float, sd: float, n: int, decimals: int, items: int = 1) -> dict:
    """Conservative GRIMMER: flag only a clear impossibility.

    Reconstruct the integer grand total from the mean, then test whether ANY
    integer sum-of-squares lands inside the SD's rounding interval. If none
    does, the SD is arithmetically impossible for integer items. We do not do
    the parity refinement, so we under-report rather than risk a false flag.
    """
    N = n * items
    if N < 2:
        return {"consistent": True, "note": "n<2, GRIMMER not applicable"}
    unit = 10.0 ** (-decimals)
    half = unit / 2.0
    # Integer grand total consistent with the mean (nearest; GRIM should gate first).
    total = round(mean * N)
    # SD rounding interval -> variance interval -> sum-of-squares interval.
    sd_lo = max(sd - half, 0.0)
    sd_hi = sd + half
    var_lo = sd_lo * sd_lo
    var_hi = sd_hi * sd_hi
    # sample variance = (SS - total^2/N) / (N-1)
    ss_lo = var_lo * (N - 1) + (total * total) / N
    ss_hi = var_hi * (N - 1) + (total * total) / N
    # Is there an integer in [ss_lo, ss_hi]?
    has_int = math.floor(ss_hi + 1e-9) >= math.ceil(ss_lo - 1e-9)
    if has_int:
        return {"consistent": True, "n_eff": N}
    return {"consistent": False, "n_eff": N,
            "detail": (f"no integer sum-of-squares in [{ss_lo:.4f}, {ss_hi:.4f}] "
                       f"for mean={mean}, sd={sd}, n={N}")}


# ---------------------------------------------------------------------------
# statcheck
# ---------------------------------------------------------------------------

_TWO_TAILED = {"t", "r", "z"}
_ONE_TAILED = {"chi2", "f"}


def _compute_p(stat: str, value: float, df1: float, df2: float | None) -> float:
    stat = stat.lower()
    if stat == "t":
        return p_from_t(value, df1)
    if stat == "z":
        return p_from_z(value)
    if stat == "r":
        return p_from_r(value, df1)  # df1 carries n for r
    if stat == "chi2":
        return p_from_chi2(value, df1)
    if stat == "f":
        if df2 is None:
            raise ValueError("F needs df2")
        return p_from_F(value, df1, df2)
    raise ValueError(f"unknown stat {stat}")


def statcheck(stat: str, value: float, df1: float, p_reported: float,
              df2: float | None = None, p_op: str = "=", tail: str = "two",
              alpha: float = 0.05) -> dict:
    """Recompute p, compare to reported, classify severity."""
    stat = stat.lower()
    computed_two = _compute_p(stat, value, df1, df2)
    if math.isnan(computed_two):
        return {"consistent": None, "severity": "advisory",
                "detail": "could not recompute (out of domain)"}

    # For inherently one-tailed stats, "computed_two" already IS the reported
    # tail. For t/r/z, offer both one- and two-tailed to avoid false positives.
    candidates = {"two": computed_two}
    if stat in _TWO_TAILED:
        candidates["one"] = computed_two / 2.0
    computed = candidates.get(tail, computed_two)

    # Decimal tolerance from the reported p's own precision.
    p_str = repr(p_reported)
    dp = len(p_str.split(".")[1]) if "." in p_str else 3
    tol = 0.5 * 10.0 ** (-dp) + 1e-9

    def _matches(cp: float) -> bool:
        if p_op == "=":
            return abs(cp - p_reported) <= tol
        if p_op == "<":
            return cp < p_reported + tol
        if p_op == ">":
            return cp > p_reported - tol
        return False

    consistent = any(_matches(cp) for cp in candidates.values())

    # Decision error: does the reported p and the (best-matching or two-tailed)
    # computed p fall on opposite sides of alpha?
    ref_computed = computed
    reported_sig = (p_reported < alpha) if p_op in ("=", "<") else (p_reported <= alpha)
    computed_sig = ref_computed < alpha
    decision_error = (reported_sig != computed_sig) and not consistent

    severity = "ok"
    if not consistent:
        severity = "block" if decision_error else "warn"

    return {
        "consistent": consistent,
        "severity": severity,
        "decision_error": decision_error,
        "computed_two_tailed": round(computed_two, 6),
        "computed_used": round(ref_computed, 6),
        "reported": p_reported,
        "reported_op": p_op,
        "tail": tail,
    }


# ---------------------------------------------------------------------------
# Batch runner
# ---------------------------------------------------------------------------

def run_batch(spec: dict) -> dict:
    findings = []
    for m in spec.get("means", []):
        gid = m.get("id", "mean")
        g = grim(m["mean"], int(m["n"]), int(m["decimals"]), int(m.get("items", 1)))
        if not g["consistent"]:
            findings.append({"id": gid, "check": "GRIM", "severity": "block", **g})
        if "sd" in m and m["sd"] is not None:
            gm = grimmer(m["mean"], m["sd"], int(m["n"]), int(m["decimals"]),
                         int(m.get("items", 1)))
            if not gm["consistent"]:
                findings.append({"id": gid, "check": "GRIMMER",
                                 "severity": "block", **gm})
    for s in spec.get("stats", []):
        sid = s.get("id", "stat")
        r = statcheck(s["stat"], float(s["value"]), float(s["df1"]),
                      float(s["p"]), df2=(float(s["df2"]) if s.get("df2") is not None else None),
                      p_op=s.get("p_op", "="), tail=s.get("tail", "two"))
        if r.get("consistent") is False:
            findings.append({"id": sid, "check": "statcheck", **r})
    n_block = sum(1 for f in findings if f.get("severity") == "block")
    n_warn = sum(1 for f in findings if f.get("severity") == "warn")
    return {
        "findings": findings,
        "summary": {"total_flagged": len(findings),
                    "block": n_block, "warn": n_warn},
        "gate": "BLOCK" if n_block else ("WARN" if n_warn else "PASS"),
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    def check(name, cond):
        nonlocal ok
        status = "PASS" if cond else "FAIL"
        if not cond:
            ok = False
        print(f"  [{status}] {name}")

    print("p-value cross-checks (known critical values ~ p=0.05):")
    check("z=1.96 -> ~0.05", abs(p_from_z(1.96) - 0.05) < 2e-3)
    check("t=2.228,df=10 -> ~0.05", abs(p_from_t(2.228, 10) - 0.05) < 2e-3)
    check("chi2=3.841,df=1 -> ~0.05", abs(p_from_chi2(3.841, 1) - 0.05) < 2e-3)
    check("F=4.965,df=1,10 -> ~0.05", abs(p_from_F(4.965, 1, 10) - 0.05) < 2e-3)
    check("r=0.5,n=20 -> ~0.0246", abs(p_from_r(0.5, 20) - 0.02458) < 2e-3)
    check("t=2.05,df=28 -> ~0.0498", abs(p_from_t(2.05, 28) - 0.04976) < 2e-3)

    print("GRIM:")
    check("mean=1.80,n=10 consistent", grim(1.80, 10, 2)["consistent"] is True)
    check("mean=1.83,n=10 INCONSISTENT", grim(1.83, 10, 2)["consistent"] is False)
    check("mean=5.19,n=28 INCONSISTENT", grim(5.19, 28, 2)["consistent"] is False)
    check("mean=5.18,n=28 consistent", grim(5.18, 28, 2)["consistent"] is True)

    print("GRIMMER (conservative):")
    # A plainly possible SD should never be flagged.
    check("mean=3.0,sd=1.0,n=20 consistent",
          grimmer(3.0, 1.0, 20, 1)["consistent"] is True)

    print("statcheck:")
    r1 = statcheck("t", 2.05, 28, 0.04, p_op="=", tail="two")
    check("t(28)=2.05 vs p=.04 flagged inconsistent", r1["consistent"] is False)
    r2 = statcheck("t", 2.05, 28, 0.05, p_op="=", tail="two")
    check("t(28)=2.05 vs p=.05 consistent", r2["consistent"] is True)
    r3 = statcheck("t", 1.50, 28, 0.02, p_op="=", tail="two")
    check("t(28)=1.50 vs p=.02 is DECISION ERROR (block)",
          r3["consistent"] is False and r3["severity"] == "block")

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Deterministic GRIM/GRIMMER/statcheck core.")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", metavar="FILE", help="batch spec (see module docstring)")
    ap.add_argument("--grim", nargs=3, metavar=("MEAN", "N", "DECIMALS"))
    ap.add_argument("--items", type=int, default=1)
    ap.add_argument("--statcheck", nargs="+",
                    metavar="STAT VALUE df1 [df2]",
                    help="e.g. --statcheck t 2.05 28")
    ap.add_argument("--p", type=float, help="reported p for --statcheck")
    ap.add_argument("--p-op", default="=", choices=["=", "<", ">"])
    ap.add_argument("--tail", default="two", choices=["two", "one"])
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.json:
        with open(args.json, "r", encoding="utf-8") as fh:
            spec = json.load(fh)
        print(json.dumps(run_batch(spec), indent=2))
        return 0

    if args.grim:
        mean, n, dec = float(args.grim[0]), int(args.grim[1]), int(args.grim[2])
        print(json.dumps(grim(mean, n, dec, args.items), indent=2))
        return 0

    if args.statcheck:
        sc = args.statcheck
        stat = sc[0]
        value = float(sc[1])
        df1 = float(sc[2])
        df2 = float(sc[3]) if len(sc) > 3 else None
        if args.p is None:
            ap.error("--statcheck requires --p")
        print(json.dumps(statcheck(stat, value, df1, args.p, df2=df2,
                                   p_op=args.p_op, tail=args.tail), indent=2))
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
