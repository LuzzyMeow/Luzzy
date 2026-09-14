# OTAV Protocol Template (Observe → Think → Act → Verify)

A lightweight, deterministic protocol for skills with fixed-step workflows where
each step requires human judgment. Best for: code review skills, deployment skills,
data migration skills.

Copy the section below into the skill's body and customize the `{{PLACEHOLDER}}` parts.

---

## Execution Protocol: OTAV

For each sub-task, execute in this order:

### Observe

- Read the current state: {{WHAT_TO_OBSERVE}}
- Identify any differences from the expected state.
- List the differences.

### Think

- What do these differences mean? {{INTERPRETATION_FRAMEWORK}}
- Which rule applies? See [## Decision Rules]({{DECISION_RULES_LINK}}).
- How many feasible solutions exist? Which is preferred? Why?

### Act

- Execute the preferred solution: {{ACTION_TEMPLATE}}
- Record: what action was taken + why it was chosen.
- If the action is destructive: confirm before proceeding.

### Verify

- Check result against expectation: {{VERIFICATION_CHECK}}
- If mismatch → return to Observe with new information.
- If match → proceed to next sub-task.
- If after 3 retries still not matching → invoke Stuck Protocol.

### Stuck Protocol

1. Report what was attempted and what went wrong.
2. Present 2-3 alternative approaches.
3. Ask the user to choose or provide new direction.
