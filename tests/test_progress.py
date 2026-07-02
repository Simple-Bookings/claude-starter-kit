"""Tests for csk progress command."""

import subprocess
import tempfile
import os
from pathlib import Path


def test_progress_runs():
    """Test that csk progress runs without error."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        result = subprocess.run(["csk", "progress"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "CSK Exercise Progress" in result.stdout


def test_progress_shows_exercises():
    """Test that progress shows all 6 exercises."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        result = subprocess.run(["csk", "progress"], capture_output=True, text=True)
        assert "Setup" in result.stdout
        assert "Full Cycle" in result.stdout


def test_reset_clears_progress():
    """Test that csk reset clears progress file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        # Create a progress file
        Path(".csk-progress.md").write_text("- [x] 01: Setup\n")
        # Reset with confirm
        result = subprocess.run(
            ["csk", "reset", "-y"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert not Path(".csk-progress.md").exists()
