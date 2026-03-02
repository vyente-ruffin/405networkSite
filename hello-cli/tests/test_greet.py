"""Tests for the greet command based on Gherkin scenarios.

Feature: Greet Command
  Scenario: User greets with a name
    Given the hello-cli is installed
    When the user runs "hello Alice"
    Then the output is "Hello, Alice!"
    And the exit code is 0

  Scenario: User requests help
    Given the hello-cli is installed
    When the user runs "hello --help"
    Then the output contains "Usage:"
    And the exit code is 0
"""

from typer.testing import CliRunner

from hello_cli.main import app

runner = CliRunner()


def test_greet_with_name():
    """Scenario: User greets with a name."""
    # When the user runs "hello Alice"
    result = runner.invoke(app, ["Alice"])

    # Then the output is "Hello, Alice!"
    assert "Hello, Alice!" in result.stdout

    # And the exit code is 0
    assert result.exit_code == 0


def test_greet_help():
    """Scenario: User requests help."""
    # When the user runs "hello --help"
    result = runner.invoke(app, ["--help"])

    # Then the output contains "Usage:"
    assert "Usage:" in result.stdout

    # And the exit code is 0
    assert result.exit_code == 0
