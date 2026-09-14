# Anti-Patterns — Full Reference with Cases

Common mistakes in skill design and how to fix them. Each entry includes symptoms,
root cause, a concrete before/after example, and the fix.

---

## AP-1: Description as Summary

**Symptom**: Agent reads the description, claims it understands the task, and executes
without loading the full skill body. The carefully crafted workflow is never read.

**Root cause**: The description field is treated as documentation or a summary. The
agent optimizes for token efficiency — if the description tells it what to do, why load
the body?

**Before (bad)**:
```yaml
description: >
  Analyzes git diff to identify issues, runs linters, checks test coverage,
  generates a code review report with severity ratings and fix suggestions.
```

**After (good)**:
```yaml
description: >
  Use when reviewing code changes, pull requests, or diffs.
  Handles multi-pass review including style, security, and test coverage.
  Do NOT use for writing new code or feature implementation.
```

**Fix**: Rewrite description to contain ONLY trigger conditions and capability hints.
Move all execution details to the body. Add negative triggers.

---

## AP-2: Decorative Formatting

**Symptom**: Body contains blockquotes, emoji, ASCII separators, nested indentation,
and narrative prose. Token budget wasted on visual elements the model ignores.

**Before (bad)**:
```markdown
> **Important Note:** Before running the migration, please ensure that you have
> backed up your database. This is a critical step that should not be skipped.

🎯 **Step 1: Analyze the Schema**

First, take a careful look at the current schema definition...

────────────────────────────────────────
```

**After (good)**:
```markdown
1. Back up the database: `pg_dump > backup.sql`
2. Read `src/db/schema.ts`. Compare against the latest file in `migrations/`.
   Flag column-type changes and renamed columns.
3. Run `npx drizzle-kit generate`.
```

**Fix**: Delete all blockquotes, emoji, separators, and decorative formatting. Use
numbered steps. State actions as imperatives. Put conditions inline: "If A → do X".

---

## AP-3: Second-Person Writing

**Symptom**: Body addresses the agent with "you should", "please note", "we recommend".
Adds tokens without adding precision.

**Before (bad)**:
```markdown
You should first check the current state of the repository.
Please note that uncommitted changes may cause issues.
We recommend running the tests before proceeding.
```

**After (good)**:
```markdown
1. Check repository state: `git status`
2. Run tests: `npm test`
   - If any test fails: fix before proceeding.
3. Proceed with the workflow.
```

**Fix**: Replace "you should" with imperatives. Replace "please note" and "we recommend"
with conditions or unconditional statements. Write as if giving orders to a machine.

---

## AP-4: Chain-Referencing

**Symptom**: A references file links to another references file, creating a loading chain.
Each hop costs a round-trip and tokens. Deep chains cause the agent to lose context.

**Before (bad)**:
```
SKILL.md → references/deployment.md → references/aws-specific.md → references/aws-networking.md
```

**After (good)**:
```
SKILL.md → references/deployment.md
SKILL.md → references/aws-deployment.md  (contains all AWS specifics, no sub-references)
```

**Fix**: Keep reference depth at exactly 1. Every reference file is linked from SKILL.md
directly. If a reference file grows too large, split it by topic but link all split
files from SKILL.md, not from each other.

---

## AP-5: Missing Negative Triggers

**Symptom**: Skill activates in contexts where it shouldn't. The agent applies code
review logic during normal coding sessions. The deployment skill activates during
discussions about deployment strategy.

**Before (bad)**:
```yaml
description: >
  Use when working with databases. Handles migrations, query optimization,
  and schema design.
```

**After (good)**:
```yaml
description: >
  Use when creating or modifying database migrations, optimizing slow queries,
  or designing new schema tables. Handles migration generation, query analysis,
  and schema validation.
  Do NOT use for basic CRUD operations, ORM configuration, or database
  connection setup.
```

**Fix**: Add a "Do NOT use for..." clause to the description. Be specific about what
the skill should NOT handle. Test with both positive triggers (should activate) and
negative triggers (should NOT activate).

---

## AP-6: Pretend Cross-Platform

**Symptom**: Skill claims to be cross-platform but uses vendor-specific fields like
`disable-model-invocation: true` (Claude Code only) or relies on platform-specific
behaviors. Fails silently or behaves unexpectedly on other platforms.

**Before (bad)**:
```yaml
---
name: deploy
description: Cross-platform deployment skill
disable-model-invocation: true  # This is Claude Code only!
context: fork                     # Also Claude Code only!
---
```

**After (good)** — for a truly cross-platform skill:
```yaml
---
name: deploy
description: >
  Use when deploying the application. Handles build, test, and push steps.
compatibility: requires: git, node>=18
metadata:
  portability: spec-level
---
```

For a Claude Code-specific skill (documented honestly):
```yaml
---
name: deploy-claude
description: >
  Use when deploying via Claude Code.
disable-model-invocation: true
compatibility: requires: claude-code>=2.1
metadata:
  portability: claude-code-only
---
```

