"""Generate 5 technique-tagged cold-outreach variants for a target company."""

from __future__ import annotations

from . import atlas, llm
from .targets import load_target


SYSTEM = """You are a senior B2B Account Executive coach writing cold-outreach variants for a job-seeking candidate.

You have access to the Closing Evidence Atlas — a Bayesian random-effects meta-analysis of named persuasion techniques. Each technique has a posterior effect size on Cohen's d with 95% CI.

You will generate exactly 5 cold-email variants. Each variant must:

1. Use a DIFFERENT primary persuasion technique from the Atlas.
2. Open with a specific, non-generic hook tied to the target company's actual product or recent move — no "I saw your company is doing great" filler.
3. Be 60–110 words. Short enough to read on a phone.
4. Have a subject line under 50 characters that signals respect for the reader's time (no all-caps, no emojis, no clickbait).
5. End with ONE clear ask. Not three. Not zero. Exactly one.
6. Avoid: behavioral-science jargon, "synergy", "circle back", buzzwords, AI-sounding cadence.
7. Sound like a real person who has actually read the product page and would be a credible AE hire.

Output format — strict markdown:

## Variant N — <technique_id>

**Posterior:** d=<value> [95% CI <lo>–<hi>], k=<studies> studies (Closing Evidence Atlas)
**Why this technique here:** <one sentence>
**Subject:** <subject line>

<body>

**Ask:** <one-sentence summary of the ask>

---
"""


def render_user_prompt(target: dict, candidate_summary: str) -> str:
    return f"""# Target company

**Company:** {target.get('company_name')}
**URL:** {target.get('company_url')}
**Category:** {target.get('category')}
**Size:** {target.get('size_band')}
**Buyer persona:**
{target.get('buyer_persona', '').strip()}

**Product one-liner:** {target.get('product_one_liner')}
**Pricing summary:** {target.get('pricing_summary')}
**Known competitors:** {', '.join(target.get('known_competitors', []))}
**Target role:** {target.get('target_role')} — {target.get('target_role_url')}
**Ideal first contact:** {target.get('ideal_first_contact', '').strip()}

# Candidate angle (Marion's wedge)

{target.get('your_angle', '').strip()}

# Candidate one-line bio

{candidate_summary}

# Technique library (from the Closing Evidence Atlas)

{atlas.technique_summary()}

# Task

Write 5 cold-outreach variants for Marion to send to the ideal first contact at {target.get('company_name')}.
Each variant uses a DIFFERENT technique from the library above.
Each variant must be specific to {target.get('company_name')}'s actual product — generic templates will be rejected.
"""


CANDIDATE_BIO = (
    "Marion Moranetz — SF-based indie iOS founder (17 apps shipped in 5 months) + persuasion-systems "
    "builder (Closing Evidence Atlas — Bayesian meta-analysis of 39 named techniques). Building "
    "outreach-lab — open-source AE tooling. Seeking first AE seat at AI-infra or dev-tools company."
)


def run(slug: str) -> str:
    target = load_target(slug)
    user = render_user_prompt(target, CANDIDATE_BIO)
    return llm.complete(SYSTEM, user, model=llm.MODEL_FAST, max_tokens=4096)
