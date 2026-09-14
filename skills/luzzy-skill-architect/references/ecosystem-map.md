# Ecosystem Map — Skills vs Everything Else

When a user asks "should this be a skill?", use this reference to make the right call.
This document maps the boundaries between Skills and all adjacent agent concepts.

---

## Skills vs CLAUDE.md / AGENTS.md

| | CLAUDE.md / AGENTS.md | Skill |
|---|---|---|
| **What it provides** | Persistent project context and conventions | Procedural knowledge for specific tasks |
| **When it loads** | At session start (always in context) | On activation (progressive disclosure) |
| **Token cost** | Paid every session, every turn | Paid only when the skill is relevant |
| **Best for** | "We use TypeScript, follow these naming rules" | "Here's how to create a new API endpoint" |
| **Examples** | Code style, architecture decisions, team preferences | Deployment workflow, code review checklist, PR template |

**Rule of thumb**: If it applies to every single interaction, put it in CLAUDE.md.
If it applies to specific scenarios, make it a skill.

**Exception**: A section of CLAUDE.md that has grown into a long procedure should be
extracted into a skill. CLAUDE.md keeps facts; skills keep workflows.

---

## Skills vs Custom Instructions / Rules (.cursor/rules/)

| | Custom Instructions / Rules | Skill |
|---|---|---|
| **Scope** | Always-on, session-wide | On-demand, task-specific |
| **Format** | Platform-specific (`.cursor/rules/`, `.instructions.md`) | Cross-platform standard (SKILL.md) |
| **Portability** | Locked to one platform | Portable across 20+ platforms |
| **Trigger** | Always applied or file-pattern matched | Description-based semantic matching |
| **Best for** | "Never use `var`", "Always add error handling" | "Generate a database migration" |

**Rule of thumb**: If it's a constraint ("always X, never Y"), use instructions/rules.
If it's a capability ("how to do X"), use a skill.

**Migration path**: Some rules can become skills. "Always run `npm test` before
committing" → make it a `pre-commit-checks` skill with a clear workflow.

---

## Skills vs MCP Servers

| | MCP Server | Skill |
|---|---|---|
| **What it provides** | Connectivity to external systems | Knowledge of how to use that connectivity |
| **Required for** | Reading live data, performing write operations | Encoding team conventions and workflows |
| **Cost** | Connection overhead + tool description tokens | Metadata tokens (~100) + body tokens on activation |
| **Best for** | Database access, API calls, issue trackers, Slack | "Our Jira workflow", "Our database naming conventions" |

**They complement, not compete.** An MCP server connects to Jira. A skill teaches the
agent your team's Jira workflow. Without MCP, the agent can't touch Jira. Without the
skill, it touches Jira wrong.

**When MCP is unnecessary**: If the agent can accomplish the task via shell commands
(`git`, `npm`, `kubectl`, `aws` CLI), skip MCP. Use a skill that teaches effective
CLI usage instead.

**Co-deployment**: When deploying both, the skill should reference the MCP server's
tools by name. The description should mention the MCP requirement in `compatibility`.

---

## Skills vs Subagents (Claude Code)

| | Subagent | Skill |
|---|---|---|
| **What it provides** | Isolated execution environment | Instructions and knowledge |
| **Context** | Clean slate per invocation | Loaded into the parent conversation |
| **Best for** | Research, exploration, parallel work | Teaching, guiding, constraining |
| **Integration** | Subagents can preload skills | Skills can fork into subagents (`context: fork`) |

**Rule of thumb**: Use a subagent when you need isolation. Use a skill when you need
knowledge transfer. Use a skill with `context: fork` to combine both.

---

## Skills vs Prompts / Prompt Templates

| | Prompt / Template | Skill |
|---|---|---|
| **What it provides** | One-time instruction injection | Reusable, version-controlled procedure |
| **Persistence** | Evaporates after the session | Lives on disk, shared via version control |
| **Sharing** | Copy-paste between teammates | Commit to repo, everyone gets it |
| **Iteration** | Ad-hoc editing, no version history | Git-tracked, reviewable in PRs |

**Rule of thumb**: If you paste the same prompt more than twice, turn it into a skill.

---

## Skills vs Bundles

| | Bundle | Skill |
|---|---|---|
| **What it provides** | Curated collection of skills | A single capability |
| **Exists as** | Documentation / recommendation | A directory with SKILL.md |
| **Purpose** | Onboarding: "for this role, install these 5 skills" | Execution: "how to do this one thing" |

**Think of bundles as playlists, skills as songs.** A bundle doesn't add new
capabilities — it groups existing skills for easier discovery.

---

## Skills vs Workflows

| | Workflow | Skill |
|---|---|---|
| **What it provides** | Skill chaining sequence | Standalone procedure |
| **Dependencies** | References multiple skills | Self-contained |
| **Purpose** | Orchestration: "ship from code to production" | Specialization: "review the code" |

**A workflow is a skill that orchestrates other skills** (see Design Pattern 4:
Workflow Chain). The orchestrator itself is a valid SKILL.md.

---

## Decision Tree: Where Should This Live?

```
I have a piece of knowledge or a procedure. Where do I put it?

├─ It's always true, always applies
│   → CLAUDE.md / custom instructions
│
├─ It's always true, only applies to certain file types
│   → Path-specific rules (.cursor/rules/ with globs)
│
├─ It's a constraint ("never do X")
│   → Instructions / rules
│
├─ It's a capability ("here's how to do X"), specific to a scenario
│   → Skill
│
├─ It needs to access an external system (database, API, Slack)
│   → MCP Server + Skill (Tool Augmentation pattern)
│
├─ It needs to run in isolation without polluting the main conversation
│   → Skill with context: fork (Claude Code) or subagent
│
├─ It chains multiple skills together
│   → Workflow Chain skill (orchestrator)
│
├─ It's a one-time instruction
│   → Prompt (paste it in chat)
│
└─ It's a curated list of skills for a role
    → Bundle (documentation)
```

---

## Platform-Specific Storage Locations

| Platform | Project skills | Personal skills |
|----------|---------------|-----------------|
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| VS Code Copilot | `.github/skills/<name>/` | User profile (VS Code settings) |
| Cursor | `.cursor/skills/<name>/` | `~/.cursor/skills/<name>/` |
| Gemini CLI | `.gemini/skills/<name>/` | `~/.gemini/skills/<name>/` |
| OpenAI Codex | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` |
| Windsurf | `.windsurf/skills/<name>/` | `~/.windsurf/skills/<name>/` |
| Roo Code | `.roo/skills/<name>/` | `~/.roo/skills/<name>/` |
| Cross-platform | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` |

`.agents/` is emerging as the cross-platform convention. OpenAI Codex and Gemini CLI
both support it. If you target multiple platforms, use `.agents/skills/`.

---

## Priority Resolution

When the same skill name exists in multiple locations:

```
Enterprise (managed) > Personal > Project > Plugin/Extension
```

Project skills committed to version control are automatically available to all team
members. Personal skills stay on your machine. Managed skills are pushed by your
organization.
