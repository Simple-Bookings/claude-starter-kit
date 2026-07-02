"""Tests for csk init command."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def test_init_creates_project():
    """Test that csk init creates a project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        result = subprocess.run(
            ["csk", "init", "test-project"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert Path("test-project").exists()
        assert Path("test-project/CLAUDE.md").exists()


def test_init_creates_claude_directory():
    """Test that csk init creates .claude directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        subprocess.run(["csk", "init", "test-project"], capture_output=True)
        assert Path("test-project/.claude").exists()
        assert Path("test-project/.claude/skills").exists()
        assert Path("test-project/.claude/agents").exists()


def test_init_creates_docs():
    """Test that csk init creates docs directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        subprocess.run(["csk", "init", "test-project"], capture_output=True)
        assert Path("test-project/docs").exists()
        assert Path("test-project/docs/VISION.md").exists()
        assert Path("test-project/docs/FEATURES.md").exists()


def test_init_force_overwrites():
    """Test that csk init --force overwrites existing directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        # Create first
        subprocess.run(["csk", "init", "test-project"], capture_output=True)
        # Try to create again without force
        result = subprocess.run(
            ["csk", "init", "test-project"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        # With force should work
        result = subprocess.run(
            ["csk", "init", "--force", "test-project"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
