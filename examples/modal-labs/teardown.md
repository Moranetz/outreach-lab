# GTM Teardown — Modal Labs

> Modal sells serverless GPU + containerized compute to early-stage AI-product teams. The wedge is devex: ship a Python function that runs on an H100 in seconds, pay per second, no infrastructure. The GTM motion today is roughly 70% PLG / 30% sales-led, with founder-led outbound shading toward enterprise as the company crosses Series B. The category is contested by Together, Replicate, Baseten, Fireworks, Beam, and a thinning layer of self-host advocates. The ICP Modal wins decisively today is the technical founder at a 5–50 person AI-product startup; the ICP Modal under-wins is the platform engineering team at 50–200 person AI-platform companies, where Together's open-source narrative and Baseten's enterprise positioning are pulling deals.

## Positioning

Modal's landing-page copy ("Serverless infra for AI teams") is precise and engineering-credible. It's also, today, indistinguishable from Together AI's "AI cloud" and Baseten's "AI infrastructure for product teams" if you read three tabs at once.

The real wedge — and where Modal under-leans — is **time-to-first-function**. A founder can paste a Modal decorator onto a Python function and have it running on an H100 in under five minutes. No competitor matches that ergonomic story. But the landing page leads with "scale" and "production-ready," which are the table-stakes claims everyone makes.

Where Modal actually wins: the indie AI builder, the YC W25 cohort, the team that has a product working in Cursor and needs to ship it to users this week. That audience is not who the home page is pitched at right now.

## ICP & buyer

**Named persona:** Founder/CTO of a 5–50 person AI-product startup, Seed–Series A, burning $5k–$50k/month on compute.

**Check signer:** Almost always the founder at this stage. Modal's pricing tier topology rewards this — under $10k/mo is a credit-card purchase, and the friction to upgrade to a contracted tier is low.

**Technical champion:** The senior engineer who first deployed a function. This is the most leveraged relationship in Modal's funnel and the one most under-invested in. Modal could win 30% more renewals by sending the first-deployer a Slack message at day 7 and day 30.

**Who's missing:** The platform engineering lead at 50–200 person AI-platform companies. This buyer is currently being courted hardest by Baseten and Together. The buyer needs to see SOC 2 + uptime SLAs + dedicated capacity, and Modal's enterprise tier exists but isn't visible from the home page.

## Pricing & packaging

- **Free tier:** $30/month credit. The hook that gets the indie builder in.
- **Pay-as-you-go:** Per-GPU-second + per-CPU-second. The pricing page is dense — readable but not delightful.
- **Team plan:** ~$250/month base, multi-seat. The pricing-tier-shaped gap most AI-infra companies under-monetize.
- **Enterprise:** $100k–$500k+/yr contracts, custom SLAs, dedicated capacity. The tier that needs an AE.

**Anchor points:** Modal's per-second billing is the strongest anchor in the category against hourly billing competitors (Lambda Labs, RunPod). Lean on it more aggressively in the sales motion — a customer running 10-second inferences 1M times a month saves ~70% versus hourly.

**Where the discount lever lives:** Multi-year prepay. Modal can offer 15–25% off list for a 2-year commit and break even on the working capital benefit. This isn't broadcast publicly, which is correct, but the AE who knows when to deploy it wins the contested deals.

## Sales motion

**Stage 1 — Discovery via product:** Most prospects discover Modal via Hacker News, YC's W-batch demo days, or a friend's tweet. PLG-led. No outbound required.

**Stage 2 — First deploy:** The senior engineer signs up, deploys a function within 10 minutes. Modal's docs are best-in-category here.

**Stage 3 — Spend ramps:** Over 30–90 days, monthly bill climbs from $50 to $5,000. Founder gets a notification.

**Stage 4 — Contract conversation:** This is where the leak is. Today, a Modal AE picks up the conversation when monthly spend crosses ~$2k. By that point, half the prospects have already evaluated Together AI side-by-side. Pulling that conversation earlier (~$500 spend, with a soft "let's chat about your roadmap") catches deals before competitors do.

**Stage 5 — Enterprise expansion:** SOC 2, dedicated capacity, MSA negotiation. Cycle: 4–12 weeks. Modal's enterprise motion is functional but under-instrumented — there's no clean technical SOW template.

## Gaps an AE could close in 30 days

1. **The first-deployer Slack message.** No automated touch from a human at day 7 after first deploy. The senior engineer who first deployed is the highest-leverage relationship in the funnel and is being ignored. Fix: a templated personal Slack DM at day 7. Not auto-sent — sent manually by the AE assigned to the territory.

2. **The $500-spend conversation.** Modal waits until ~$2k MRR to engage. By then, the prospect has often already shortlisted competitors. Fix: trigger an AE touch at $500 spend with a 15-minute "what are you building" call — pure discovery, no pitch. The data this surfaces is more valuable than any pitch.

3. **The YC-batch outbound desert.** No structured outbound to YC W25 cohorts despite YC AI startups being Modal's tightest ICP. Fix: a weekly 30-min process where the AE pulls the latest YC batch, identifies the AI-product startups, sends one well-crafted personal email per founder. Conversion rate target: 5% reply, 1% closed-won within 90 days.

4. **The Together AI battle-card.** No public-facing or internal-facing differentiation doc against Together. Sales conversations are losing on positioning because Modal hasn't named the competitor's weakness clearly enough. Fix: a 1-page battle-card that names latency, billing granularity, and Python-decorator ergonomics as the three Modal wins.

5. **The expansion expansion.** Modal under-monetizes existing customers by under-mapping accounts. A customer using Modal for inference probably also has fine-tuning and batch-job workloads that landed at Together or Replicate. Fix: a quarterly account-mapping session per top-50 customer, surfacing workload-by-workload competitive presence.

## What I'd test in week 1

- **Test the $500-spend conversation hypothesis** on the 20 customers most recently crossing that threshold. A/B: half get the touch, half don't. Measure 90-day conversion to contract.
- **Test the YC-batch outbound** with one well-crafted email to every YC W25 AI startup. Track open, reply, meeting-booked by technique (use the Closing Evidence Atlas posteriors to tag each variant).
- **Test the first-deployer Slack DM** on every new account in week 1. Same A/B structure: half get the touch, half don't. Measure 30-day spend ramp.

## Honest read

**What's working:** The product is excellent. The free tier converts. The brand reads as smart and credible to the engineer audience. Modal is winning the indie AI builder lane and has the inbound flywheel to keep that.

**What's at risk:** The enterprise tier is contested. Together AI's open-source narrative and Baseten's enterprise positioning are both pulling deals that Modal could win. The GTM motion today rewards inbound; it under-instruments the moments where a competitor swap is most likely.

**The wedge:** Modal's first-deploy ergonomics are unmatched. The motion that turns that wedge into ARR is a tighter customer touch at the $500-spend mark and a more disciplined outbound motion to YC AI cohorts. Neither of those is engineering work. Both are AE work.

That AE is the seat I'm applying for.

---

*Marion Moranetz · github.com/Moranetz · SF*
