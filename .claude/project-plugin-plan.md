---
name: project-plugin-plan
version: 0.2.0
status: framework-complete
last_updated: 2026-01-10
---

# Project Plugin Plan

## Goal

Create a `/project` command that:
1. Builds PRD through freeform conversation (senior engineer mindset)
2. Generates Gherkin scenarios for each feature
3. Validates prerequisites before execution
4. Converts scenarios to TDD-structured tasks
5. Executes each task wrapped in Ralph Loop with deterministic verification

## Architecture Overview

```
/project "description" or /project (start conversation)
     │
     ▼
┌─────────────────────────────────────────────────────┐
│ PHASE 1: Conversational Discovery                   │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ User describes what they want                   │ │
│ │         ↓                                       │ │
│ │ Claude responds with:                           │ │
│ │  • Understanding of the ask                     │ │
│ │  • Recommended tools/tech/MCP servers           │ │
│ │  • ONE clarifying question if genuinely needed  │ │
│ │  • Proportionate blocker flags (scope-aware)    │ │
│ │         ↓                                       │ │
│ │ Loop until user confirms ("yes")                │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ MUST GATHER: All mandatory PRD fields              │
│ DERIVE: scope from conversation (ask if unclear)   │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │ User types "yes"
                       ▼
┌─────────────────────────────────────────────────────┐
│ PHASE 2: Generate PRD + Gherkin Scenarios           │
│                                                     │
│ Build PRD with mandatory JSON structure             │
│ Generate Gherkin scenario for each feature          │
│ Save to: .claude/project.local.md                   │
│ Show user for confirmation                          │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │ User confirms scenarios
                       ▼
┌─────────────────────────────────────────────────────┐
│ PHASE 0: Prerequisites Check                        │
│                                                     │
│ For each prerequisite in PRD:                       │
│   ✓ Azure subscription → verify with az account    │
│   ✓ GitHub access → verify with gh auth status     │
│   ✓ API keys → verify env vars exist               │
│   ✓ Tools installed → verify commands available    │
│                                                     │
│ ❌ STOP if any prerequisite fails                   │
│ ✓ Continue only when ALL prerequisites pass        │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │ All prerequisites verified
                       ▼
┌─────────────────────────────────────────────────────┐
│ PHASE 3: Convert Gherkin → TDD Tasks                │
│                                                     │
│ For each Gherkin scenario:                          │
│   1. Generate TEST task (runs first, expects fail)  │
│   2. Generate IMPLEMENT task (makes test pass)      │
│                                                     │
│ Task categories (execution order):                  │
│   1. Setup     - Environment, dependencies          │
│   2. Infra     - Azure resources, databases         │
│   3. App       - Application code, features         │
│   4. Deploy    - Deployment, CI/CD                  │
│   5. Smoke     - End-to-end verification            │
│                                                     │
│ Save to: .claude/project-tasks.md                   │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ PHASE 4: Execute via Ralph Loop                     │
│                                                     │
│ For each task (parallel where no dependencies):     │
│                                                     │
│   /ralph-loop "                                     │
│     PROJECT: [context]                              │
│     TASK: [description]                             │
│     VERIFY: [actual_test_command]                   │
│     Output <promise>[criteria]</promise>            │
│     ONLY when verification command passes           │
│   " --completion-promise "[criteria]"               │
│     --max-iterations [N]                            │
│                                                     │
│ Verification = actual test execution, not promises  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Mandatory PRD Structure

All fields MUST be gathered during Phase 1 (derived or asked):

```yaml
# REQUIRED - Deterministic structure
project_name: string              # e.g., "todo-cli"
project_type: enum                # CLI | WebApp | API | Integration | Infrastructure
scope: enum                       # POC | Lab | Production
primary_goal: string              # Single sentence describing what this solves
success_criteria: string          # Overall project success (I derive per-task criteria)

features:                         # Array of features with Gherkin
  - name: string
    description: string
    scenario:                     # Gherkin format
      given: string
      when: string
      then: string
    acceptance_criteria: string[]

technical_stack:
  language: string                # e.g., "Python 3.x"
  framework: string               # e.g., "Typer"
  storage: string                 # e.g., "JSON file" | "PostgreSQL"

infrastructure:
  hosting: enum                   # Local | Azure
  deployment: enum                # Manual | GitHub Actions | Azure DevOps

prerequisites:                    # What MUST exist before execution
  - type: enum                    # azure | github | api_key | tool
    name: string                  # e.g., "OPENAI_API_KEY"
    verify_command: string        # e.g., "test -n \"$OPENAI_API_KEY\""

