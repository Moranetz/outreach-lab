"""Per-company resume bullet tailoring."""

from __future__ import annotations

import yaml

from . import llm
from .targets import load_resume, load_target

SYSTEM = """You are a senior resume editor specializing in early-career AE candidates breaking into AI-infrastructure and developer-tools sales.

You will produce a tailored resume bullet patch for a specific target company.

Output format — strict markdown:

# Resume tailoring — <Company name>

## Lead-with bullets (above the fold, in this order)

1. <bullet — rewritten and tightened for this company; 1-2 lines>
2. <bullet — rewritten and tightened>
3. <bullet — rewritten and tightened>

## Supporting bullets (mid-resume)

- <bullet>
- <bullet>
- <bullet>

## Cut entirely for this application

- <bullet> — reason

## Cover-letter opener (1 paragraph, 3-5 sentences)

<opener — must sound like a real person, must reference the company's actual product or recent move, must not start with "I am writing to apply">

## Headline (under the candidate name)

<one-line positioning, 8-14 words>

Rules:
- Every bullet must be honest. Do not invent metrics. Do not promote bullets above their actual evidence in the master_resume.yaml.
- Lead with credibility moves the buyer will care about, not what's most impressive in the abstract.
- Cut everything that dilutes. A 3-bullet resume that hits hard beats a 12-bullet resume that hedges.
- Cover-letter opener must reference something specific about THIS company — but only specifics that appear in the target config or are flagged as `<verify>` placeholders. Do NOT invent a recent launch, a specific customer, or a quote.
- The Atlas posteriors cited in the cover letter must match the technique library exactly — do not round or change them.
"""


def run(slug: str) -> str:
    target = load_target(slug)
    resume = load_resume()
    user = f"""# Target company

{yaml.safe_dump(target, sort_keys=False, default_flow_style=False)}

# Candidate's master resume bullet library

{yaml.safe_dump(resume, sort_keys=False, default_flow_style=False)}

# Task

Produce the tailored resume bullet patch for this company. Use the bullets that match this company's category (the 'relevance' field per bullet). Cut anything tagged 'cut' for this category. Rewrite each surviving bullet to point AT this company's specific buyer pain.
"""
    return llm.complete(SYSTEM, user, model=llm.MODEL_DEEP, max_tokens=4096)
