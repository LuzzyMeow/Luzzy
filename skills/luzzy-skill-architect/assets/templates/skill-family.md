---
name: {{ORCHESTRATOR_NAME}}
description: >
  Use when {{ORCHESTRATOR_TRIGGER}}.
  Handles end-to-end workflow: {{CAPABILITIES}}.
  Do NOT use for individual steps (use the specific child skill instead).
license: {{LICENSE}}
metadata:
  version: "1.0.0"
  author: "{{AUTHOR}}"
  category: "{{CATEGORY}}"
  maturity: "L5"
  composition: "workflow-chain"
  child_skills: ["{{CHILD_1}}", "{{CHILD_2}}", "{{CHILD_3}}"]
---

# {{ORCHESTRATOR_TITLE}}

Orchestrates the {{WORKFLOW_NAME}} workflow by coordinating {{NUM_CHILDREN}} child
skills in sequence. Each child skill handles a specific phase. This orchestrator
ensures correct order, validates handoffs, and handles failures.

## Workflow Chain

Execute each step in order. Do not skip. If any step fails, stop and report.

### Step 1: {{PHASE_1_NAME}}

Invoke: `/{{CHILD_SKILL_1}}` skill.
Input: {{PHASE_1_INPUT}}
Expected output: {{PHASE_1_OUTPUT}}
Handoff check: {{PHASE_1_HANDOFF}}

### Step 2: {{PHASE_2_NAME}}

Invoke: `/{{CHILD_SKILL_2}}` skill.
Input: {{PHASE_2_INPUT}} (from Step 1 output)
Expected output: {{PHASE_2_OUTPUT}}
Handoff check: {{PHASE_2_HANDOFF}}

### Step 3: {{PHASE_3_NAME}}

Invoke: `/{{CHILD_SKILL_3}}` skill.
Input: {{PHASE_3_INPUT}} (from Step 2 output)
Expected output: {{PHASE_3_OUTPUT}}
Handoff check: {{PHASE_3_HANDOFF}}

## Failure Handling

- If Step 1 fails: {{FAILURE_1_RECOVERY}}
- If Step 2 fails: {{FAILURE_2_RECOVERY}}
- If Step 3 fails: {{FAILURE_3_RECOVERY}}

## Child Skills

| Skill | Purpose | Directory |
|-------|---------|-----------|
| `/{{CHILD_SKILL_1}}` | {{CHILD_1_PURPOSE}} | `{{CHILD_1_DIR}}/` |
| `/{{CHILD_SKILL_2}}` | {{CHILD_2_PURPOSE}} | `{{CHILD_2_DIR}}/` |
| `/{{CHILD_SKILL_3}}` | {{CHILD_3_PURPOSE}} | `{{CHILD_3_DIR}}/` |

## Examples

### Full Run
```
User: {{EXAMPLE_FULL_RUN_PROMPT}}
→ Step 1: {{CHILD_SKILL_1}} completes → {{EXAMPLE_STEP_1_RESULT}}
→ Step 2: {{CHILD_SKILL_2}} completes → {{EXAMPLE_STEP_2_RESULT}}
→ Step 3: {{CHILD_SKILL_3}} completes → {{EXAMPLE_STEP_3_RESULT}}
→ Done: {{FINAL_RESULT}}
```

### Partial Run (with failure)
```
User: {{EXAMPLE_PARTIAL_RUN_PROMPT}}
→ Step 1: {{CHILD_SKILL_1}} completes → OK
→ Step 2: {{CHILD_SKILL_2}} fails → {{EXAMPLE_FAILURE}}
→ Stop and report: {{FAILURE_REPORT}}
```

## Directory Layout

```
{{ORCHESTRATOR_NAME}}/           # This orchestrator
├── SKILL.md
└── references/
    └── chain-spec.md            # Formal chain specification
{{CHILD_1_DIR}}/                 # Child skill 1
├── SKILL.md
{{CHILD_2_DIR}}/                 # Child skill 2
├── SKILL.md
{{CHILD_3_DIR}}/                 # Child skill 3
├── SKILL.md
```
