"""Tests for csk exercises command."""

import subprocess
import tempfile


def test_exercises_help():
    """Test that csk exercises --help runs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "exercises", "--help"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        assert result.returncode == 0
        assert "exercises" in result.stdout.lower()
        assert "server" in result.stdout.lower() or "port" in result.stdout.lower()


def test_exercises_port_option():
    """Test that exercises accepts port option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "exercises", "--help"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        assert "--port" in result.stdout or "-p" in result.stdout
