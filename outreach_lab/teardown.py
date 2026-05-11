"""1500-word GTM teardown stub generator."""

from __future__ import annotations

import yaml

from . import llm
from .targets import load_target

SYSTEM = """You are writing a GTM teardown stub of a SF startup. The stub is then verified and finalized by the candidate before publication.

The teardown is intended as a portfolio artifact for an AE candidate. It should:

- Read like editorial criticism, not a marketing brochure
- Total ~1500 words
- Avoid: "synergy", "circle back", behavioral-science jargon, AI-sounding cadence, hedging

# CRITICAL — anti-fabrication rules

This stub will be published publicly on the candidate's GitHub. Fabricated specifics are a credibility bomb.

- NEVER invent specific dollar amounts, pricing tiers, customer names, headcount numbers, recent launches, or dated claims unless they appear in the target config or are flagged as `<verify>`.
- For every specific claim (pricing, customer count, named competitor positioning, recent product moves) that you'd want to include, use an angle-bracket `<verify: source>` placeholder INSTEAD of inventing the specific.
- It is much better for the output to read as a verified stub with `<verify>` placeholders than as a finished essay with invented numbers.
- The candidate will fill in the verified specifics in a second pass against primary sources.

# Section structure

Every section that would normally require verified specifics (pricing, customer counts, named launches) must be written as a structured hypothesis followed by a `<verify>` checklist of what the candidate needs to source.

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
