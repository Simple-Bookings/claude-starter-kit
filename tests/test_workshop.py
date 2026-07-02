"""Tests for csk workshop command."""

import subprocess
import tempfile


def test_workshop_help():
    """Test that csk workshop --help runs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "workshop", "--help"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        assert result.returncode == 0
        assert "workshop" in result.stdout.lower()
        assert "kompendium" in result.stdout.lower() or "materials" in result.stdout.lower()


def test_workshop_port_option():
    """Test that workshop accepts port option with default 9123."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "workshop", "--help"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        assert "--port" in result.stdout or "-p" in result.stdout
        assert "9123" in result.stdout  # Default port


def test_workshop_stop_subcommand():
    """Test that workshop stop subcommand exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "workshop", "stop", "--help"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        assert result.returncode == 0
        assert "stop" in result.stdout.lower()


def test_workshop_restart_subcommand():
    """Test that workshop restart subcommand exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["csk", "workshop", "restart", "--help"],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        assert result.returncode == 0
        assert "restart" in result.stdout.lower()
