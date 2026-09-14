---
name: {{SKILL_NAME}}
description: >
  Use when {{TRIGGER_CONDITIONS}}.
  Handles {{CAPABILITIES}}.
  Do NOT use for {{NEGATIVE_TRIGGERS}}.
license: {{LICENSE}}
compatibility: >
  requires: {{DEPENDENCIES}}
metadata:
  version: "1.0.0"
  author: "{{AUTHOR}}"
  category: "{{CATEGORY}}"
  maturity: "L3"
---

# {{SKILL_TITLE}}

{{ONE_SENTENCE_PURPOSE}}

## Workflow

1. {{STEP_1}}
   Verify: {{VERIFICATION_1}}
2. {{STEP_2}}
   - If {{CONDITION_A}} → follow [references/{{FILE_A}}.md](references/{{FILE_A}}.md).
   - If {{CONDITION_B}} → follow [references/{{FILE_B}}.md](references/{{FILE_B}}.md).
   Verify: {{VERIFICATION_2}}
3. {{STEP_3}}
   Run: `{{SCRIPT_COMMAND}}`
   Verify: {{VERIFICATION_3}}

## Examples

Input: {{EXAMPLE_INPUT_1}}
Output: {{EXAMPLE_OUTPUT_1}}

Input: {{EXAMPLE_INPUT_2}}
Output: {{EXAMPLE_OUTPUT_2}}

## Conditions

- If {{CONDITION_A}}: {{ACTION_A}}
- If {{CONDITION_B}}: {{ACTION_B}}
- Edge case {{EDGE_CASE}}: {{EDGE_ACTION}}

## Reference Files

| File | Load when |
|------|-----------|
| [references/{{FILE_A}}.md](references/{{FILE_A}}.md) | {{LOADING_CONDITION_A}} |
| [references/{{FILE_B}}.md](references/{{FILE_B}}.md) | {{LOADING_CONDITION_B}} |

## Scripts

| Script | Run when | Command |
|--------|----------|---------|
| `scripts/{{SCRIPT}}.py` | {{SCRIPT_CONDITION}} | `python scripts/{{SCRIPT}}.py {{ARGS}}` |

## Templates

| Template | Use for |
|----------|---------|
| [assets/{{TEMPLATE}}.md](assets/{{TEMPLATE}}.md) | {{TEMPLATE_PURPOSE}} |
