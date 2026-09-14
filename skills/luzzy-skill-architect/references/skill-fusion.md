# Skill Fusion — Full Methodology

Merge two or more skills into a unified Skill Family while preserving every
original function, document, script, and source repository. The governing principle:
**1+1≥2, never 1+1<2**.

---

## Fusion Eligibility — Pre-Merge Assessment

Before fusing, the agent evaluates each candidate pair against four dimensions.
Passing threshold: ≥60 points out of 100 AND no CRITICAL conflicts.

### Dimension 1: Domain Overlap (0–30 pts)

| Score | Condition |
|-------|-----------|
| 30 | Same domain, complementary phases (e.g., `code-review` + `test-runner`) |
| 20 | Adjacent domains with clear handoff points |
| 10 | Related but loosely coupled |
| 0 | Unrelated domains — fusion adds no synergy |

### Dimension 2: Conflict Risk (CRITICAL / 0–25 pts)

**CRITICAL check — auto-reject if true:**
- Both skills claim `name` that would collide in child directories.
- Both skills have contradictory tool restrictions (`allowed-tools` vs `disallowed-tools`).
- Both skills target mutually exclusive platforms.

| Score | Condition |
|-------|-----------|
| 25 | No conflicts detected |
| 15 | Minor naming overlap (resolvable via namespace prefix) |
| 5 | Significant overlap requiring manual resolution |
| 0 | Unresolvable conflict without losing functionality |

### Dimension 3: Complementarity (0–25 pts)

| Score | Condition |
|-------|-----------|
| 25 | Skills fill clear gaps for each other (input/output chain) |
| 15 | Partial complement — some shared context, mostly independent |
| 5 | Minimal complement — skills address separate concerns |
| 0 | Redundant — skills do the same thing |

### Dimension 4: Structure Cleanliness (0–20 pts)

| Score | Condition |
|-------|-----------|
| 20 | All candidates are well-formed (pass `skills-ref validate`) |
| 10 | Some candidates need minor fixes before fusion |
| 0 | Candidates have structural issues that block clean fusion |

### Verdict Matrix

| Total Score | Verdict |
|-------------|---------|
| ≥80 | **STRONG FUSION** — high synergy, proceed immediately |
| 60–79 | **FEASIBLE FUSION** — proceed with noted caveats |
| 40–59 | **WEAK FUSION** — agent recommends against; user override required |
| <40 or CRITICAL | **REJECT** — fusion would violate 1+1≥2 principle |

---

## Three Fusion Levels

### L1 — Direct Fusion (2+ standalone skills → 1 family)

```
Input:  skill-A/ + skill-B/
Output: fusion-AB/
        ├── SKILL.md           # Parent orchestrator
        ├── references/
        │   └── fusion-map.md  # Documenting the fusion structure
        ├── skill-A/           # Child skill, preserved intact
        │   ├── SKILL.md
        │   └── ...
        ├── skill-B/           # Child skill, preserved intact
        │   ├── SKILL.md
        │   └── ...
        └── scripts/
            └── check-updates.py
```

**Orchestrator SKILL.md** describes the fusion:
- Lists all child skills with their roles in the family.
- Declares trigger phrases that activate the orchestrator.
- Provides routing logic: which child skill handles which user request.
- Records source repositories in metadata.

### L2 — Incremental Fusion (existing family + new skill)

```
Input:  fusion-AB/ + skill-C/
Output: fusion-ABC/
        ├── SKILL.md           # Updated orchestrator
        ├── references/
        │   └── fusion-map.md  # Updated with skill-C
        ├── skill-A/
        ├── skill-B/
        ├── skill-C/           # New child
        └── scripts/
            └── check-updates.py
```

**Workflow**:
1. Re-run L1 pre-merge assessment for (family-AB + skill-C).
2. If passing: add skill-C as a child directory.
3. Update orchestrator SKILL.md: add routing logic, update trigger phrases.
4. Update `fusion-map.md`: document the new addition.
5. Update `check-updates.py` metadata: register skill-C's source.

### L3 — Self-Update (source repos → merged skill sync)

**Metadata format in orchestrator SKILL.md**:
```yaml
metadata:
  composition: "skill-family"
  source_skills:
    - name: "code-review"
      repo: "https://github.com/org/code-review-skill.git"
      version: "v1.0.0"
      last_sync: "2026-06-11"
    - name: "test-runner"
      repo: "https://github.com/org/test-runner-skill.git"
      version: "v2.1.0"
      last_sync: "2026-06-11"
  self_update:
    enabled: true
    check_interval: "on-audit"
```

