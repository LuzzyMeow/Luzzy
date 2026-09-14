# Design Patterns — Full Reference

Seven reusable patterns for skill engineering. Each pattern includes: what problem it
solves, when to use it, the core structure, and a minimal example.

**Note**: File paths in example directory trees (e.g., `references/aws.md`,
`scripts/validate.py`) are illustrative examples within hypothetical skills — they do
not reference actual files in this project.

---

## Pattern 1: Trigger-First

**Problem**: Skill never activates because the agent reads the description, infers the
procedure, and skips loading the body.

**Solution**: Write the description BEFORE the body. The description contains ONLY
trigger conditions and capability hints. All execution steps are in the body.

**When to use**: Every skill that should be auto-activated by the agent. Skip this
pattern only for `disable-model-invocation: true` skills.

**Decision**: Always apply Trigger-First for model-invocable skills.

**Example**:
```yaml
---
name: commit-generator
description: >
  Use when writing commit messages, generating conventional commits,
  or reviewing staged changes for commit. Handles conventional commit format,
  scope detection, and breaking change notation.
---
```

The body then contains the complete commit generation workflow — never previewed in
the description.

---

## Pattern 2: Progressive Disclosure

**Problem**: Body is too large (>500 lines). Loading it all at once wastes tokens in
scenarios where only a subset of the content is relevant.

**Solution**: Body contains core workflow + navigation pointers. Details live in
`references/` files loaded only when needed. Scripts in `scripts/` run only when called.

**When to use**: Any skill where:
- Body exceeds 500 lines.
- Different invocation scenarios need different subsets of content.
- Domain-specific details vary by platform/environment.

**Structure**:
```
my-skill/
├── SKILL.md              # Core workflow (≤500 lines) + pointers
├── references/
│   ├── aws.md            # AWS-specific: loaded only for AWS deployments
│   ├── gcp.md            # GCP-specific: loaded only for GCP deployments
│   └── troubleshooting.md # Common issues: loaded on failure
└── scripts/
    └── validate.py       # Pre-deploy checks: run before deployment
```

**Example — SKILL.md excerpt**:
```markdown
## Deployment Workflow

1. Determine target platform from user input.
2. If AWS → load and follow [references/aws.md](references/aws.md).
3. If GCP → load and follow [references/gcp.md](references/gcp.md).
4. Run pre-deploy checks: `python scripts/validate.py --target=<platform>`
   Verify: exit code 0, no warnings.
5. Execute deployment.
```

---

## Pattern 3: Domain Variant

**Problem**: One skill needs to support multiple platforms, frameworks, or environments.
Putting all variants in one file creates a bloated body.

**Solution**: Common logic in SKILL.md body. Platform-specific differences in separate
`references/` files. Body contains a selection step that routes to the correct variant.

**When to use**: When the core workflow is the same across variants, but the
implementation details differ (e.g., deploy to AWS vs GCP, generate React vs Vue
components).

**Structure**:
```
deploy/
├── SKILL.md
├── references/
│   ├── aws.md
│   ├── gcp.md
│   ├── azure.md
│   └── vercel.md
└── scripts/
    └── pre-check.py     # Common across all platforms
```

**Example — SKILL.md routing**:
```markdown
1. Identify the deployment target. Supported: aws, gcp, azure, vercel.
2. Load the platform guide: [references/<target>.md](references/<target>.md).
3. Run pre-deploy checks: `python scripts/pre-check.py`
4. Follow the platform guide for the actual deployment.
```

---

## Pattern 4: Workflow Chain

**Problem**: A complex process spans multiple distinct steps, each of which could be a
standalone skill. The user wants to run the entire chain.

**Solution**: Create an orchestrator skill that declares the sequence, handoff
conditions, and which child skills to invoke at each step.

**When to use**: When a process naturally decomposes into steps that each deserve
their own skill (different triggers, different maintenance, different authors).

**Limitations**: Cross-skill invocation is not yet standardized in the agentskills.io
spec. Current approach: the orchestrator instructs the agent to invoke child skills
by name using the platform's skill invocation mechanism.

**Structure**:
```
ship-it/                    # Orchestrator
├── SKILL.md
└── references/
    └── chain-spec.md       # Formal definition of the chain
code-review/                # Step 1
├── SKILL.md
test-runner/                # Step 2
├── SKILL.md
deploy-staging/             # Step 3
├── SKILL.md
notify-team/                # Step 4
├── SKILL.md
```

