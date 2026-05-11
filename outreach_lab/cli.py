"""CLI entrypoint."""

from __future__ import annotations

from pathlib import Path

import click

from . import brief, compose, tailor, teardown, track


OUTPUTS = Path(__file__).resolve().parent.parent / "outputs"


def _write(slug: str, filename: str, content: str) -> Path:
    out_dir = OUTPUTS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    path.write_text(content)
    return path


@click.group()
def cli() -> None:
    """outreach-lab — technique-tagged cold-outreach generator backed by the Closing Evidence Atlas."""


@cli.command("brief")
@click.argument("slug")
def cmd_brief(slug: str) -> None:
    """One-page company brief."""
    content = brief.run(slug)
    path = _write(slug, "brief.md", content)
    click.echo(f"Wrote {path}")


@cli.command("compose")
@click.argument("slug")
def cmd_compose(slug: str) -> None:
    """Generate 5 technique-tagged cold emails."""
    content = compose.run(slug)
    path = _write(slug, "emails.md", content)
    click.echo(f"Wrote {path}")


@cli.command("tailor")
@click.argument("slug")
def cmd_tailor(slug: str) -> None:
    """Generate per-company resume bullet patches."""
    content = tailor.run(slug)
    path = _write(slug, "resume-tailor.md", content)
    click.echo(f"Wrote {path}")


@cli.command("teardown")
@click.argument("slug")
def cmd_teardown(slug: str) -> None:
    """1500-word GTM teardown stub."""
    content = teardown.run(slug)
    path = _write(slug, "teardown.md", content)
    click.echo(f"Wrote {path}")


@cli.command("track")
@click.argument("slug")
@click.option("--variant", "variant_id", required=True, help="Variant id you sent (e.g. v3)")
@click.option("--technique", "technique_id", required=True, help="Technique id from the Atlas")
@click.option("--subject", required=True)
@click.option("--recipient", "recipient_role", default="", help="Role of recipient")
@click.option("--channel", default="email", type=click.Choice(["email", "linkedin", "twitter"]))
@click.option("--response", default="none", type=click.Choice(["none", "opened", "replied", "meeting-booked", "bounced"]))
@click.option("--outcome", default="pending", type=click.Choice(["pending", "dead", "qualified", "closed-won", "closed-lost"]))
@click.option("--notes", default="")
def cmd_track(slug: str, **kwargs) -> None:
    """Log a send + outcome to outreach_log.csv."""
    from .targets import load_target

    target = load_target(slug)
    track.append({"slug": slug, "company": target.get("company_name", ""), **kwargs})
    click.echo("Logged.")


@cli.command("analyze")
def cmd_analyze() -> None:
    """Cohort response rate by technique."""
    click.echo(track.analyze())


@cli.command("all")
@click.argument("slug")
def cmd_all(slug: str) -> None:
    """Run brief + compose + tailor + teardown in one shot."""
    for name, mod in [
        ("brief", brief),
        ("compose", compose),
        ("tailor", tailor),
        ("teardown", teardown),
    ]:
        click.echo(f"Running {name}...")
        content = mod.run(slug)
        ext = {
            "brief": "brief.md",
            "compose": "emails.md",
            "tailor": "resume-tailor.md",
            "teardown": "teardown.md",
        }[name]
        path = _write(slug, ext, content)
        click.echo(f"  → {path}")
    click.echo(f"\nDone. See outputs/{slug}/")


if __name__ == "__main__":
    cli()
