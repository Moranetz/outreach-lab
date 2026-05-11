"""Tests for the targets module."""

from __future__ import annotations

import pytest

from outreach_lab import targets


def test_load_example_target():
    cfg = targets.load_target("modal-labs")
    assert cfg["slug"] == "modal-labs"
    assert cfg["company_name"] == "Modal Labs"
    assert "buyer_persona" in cfg


def test_load_unknown_target_raises():
    with pytest.raises(FileNotFoundError):
        targets.load_target("definitely-not-a-real-slug")


def test_load_resume():
    resume = targets.load_resume()
    assert "candidate" in resume
    assert "master_bullets" in resume
    # spot-check a known bullet category
    assert "shipping" in resume["master_bullets"]
