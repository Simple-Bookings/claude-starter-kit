"""Tests for the csk test command."""

from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from csk.commands.test import test


def test_test_runs_pytest():
    """Test that csk test invokes pytest."""
    runner = CliRunner()

    with patch("csk.commands.test.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = runner.invoke(test)

        # Should call subprocess.run with pytest
        assert mock_run.called
        call_args = mock_run.call_args[0][0]
        assert "pytest" in " ".join(call_args)


def test_test_verbose_flag():
    """Test that -v flag is passed to pytest."""
    runner = CliRunner()

    with patch("csk.commands.test.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = runner.invoke(test, ["-v"])

        call_args = mock_run.call_args[0][0]
        assert "-v" in call_args


def test_test_coverage_flag():
    """Test that --coverage flag adds coverage args."""
    runner = CliRunner()

    with patch("csk.commands.test.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = runner.invoke(test, ["--coverage"])

        call_args = mock_run.call_args[0][0]
        assert "--cov=csk" in call_args
        assert "--cov-report=term-missing" in call_args


def test_test_returns_pytest_exit_code():
    """Test that csk test returns pytest's exit code."""
    runner = CliRunner()

    with patch("csk.commands.test.subprocess.run") as mock_run:
        # Simulate test failure
        mock_run.return_value = MagicMock(returncode=1)
        result = runner.invoke(test)

        assert result.exit_code == 1
