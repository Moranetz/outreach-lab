"""1-page company brief — the orientation doc before composing/tailoring."""

from __future__ import annotations

import yaml

from . import llm
from .targets import load_target

SYSTEM = """You are briefing an AE candidate on a target company before they apply.

Output format — strict markdown, ~400 words total:

# Brief — <Company name>

## In one sentence

<what this company sells, to whom, at what stage>

## The buyer

<the person who signs the contract — role, mindset, decision speed, what they read>

## Why this seat fits Marion

<3-5 bullets matching Marion's actual portfolio to this company's wedge>

## Reasons to skip

<2-3 honest reasons this might not be the right fit>

## First-30-days bet

<one paragraph: what Marion would credibly say she'd do in month one>
"""


def run(slug: str) -> str:
    target = load_target(slug)
    user = f"""# Target company config

{yaml.safe_dump(target, sort_keys=False, default_flow_style=False)}

Write the brief.
"""
    return llm.complete(SYSTEM, user, model=llm.MODEL_FAST, max_tokens=2048)
