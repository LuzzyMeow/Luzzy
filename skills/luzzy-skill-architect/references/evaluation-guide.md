# Evaluation Guide — L3 Batch Evaluation

This guide describes how to set up and run L3 batch evaluations for skills. This is
the evaluation tier adapted from open-source skill evaluation practices for
cross-platform use.

**When to use L3**: The skill is critical to your workflow, changes frequently, or is
used by multiple team members. L1 (trigger test) and L2 (single run) are sufficient
for most skills.

---

## Evaluation Architecture

```
skill-name/
├── SKILL.md
├── evals/
│   ├── evals.json          # Test cases with assertions
│   ├── benchmark.json       # Aggregated results from last run
│   └── eval_metadata.json   # Evaluation configuration
└── scripts/
    └── run-eval.py          # (Future) Automated evaluation runner
```

---

## evals.json Format

Each test case defines: a user prompt, the expected skill activation, and assertions
on the output.

```json
{
  "skill": "my-skill",
  "version": "1.0.0",
  "cases": [
    {
      "id": "trigger-001",
      "prompt": "Generate a commit message for my staged changes",
      "expect_activation": true,
      "assertions": [
        {
          "type": "format",
          "check": "matches_regex",
          "pattern": "^(feat|fix|refactor|docs|test|chore)\\(.+\\): .+"
        },
        {
          "type": "length",
          "check": "max_chars",
          "value": 72,
          "field": "subject_line"
        }
      ]
    },
    {
      "id": "trigger-002",
      "prompt": "Add a new button to the homepage",
      "expect_activation": false,
      "assertions": []
    },
    {
      "id": "output-001",
      "prompt": "Review this PR: https://github.com/org/repo/pull/42",
      "expect_activation": true,
      "assertions": [
        {
          "type": "content",
          "check": "contains_section",
          "value": "Security Concerns"
        },
        {
          "type": "content",
          "check": "contains_section",
          "value": "Test Coverage"
        },
        {
          "type": "content",
          "check": "contains_section",
          "value": "Style Issues"
        }
      ]
    }
  ]
}
```

### Assertion Types

| Type | Check | Description |
|------|-------|-------------|
| `format` | `matches_regex` | Output must match a regex pattern |
| `format` | `is_json` | Output must be valid JSON |
| `format` | `is_yaml` | Output must be valid YAML |
| `length` | `max_chars` | Field must not exceed character limit |
| `length` | `min_chars` | Field must be at least this many characters |
| `content` | `contains` | Output must contain a specific string |
| `content` | `contains_section` | Output must contain a named section |
| `content` | `not_contains` | Output must NOT contain a specific string |
| `behavior` | `tool_called` | A specific tool must be invoked |
| `behavior` | `tool_not_called` | A specific tool must NOT be invoked |

---

## benchmark.json Format

Aggregated results from the most recent evaluation run.

```json
{
  "skill": "my-skill",
  "version": "1.0.0",
  "run_date": "2026-06-11T10:00:00Z",
  "total_cases": 10,
  "passed": 9,
  "failed": 1,
  "pass_rate": 0.90,
  "results": [
    {
      "case_id": "trigger-001",
      "passed": true,
      "activation_correct": true,
      "assertions_passed": 2,
      "assertions_total": 2
    },
    {
      "case_id": "output-001",
      "passed": false,
      "activation_correct": true,
      "assertions_passed": 2,
      "assertions_total": 3,
      "failures": [
        "Missing section: Test Coverage"
      ]
    }
  ]
}
```

---

## eval_metadata.json Format

Configuration for the evaluation run.

```json
{
  "skill": "my-skill",
  "eval_version": "1.0.0",
  "min_pass_rate": 0.90,
  "max_retries": 3,
  "timeout_seconds": 300,
  "evaluator": "human",
  "notes": "L3 evaluation requires manual execution or an automated runner."
}
```

---

## Running an L3 Evaluation

### Manual Process (Current)

1. Create `evals/evals.json` with test cases.
2. For each case, invoke the skill with the given prompt.
3. For activation cases (`expect_activation: true`): verify the skill triggered.
4. For the triggered cases: verify each assertion against the output.
5. Record results in `evals/benchmark.json`.
6. Calculate pass rate. Target: ≥90%.

### Automated Process (Future)

When a `scripts/run-eval.py` becomes available:

```bash
python scripts/run-eval.py <skill-directory>
```

This script will:
- Load `evals/evals.json`.
- Execute each test case by invoking the skill.
- Check assertions against the output.
- Generate `evals/benchmark.json`.
- Report pass rate and failures.

---

## Trigger Test Design — Best Practices

A good L1 trigger test (always do this before L3):

1. **Positive triggers (should activate)**: 5-7 prompts that should trigger the skill.
   Cover different phrasings and synonym variations.
2. **Negative triggers (should NOT activate)**: 3-5 prompts that are close to the
   skill's domain but should NOT trigger it.
3. **Edge cases**: 2-3 prompts that are ambiguous — these reveal whether your
   description is too narrow or too broad.

Example trigger test spreadsheet:

| # | Prompt | Should Activate? | Actually Activated? | Notes |
|---|--------|-----------------|--------------------|-------|
| 1 | "Create a commit message" | Yes | Yes | - |
| 2 | "What should I put in my commit?" | Yes | Yes | - |
| 3 | "Generate conventional commit" | Yes | Yes | - |
| 4 | "Write a git message for my changes" | Yes | No | Missing keyword "commit" |
| 5 | "I staged some files, help me commit" | Yes | Yes | - |
| 6 | "Add a login button to the page" | No | No | - |
| 7 | "What's the git log format?" | No | Yes | False positive! Add negative trigger about git log |
| 8 | "Show me the commit history" | No | Yes | False positive! Add negative trigger |

---

## Interpreting Results

| Pass Rate | Assessment | Action |
|-----------|-----------|--------|
| ≥95% | Excellent | Skill is well-tuned. |
| 90-94% | Good | Minor description or assertion adjustments. |
| 80-89% | Needs work | Focus on false negatives (missing triggers) or false positives. |
| <80% | Problematic | Major rewrite of description or body needed. |

---

## Regression Testing

After any modification to the skill, re-run the evaluation and compare to the previous
benchmark. A regression is any previously-passing test case that now fails.

```bash
# Compare benchmarks (conceptual)
diff <(jq '.results' old_benchmark.json) <(jq '.results' new_benchmark.json)
```

If pass rate drops below the previous benchmark, investigate the failing cases before
committing the change.

---

## Integration with Original skill-creator

The original anthropics/skill-creator includes:
- `scripts/aggregate_benchmark` — aggregates multiple eval runs
- `eval-viewer/generate_review.py` — generates an HTML review of eval results
- `agents/grader.md` and `agents/analyzer.md` — Claude subagents for automated grading

These tools are Claude Code-specific. For cross-platform evaluation, adapt the concepts
to your platform's capabilities or use manual evaluation.
