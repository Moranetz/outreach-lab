# outreach-lab

> Technique-tagged cold-outreach generator backed by a Bayesian meta-analysis of named persuasion techniques.

Built by [Marion Moranetz](https://github.com/Moranetz) as part of an AE job search. The tool generates per-company outreach materials AND logs every send into the dataset for an in-flight 100-outreach experiment.

This repo is two things at once:
1. **A working CLI** — generates emails, resume bullets, and GTM teardowns tailored to each target company
2. **A portfolio artifact** — proof that the candidate builds sales tooling, not just talks about it

---

## What it does

For any target company, in ~90 seconds:

```bash
outreach-lab all modal-labs
```

produces:

```
outputs/modal-labs/
├── brief.md            # one-page company brief
├── emails.md           # 5 cold-email variants, each using a different Atlas technique
├── resume-tailor.md    # which bullets to lead with for this company, what to cut
└── teardown.md         # 1500-word GTM teardown stub
```

Each email cites the **posterior effect size** of the technique it uses, from the [Closing Evidence Atlas](https://github.com/Moranetz/closing-evidence-atlas) — a pre-registered Bayesian random-effects meta-analysis of named persuasion techniques (44 records extracted, 6 per-technique posteriors at v0.1).

## Why this exists

A standard AE job search produces a single resume sent to fifty companies and a single cold email rewritten by hand each time. Both are leaky.

This tool inverts both:

- **Per-target tailoring is mechanical, not manual.** The candidate's master bullets live in `data/master_resume.yaml`. Each one is tagged with the company categories it's relevant to. The tailor command picks the right subset and rewrites them for the target.
- **Outreach is technique-tagged, not vibes-based.** Five variants per target, each tagged with a technique from the Atlas + that technique's posterior effect size. Sends get logged. After 100 sends, the candidate has a real dataset on which techniques moved which buyers.

The dataset is the 100-outreach experiment. The repo is the cover letter.

## Install

```bash
git clone https://github.com/Moranetz/outreach-lab.git
cd outreach-lab
python -m venv .venv && source .venv/bin/activate
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
```

## Use

### 1. Add a target

Create `targets/<slug>.yaml` (see `targets/example.yaml`):

```yaml
slug: modal-labs
company_name: Modal Labs
company_url: https://modal.com
category: ai-infra
size_band: 50-100 people
buyer_persona: |
  Founder/CTO of an AI-product startup ...
product_one_liner: Serverless GPU + containerized compute for AI workloads.
pricing_summary: Per-GPU-second + per-CPU-second. Enterprise $100k+.
known_competitors: [Together AI, Replicate, Baseten]
your_angle: |
  You are the buyer Modal sells to ...
target_role: Account Executive
target_role_url: https://modal.com/careers
ideal_first_contact: |
  Head of GTM, VP Sales, or founder directly.
```

### 2. Generate

```bash
outreach-lab brief modal-labs        # 400-word company brief
outreach-lab compose modal-labs      # 5 technique-tagged emails
outreach-lab tailor modal-labs       # per-company resume patch
outreach-lab teardown modal-labs     # 1500-word GTM teardown
outreach-lab all modal-labs          # all four in one shot
```

### 3. Send + log

Pick the best variant. Send manually (no auto-send — at the deal sizes Marion is targeting, every send is a deliberate act). Log it:

```bash
outreach-lab track modal-labs \
  --variant v3 \
  --technique scarcity-urgency \
  --subject "3 design partners left for Q3" \
  --recipient "VP Sales" \
  --response opened
```

### 4. Analyze

```bash
outreach-lab analyze
```

```
Total sends: 47
Technique          | sent | opened | replied | meetings
-------------------|------|--------|---------|---------
loss-framing       |  12  |   8    |   3     |   2
specificity-cred…  |   9  |   7    |   4     |   2
social-proof       |  11  |   5    |   2     |   1
scarcity-urgency   |   8  |   3    |   1     |   0
gain-framing       |   7  |   4    |   2     |   1
```

That table — built up over real sends — is the dataset that an AE hire promises. Most candidates promise the dataset. This candidate ships it.

## Architecture

```
outreach_lab/
├── cli.py        # Click entrypoint
├── atlas.py      # Loads techniques + posteriors from Closing Evidence Atlas
├── brief.py      # Brief generator
├── compose.py    # 5-variant email generator
├── tailor.py     # Per-company resume bullet patch
├── teardown.py   # 1500-word GTM teardown
├── track.py      # CSV logging + cohort analysis
├── targets.py    # Loads per-company YAML configs
└── llm.py        # Anthropic Claude API wrapper

data/
├── techniques.json     # 6 techniques + posteriors (mirrors Closing Evidence Atlas v0.1)
└── master_resume.yaml  # Candidate's master bullet library, tagged by category

targets/
└── *.yaml              # One per target company. example.yaml is committed.

outputs/                # Per-target generated artifacts. Gitignored.
outreach_log.csv        # The 100-outreach dataset. Gitignored.
```

## What this repo is NOT

- Not an email blaster. Manual send only. No SMTP integration. No LinkedIn automation. No scraping.
- Not a CRM. It's a generation + logging tool. Real CRM lives in the candidate's head.
- Not a personality test. Five variants per target gives the recipient five chances at a hook, not five attempts at the same hook.

## License

MIT. Forking encouraged. If you ship a variant of this for your own AE search, ping [@Moranetz](https://github.com/Moranetz).

## See also

- [closing-evidence-atlas](https://github.com/Moranetz/closing-evidence-atlas) — the meta-analysis this tool draws posteriors from
- [selected-work](https://github.com/Moranetz/selected-work) — Marion's curated portfolio
- [moranetz.github.io](https://moranetz.github.io) — the front door
