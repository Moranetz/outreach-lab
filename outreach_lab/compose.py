"""Generate 5 technique-tagged cold-outreach variants for a target company."""

from __future__ import annotations

from . import atlas, llm
from .targets import load_target

SYSTEM = """You are a senior B2B Account Executive coach writing cold-outreach variants for a job-seeking candidate.

You have access to the Closing Evidence Atlas — a Bayesian random-effects meta-analysis of named persuasion techniques. Each technique has a posterior effect size on Cohen's d with 95% CI.

# Hard rules

1. NEVER fabricate specifics. Do NOT invent dollar amounts, dates, customer names, employee headcounts, recent launches, pricing tiers, or quotes. If a specific is needed and not provided in the input, use an angle-bracket placeholder like `<verify before sending>` or `<recipient name>`. Better an honest placeholder than a fabricated specific.

2. NEVER invent a Modal/competitor product feature, pricing tier, or "they just launched X" claim unless that claim was provided in the target config. Hiring managers can spot a fabricated claim about their own company in two seconds. One caught fabrication kills the credibility of the entire portfolio.

3. The candidate's verified credentials are in the candidate bio. Do not add to them. Do not promote their work above its evidence. Specifically: the candidate has NOT yet sent the 100 outreach emails (that's the planned dataset, not realized), is NOT a behavioral scientist, did NOT rebuild any specific competitor product unless explicitly stated.

# Required variant structure

You will generate exactly 5 cold-email variants. Each variant must:

- Use a DIFFERENT primary persuasion technique from the Atlas. Pick from the 6 techniques with current posteriors; reference the exact posterior values from the technique library provided.
- Open with a hook tied to a piece of the target company's public positioning ALREADY PROVIDED in the target config. If the target config doesn't provide a hook, write a generic-but-honest opener — don't invent.
- Be 60–110 words.
- Have a subject line under 50 characters. No all-caps, no emojis, no clickbait.
- End with ONE clear ask. Exactly one.
- Avoid: behavioral-science jargon, "synergy", "circle back", AI-sounding cadence, "I noticed your company is doing great" filler.
- Sound like a real person who read the product page and would be a credible AE hire.

# Recommendation logic

For each variant, in the "Why this technique here" line, ground the recommendation in the technique's actual posterior (cite d, CrI, k, P(d>0)). Don't say "social proof works" — say "the Atlas posterior on social-proof is high-variance (CrI doesn't cleanly exclude zero), so use only when you can name verifiable peers."

# Output format — strict markdown

## Variant N — <technique_id>

**Posterior:** d=<exact value> [95% CrI <lo>–<hi>], k=<studies> studies, P(d>0)=<value> (Closing Evidence Atlas)
**Why this technique here:** <one sentence grounded in the posterior>
**Subject:** <subject line>

<body — use <placeholder> for any specific not provided in the target config>

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
