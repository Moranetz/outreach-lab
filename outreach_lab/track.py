"""CSV log of every send + outcome. The dataset for the 100-outreach experiment."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from . import atlas

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


def validate_technique(technique_id: str) -> None:
    """Reject unknown technique ids — protects the dataset from typos."""
    if technique_id not in atlas.all_technique_ids():
        valid = sorted(atlas.all_technique_ids())
        raise ValueError(
            f"Unknown technique id '{technique_id}'. Valid ids:\n  "
            + "\n  ".join(valid)
        )


def append(row: dict) -> None:
    if row.get("technique_id"):
        validate_technique(row["technique_id"])
    _ensure_header()
    row.setdefault("sent_date", date.today().isoformat())
    row = {k: row.get(k, "") for k in FIELDS}
    with LOG_PATH.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)


def analyze(rich_output: bool = True) -> str:
    """Cohort response rate by technique. Rich-formatted by default."""
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

    if rich_output:
        try:
            from rich.console import Console
            from rich.table import Table
        except ImportError:
            rich_output = False

    if rich_output:
        from io import StringIO

        from rich.console import Console
        from rich.table import Table

        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=88)
        table = Table(title=f"Outreach cohort — {total} sends", show_lines=False)
        table.add_column("Technique", style="cyan", no_wrap=True)
        table.add_column("Sent", justify="right")
        table.add_column("Opened", justify="right")
        table.add_column("Replied", justify="right")
        table.add_column("Meetings", justify="right")
        table.add_column("Open %", justify="right")
        table.add_column("Reply %", justify="right")

        for tech, b in sorted(by_tech.items(), key=lambda x: -x[1]["sent"]):
            open_pct = (b["opened"] / b["sent"]) * 100 if b["sent"] else 0
            reply_pct = (b["replied"] / b["sent"]) * 100 if b["sent"] else 0
            table.add_row(
                tech,
                str(b["sent"]),
                str(b["opened"]),
                str(b["replied"]),
                str(b["meeting"]),
                f"{open_pct:.0f}%",
                f"{reply_pct:.0f}%",
            )

        console.print(table)
        return buf.getvalue()

    lines = [f"Total sends: {total}", "", "Technique | sent | opened | replied | meetings"]
    lines.append("---------|------|--------|---------|--------")
    for tech, b in sorted(by_tech.items(), key=lambda x: -x[1]["sent"]):
        lines.append(
            f"{tech} | {b['sent']} | {b['opened']} | {b['replied']} | {b['meeting']}"
        )
    return "\n".join(lines)
