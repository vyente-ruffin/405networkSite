---
description: Start a new project with conversational PRD building
argument-hint: "[description]"
allowed-tools: AskUserQuestion, Write, Read, Bash, TodoWrite, Task
---

# Project Command

Initiate a project through freeform conversation, generate PRD with Gherkin scenarios, verify prerequisites, and execute via Ralph Loop.

---

## Phase 1: Conversational Discovery

If user provided a description with the command ($ARGUMENTS), start there.
Otherwise, ask: "What do you want to build?"

**For each user response:**

1. **Reflect understanding** - Show what you understood they want (clear enough they know you "get it")

2. **State recommendations** - Tools, MCP servers, framework, storage approach

3. **Ask ONE clarifying question if genuinely needed** - Examples:
   - "Is this a quick POC/lab project, or production-bound?"
   - "Should this persist data locally or to a database?"
   - Skip if you can reasonably infer from context

4. **Flag blockers proportionately** (scope-aware):
   - POC/Lab: don't lecture about security for local test apps
   - Production: flag missing auth, security, or critical requirements
   - If you use judgment, state what that judgment is

5. **Build toward "yes"** - Response should lead to refinement or confirmation

**Mandatory fields to gather** (derive from conversation, ask only if unclear):

- project_name
- project_type (CLI | WebApp | API | Integration | Infrastructure)
- scope (POC | Lab | Production) ← MUST know this to calibrate responses
- primary_goal
- features (at least 1)
- technical_stack (language, framework, storage)
- infrastructure (hosting, deployment)
- prerequisites (tools, API keys, Azure access if needed)

**Response format:**

```
I understand you want to build: [clear description]

Scope: [POC/Lab/Production]

My approach:
- [language/framework choice with brief reasoning]
- [storage approach]
- [MCP servers I'd use: Context7 for docs, etc.]

[One question if genuinely unclear, OR "Say 'yes' to proceed to PRD generation"]
```

**Loop continues until user types "yes" or equivalent confirmation.**

---

## Phase 2: Generate PRD + Gherkin Scenarios

When user confirms, create PRD at `.claude/project.local.md`:

```yaml
---
project_name: [name]
project_type: [CLI | WebApp | API | Integration | Infrastructure]
scope: [POC | Lab | Production]
status: prd-complete
created: [YYYY-MM-DD]
---

# PRD: [Project Name]

## Overview
[What this project is and why]

## Goals & Objectives
- **Primary goal**: [single sentence]
- **Problem solved**: [what pain point this addresses]
- **Success criteria**: [overall project success - you derive per-task criteria]
- **Scope**: [POC/Lab/Production context]

## Features & Requirements

### Feature 1: [Name]
- **Description**: [what it does]
- **Command/Endpoint**: [how user interacts]
- **Acceptance Criteria**: [specific verifiable outcomes]
- **Dependencies**: [what it needs first]

**Gherkin Scenario:**
```gherkin
Feature: [Name]
  Scenario: [Primary use case]
    Given [precondition]
    When [action user takes]
    Then [expected outcome]
    And [additional verification if needed]
```

[Repeat for each feature]

## Technical Approach
- **Language**: [e.g., Python 3.x]
- **Framework**: [e.g., Typer, FastAPI]
- **Storage**: [e.g., JSON file, PostgreSQL]
- **Key libraries**: [specific packages]

## Infrastructure
- **Hosting**: [Local | Azure]
- **Deployment**: [Manual | GitHub Actions | Azure DevOps]

## Prerequisites
[What must exist before execution]
- [ ] [Tool/access] - verify command: `[command]`

## Tools & Resources
- **MCP Servers**: [Context7 for X, etc.]

## Out of Scope
- [Explicit boundaries]

## Notes
[Context worth preserving]
```

After generating PRD, say:

"PRD created at `.claude/project.local.md` with Gherkin scenarios for each feature. Review and let me know changes, or say **'ready'** to proceed."

---

## Phase 0: Prerequisites Check

When user says "ready", verify ALL prerequisites before continuing:

```bash
# For each prerequisite, run its verify_command
# Examples:
# Python: python3 --version
# Azure: az account show
# GitHub: gh auth status
# API key: test -n "$OPENAI_API_KEY" && echo "exists"
```

**If ANY prerequisite fails:**

Stop and report:
```
❌ Prerequisites check failed:
- [prerequisite]: [error message]

Please fix before continuing. Run `/project` again when ready.
```

**If ALL pass:**

```
✓ Prerequisites verified:
- [each one with ✓]

Proceeding to task generation...
```

---

## Phase 3: Convert Gherkin → TDD Tasks

Generate tasks from Gherkin scenarios. Save to `.claude/project-tasks.md`:

**Task Categories (execution order):**
1. **Setup** - Environment, dependencies, project structure
2. **Infra** - Azure resources, databases, secrets
3. **App** - Application features (test then implement)
4. **Deploy** - CI/CD, deployment pipelines
5. **Smoke** - End-to-end verification

**For each Gherkin scenario, generate TWO tasks:**

```yaml
# 1. Test Task (runs first, expects fail in TDD style)
- id: feature-1-test
  category: app
  type: test
  description: "Write test for: [Feature Name]"
  gherkin: "[Given/When/Then from PRD]"
  verification: "[pytest/curl/etc command]"
  expected_initial: FAIL
  dependencies: [setup tasks]

# 2. Implement Task (makes test pass)
- id: feature-1-impl
  category: app
  type: implement
  description: "Implement: [Feature Name]"
  gherkin: "[Given/When/Then from PRD]"
  verification: "[same test command]"
  expected: PASS
  dependencies: [feature-1-test]
```

---

## Phase 4: Execute via Ralph Loop

For each task (parallel where dependencies allow):

```bash
/ralph-loop "
  PROJECT: [project_name] ([scope] [project_type])

  TASK: [description]

  GHERKIN:
    [Given/When/Then]

  VERIFICATION (run this command):
    [actual test command]

  Output <promise>[success criteria]</promise>
  ONLY when verification command returns success (exit 0)
" --completion-promise "[criteria]" --max-iterations 10
```

**Verification = actual test execution, NOT vague promises.**

---

## Key Principles

1. **Minimal friction** - Don't ask what you can infer
2. **Senior engineer mindset** - Think critically, flag real blockers proportionately
3. **Derive scope early** - Ask if unclear, it calibrates everything
4. **Build toward "yes"** - Every response moves toward confirmation
5. **Deterministic structure** - Mandatory fields, Gherkin format, TDD tasks
6. **No manual verification** - Every task has an executable test
