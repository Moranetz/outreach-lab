"""Smoke tests for the CLI — exercises the surface without spending API budget."""

from __future__ import annotations

from click.testing import CliRunner

from outreach_lab.cli import cli


def test_help_works():
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "outreach-lab" in result.output


def test_techniques_lists_all_populations():
    result = CliRunner().invoke(cli, ["techniques"])
    assert result.exit_code == 0
    assert "With current posteriors" in result.output
    assert "Empirical deserts" in result.output
    assert "gain-framing" in result.output
    assert "trial-close" in result.output  # desert


def test_techniques_filtered_by_cluster():
    result = CliRunner().invoke(cli, ["techniques", "--cluster", "framing"])
    assert result.exit_code == 0
    assert "gain-framing" in result.output
    # should not include structural-close techniques
    assert "trial-close" not in result.output


def test_track_with_unknown_technique_fails():
    result = CliRunner().invoke(cli, [
        "track", "modal-labs",
        "--variant", "v1",
        "--technique", "not-a-technique",
        "--subject", "test",
    ])
    assert result.exit_code == 1
    assert "Unknown technique id" in result.output


def test_analyze_with_empty_log(tmp_path, monkeypatch):
    from outreach_lab import track
    monkeypatch.setattr(track, "LOG_PATH", tmp_path / "log.csv")
    result = CliRunner().invoke(cli, ["analyze", "--plain"])
    assert result.exit_code == 0
    assert "No log yet" in result.output or "No sends" in result.output


def test_version():
    result = CliRunner().invoke(cli, ["--version"])
    assert result.exit_code == 0