**Fix**: Decide the portability target before writing frontmatter. Document it in
`metadata.portability`. If the target is cross-platform, do not use any vendor-specific
fields. If the target is single-vendor, state it explicitly.

---

## AP-7: Monolithic Skill

**Symptom**: One skill does code review, deployment, Slack notification, changelog
generation, and version bumping. Hard to maintain, hard to test, triggers in too many
contexts.

**Before (bad)**:
```yaml
name: do-everything
description: >
  Use when you need to review code, deploy, notify the team, generate changelogs,
  bump versions, or create release notes.
---
# Workflow
1. Review the code...
2. Run tests...
3. Deploy to staging...
4. Verify deployment...
5. Notify Slack...
6. Generate changelog...
7. Bump version...
8. Create GitHub release...
```

**After (good)** — decomposed into a skill family:
```yaml
# code-review/SKILL.md — handles step 1
# run-tests/SKILL.md — handles step 2
# deploy-staging/SKILL.md — handles steps 3-4
# notify-team/SKILL.md — handles step 5
# release/SKILL.md — handles steps 6-8
# ship-it/SKILL.md — orchestrator that chains them all
```

**Fix**: Identify distinct responsibilities. Create one skill per responsibility. If
they need to run in sequence, create a parent orchestrator skill using the Workflow
Chain pattern.

---

## AP-8: No Verification Steps

**Symptom**: Skill executes actions but never checks results. Migration runs but nobody
verifies the schema changed correctly. Deployment completes but nobody confirms the app
is actually serving traffic.

**Before (bad)**:
```markdown
1. Run `npm run build`
2. Run `npm run deploy`
3. Notify the team
```

**After (good)**:
```markdown
1. Run `npm run build`
   Verify: exit code is 0. No error output.
2. Run `npm run deploy`
   Verify: exit code is 0. Response contains "deployment successful".
3. Run `curl -s https://app.example.com/health`
   Verify: HTTP 200. Response body contains "ok".
4. Notify the team with deployment status.
```

**Fix**: Add a `Verify:` line after every action that produces an observable result.
Check exit codes, response bodies, file existence, or any other verifiable output.

---

## AP-9: Description Too Conservative

**Symptom**: Skill has a perfectly good workflow but never activates because the
description lacks trigger keywords that match real user utterances.

**Before (bad)**:
```yaml
description: Database migration helper.
```

**After (good)**:
```yaml
description: >
  Use when creating database migrations, running migrations, rolling back
  migrations, generating migration files, or fixing migration conflicts.
  Handles schema diff, migration generation, up/down/rollback operations.
```

**Fix**: List every phrase a user might say to invoke this skill. Include synonyms
("create migration" / "generate migration" / "add migration"). Include the action
verbs users use. Test with real prompts.

---

## AP-10: Body as Documentation

**Symptom**: Body explains what the skill does and why, instead of providing executable
instructions. Reads like a README, not a workflow.

**Before (bad)**:
```markdown
# API Generator

This skill helps you generate API endpoints for your Express application.
It follows our team's conventions for RESTful API design, which we adopted
in Q3 2025 after evaluating several approaches. The key benefits are...

## Background

Our API conventions were designed to...
```

**After (good)**:
```markdown
# API Generator

1. Determine the resource name from user input.
2. Create the route file: `src/routes/<resource>.ts`
   Template: `assets/route-template.ts`
3. Create the controller: `src/controllers/<resource>.ts`
   Template: `assets/controller-template.ts`
4. Add validation schema: `src/validators/<resource>.ts`
5. Register route in `src/app.ts` under `// API_ROUTES` marker.
6. Run `npm test -- --testPathPattern=<resource>`
   Verify: all tests pass.
```

**Fix**: Delete all explanatory prose. Keep only executable instructions, conditions,
verification steps, and examples.

---

## Quick Audit Checklist

When reviewing a skill, check for:

- [ ] AP-1: Does description contain execution steps? → Must only contain triggers.
- [ ] AP-2: Are there blockquotes, emoji, or separators? → Delete them.
- [ ] AP-3: Is there "you", "please", "we recommend"? → Rewrite as imperatives.
- [ ] AP-4: Do reference files link to other reference files? → Flatten to one level.
- [ ] AP-5: Are negative triggers present? → Add "Do NOT use for...".
- [ ] AP-6: Are vendor-specific fields used without declaration? → Add portability metadata.
- [ ] AP-7: Does one skill do more than one distinct thing? → Decompose.
- [ ] AP-8: Does every action have a verification step? → Add "Verify:".
- [ ] AP-9: Would 10 real user utterances all trigger this skill? → Test and add keywords.
- [ ] AP-10: Is there explanatory prose instead of instructions? → Delete prose, keep steps.
