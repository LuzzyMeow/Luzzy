---
name: luzzy-skill-architect
description: >
  Use when users want to create, design, improve, audit, or fuse skills (SKILL.md).
  Handles full skill lifecycle: intent capture, directory structure design,
  YAML frontmatter authoring, body writing, trigger validation, iteration,
  maturity assessment, anti-pattern detection, skill composition planning,
  and skill fusion (merge 2+ skills into a Skill Family with 1+1>=2 guarantee).
  Use when the user says "create a skill", "design a skill", "improve my skill",
  "audit this skill", "review my SKILL.md", "check my skill quality",
  "merge skills", "combine skills", "fuse these skills", "unify skills",
  or asks about skill engineering methodology, agentskills.io specification,
  progressive disclosure, or cross-platform portability. Also use when a user
  pastes a long prompt and says "turn this into a skill".
  Do NOT use for writing general documentation, README files, or standalone
  scripts unrelated to the Agent Skills format.
license: Apache-2.0
compatibility: >
  requires: python>=3.8 (for scripts); skills-ref>=0.1.0 (optional, for validation)
metadata:
  version: "1.0.0"
  author: "Luzzy-Skill Architect Team"
  status: "stable"
  category: "meta-skill"
  portability: "spec-level"
  target-maturity: "L3"
allowed-tools: Read Write Edit Bash Glob Grep WebFetch WebSearch Skill
---

# Luzzy-Skill Architect

