---
project_name: hello-cli
project_type: CLI
scope: Lab
status: prd-complete
created: 2026-01-10
---

# PRD: hello-cli

## Overview
A minimal Python CLI that greets users by name. This is a POC/lab project to validate the `/project` workflow end-to-end.

## Goals & Objectives
- **Primary goal**: Print a personalized greeting when given a name
- **Problem solved**: Testing the /project → PRD → TDD → Ralph Loop pipeline
- **Success criteria**: Running `hello Alice` outputs `Hello, Alice!`
- **Scope**: Lab project - no production concerns

## Features & Requirements

### Feature 1: Greet Command
- **Description**: Takes a name argument and prints a greeting
- **Command**: `hello <name>`
- **Acceptance Criteria**:
  - Outputs "Hello, [name]!" to stdout
  - Exits with code 0 on success
  - Shows help with `hello --help`
- **Dependencies**: None

**Gherkin Scenario:**
```gherkin
Feature: Greet Command
  Scenario: User greets with a name
    Given the hello-cli is installed
    And Python 3.x is available
    When the user runs "hello Alice"
    Then the output is "Hello, Alice!"
    And the exit code is 0

  Scenario: User requests help
    Given the hello-cli is installed
    When the user runs "hello --help"
    Then the output contains "Usage:"
    And the exit code is 0
```

## Technical Approach
- **Language**: Python 3.x
- **Framework**: Typer
- **Storage**: None (stateless)
- **Key libraries**: typer

## Infrastructure
- **Hosting**: Local
- **Deployment**: Manual via venv (pip install -e .)

## Prerequisites
- [ ] Python 3.x - verify: `python3 --version`
- [ ] pip available - verify: `pip3 --version`
- [ ] venv created - verify: `test -d .venv && .venv/bin/python --version`

## Tools & Resources
- **MCP Servers**: Context7 for Typer documentation

## Out of Scope
- Configuration files
- Multiple languages/localization
- Logging or telemetry
- Distribution/packaging beyond local install

## Notes
This is a test project for the /project plugin workflow. Intentionally minimal to validate the framework.
