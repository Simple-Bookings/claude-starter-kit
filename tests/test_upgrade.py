"""Tests for csk upgrade command."""

import os
import subprocess
import tempfile


def test_upgrade_check_runs():
    """Test that csk upgrade --check runs without error."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "upgrade", "--check"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        assert result.returncode == 0
        assert "Current version" in result.stdout


def test_upgrade_shows_version():
    """Test that upgrade shows current version."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "upgrade", "--check"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        # Should show version even if update check fails
        assert "version" in result.stdout.lower()
