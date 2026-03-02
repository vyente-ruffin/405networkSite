---
project: hello-cli
generated: 2026-01-10
status: pending
---

# hello-cli Tasks

## Category 1: Setup

### setup-1: Create venv and project structure
- **category**: setup
- **type**: setup
- **description**: Create Python venv and project structure for hello-cli
- **verification**: `test -d .venv && test -f hello_cli/__init__.py && test -f pyproject.toml`
- **expected**: PASS
- **dependencies**: []

### setup-2: Install dependencies
- **category**: setup
- **type**: setup
- **description**: Install typer and pytest in venv
- **verification**: `.venv/bin/pip freeze | grep -q typer && .venv/bin/pip freeze | grep -q pytest`
- **expected**: PASS
- **dependencies**: [setup-1]

---

## Category 3: App (TDD)

### feature-1-test: Write test for Greet Command
- **category**: app
- **type**: test
- **description**: Write pytest tests for the greet command
- **gherkin**: |
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
- **verification**: `.venv/bin/pytest tests/test_greet.py -v --tb=short 2>&1 | grep -q "FAILED\|passed"`
- **expected_initial**: FAIL (TDD - test written before implementation)
- **dependencies**: [setup-2]

### feature-1-impl: Implement Greet Command
- **category**: app
- **type**: implement
- **description**: Implement the greet command to make tests pass
- **gherkin**: (same as feature-1-test)
- **verification**: `.venv/bin/pytest tests/test_greet.py -v --tb=short`
- **expected**: PASS
- **dependencies**: [feature-1-test]

---

## Category 5: Smoke

### smoke-1: End-to-end verification
- **category**: smoke
- **type**: e2e
- **description**: Verify hello-cli works end-to-end after install
- **verification**: `.venv/bin/pip install -e . && .venv/bin/hello Alice | grep -q "Hello, Alice!"`
- **expected**: PASS
- **dependencies**: [feature-1-impl]

---

## Execution Order

```
setup-1 → setup-2 → feature-1-test → feature-1-impl → smoke-1
```

## Task Summary

| ID | Category | Type | Description | Depends On |
|----|----------|------|-------------|------------|
| setup-1 | setup | setup | Create venv and project structure | - |
| setup-2 | setup | setup | Install dependencies | setup-1 |
| feature-1-test | app | test | Write test for Greet Command | setup-2 |
| feature-1-impl | app | implement | Implement Greet Command | feature-1-test |
| smoke-1 | smoke | e2e | End-to-end verification | feature-1-impl |
