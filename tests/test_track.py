"""Tests for the track module."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from outreach_lab import track


def test_validate_known_technique_passes():
    track.validate_technique("gain-framing")
    track.validate_technique("assumptive")


def test_validate_unknown_technique_rejects():
    with pytest.raises(ValueError) as exc:
        track.validate_technique("not-a-real-technique")
    assert "Unknown technique id" in str(exc.value)


def test_append_validates_technique(monkeypatch, tmp_path):
    log = tmp_path / "log.csv"
    monkeypatch.setattr(track, "LOG_PATH", log)
    with pytest.raises(ValueError):
        track.append({"technique_id": "fake-id", "slug": "x", "subject": "test"})


def test_append_writes_row(monkeypatch, tmp_path):
    log = tmp_path / "log.csv"
    monkeypatch.setattr(track, "LOG_PATH", log)
    track.append({
        "technique_id": "gain-framing",
        "slug": "modal-labs",
        "company": "Modal Labs",
        "variant_id": "v1",
        "subject": "test",
        "response": "opened",
    })
    rows = list(csv.DictReader(log.open()))
    assert len(rows) == 1
    assert rows[0]["technique_id"] == "gain-framing"
    assert rows[0]["response"] == "opened"
    assert rows[0]["sent_date"]  # auto-filled


def test_analyze_empty_log(monkeypatch, tmp_path):
    log = tmp_path / "nope.csv"
    monkeypatch.setattr(track, "LOG_PATH", log)
    out = track.analyze()
    assert "No log yet" in out


def test_analyze_aggregates_by_technique(monkeypatch, tmp_path):
    log = tmp_path / "log.csv"
    monkeypatch.setattr(track, "LOG_PATH", log)
    for response in ("opened", "replied", "none", "meeting-booked"):
        track.append({
            "technique_id": "gain-framing",
            "slug": "x", "subject": "s", "variant_id": "v1",
            "response": response,
        })
    out = track.analyze(rich_output=False)
    assert "gain-framing" in out
    assert "Total sends: 4" in out