**Self-update workflow** (triggered during Luzzy-Skill-Architect audit):

1. Read `metadata.source_skills`.
2. For each source, fetch the remote repo and compare version tags.
3. If newer version found → report to user with a diff summary.
4. User decides: accept update / defer / skip.
5. If accepted: replace child skill directory with new version, update metadata.
6. Run post-update validation: verify orchestrator still routes correctly.

**`scripts/check-updates.py` usage**:
```bash
python scripts/check-updates.py --skill-dir <path>
```
Output: a JSON report of which sources have updates available.

---

## Orchestrator SKILL.md Template

```yaml
---
name: <fusion-name>
description: >
  Use when <combined trigger conditions>.
  Handles <combined capabilities>.
  Do NOT use for <negative triggers>.
license: <LICENSE>
compatibility: requires: <dependencies>
metadata:
  version: "1.0.0"
  composition: "skill-family"
  maturity: "L5"
  child_skills: ["<skill-a>", "<skill-b>"]
  source_skills:
    - name: "<skill-a>"
      repo: "<git-url>"
      version: "<version>"
      last_sync: "<date>"
    - name: "<skill-b>"
      repo: "<git-url>"
      version: "<version>"
      last_sync: "<date>"
  self_update:
    enabled: true
    check_interval: "on-audit"
allowed-tools: Read Write Edit Bash Glob Grep Skill
---

# <Fusion Title>

Orchestrates <N> skills in the <domain> domain. Each child skill handles a
specialized phase. This orchestrator routes user requests to the correct child.

## Child Skills

| Skill | Purpose | Source |
|-------|---------|--------|
| <skill-a> | <purpose> | <git-url> |
| <skill-b> | <purpose> | <git-url> |

## Routing Logic

| User says | Route to |
|-----------|----------|
| <trigger for skill-a> | Invoke child `<skill-a>` |
| <trigger for skill-b> | Invoke child `<skill-b>` |
| <combined trigger> | Execute in sequence: `<skill-a>` → `<skill-b>` |

## Fusion Map

See [references/fusion-map.md](references/fusion-map.md) for the full merge
rationale, compatibility assessment, and child skill version history.
```

---

## Fusion Map Template (`references/fusion-map.md`)

```markdown
# Fusion Map — <fusion-name>

## Merge Rationale

Why these skills were fused. The compatibility assessment result.

## Pre-Merge Assessment

| Dimension | Skill-A | Skill-B | Score |
|-----------|---------|---------|-------|
| Domain Overlap | | | /30 |
| Conflict Risk | | | /25 |
| Complementarity | | | /25 |
| Structure | | | /20 |
| **Total** | | | **/100** |

## Child Skill Inventory

| Skill | Version | Source Repo | Key Files |
|-------|---------|-------------|-----------|
| <skill-a> | v1.0.0 | <url> | SKILL.md, scripts/... |
| <skill-b> | v2.1.0 | <url> | SKILL.md, references/... |

## Update History

| Date | Action | Detail |
|------|--------|--------|
| 2026-06-11 | Created | Initial fusion of skill-a + skill-b |
| - | - | - |
```

---

## Anti-Patterns Specific to Fusion

| Anti-pattern | Fix |
|-------------|------|
| Forced fusion of unrelated skills | Run pre-merge assessment; reject if <60 |
| Deleting child skill content during merge | Child directories must remain intact |
| Ignoring source repos | Always record `metadata.source_skills` |
| Orphaned child skills | Every child must appear in orchestrator's routing table |
| Update without version tracking | Always update `last_sync` in metadata |
| Monolithic fusion (merging bodies into one file) | Use Skill Family pattern, not deep merge |

---

## Integration with Luzzy-Skill-Architect

### Phase 2.5 — Fusion Analysis

Inserted between Phase 2 (Structure Design) and Phase 3 (Write SKILL.md):

1. If user wants to fuse skills → enter Fusion Analysis.
2. Load and parse all candidate SKILL.md files.
3. Run pre-merge assessment (4 dimensions, score calculation).
4. Present verdict with detailed breakdown.
5. If verdict is STRONG or FEASIBLE → design the Skill Family directory tree.
6. If WEAK → present risks, require explicit user confirmation.
7. If REJECT → explain why, suggest alternatives.
8. Proceed to Phase 3: write orchestrator SKILL.md + fusion-map.md.

### Phase 4+ — Self-Update Check

During audit of any L5 composed skill:
1. Check `metadata.source_skills`.
2. Run `scripts/check-updates.py` if available.
3. Report available updates.
4. User decides: sync now / schedule / ignore.
