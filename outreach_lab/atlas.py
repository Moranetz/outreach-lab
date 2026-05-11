"""Load the Closing Evidence Atlas technique library.

Surfaces three populations:
  - techniques with posteriors (k>=2 meta-eligible studies)
  - techniques with inclusion literature but no posterior yet
  - the 'empirical deserts' (k=0) — 15 named closing techniques widely taught with
    zero peer-reviewed studies meeting Atlas inclusion criteria

Output is consumed by compose/tailor/teardown prompts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_raw() -> dict[str, Any]:
    with (_DATA_DIR / "techniques.json").open() as f:
        return json.load(f)


def load_techniques() -> list[dict[str, Any]]:
    """Techniques with current posteriors."""
    return _load_raw()["techniques"]


def techniques_without_posteriors() -> list[dict[str, Any]]:
    """Techniques with k>=5 inclusion records but no Phase 3 posterior yet."""
    return _load_raw().get("techniques_without_posteriors", [])


def fragile_techniques() -> list[dict[str, Any]]:
    """Techniques with <5 studies — high uncertainty."""
    return _load_raw().get("fragile_techniques", [])


def empirical_deserts() -> list[dict[str, Any]]:
    """The 15 named closing techniques with zero peer-reviewed studies meeting inclusion criteria."""
    return _load_raw().get("empirical_deserts", [])


def all_technique_ids() -> set[str]:
    raw = _load_raw()
    return (
        {t["id"] for t in raw["techniques"]}
        | {t["id"] for t in raw.get("techniques_without_posteriors", [])}
        | {t["id"] for t in raw.get("fragile_techniques", [])}
        | {t["id"] for t in raw.get("empirical_deserts", [])}
    )


def technique_summary() -> str:
    """Compact technique cheat-sheet for prompt injection.

    Includes only techniques that have current posteriors AND non-empty
    'when_to_use' / 'when_to_avoid' guidance — i.e. the recommended-for-use set.
    """
    lines = []
    for t in load_techniques():
        p = t["atlas_posterior"]
        caveat = f" CAVEAT: {t['caveats']}" if "caveats" in t else ""
        lines.append(
            f"- {t['name']} (id={t['id']}, cluster={t['cluster']}): "
            f"d={p['d_mu']} [95% CrI {p['ci_lower']}-{p['ci_upper']}], "
            f"k={p['k_studies']} studies, P(d>0)={p['p_mu_gt_zero']}. "
            f"{t['definition']} "
            f"USE WHEN: {t['when_to_use']} AVOID WHEN: {t['when_to_avoid']}.{caveat}"
        )
    return "\n".join(lines)


def get_technique(technique_id: str) -> dict[str, Any]:
    """Look up a single technique by id. Searches all populations."""
    for population in (
        load_techniques(),
        techniques_without_posteriors(),
        fragile_techniques(),
        empirical_deserts(),
    ):
        for t in population:
            if t["id"] == technique_id:
                return t
    raise KeyError(f"Unknown technique id: {technique_id}")
