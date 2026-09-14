# Skill Maturity Model — Full Reference

The six-level maturity model provides a diagnostic framework and upgrade path for any
Agent Skill. Use this reference when auditing an existing skill or planning an upgrade.

---

## Level L0 — Ad-hoc Prompt

**What it is**: Instructions pasted into chat manually each time. No file. No version
control. Knowledge evaporates when the session ends.

**Signs you're at L0**:
- You copy-paste the same long prompt repeatedly.
- Different team members use different (and inconsistent) versions of the same instructions.
- No one else on the team knows the procedure exists.

**Upgrade to L1**:
1. Create a directory: `mkdir <skill-name>/`
2. Write a `SKILL.md` with minimal YAML frontmatter (name + description).
3. Paste the prompt content into the body (don't worry about formatting yet).
4. Run `skills-ref validate <skill-name>/` to check frontmatter validity.
5. Place it in the appropriate storage location (project: `.claude/skills/` or
   cross-platform: `.agents/skills/`).

---

## Level L1 — Named Skill

**What it is**: A `SKILL.md` file with a valid `name` and `description`. The agent can
discover it. The skill has a permanent home on disk.

**Minimum requirements**:
```yaml
---
name: my-skill
description: Use when [trigger conditions]. Handles [capabilities].
---
```

**Signs you're at L1**:
- Skill appears in skill listings.
- Agent sometimes activates it, sometimes doesn't.
- Body is essentially a raw prompt dump — no structure.

**Upgrade to L2**:
1. Add a `## Workflow` section with numbered steps.
2. Add conditional branches (`If A → do X; if B → do Y`).
3. Add at least 2 concrete input/output examples.
4. Add verification steps after each major action.
5. Remove narrative prose, emoji, and decorative formatting.
6. Run L1 trigger test: list 5-10 user utterances and verify ≥80% match.

---

## Level L2 — Structured Skill

**What it is**: A SKILL.md with a clear workflow structure, conditional logic, examples,
and built-in verification. The agent reliably follows the procedure.

**Hallmarks**:
- `## Workflow` with numbered steps.
- Explicit conditional branches.
- At least 2 I/O example pairs.
- `Verify:` at the end of each major step.
- Body uses imperative mood, dense format.

**Signs you're at L2**:
- Agent consistently follows the workflow.
- Trigger activation is reliable (≥80% in L1 test).
- Body is well-structured but still a single file.

**Upgrade to L3**:
1. Audit body length. If > 500 lines, identify sections to extract.
2. Identify content that is only needed in specific scenarios (not every invocation).
3. Move domain-specific details to `references/<topic>.md`.
4. Move deterministic computations to `scripts/<script>.py` (or .sh/.js).
5. Move templates to `assets/<template>.md`.
6. In SKILL.md body, replace extracted content with navigation pointers:
   "For AWS-specific steps, see [references/aws.md](references/aws.md)"
7. Ensure every extracted file is referenced from SKILL.md with clear loading conditions.

---

## Level L3 — Progressive Skill

**What it is**: A multi-file skill that uses progressive disclosure. The body stays
under 500 lines. Supporting files load only when needed.

**Directory structure**:
```
skill-name/
├── SKILL.md          # Core workflow + navigation pointers (≤500 lines)
├── scripts/          # Executable code (loaded = executed)
│   └── helper.py
├── references/       # Domain docs (loaded = read into context on demand)
│   ├── aws.md
│   └── gcp.md
└── assets/           # Templates (loaded = used as fill-in basis)
    └── template.md
```

**Progressive disclosure in action**:
1. At session start: only `name` + `description` loaded (~100 tokens).
2. When activated: full `SKILL.md` body loaded (≤5000 tokens).
3. When needed: specific `references/` file loaded. `scripts/` executed. `assets/` used.

**Signs you're at L3**:
- Body under 500 lines.
- Every supporting file has an explicit loading condition documented in SKILL.md.
- Agent loads references only when they're relevant (not every invocation).
- No unused files in the directory.

**Upgrade to L4**:
1. Set up the L3 evaluation framework. See the Evaluation Guide referenced in SKILL.md
   under "Reference Files".
2. Create `evals/evals.json` with at least 5 test cases.
3. Run the evaluation and establish a baseline benchmark.
4. Fix any failures. Re-run. Aim for ≥90% pass rate.
5. Document the benchmark results.

---

## Level L4 — Verified Skill

**What it is**: A skill with reproducible evaluation data. Every change can be measured
against a benchmark. No regressions go unnoticed.

**Hallmarks**:
- `evals/evals.json` with test cases and assertions.
- Benchmark data from at least one evaluation run.
- Pass rate ≥90%.
- Evaluation can be re-run after any modification.

**Signs you're at L4**:
- You can answer "did this change make the skill better or worse?" with data.
- Trigger activation and output format are quantitatively verified.
- Team members trust the skill for critical workflows.

**Upgrade to L5**:
1. Identify related skills in the same domain.
2. Design a parent orchestrator skill that coordinates them.
3. Define clear interfaces: what each child skill expects as input and produces as output.
4. Document the handoff conditions between skills.
5. Create the orchestrator's SKILL.md with the workflow chain.
6. Test the end-to-end chain.

---

## Level L5 — Composed Skill

**What it is**: A skill ecosystem where multiple skills work together as a family or
chained workflow. The orchestrator coordinates; child skills specialize.

**Three composition patterns** (see Design Patterns table in SKILL.md for full details):

| Pattern | Structure | Use case |
|---------|-----------|----------|
| Domain Variant | One SKILL.md + references/{variant}.md | Same skill, different platforms |
| Skill Family | Parent orchestrator + child skill directories | Multiple related skills in a domain |
| Workflow Chain | Sequential declaration in orchestrator SKILL.md | Output of A → input of B → input of C |

**Limitations**: Cross-skill invocation is NOT yet standardized in the agentskills.io
spec (see [Issue #137](https://github.com/agentskills/agentskills/issues/137)).
Current implementations use documentation conventions:
- The orchestrator's SKILL.md instructs the agent to invoke child skills by name.
- Skill names are referenced as `/skill-name` in instructions.
- This relies on the agent platform supporting slash-command invocation within skills.

---

## Quick Diagnostic Questions

To determine a skill's level without reading the full reference:

1. Does a `SKILL.md` exist? → If no: L0. If yes: continue.
2. Does `name` and `description` pass `skills-ref validate`? → If no: between L0-L1. If
   yes: at least L1.
3. Does body have a structured `## Workflow` with numbered steps? → If no: L1. If yes:
   at least L2.
4. Are there `scripts/`, `references/`, or `assets/` directories with content? → If no:
   L2. If yes: at least L3.
5. Does `evals/evals.json` exist with benchmark data? → If no: L3. If yes: at least L4.
6. Does the skill reference or coordinate with other skills? → If no: L4. If yes: L5.