Create, audit, and elevate Agent Skills following the
[agentskills.io](https://agentskills.io/specification) open standard.

## Execution Protocol: PPER

Every interaction with the user follows this mandatory cycle.
Do not skip stages. Do not merge stages.

### Stage 1 — Perception

1. Identify the user's explicit request and emotional tone.
2. Determine which stage of the skill lifecycle is active (intent → structure →
   write → verify → iterate).
3. Detect implicit needs (e.g., user described a workflow but didn't realize it
   needs a `scripts/` directory).

**Check before proceeding**: Is the user's core need stated in one sentence?

### Stage 2 — Planning

1. Decompose the request into sub-goals.
2. Generate at least two feasible approaches. Choose the best one.
3. Identify which reference files to load (see [references/](references/)).
4. If information is MISSING and BLOCKING progress → ask a closed-form question.
   If information is MISSING but can be assumed → note the assumption and proceed.

**Check before proceeding**: Are at least two approaches on the table?

### Stage 3 — Execution

1. Carry out the planned actions: write files, run validation, present output.
2. After each action, self-check: did the result match expectation?
3. If the result diverges → return to Stage 2 with new information.

**Check before proceeding**: Has every file written been verified to exist?

### Stage 4 — Reflection

1. Compare output against quality gates (see each lifecycle phase's gate below).
2. Predict user's likely reaction. Prepare follow-up.
3. Record noteworthy patterns or user preferences.

**Check before proceeding**: Does the output pass all applicable gates?

### Stuck Protocol

If two consecutive rounds produce no substantive progress:
1. State explicitly what the blocker is.
2. Present 2-3 concrete options for the user to choose from.
3. Never guess the user's intent when blocked.

## Five-Phase Skill Lifecycle

**Flow**: Understand Intent → Design Structure → Write SKILL.md → Verify Trigger → Iterate (loops back to Understand Intent).

### Phase 1 — Understand Intent

Ask these six questions. Do not skip any unless the user already answered it.

| # | Question | Why |
|---|----------|-----|
| 1 | What task does this skill accomplish? | Core function |
| 2 | What phrases trigger it? What would users say? | Collect trigger keywords |
| 3 | What type? Generation / Automation / Knowledge enhancement | Shapes structure choices |
| 4 | Does it need scripts? Reference docs? Templates? | Maps to scripts/ references/ assets/ |
| 5 | Is this standalone or part of a skill family? | Determines composition strategy |
| 6 | What does "done" look like? Expected output format? | Benchmark for verification |

Deliverable: a skill profile card (verbal or written) with all six answers.

**Phase 1 Gate:**
- [ ] Core need stated in one sentence?
- [ ] At least 3 trigger phrases listed?
- [ ] Skill type identified?
- [ ] Portability target declared? (spec-level / cross-vendor / single-vendor)
- [ ] User confirmed the profile card?

### Phase 2 — Design Structure

Design the directory tree before writing content. Decision rules:

| Condition | Action |
|-----------|--------|
| Needs deterministic scripts | Add scripts/ |
| Body likely exceeds 500 lines | Split into references/ |
| Supports multiple platform variants | Create references/{variant}.md |
| Produces fixed-format output | Add assets/ with templates |
| Part of a skill family | Discuss composition patterns |
| None of the above | Single SKILL.md is enough |

**Three composition patterns:**

| Pattern | Structure | When to use |
|---------|-----------|-------------|
| Domain Variant | `skill/SKILL.md` + `references/{aws,gcp}.md` | One skill, multiple platforms |
| Skill Family | Parent `toolkit/SKILL.md` orchestrates child skills | Multiple related skills in a domain |
| Workflow Chain | `SKILL.md` declares step sequence + handoff points | Output of skill A feeds skill B |

Deliverable: a directory tree sketch with a reason for every file and folder.

**Phase 2 Gate:**
- [ ] Every directory and file has a clear reason to exist?
- [ ] Each script has a corresponding invocation guide in SKILL.md?
- [ ] References follow "one file, one topic"?
- [ ] Reference depth ≤ 1 (no chain-loading)?
- [ ] No over-engineering (empty directories)?
- [ ] If composition applies, pattern is explicit?

### Phase 2.5 — Fusion Analysis (when merging 2+ skills)

Triggered when the user wants to combine multiple skills into one Skill Family.
Before writing any content, assess whether fusion satisfies 1+1≥2.

**Step 1 — Parse candidates**: Load SKILL.md from each candidate skill directory.
**Step 2 — Run assessment**: Score each pair on four dimensions (see `references/skill-fusion.md`):
| Dimension | Max | What to check |
|-----------|-----|---------------|
| Domain Overlap | 30 | Shared keywords, trigger proximity |
| Conflict Risk | 25 | Name collisions, platform conflicts, tool restrictions |
| Complementarity | 25 | I/O chain potential, domain adjacency |
| Structure | 20 | Valid frontmatter, clean descriptions |

**Step 3 — Automated tool**: Run `scripts/fusion-analyzer.py <dir1> <dir2> [...]` for quantitative scoring.

**Step 4 — Verdict**:
- ≥80: STRONG — proceed immediately.
- 60–79: FEASIBLE — proceed with noted caveats.
- 40–59: WEAK — agent recommends against; require user override.
- <40 or CRITICAL conflict: REJECT — explain why and suggest alternatives.

**Step 5 — Design family structure** (if approved):
```
fusion-name/
├── SKILL.md             # Parent orchestrator with routing table
├── references/
│   └── fusion-map.md    # Merge rationale + compatibility report
├── <skill-a>/           # Child skill preserved intact
├── <skill-b>/           # Child skill preserved intact
└── scripts/
    └── check-updates.py # Self-update checker
```

**Step 6 — Record source repos** in orchestrator metadata:
```yaml
metadata:
  source_skills:
    - name: "<skill-a>"
      repo: "<git-url>"
      version: "<version>"
      last_sync: "<date>"
  self_update:
    enabled: true
    check_interval: "on-audit"
```

**Fusion Gate:**
- [ ] Pre-merge assessment score ≥60 OR user explicitly overrode WEAK verdict?
- [ ] All child skill directories preserved intact?
- [ ] Orchestrator has routing logic for every child?
- [ ] Source repos recorded in metadata?
- [ ] fusion-map.md documents the merge rationale?

### Phase 3 — Write SKILL.md

**YAML frontmatter guide — all six standard fields:**

```yaml
---
name: <skill-name>            # 1-64 chars, lowercase+digits+hyphens, must match dirname
description: >                # 1-1024 chars. Trigger conditions ONLY. No execution steps.
  Use when [specific triggers].
  Handles [capability], [capability].
  Do NOT use for [negative triggers].
license: <LICENSE>            # Optional. License name or reference to bundled LICENSE file.
compatibility: >              # Optional. ≤500 chars. Only write if there are env requirements.
  requires: python>=3.11
metadata:                     # Optional. Arbitrary key-value pairs.
  version: "1.0.0"
  author: "Name"
allowed-tools: <TOOLS>        # Optional. Space-separated tool names.
---
```

**Body writing rules — mandatory:**

| Rule | Bad | Good |
|------|-----|------|
| Imperative mood | "You should run the linter" | "Run the linter" |
| Dense format | `> **Note:** ...` with emoji and separators | Plain numbered steps |
| Workflow as numbered steps | Narrative paragraphs | `1.` `2.` `3.` |
| Examples as I/O pairs | "For instance, if the input is..." | `Input: xxx → Output: yyy` |
| Explicit conditionals | Implicit assumptions | `If A → do X; if B → do Y` |
| Built-in verification | No checks | `Verify: X matches expected Y` |
| Under 500 lines | Monolithic body | Core in body, details in references/ |

**Writing supporting files:**

- `scripts/`: each script MUST have a usage description in SKILL.md body.
- `references/`: one topic per file. No chain-referencing. Add a table of contents
  if the file exceeds 300 lines.
- `assets/`: use `{{PLACEHOLDER}}` for fill-in slots in templates.

Deliverable: a complete skill directory, at minimum with a `SKILL.md`.

**Phase 3 Gate — Content:**
- [ ] `name` matches directory name and follows naming spec?
- [ ] `description` contains only trigger conditions (no execution steps)?
- [ ] `description` includes negative triggers ("Do NOT use for...")?
- [ ] Body uses imperative mood, no second-person ("you")?
- [ ] Body uses dense format, no decorative blockquotes/emoji/separators?
- [ ] Body includes at least 2 input/output examples?
- [ ] Body includes verification steps?
- [ ] Body ≤ 500 lines?
- [ ] Passes `skills-ref validate` (if available)?

### Phase 4 — Verify Trigger

**Three-tier verification:**

| Tier | Method | Scope | Threshold |
|------|--------|-------|-----------|
| L1 — Trigger Test | List 5-10 user utterances, check if description matches | All skills, mandatory | ≥80% correct activation |
| L2 — Single Run | Execute once end-to-end, check output format | Automation skills, recommended | No mid-flow interruption |
| L3 — Batch Eval | Full evals.json + benchmark (see `references/evaluation-guide.md`) | Critical skills, optional | Per eval assertions |

**Trigger test feedback loop:**

- Activation rate < 80% → return to Phase 3, adjust description.
- False positives (activates when it shouldn't) → add negative triggers.
- False negatives (should activate but doesn't) → add synonyms/keywords.

Deliverable: verification report with test results and improvement suggestions.

**Phase 4 Gate:**
- [ ] L1 trigger test pass rate ≥ 80%?
- [ ] L2 (if applicable): one full run completed without interruption?
- [ ] Negative triggers added if false positives found?
- [ ] Actual trigger behavior matches intent?

### Phase 5 — Iterate

1. Analyze verification report → identify issues → modify SKILL.md → re-verify.
2. Repeat until target maturity is reached or the user is satisfied.
3. Optional: record version + changelog in `metadata.version`.

**Specialized iterations:**
- **Description tuning**: use trigger test results to refine keywords.
- **Token budget review**: compress body without losing clarity.
- **Portability audit**: confirm no accidental vendor-specific field dependencies.

**Phase 5 Gate:**
- [ ] User confirmed satisfaction?
- [ ] `metadata.version` and `metadata.author` recorded?
- [ ] (Optional) Target maturity level reached?
- [ ] (Optional) Portability audit passed?

## Skill Maturity Model

Use this to diagnose and upgrade skills.

| Level | Name | Hallmark | Artifacts |
|-------|------|----------|-----------|
| L0 | Ad-hoc Prompt | Pasted manually, no file | Nothing |
| L1 | Named Skill | SKILL.md with valid name + description | Single SKILL.md |
| L2 | Structured Skill | Numbered workflow steps + conditionals | Structured body |
| L3 | Progressive Skill | scripts/ references/ or assets/ with lazy loading | Multi-file tree |
| L4 | Verified Skill | Passed L3 batch eval, reproducible benchmark | evals.json + benchmark |
| L5 | Composed Skill | Coordinates with other skills as a family or chain | Multi-skill + orchestration |

See `references/maturity-model.md` for the full upgrade path for each level.

## Design Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Trigger-First | Skill never activates | Write description BEFORE body; never leak steps into description |
| Progressive Disclosure | Body too large | Core ≤500 lines; details in references/ with navigation pointers |
| Domain Variant | Multiple platforms | Common logic in body; differences in references/{variant}.md |
| Workflow Chain | Multi-step orchestration | Parent declares sequence + handoff conditions |
| Tool Augmentation | MCP exists but lacks know-how | Skill teaches agent *how* to use MCP tools, doesn't replace them |
| Template Factory | Strict output format | Templates in assets/; fill rules + quality checklist in body |
| Skill Fusion | Multiple skills need to work as one | Parent orchestrator + child dirs intact; source repos tracked; self-update enabled |

See `references/design-patterns.md` for full decision trees per pattern.
See `references/skill-fusion.md` for complete fusion methodology.


## Anti-Patterns — Quick Reference

| Anti-pattern | Fix |
|-------------|------|
| Description reads like a summary → agent skips body | Rewrite as trigger-only |
| Decorative formatting (blockquotes, emoji, separators) | Delete all decoration |
| Second-person writing ("You should...") | Rewrite as imperative |
| Chain-referencing (references → references) | Flatten to one level |
| No negative triggers → false activations | Add "Do NOT use for..." |
| Pretending to be cross-platform but needing vendor fields | Declare portability target honestly |
| One skill doing too many things | Decompose into skill family |
| No verification steps → silent failures | Add "Verify:" after each step |
| Description too conservative → never activates | Add more trigger keywords and synonyms |
| Body reads like a README, not executable instructions | Delete prose, keep imperative steps |

See `references/anti-patterns.md` for detailed cases with before/after examples.


## Ecosystem Decision Tree

| Need | Solution |
|------|----------|
| Always-on, applies to every session | CLAUDE.md / custom instructions |
| Scenario-specific workflow | Skill |
| External API/database access | MCP Server + Skill (Tool Augmentation) |
| Isolated, async execution | Skill with platform-specific isolation (see [references/vendor-extensions.md](references/vendor-extensions.md)) |
| Multiple skills to coordinate | Workflow Chain / Skill Family |
| One-off assistant behavior tweak | Prompt (not a skill) |

See `references/ecosystem-map.md` for the full Skills vs CLAUDE.md vs MCP vs Rules comparison.


## Examples

Input: "Create a skill that generates database migrations for our team"
Output:
  Phase 1 — Intent: skill type = Generation. Triggers: "create migration", "add migration",
  "generate schema diff". Needs: script (migration runner), references (per-DB variants).
  Portability: spec-level.
  Phase 2 — Structure: db-migration/SKILL.md + references/{postgres,mysql}.md +
  scripts/generate.py.
  Phase 3 — Write SKILL.md: trigger-first description. Body with 5-step workflow + Verify
  after each step. Under 500 lines.
  Phase 4 — Verify: L1 trigger test 8/10 → add negative trigger "Do NOT use for schema
  design discussions" → 9/10. Pass.

Input: "Audit my deploy skill — it keeps activating when I talk about deployment strategy"
Output:
  AP-1 detected: description says "analyzes deployment config, runs build, pushes to
  staging" — execution steps leaked. Fix: rewrite as "Use when deploying to staging.
  Handles build and push."
  AP-5 detected: no negative triggers. Fix: add "Do NOT use for deployment strategy
  discussions or infrastructure planning."
  Maturity: L1 → upgrade path to L3 via Progressive Disclosure (split cloud-specific
  steps into references/{aws,gcp}.md).

Input: "What maturity level is my code-review skill?"
Output:
  Quick diagnostic:
  1. SKILL.md exists? Yes.
  2. name + description valid? Yes.
  3. Structured ## Workflow? Yes (numbered steps, conditionals).
  4. scripts/ references/ or assets/? No.
  → Level: L2. Upgrade to L3: split security checklist and style guide into references/.

Input: "Fuse my code-review and test-runner skills into one PR-check skill"
Output:
  Phase 2.5 — Fusion Analysis: parse SKILL.md from both candidates.
  code-review + test-runner:
    Domain Overlap: 30/30 (strong — same CI pipeline domain)
    Conflict Risk: 25/25 (none)
    Complementarity: 25/25 (strong — review output feeds test selection)
    Structure: 20/20 (both pass skills-ref validate)
    Total: 100/100 — VERDICT: STRONG.
  Design family: pr-checks/SKILL.md orchestrator with routing table.
  Children: code-review/ and test-runner/ preserved intact.
  Record source repos in metadata.source_skills for self-update.


## Self-Referential Checklist

This skill itself must pass its own standards:

- [ ] description is trigger-only, no execution steps leaked?
- [ ] body uses dense format, no decorative elements?
- [ ] body ≤ 500 lines, details in references/?
- [ ] references/ has clear loading conditions per file?
- [ ] assets/ templates use {{PLACEHOLDER}} markers?
- [ ] Passes `skills-ref validate` (if available)?
- [ ] Self-assessed maturity: L3+?


## Reference Files

Load these on demand when the user's needs match:

| File | Load when |
|------|-----------|
| [references/maturity-model.md](references/maturity-model.md) | User wants to diagnose or upgrade skill level |
| [references/design-patterns.md](references/design-patterns.md) | User needs to choose or understand a design pattern |
| [references/anti-patterns.md](references/anti-patterns.md) | User wants to audit or fix a problematic skill |
| [references/ecosystem-map.md](references/ecosystem-map.md) | User asks "skill vs CLAUDE.md vs MCP?" |
| [references/vendor-extensions.md](references/vendor-extensions.md) | User targets Claude Code / VS Code / specific platform |
| [references/evaluation-guide.md](references/evaluation-guide.md) | User wants L3 batch evaluation setup |
| [references/skill-fusion.md](references/skill-fusion.md) | User wants to merge 2+ skills, check fusion eligibility, or set up self-update |

## Template Files

| File | Use when |
|------|----------|
| [assets/templates/skill-basic.md](assets/templates/skill-basic.md) | Creating a simple L1 skill (single file) |
| [assets/templates/skill-structured.md](assets/templates/skill-structured.md) | Creating an L2-L3 skill (with references split) |
| [assets/templates/skill-family.md](assets/templates/skill-family.md) | Creating an L5 skill family with orchestration |

## Protocol Templates

| File | Use when |
|------|----------|
| [assets/protocols/pper-protocol.md](assets/protocols/pper-protocol.md) | User wants to embed PPER thinking protocol in their own skill |
| [assets/protocols/otav-protocol.md](assets/protocols/otav-protocol.md) | User wants a lightweight Observe-Think-Act-Verify protocol |
| [assets/protocols/react-protocol.md](assets/protocols/react-protocol.md) | User wants an exploratory Thought-Action-Observation loop |

## Scripts

| File | Use when |
|------|----------|
| [scripts/validate-trigger.py](scripts/validate-trigger.py) | Automating L1 trigger validation. Run: `python scripts/validate-trigger.py <skill-dir>` |
| [scripts/fusion-analyzer.py](scripts/fusion-analyzer.py) | Assessing fusion compatibility. Run: `python scripts/fusion-analyzer.py <dir1> <dir2> [...]` |
| [scripts/check-updates.py](scripts/check-updates.py) | Checking source repo updates. Run: `python scripts/check-updates.py --skill-dir <path>` |
| `scripts/run-eval.py` (planned) | Automated L3 batch evaluation runner. See [references/evaluation-guide.md](references/evaluation-guide.md). |
