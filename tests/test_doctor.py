"""Tests for csk doctor command."""

import subprocess


def test_doctor_runs():
    """Test that csk doctor runs without error."""
    result = subprocess.run(["csk", "doctor"], capture_output=True, text=True)
    assert "CSK2 Environment Check" in result.stdout
    # Should exit 0 if all checks pass, 1 if some fail
    assert result.returncode in [0, 1]


def test_doctor_checks_git():
    """Test that doctor checks for git."""
    result = subprocess.run(["csk", "doctor"], capture_output=True, text=True)
    assert "git" in result.stdout.lower()


def test_doctor_checks_claude():
    """Test that doctor checks for claude."""
    result = subprocess.run(["csk", "doctor"], capture_output=True, text=True)
    assert "claude" in result.stdout.lower()
