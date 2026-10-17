#!/usr/bin/env python3
"""Claim-level coverage report for a panel synthesis.

Reads the claim ledger a coverage-check subagent writes (see
references/synthesis-modes.md, "Claim coverage check") and states, in plain
words, how many of the lenses' distinct points survived into the synthesis.

Ledger shape:
    {"lenses": [{"lens": "<name>", "claims": [{"claim": "...", "status": "kept|dropped|contradicted"}]}]}

Judging whether a claim was kept is the subagent's job (a model judgment);
this script only checks the ledger's structure and counts.

Exit 0 every lens kept at least one point; 1 a lens was silenced (nothing
kept); 2 unusable input.
"""
import json
import sys

STATUSES = {"kept", "dropped", "contradicted"}


def summarize(data):
    lenses = data.get("lenses") if isinstance(data, dict) else None
    if not isinstance(lenses, list) or not lenses:
        raise ValueError("ledger needs a non-empty 'lenses' list")
    kept, total = 0, 0
    dropped, contradicted, silenced = [], [], []
    for entry in lenses:
        name = entry.get("lens")
        claims = entry.get("claims")
        if not name or not isinstance(claims, list) or not claims:
            raise ValueError(f"lens {name!r} needs a name and at least one claim")
        lens_kept = 0
        for c in claims:
            status = c.get("status")
            if status not in STATUSES:
                raise ValueError(f"lens {name!r}: unknown status {status!r}")
            total += 1
            if status == "kept":
                kept += 1
                lens_kept += 1
            elif status == "dropped":
                dropped.append((name, c.get("claim", "")))
            else:
                contradicted.append((name, c.get("claim", "")))
        if lens_kept == 0:
            silenced.append(name)
    return {"kept": kept, "total": total, "dropped": dropped,
            "contradicted": contradicted, "silenced": silenced}


def render(report):
    lines = [f"Kept {report['kept']} of {report['total']} distinct points."]
    if report["dropped"]:
        lines.append("Dropped:")
        lines += [f"- {lens}: {claim}" for lens, claim in report["dropped"]]
    if report["contradicted"]:
        lines.append("Contradicted by the synthesis:")
        lines += [f"- {lens}: {claim}" for lens, claim in report["contradicted"]]
    if report["silenced"]:
        lines.append("Silenced (no point kept): " + ", ".join(report["silenced"]))
    return "\n".join(lines)


def main(argv):
    if len(argv) != 2:
        print("usage: coverage_report.py <ledger.json>", file=sys.stderr)
        return 2
    try:
        with open(argv[1]) as f:
            report = summarize(json.load(f))
    except (OSError, ValueError) as e:  # json.JSONDecodeError is a ValueError
        print(f"coverage_report: {e}", file=sys.stderr)
        return 2
    print(render(report))
    return 1 if report["silenced"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
