"""1500-word GTM teardown stub generator."""

from __future__ import annotations

import yaml

from . import llm
from .targets import load_target


SYSTEM = """You are writing a public GTM teardown of a SF startup.

The teardown is intended as a portfolio artifact for an AE candidate. It should:

- Read like editorial criticism, not a marketing brochure
- Be specific. Cite actual landing-page copy, pricing tiers, named competitors
- Identify 3-5 concrete gaps the candidate could fix in their first 30 days
- Total ~1500 words
- Avoid: "synergy", "circle back", behavioral-science jargon, AI-sounding cadence, hedging

Output format — strict markdown:

# GTM Teardown — <Company name>

> One-paragraph thesis. What is this company selling, to whom, and what is the GTM motion (PLG / sales-led / hybrid).

## Positioning

Who they say they're for. Who they actually win with. What the message-market gap looks like.

## ICP & buyer

The named buyer persona. The check-signer. The technical champion. Who is missing.

## Pricing & packaging

Tier-by-tier. Anchor points. Where the discount lever lives. What competitors charge.

## Sales motion

How a prospect goes from first touch to closed-won. Who runs each stage. Where it leaks.

## Gaps an AE could close in 30 days

1. <gap> — <specific tactical move>
2. <gap> — <specific tactical move>
3. <gap> — <specific tactical move>

## What I'd test in week 1

- <experiment>
- <experiment>
- <experiment>

## Honest read

What's actually working. What's at risk. What's the wedge.
"""


def run(slug: str) -> str:
    target = load_target(slug)
    user = f"""# Target company

{yaml.safe_dump(target, sort_keys=False, default_flow_style=False)}

# Task

Write the GTM teardown of {target.get('company_name')}. Length: ~1500 words. Voice: editorial criticism, not marketing copy. Specific examples. No hedging.
"""
    return llm.complete(SYSTEM, user, model=llm.MODEL_DEEP, max_tokens=8192)
