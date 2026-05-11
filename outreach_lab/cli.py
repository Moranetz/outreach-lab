"""CLI entrypoint."""

from __future__ import annotations

from pathlib import Path

import click

from . import atlas, brief, compose, tailor, teardown, track

OUTPUTS = Path(__file__).resolve().parent.parent / "outputs"
TARGETS_DIR = Path(__file__).resolve().parent.parent / "targets"


def _write(slug: str, filename: str, content: str) -> Path:
    out_dir = OUTPUTS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    path.write_text(content)
    return path


@click.group()
@click.version_option()
def cli() -> None:
    """outreach-lab — technique-tagged cold-outreach generator backed by the Closing Evidence Atlas."""


@cli.command("init")
@click.argument("slug")
@click.option("--company", "company_name", required=True, help="Company display name")
@click.option("--url", "company_url", required=True, help="Company homepage URL")
@click.option("--category", default="ai-infra", type=click.Choice(["ai-infra", "dev-tools", "fintech", "sales-tools", "other"]))
def cmd_init(slug: str, company_name: str, company_url: str, category: str) -> None:
    """Scaffold a new target YAML config."""
    path = TARGETS_DIR / f"{slug}.yaml"
    if path.exists():
        click.echo(f"Target {path} already exists. Edit it directly, or remove it first.")
        raise SystemExit(1)
    template = f"""slug: {slug}
company_name: {company_name}
company_url: {company_url}
careers_url: {company_url}/careers  # verify
category: {category}
size_band: <verify — e.g. 50-100 people>
buyer_persona: |
  <verify — who signs the contract; what role, decision speed, what they read>
product_one_liner: <verify — one sentence from their landing page>
pricing_summary: <verify — actual pricing tiers from their /pricing page>
known_competitors: [<verify>, <verify>]
your_angle: |
  <fill in — why this seat fits Marion specifically>
target_role: Account Executive
target_role_url: {company_url}/careers
ideal_first_contact: |
  <verify — LinkedIn search query to find the right person>
"""
    path.write_text(template)
    click.echo(f"Created {path}")
    click.echo("Next: edit the <verify> placeholders with sourced specifics, then:")
    click.echo(f"  outreach-lab all {slug}")


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


@cli.command("techniques")
@click.option("--cluster", default=None, help="Filter by cluster (framing, compliance, etc.)")
def cmd_techniques(cluster: str | None) -> None:
    """List every technique in the Atlas catalog and its evidence status."""
    raw = atlas._load_raw()

    def _show(label: str, items: list[dict]) -> None:
        rows = [t for t in items if not cluster or t.get("cluster") == cluster]
        if not rows:
            return
        click.echo(f"\n## {label} ({len(rows)})\n")
        for t in rows:
            posterior = ""
            if "atlas_posterior" in t:
                p = t["atlas_posterior"]
                posterior = f"  d={p['d_mu']} [{p['ci_lower']}-{p['ci_upper']}], k={p['k_studies']}"
            click.echo(f"  {t['id']:<28}  {t.get('cluster','-'):<22}{posterior}")

    _show("With current posteriors", raw["techniques"])
    _show("Inclusion literature, posterior pending", raw.get("techniques_without_posteriors", []))
    _show("Fragile (<5 studies)", raw.get("fragile_techniques", []))
    _show("Empirical deserts (zero peer-reviewed studies meeting inclusion criteria)",
          raw.get("empirical_deserts", []))


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
    try:
        track.append({"slug": slug, "company": target.get("company_name", ""), **kwargs})
    except ValueError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1) from e
    click.echo("Logged.")


@cli.command("analyze")
@click.option("--plain/--rich", default=False, help="Plain-text output instead of rich table")
def cmd_analyze(plain: bool) -> None:
    """Cohort response rate by technique."""
    click.echo(track.analyze(rich_output=not plain))


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
