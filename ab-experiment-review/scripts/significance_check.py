# -*- coding: utf-8 -*-
"""Two-proportion A/B significance check (frequentist).

Usage:
  python significance_check.py --control-n 10000 --control-c 450 --treatment-n 10000 --treatment-c 520
"""
import argparse
import math


def two_sided_p_from_z(z):
    # Phi(z) via erfc
    def normal_cdf(x):
        return 0.5 * math.erfc(-x / math.sqrt(2.0))
    return 2.0 * (1.0 - normal_cdf(abs(z)))


def main():
    ap = argparse.ArgumentParser(description="Two-proportion AB significance check")
    ap.add_argument("--control-n", type=int, required=True, help="control group sample size")
    ap.add_argument("--control-c", type=int, required=True, help="control group events (e.g. conversions)")
    ap.add_argument("--treatment-n", type=int, required=True, help="treatment group sample size")
    ap.add_argument("--treatment-c", type=int, required=True, help="treatment group events (e.g. conversions)")
    args = ap.parse_args()

    if args.control_c > args.control_n or args.treatment_c > args.treatment_n:
        raise SystemExit("events must not exceed sample size")

    n1, c1 = args.control_n, args.control_c
    n2, c2 = args.treatment_n, args.treatment_c
    p1 = c1 / n1
    p2 = c2 / n2
    p_pool = (c1 + c2) / (n1 + n2)

    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se if se > 0 else float("inf")
    p_value = two_sided_p_from_z(z)

    diff = p2 - p1
    diff_pp = diff * 100
    rel_lift = (diff / p1 * 100) if p1 > 0 else float("inf")
    ci_half = 1.96 * se

    print("== A/B significance check ==")
    print(f"Control   : n={n1:,}  events={c1:,}  rate={p1:.4%}")
    print(f"Treatment : n={n2:,}  events={c2:,}  rate={p2:.4%}")
    print(f"Absolute diff : {diff_pp:+.2f} pp")
    print(f"Relative lift : {rel_lift:+.2f}%")
    print(f"z = {z:.3f} | two-sided p = {p_value:.4f}")
    print(f"95% CI of diff: [{diff_pp - ci_half * 100:+.2f} pp, {diff_pp + ci_half * 100:+.2f} pp]")
    if p_value < 0.05:
        print("Verdict: statistically significant at alpha=0.05")
    else:
        print("Verdict: NOT statistically significant at alpha=0.05")

    print("Note: statistical significance != business significance. "
          "Check baseline, guardrail metrics, duration and confounders before shipping.")


if __name__ == "__main__":
    main()
