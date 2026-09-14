# ReAct Protocol Template (Thought → Action → Observation)

A flexible, exploratory protocol for skills where the execution path cannot be
predetermined. Best for: bug fixing skills, codebase exploration skills, requirements
analysis skills.

Copy the section below into the skill's body and customize the `{{PLACEHOLDER}}` parts.

---

## Execution Protocol: ReAct

Enter a loop. Continue until the task is complete or no progress is possible.

### Thought

Answer three questions:
1. What do I understand so far? {{CONTEXT_DOMAIN}}
2. What is the biggest uncertainty? {{UNCERTAINTY_FOCUS}}
3. What is the next best action to reduce this uncertainty?

### Action

Execute one specific, observable operation:
- Read a file → use Read
- Search code → use Grep or Glob
- Modify code → use Edit or Write
- Run a command → use Bash
- Look up information → use WebSearch or WebFetch

Record what action was taken.

### Observation

- What did the action return? {{EXPECTED_OUTPUT_FORMAT}}
- Does this result change my understanding? How?
- Does it invalidate any previous assumptions?

### Loop Decision

- Task goal achieved → summarize and exit.
- Progress made but not done → continue loop.
- No progress for 3 consecutive rounds → invoke Stuck Protocol.

### Stuck Protocol

1. Report findings so far: what is known, what remains unknown.
2. State what was attempted and why it didn't work.
3. Present 2-3 alternative investigation paths.
4. Ask the user for guidance or new direction.

### {{DOMAIN_SPECIFIC_RULES}}

Add domain-specific decision rules here. Examples:
- {{RULE_1}}: If `{{CONDITION}}` → prefer `{{APPROACH}}`.
- {{RULE_2}}: Never modify `{{PROTECTED_FILES}}` without explicit confirmation.
- {{RULE_3}}: If the error message contains `{{PATTERN}}` → check `{{COMMON_FIX}}`.
