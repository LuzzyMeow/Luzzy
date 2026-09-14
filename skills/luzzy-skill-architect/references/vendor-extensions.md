# Vendor Extensions — Platform-Specific YAML Fields

This document catalogs YAML frontmatter fields that fall OUTSIDE the agentskills.io
specification but are supported by specific platforms. Use this as a reference when
you need platform-specific features.

**Important**: Using these fields breaks cross-platform portability. Only use them
when you've explicitly chosen a single-vendor target. Document this choice in
`metadata.portability`.

---

## Claude Code Extensions

All Claude Code-specific fields are documented at:
https://code.claude.com/docs/en/skills

| Field | Type | Purpose |
|-------|------|---------|
| `disable-model-invocation` | boolean | Prevents Claude from auto-loading the skill. Set `true` for user-invoked-only skills like `/deploy`. |
| `user-invocable` | boolean | Set `false` to hide from the `/` menu. Use for background knowledge skills. |
| `when_to_use` | string | Additional trigger context appended to `description`. Counts toward the 1536-char listing cap. |
| `argument-hint` | string | Hint shown during autocomplete. Example: `[issue-number]`. |
| `arguments` | string or list | Named positional arguments for `$name` substitution in body. |
| `context` | string | Set to `fork` to run the skill in an isolated subagent context. |
| `agent` | string | Subagent type when `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, or custom agent name. |
| `model` | string | Model override for the turn. Same values as `/model`. Use `inherit` to keep active model. |
| `effort` | string | Effort level override: `low`, `medium`, `high`, `xhigh`, `max`. |
| `hooks` | object | Hooks scoped to this skill's lifecycle. See Claude Code hooks docs. |
| `paths` | string or list | Glob patterns limiting when the skill activates. Example: `"src/api/**"`. |
| `shell` | string | Shell for inline commands. `bash` (default) or `powershell`. |
| `disallowed-tools` | string or list | Tools removed from Claude's pool while this skill is active. |

**Example — Claude Code-only skill**:
```yaml
---
name: deploy-staging
description: Deploy the current branch to staging.
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash(git *) Bash(npm *) Bash(kubectl *)
arguments: [branch, environment]
argument-hint: "[branch] [environment]"
---
```

**String substitutions available in Claude Code skills**:
- `$ARGUMENTS` — all arguments
- `$ARGUMENTS[N]` or `$N` — nth argument
- `$name` — named argument from `arguments` field
- `${CLAUDE_SESSION_ID}` — current session ID
- `${CLAUDE_EFFORT}` — current effort level
- `${CLAUDE_SKILL_DIR}` — directory containing this skill's SKILL.md

**Dynamic context injection (Claude Code only)**:
- Inline: `` !`command` `` — runs before Claude sees the content
- Fenced block: ` ```! ` — for multi-line commands

---

## VS Code / GitHub Copilot Extensions

Copilot supports a subset of Claude Code's fields through its Agent Skills integration.

| Field | Supported? | Notes |
|-------|-----------|-------|
| `disable-model-invocation` | Yes | Since December 2025 |
| `user-invocable` | Partial | Managed through VS Code settings differently |
| Other Claude Code fields | No | Not supported in Copilot |

---

## OpenAI Codex Extensions

Codex uses a SEPARATE configuration file for invocation control: `.agents/openai.yaml`.

```yaml
# .agents/openai.yaml
policy:
  allow_implicit_invocation: false  # Equivalent to disable-model-invocation
```

This means: if you target both Claude Code and Codex, you need `disable-model-invocation`
in SKILL.md for Claude AND `allow_implicit_invocation: false` in `agents/openai.yaml`
for Codex.

---

## Gemini CLI

Gemini CLI follows the agentskills.io spec with full cross-platform compliance. Uses
`.gemini/skills/` (project) and `~/.gemini/skills/` (personal). No vendor-specific
YAML frontmatter fields. Supports `.agents/skills/` as an alternative location.

## Cursor

Uses `.cursor/skills/` (project) and `~/.cursor/skills/` (personal). Supports the
standard six fields. No vendor extensions.

## Windsurf

Uses `.windsurf/skills/` (project). Fully spec-compliant. No additional YAML fields.

---

## Portability Decision Matrix

| If you need... | Spec-level | Claude+VS Code | Claude-only |
|---|---|---|---|
| Basic name + description | ✓ | ✓ | ✓ |
| License, compatibility, metadata | ✓ | ✓ | ✓ |
| allowed-tools (experimental) | ✓ | ✓ | ✓ |
| disable-model-invocation | ✗ | ✓ | ✓ |
| user-invocable | ✗ | ✓ | ✓ |
| context: fork | ✗ | ✗ | ✓ |
| agent selection | ✗ | ✗ | ✓ |
| model/effort override | ✗ | ✗ | ✓ |
| hooks, paths | ✗ | ✗ | ✓ |
| dynamic context injection | ✗ | ✗ | ✓ |

**Recommendation**: Start at spec-level. Only add vendor extensions when you have a
specific, documented reason that can't be achieved with standard fields alone. Record
the portability choice in metadata.

---

## Writing Portable Skills That Gracefully Degrade

A skill can use vendor extensions while remaining functional on platforms that ignore
them. Key techniques:

1. **Keep the core workflow in the body** using only standard tool references
   (`Read`, `Write`, `Bash`). Vendor extensions should add convenience, not replace
   core functionality.
2. **Use `compatibility` to declare requirements** so other platforms know what
   they're missing.
3. **Document what happens without the extension** in a `references/` note.

Example:
```yaml
---
name: deploy
description: >
  Use when deploying to production.
compatibility: >
  requires: git, node>=18
  optional: claude-code (for context: fork with isolated execution)
metadata:
  portability: spec-level-with-optional-claude-extensions
---
```
