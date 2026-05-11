# dashboard/

Static HTML dashboard for visualizing the `outreach_log.csv` cohort response-rate table publicly.

## What it shows

- Total sends, any-response count, reply count, meetings booked
- Per-technique cohort table (sent / opened / replied / meetings / percentages)
- Open-rate bar chart sorted by technique
- The Atlas posteriors as reference, so a reader can cross-check whether observed open-rate aligns with underlying d-values

## Local preview

```bash
cd dashboard
python -m http.server 8000
open http://localhost:8000
```

`fetch()` is blocked when opening `index.html` via `file://` in most browsers — use the local server.

## Live data

`index.html` reads `sample_log.csv` by default (12 example rows, banner says "Sample data"). To use your real data:

1. Run `outreach-lab track ...` to log real sends to the project's `outreach_log.csv`
2. Copy that file into `dashboard/` and rename to `sample_log.csv` (or change the fetch URL in `index.html`)
3. Refresh

## GitHub Pages

To host publicly:

1. Push the repo with `dashboard/` committed
2. Repo Settings → Pages → Source: `main` branch, `/dashboard` folder
3. The dashboard publishes at `https://Moranetz.github.io/outreach-lab/`

## Design notes

- No framework, no build step, no chart library — plain HTML / CSS / vanilla JS
- Editorial typography (Inter / JetBrains Mono), navy accent #1E3A5F
- Mobile-friendly (collapses summary cards + tightens bar-chart widths under 700px)
- Drops the banner once `sample_log.csv` is replaced with a non-sample file (rename, or edit `index.html` to remove the banner div)