out_of_scope: string[]            # Explicit boundaries
```

## Gherkin Scenario Format

Each feature maps to a Gherkin scenario (Given/When/Then):

```gherkin
Feature: Add Task
  Scenario: User adds a new task
    Given the todo-cli is installed
    And the tasks.json file exists
    When the user runs "todo add 'Buy groceries'"
    Then a new task is created with description "Buy groceries"
    And the task has a unique ID
    And the task has status "pending"
```

## TDD Task Derivation

For each Gherkin scenario, I generate TWO tasks:

### 1. Test Task (runs first)
```yaml
task:
  id: feature-1-test
  category: app
  type: test
  description: "Write test for: Add Task"
  gherkin_source: "Feature: Add Task..."
  verification_command: "pytest tests/test_add.py -v"
  expected_initial_result: FAIL  # TDD: test fails before implementation
  dependencies: [setup-1]
```

### 2. Implement Task (makes test pass)
```yaml
task:
  id: feature-1-impl
  category: app
  type: implement
  description: "Implement: Add Task"
  gherkin_source: "Feature: Add Task..."
  verification_command: "pytest tests/test_add.py -v"
  expected_result: PASS  # Implementation must make test pass
  dependencies: [feature-1-test]
```

## Task Categories & Execution Order

| Category | Phase | Examples | Parallelizable |
|----------|-------|----------|----------------|
| Setup | 1 | venv, dependencies, project structure | No (sequential) |
| Infra | 2 | Azure resources, databases, secrets | Partially |
| App | 3 | Features, business logic, API endpoints | Yes (by feature) |
| Deploy | 4 | CI/CD, deployment pipelines | No |
| Smoke | 5 | End-to-end tests, integration verification | No |

## Verification Commands by Category

Each task category has deterministic verification patterns:

### Setup Tasks
```bash
# Python venv exists
test -d .venv && .venv/bin/python --version

# Dependencies installed
.venv/bin/pip freeze | grep -q typer

# Project structure exists
test -f src/__init__.py && test -f pyproject.toml
```

### Infrastructure Tasks
```bash
# Azure resource exists
az resource show --name $RESOURCE_NAME --resource-group $RG

# Database accessible
pg_isready -h $DB_HOST -p 5432

# Secret exists in vault
az keyvault secret show --name $SECRET --vault-name $VAULT
```

### Application Tasks
```bash
# Unit tests pass
pytest tests/unit/ -v --tb=short

# Integration tests pass
pytest tests/integration/ -v --tb=short

# API responds correctly
curl -s localhost:3000/api/health | jq -e '.status == "ok"'
```

### Deployment Tasks
```bash
# GitHub Actions workflow valid
gh workflow view deploy.yml

# Deployment succeeded
az webapp show --name $APP --query state -o tsv | grep -q Running
```

### Smoke Tasks
```bash
# End-to-end test passes
pytest tests/e2e/ -v

# Production endpoint responds
curl -s https://app.example.com/health | jq -e '.status == "ok"'
```

## Scope-Based Behavior

Phase 1 MUST derive scope, which affects:

| Aspect | POC/Lab | Production |
|--------|---------|------------|
| Security concerns | Mentioned lightly | Block if missing |
| Infrastructure | Local-first | Cloud-required |
| Testing depth | Happy path | Edge cases + security |
| Prerequisites | Minimal | Comprehensive |
| Documentation | Optional | Required |

## Ralph Loop Integration

Each task maps to Ralph Loop with ACTUAL verification:

```bash
/ralph-loop "
  PROJECT: todo-cli (Lab/POC Python CLI)

  TASK: Implement Add Task feature

  GHERKIN:
    Given the todo-cli is installed
    When the user runs 'todo add Buy groceries'
    Then a new task is created with description 'Buy groceries'

  VERIFICATION (run this command):
    pytest tests/test_add.py::test_add_task -v

  Output <promise>Add Task feature implemented and tested</promise>
  ONLY when pytest returns exit code 0
" --completion-promise "Add Task feature implemented and tested" \
  --max-iterations 10
```

## Plugin File Structure

```
.claude/
├── commands/
│   └── project.md          # /project command
├── project.local.md        # Generated PRD (per project)
├── project-tasks.md        # Generated tasks (per project)
└── project-plugin-plan.md  # This file (framework reference)
```

## Senior Engineer Mindset

During Phase 1 conversation:

1. **Reflect understanding** - Show I "get it" without being robotic
2. **Recommend** - State my tool/tech recommendations with reasoning
3. **Ask sparingly** - ONE clarifying question if genuinely needed
4. **Flag proportionately** - Security matters more for production than lab
5. **Use judgment** - State what that judgment is when I use it
6. **Build toward "yes"** - Each response moves toward confirmation

## References

- Gherkin syntax: Cucumber standard (since 2008)
- TDD workflow: Test → Fail → Implement → Pass
- Ralph Loop: Anthropic official plugin for iterative verification
- Plugin architecture: Anthropic official documentation
