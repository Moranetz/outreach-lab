"""CSV log of every send + outcome. The dataset for the 100-outreach experiment."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "outreach_log.csv"

FIELDS = [
    "sent_date",
    "slug",
    "company",
    "variant_id",
    "technique_id",
    "subject",
    "recipient_role",
    "channel",       # email | linkedin | twitter
    "response",      # none | opened | replied | meeting-booked | bounced
    "outcome",       # pending | dead | qualified | closed-won | closed-lost
    "notes",
]


def _ensure_header() -> None:
    if not LOG_PATH.exists():
        with LOG_PATH.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def append(row: dict) -> None:
    _ensure_header()
    row.setdefault("sent_date", date.today().isoformat())
    row = {k: row.get(k, "") for k in FIELDS}
    with LOG_PATH.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)


def analyze() -> str:
    """Cohort response rate by technique."""
    if not LOG_PATH.exists():
        return "No log yet. Use `outreach-lab track` after each send."

    by_tech: dict[str, dict[str, int]] = {}
    total = 0
    with LOG_PATH.open() as f:
        for row in csv.DictReader(f):
            tech = row["technique_id"] or "unknown"
            bucket = by_tech.setdefault(tech, {"sent": 0, "opened": 0, "replied": 0, "meeting": 0})
            bucket["sent"] += 1
            total += 1
            r = row["response"]
            if r in ("opened", "replied", "meeting-booked"):
                bucket["opened"] += 1
            if r in ("replied", "meeting-booked"):
                bucket["replied"] += 1
            if r == "meeting-booked":
                bucket["meeting"] += 1

    if total == 0:
        return "No sends logged yet."

    lines = [f"Total sends: {total}", "", "Technique | sent | opened | replied | meetings"]
    lines.append("---------|------|--------|---------|--------")
    for tech, b in sorted(by_tech.items(), key=lambda x: -x[1]["sent"]):
        lines.append(
            f"{tech} | {b['sent']} | {b['opened']} | {b['replied']} | {b['meeting']}"
        )
    return "\n".join(lines)
