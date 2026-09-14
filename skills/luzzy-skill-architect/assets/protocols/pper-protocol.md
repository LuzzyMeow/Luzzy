# PPER Thinking Protocol Template

Embed this protocol in a skill's SKILL.md body when the skill needs a structured
Perception → Planning → Execution → Reflection loop for reliable execution.

Copy the section below into the skill's body and customize the `{{PLACEHOLDER}}` parts
with specific content relevant to that skill.

---

## Execution Protocol: PPER

Every interaction follows this mandatory cycle. Do not skip stages.

### Stage 1 — Perception

1. Read the current state: {{WHAT_TO_OBSERVE}}
2. Identify what has changed since the last check.
3. Determine the user's explicit request and implicit needs.

Check before proceeding: {{PERCEPTION_CHECK}}

### Stage 2 — Planning

1. Decompose the goal into sub-goals: {{SUBGOAL_LIST}}
2. Generate at least two approaches. Choose the best.
3. If information is MISSING and BLOCKING → ask. If assumable → note and proceed.

Check before proceeding: {{PLANNING_CHECK}}

### Stage 3 — Execution

1. Execute the planned action: {{ACTION_STEPS}}
2. After each action, verify: {{VERIFICATION_STEPS}}
3. If result diverges from expectation → return to Stage 2.

Check before proceeding: {{EXECUTION_CHECK}}

### Stage 4 — Reflection

1. Compare output against success criteria: {{SUCCESS_CRITERIA}}
2. Record any patterns or preferences for future use.
3. Present results to the user.

Check before proceeding: {{REFLECTION_CHECK}}

### Stuck Protocol

If two consecutive rounds produce no progress:
1. State what is blocking progress.
2. Present 2-3 concrete options.
3. Never guess when blocked.
