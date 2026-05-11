"""Tests for the atlas module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from outreach_lab import atlas


def test_load_techniques_returns_list():
    techs = atlas.load_techniques()
    assert isinstance(techs, list)
    assert len(techs) >= 1


def test_every_loaded_technique_has_posterior():
    for t in atlas.load_techniques():
        assert "atlas_posterior" in t, f"{t['id']} missing posterior"
        p = t["atlas_posterior"]
        for field in ("d_mu", "ci_lower", "ci_upper", "k_studies"):
            assert field in p, f"{t['id']}.posterior missing {field}"
        assert p["ci_lower"] <= p["d_mu"] <= p["ci_upper"], (
            f"{t['id']}: posterior mean {p['d_mu']} outside CI [{p['ci_lower']}, {p['ci_upper']}]"
        )


def test_atlas_posteriors_match_canonical():
    """The posteriors in techniques.json must match the actual Closing Evidence Atlas values.

    Source of truth: /Users/marion/Developer/closing-evidence-atlas/results/pilot_posterior_summaries.csv
    (Atlas v0.5 draft, post-atlas-009-fix). If the Atlas re-runs and these change, update both.
    """
    canonical = {
        "gain-framing":           {"d_mu": 0.354, "k_studies": 9},
        "loss-framing":           {"d_mu": 0.327, "k_studies": 7},
        "regulatory-fit":         {"d_mu": 0.484, "k_studies": 3},
        "extreme-anchor":         {"d_mu": 0.435, "k_studies": 2},
        "social-proof":           {"d_mu": 0.682, "k_studies": 2},
        "commitment-consistency": {"d_mu": 0.590, "k_studies": 2},
    }
    loaded = {t["id"]: t for t in atlas.load_techniques()}
    for tid, expected in canonical.items():
        assert tid in loaded, f"Missing {tid} in techniques.json"
        p = loaded[tid]["atlas_posterior"]
        # within 0.005 of canonical (small rounding tolerance)
        assert abs(p["d_mu"] - expected["d_mu"]) < 0.005, (
            f"{tid}: d_mu {p['d_mu']} drift from canonical {expected['d_mu']}"
        )
        assert p["k_studies"] == expected["k_studies"], f"{tid}: k drift"


def test_no_fabricated_techniques_in_with_posteriors():
    """techniques.json must not include any technique with a posterior that doesn't exist in the Atlas."""
    canonical_ids = {
        "gain-framing", "loss-framing", "regulatory-fit",
        "extreme-anchor", "social-proof", "commitment-consistency",
    }
    loaded_ids = {t["id"] for t in atlas.load_techniques()}
    assert loaded_ids <= canonical_ids, (
        f"Found technique IDs in techniques.json not in canonical Atlas: {loaded_ids - canonical_ids}"
    )


def test_full_catalog_covers_39_techniques():
    """Atlas catalogs 39 named techniques. The combined four populations should cover all of them."""
    ids = atlas.all_technique_ids()
    assert len(ids) >= 39, f"Expected ≥39 catalog techniques, got {len(ids)}"


def test_empirical_deserts_present():
    """The Atlas's most counterintuitive finding — 15 named techniques with zero peer-reviewed studies."""
    deserts = atlas.empirical_deserts()
    assert len(deserts) == 15, f"Expected 15 empirical-desert techniques, got {len(deserts)}"
    # spot-check named ones — these are the structural closes widely taught with zero peer-reviewed studies
    desert_ids = {d["id"] for d in deserts}
    for tid in ("alternative-choice", "ben-franklin", "summary-close", "trial-close"):
        assert tid in desert_ids, f"{tid} should be in empirical_deserts"


def test_technique_summary_renders_with_posteriors():
    summary = atlas.technique_summary()
    assert "gain-framing" in summary
    assert "d=0.354" in summary
    assert "P(d>0)=1.0" in summary
    assert "USE WHEN" in summary


def test_get_technique_searches_all_populations():
    assert atlas.get_technique("gain-framing")["name"] == "Gain framing"
    # from empirical deserts
    assert atlas.get_technique("assumptive")["name"] == "Assumptive close"
    with pytest.raises(KeyError):
        atlas.get_technique("not-a-real-technique")