**Example — Orchestrator SKILL.md**:
```markdown
## Ship It Workflow

Execute each step in order. Do not skip steps. If any step fails, stop and report.

1. Run the code review: invoke `/code-review` skill on the current changes.
   Handoff: if review passes, proceed. If issues found, fix and re-run.
2. Run the test suite: invoke `/test-runner` skill.
   Handoff: all tests must pass.
3. Deploy to staging: invoke `/deploy-staging` skill with the current branch.
   Handoff: deployment must succeed and health check pass.
4. Notify the team: invoke `/notify-team` skill with deployment summary.
```

---

## Pattern 5: Tool Augmentation

**Problem**: An MCP server provides access to an external system (Jira, GitHub, Slack),
but the agent doesn't know your team's conventions for using those tools.

**Solution**: Create a skill that teaches the agent HOW to use MCP-provided tools. The
skill doesn't replace the MCP server — it augments it with procedural knowledge.

**When to use**: Any time an MCP server is installed but the agent uses its tools
naively (e.g., creates Jira tickets with wrong fields, sends Slack messages to wrong
channels, queries the database with inefficient patterns).

**Structure**:
```
jira-workflow/
├── SKILL.md              # Conventions + workflow
├── references/
│   ├── field-guide.md    # Which Jira fields matter, what values are valid
│   └── templates.md      # Standard issue descriptions for common types
└── assets/
    └── issue-template.md
```

**Example — SKILL.md excerpt**:
```markdown
## Creating a Jira Issue

1. Identify the issue type: Bug / Task / Story / Epic.
2. Select the project key based on the affected service:
   - API service → PROJ-API
   - Web frontend → PROJ-WEB
   - Infrastructure → PROJ-INFRA
3. Set priority using our team's rubric (see [references/field-guide.md](references/field-guide.md)).
4. Use the template in [assets/issue-template.md](assets/issue-template.md). Fill in:
   - Summary: [Component] Brief description
   - Description: Steps to reproduce (for bugs) / Acceptance criteria (for stories)
   - Labels: service name + severity
5. Create the issue using the Jira MCP tool.
   Verify: issue created with correct project, type, and labels.
```

---

## Pattern 6: Template Factory

**Problem**: The skill produces output with a strict format (reports, config files,
code scaffolds). Writing the format rules in prose is error-prone.

**Solution**: Put the format as a template in `assets/`. The body contains fill-in
rules and a quality checklist. The agent fills the template rather than generating
from scratch.

**When to use**: When output format matters and deviation from the template would
cause downstream issues (e.g., config files that must parse correctly, reports that
must match a company format).

**Structure**:
```
report-generator/
├── SKILL.md
├── assets/
│   ├── weekly-report.md     # Template with {{PLACEHOLDER}} markers
│   └── incident-report.md   # Another template variant
└── references/
    └── style-guide.md       # Writing conventions
```

**Example — SKILL.md excerpt**:
```markdown
1. Determine report type from user input: weekly / incident.
2. Load template: [assets/<type>-report.md](assets/<type>-report.md).
3. Fill template placeholders:
   - {{DATE}} → current date in YYYY-MM-DD format
   - {{METRICS}} → pull from the monitoring dashboard
   - {{ACTION_ITEMS}} → generate from open issues
4. Quality check:
   - All placeholders replaced?
   - Date format consistent?
   - No placeholder text remaining?
   - Output matches the template structure exactly?
```

---

## Pattern Selection Decision Tree

```
User describes the need:
├─ "I want the agent to auto-detect when to use this"
│   → Apply Trigger-First (Pattern 1)
├─ "The skill has a lot of reference material"
│   → Apply Progressive Disclosure (Pattern 2)
├─ "It should work on AWS and GCP and Azure"
│   → Apply Domain Variant (Pattern 3)
├─ "It's a multi-step process with distinct phases"
│   → Apply Workflow Chain (Pattern 4)
├─ "We have an MCP server but the agent uses it wrong"
│   → Apply Tool Augmentation (Pattern 5)
├─ "The output must follow a strict format/template"
│   → Apply Template Factory (Pattern 6)
└─ Multiple of the above apply → Compose patterns
```

Patterns are composable. A skill can use Trigger-First for its description,
Progressive Disclosure for its structure, and Template Factory for its output —
all at the same time.
