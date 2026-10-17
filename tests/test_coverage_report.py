"""Tests for scripts/coverage_report.py (claim-level coverage of a synthesis)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "coverage_report.py"
sys.path.insert(0, str(SCRIPT.parent))
import coverage_report as cr  # noqa: E402


def _ledger(*lenses):
    return {"lenses": [{"lens": name, "claims": claims} for name, claims in lenses]}


def _c(text, status):
    return {"claim": text, "status": status}


def test_counts_kept_out_of_distinct_points():
    data = _ledger(
        ("taleb", [_c("tail risk", "kept"), _c("fragile supply", "dropped")]),
        ("gelman", [_c("small sample", "kept")]),
    )
    report = cr.summarize(data)
    assert report["kept"] == 2
    assert report["total"] == 3
    assert report["dropped"] == [("taleb", "fragile supply")]
    assert report["silenced"] == []


def test_contradicted_is_listed_separately_and_not_kept():
    data = _ledger(("kuhn", [_c("paradigm shift", "contradicted"), _c("anomaly", "kept")]))
    report = cr.summarize(data)
    assert report["kept"] == 1
    assert report["contradicted"] == [("kuhn", "paradigm shift")]


def test_lens_with_nothing_kept_is_silenced():
    data = _ledger(
        ("a", [_c("x", "kept")]),
        ("b", [_c("y", "dropped"), _c("z", "contradicted")]),
    )
    assert cr.summarize(data)["silenced"] == ["b"]


def test_unknown_status_is_rejected():
    with pytest.raises(ValueError):
        cr.summarize(_ledger(("a", [_c("x", "maybe")])))


def test_lens_without_claims_is_rejected():
    with pytest.raises(ValueError):
        cr.summarize(_ledger(("a", [])))


def test_render_states_counts_in_plain_words():
    data = _ledger(("taleb", [_c("tail risk", "kept"), _c("fragile supply", "dropped")]))
    text = cr.render(cr.summarize(data))
    assert "Kept 1 of 2 distinct points" in text
    assert "taleb: fragile supply" in text


def _run(tmp_path, data):
    p = tmp_path / "ledger.json"
    p.write_text(json.dumps(data) if not isinstance(data, str) else data)
    return subprocess.run([sys.executable, str(SCRIPT), str(p)], capture_output=True, text=True)


def test_cli_exit_0_when_every_lens_keeps_something(tmp_path):
    r = _run(tmp_path, _ledger(("a", [_c("x", "kept")]), ("b", [_c("y", "kept"), _c("z", "dropped")])))
    assert r.returncode == 0
    assert "Kept 2 of 3" in r.stdout


def test_cli_exit_1_when_a_lens_is_silenced(tmp_path):
    r = _run(tmp_path, _ledger(("a", [_c("x", "kept")]), ("b", [_c("y", "dropped")])))
    assert r.returncode == 1
    assert "b" in r.stdout


def test_cli_exit_2_on_bad_input(tmp_path):
    r = _run(tmp_path, "not json")
    assert r.returncode == 2
