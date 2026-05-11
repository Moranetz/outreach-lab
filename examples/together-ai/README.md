# Together AI example

Run `outreach-lab all together-ai` against the config in `targets/together-ai.yaml` to generate this target's full output set.

The target config currently has `<verify>` placeholders for company specifics (pricing, headcount, recent launches) — that is intentional. The pattern is:

1. Run `outreach-lab init together-ai --company "Together AI" --url https://www.together.ai`
2. Fill in `<verify>` placeholders with sourced specifics from primary research (their pricing page, careers page, customer interviews)
3. THEN run `outreach-lab all together-ai`

This file exists to document that the pattern works on more than one company. The Modal Labs example in `examples/modal-labs/` is fully populated.
