"""Load target-company configs from YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_TARGETS_DIR = Path(__file__).resolve().parent.parent / "targets"


def load_target(slug: str) -> dict[str, Any]:
    """Load a target's YAML config. Falls back to example.yaml for the demo slug."""
    candidate = _TARGETS_DIR / f"{slug}.yaml"
    if not candidate.exists():
        example = _TARGETS_DIR / "example.yaml"
        if example.exists():
            with example.open() as f:
                cfg = yaml.safe_load(f)
            if cfg.get("slug") == slug:
                return cfg
        raise FileNotFoundError(
            f"No config for slug='{slug}'. Create {candidate} (see targets/example.yaml)."
        )
    with candidate.open() as f:
        return yaml.safe_load(f)


def load_resume() -> dict[str, Any]:
    """Load the master resume bullet library."""
    path = Path(__file__).resolve().parent.parent / "data" / "master_resume.yaml"
    with path.open() as f:
        return yaml.safe_load(f)
