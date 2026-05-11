# Examples

Each subdirectory is the output of `outreach-lab all <slug>` for a real target company in Marion's job search.

- [`modal-labs/`](./modal-labs/) — Account Executive at Modal Labs (AI-infra, ~70 people, serverless GPU)

Add a new example by creating a target config (`targets/<slug>.yaml`) and running:

```bash
outreach-lab all <slug>
cp -r outputs/<slug> examples/<slug>
```
