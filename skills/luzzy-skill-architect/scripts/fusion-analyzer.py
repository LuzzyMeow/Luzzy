#!/usr/bin/env python3
"""
Fusion Compatibility Analyzer for Agent Skills.

Evaluates whether two or more skills can be merged into a Skill Family
without violating the 1+1>=2 principle.

Usage:
    python scripts/fusion-analyzer.py <skill-dir-1> <skill-dir-2> [skill-dir-3 ...]

Output: JSON assessment report with scores, conflict flags, and verdict.
"""

import json
import re
import argparse
from pathlib import Path


def parse_skill(skill_dir: Path) -> dict:
    """Extract metadata from a skill's SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {"error": f"{skill_md} not found", "dir": str(skill_dir)}

    content = skill_md.read_text(encoding="utf-8")
    parts = content.split("---", 2)

    if len(parts) < 3:
        return {"error": "Missing YAML frontmatter", "dir": str(skill_dir)}

    frontmatter = parts[1]
    meta = {"dir": str(skill_dir.name)}

    # Parse frontmatter line by line
    current_key = None
    for line in frontmatter.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped and not stripped.startswith(" "):
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val == ">" or val == "|":
                current_key = key
                meta[key] = ""
            elif val:
                meta[key] = val
                current_key = None
        elif current_key:
            meta[current_key] = meta.get(current_key, "") + " " + stripped
            current_key = None if not stripped.endswith("\\") else current_key

    return meta


def keywords(text: str) -> set:
    """Extract significant keywords (3+ chars, excluding stop words)."""
    stop = {
        "the", "and", "for", "use", "when", "not", "this", "that",
        "with", "from", "are", "was", "has", "have", "does", "did",
        "can", "will", "also", "handles", "only", "its", "but", "nor"
    }
    return set(w.lower() for w in re.findall(r'\b\w{3,}\b', text.lower()) if w.lower() not in stop)


def score_overlap(skill_a: dict, skill_b: dict) -> tuple:
    """Dimension 1: Domain Overlap (0-30)."""
    desc_a = skill_a.get("description", "")
    desc_b = skill_b.get("description", "")
    kw_a = keywords(desc_a)
    kw_b = keywords(desc_b)

    if not kw_a or not kw_b:
        return 10, "insufficient"

    intersection = kw_a & kw_b
    union = kw_a | kw_b
    ratio = len(intersection) / len(union) if union else 0

    if ratio >= 0.3:
        return 30, "strong"
    elif ratio >= 0.15:
        return 20, "moderate"
    elif ratio >= 0.05:
        return 10, "weak"
    else:
        return 0, "none"


def score_conflicts(skill_a: dict, skill_b: dict) -> tuple:
    """Dimension 2: Conflict Risk (CRITICAL / 0-25)."""
    critical = []
    warnings = []

    # Name collision check
    name_a = skill_a.get("name", "")
    name_b = skill_b.get("name", "")
    if name_a == name_b:
        critical.append(f"Name collision: both skills named '{name_a}'")

    # Platform conflict
    compat_a = skill_a.get("compatibility", "")
    compat_b = skill_b.get("compatibility", "")
    if compat_a and compat_b and compat_a != compat_b:
        warnings.append("Different compatibility requirements")

    # Tool conflict
    allowed_a = set(skill_a.get("allowed-tools", "").split())
    allowed_b = set(skill_b.get("allowed-tools", "").split())
    if allowed_a and allowed_b and allowed_a != allowed_b:
        warnings.append("Different allowed-tools configurations")

    # License conflict
    lic_a = skill_a.get("license", "")
    lic_b = skill_b.get("license", "")
    if lic_a and lic_b and lic_a != lic_b:
        warnings.append(f"License mismatch: {lic_a} vs {lic_b}")

    if critical:
        return 0, "critical", critical + warnings
    if len(warnings) >= 3:
        return 5, "high", warnings
    if warnings:
        return 15, "minor", warnings
    return 25, "none", []


def score_complementarity(skill_a: dict, skill_b: dict) -> tuple:
    """Dimension 3: Complementarity (0-25)."""
    desc_a = skill_a.get("description", "")
    desc_b = skill_b.get("description", "")

    # Check if one skill's output appears in the other's input keywords
    a_verbs = {"generate", "create", "produce", "build", "write", "output", "deploy", "commit"}
    b_inputs = {"input", "consume", "receive", "read", "parse", "review", "analyze", "check", "test", "verify"}

    a_output = set(w for w in re.findall(r'\b\w{4,}\b', desc_a.lower()) if w in a_verbs)
    b_input = set(w for w in re.findall(r'\b\w{4,}\b', desc_b.lower()) if w in b_inputs)

    # Chain detection: one generates, the other consumes
    chain_score = 10 if (a_output and b_input) or (
        set(w for w in re.findall(r'\b\w{4,}\b', desc_b.lower()) if w in a_verbs) and
        set(w for w in re.findall(r'\b\w{4,}\b', desc_a.lower()) if w in b_inputs)
    ) else 0

    # Domain adjacency: related but distinct sub-domains
    domain_a = keywords(desc_a)
    domain_b = keywords(desc_b)
    shared = len(domain_a & domain_b)
    if shared >= 5:
        chain_score += 15
    elif shared >= 2:
        chain_score += 8
    else:
        chain_score += 3

    if chain_score >= 20:
        return 25, "strong"
    elif chain_score >= 12:
        return 15, "moderate"
    elif chain_score >= 5:
        return 5, "weak"
    return 0, "none"


def score_structure(skill_a: dict, skill_b: dict) -> tuple:
    """Dimension 4: Structure Cleanliness (0-20)."""
    score = 20
    issues = []

    for skill, label in [(skill_a, "A"), (skill_b, "B")]:
        if "error" in skill:
            score -= 10
            issues.append(f"Skill {label}: {skill['error']}")
            continue
        name = skill.get("name", "")
        if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name):
            score -= 5
            issues.append(f"Skill {label}: name '{name}' violates spec format")
        desc = skill.get("description", "")
        if len(desc) < 20:
            score -= 3
            issues.append(f"Skill {label}: description too short ({len(desc)} chars)")
        if len(desc) > 1024:
            score -= 3
            issues.append(f"Skill {label}: description exceeds 1024 chars ({len(desc)})")

    return max(0, score), "issues" if issues else "clean", issues


def analyze(skill_dirs: list) -> dict:
    """Run full fusion analysis on all skill pairs."""
    skills = [parse_skill(Path(d)) for d in skill_dirs]

    report = {
        "skills": [s.get("name", s.get("dir", "unknown")) for s in skills],
        "pairs": [],
        "aggregate_verdict": "PENDING",
        "total_skills": len(skills),
    }

    all_scores = []
    all_criticals = []

    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            a, b = skills[i], skills[j]
            name_a = a.get("name", a.get("dir", "?"))
            name_b = b.get("name", b.get("dir", "?"))

            overlap, ov_label = score_overlap(a, b)
            conf_score, conf_label, conf_details = score_conflicts(a, b)
            comp_score, comp_label = score_complementarity(a, b)
            struct_score, struct_label, struct_issues = score_structure(a, b)

            total = overlap + conf_score + comp_score + struct_score
            all_scores.append(total)

            verdict = "STRONG" if total >= 80 else "FEASIBLE" if total >= 60 else "WEAK" if total >= 40 else "REJECT"
            if conf_label == "critical":
                verdict = "REJECT"
                all_criticals.extend(conf_details)

            pair = {
                "pair": f"{name_a} + {name_b}",
                "scores": {
                    "domain_overlap": f"{overlap}/30 ({ov_label})",
                    "conflict_risk": f"{conf_score}/25 ({conf_label})",
                    "complementarity": f"{comp_score}/25 ({comp_label})",
                    "structure": f"{struct_score}/20 ({struct_label})",
                    "total": f"{total}/100",
                },
                "verdict": verdict,
                "details": {
                    "conflicts": conf_details,
                    "structure_issues": struct_issues,
                },
            }
            report["pairs"].append(pair)

    # Aggregate verdict
    if any(p["verdict"] == "REJECT" for p in report["pairs"]):
        report["aggregate_verdict"] = "REJECT"
    elif any(p["verdict"] == "WEAK" for p in report["pairs"]):
        report["aggregate_verdict"] = "WEAK"
    elif any(p["verdict"] == "FEASIBLE" for p in report["pairs"]):
        report["aggregate_verdict"] = "FEASIBLE"
    else:
        report["aggregate_verdict"] = "STRONG"

    report["average_score"] = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Fusion Compatibility Analyzer for Agent Skills"
    )
    parser.add_argument(
        "skill_dirs",
        nargs="+",
        help="Paths to skill directories to analyze (2 or more)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    args = parser.parse_args()

    if len(args.skill_dirs) < 2:
        parser.error("At least 2 skill directories are required")

    report = analyze(args.skill_dirs)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("  Skill Fusion Analysis Report")
        print("=" * 60)
        print(f"\nCandidates: {', '.join(report['skills'])}")
        print(f"Total pairs assessed: {len(report['pairs'])}")
        print(f"Average score: {report['average_score']}/100")
        print(f"Aggregate verdict: {report['aggregate_verdict']}")
        print()

        for pair in report["pairs"]:
            print(f"--- {pair['pair']} ---")
            for dim, score in pair["scores"].items():
                print(f"  {dim}: {score}")
            print(f"  Verdict: {pair['verdict']}")

            if pair["details"]["conflicts"]:
                print("  Conflicts:")
                for c in pair["details"]["conflicts"]:
                    print(f"    - {c}")

            if pair["details"]["structure_issues"]:
                print("  Structure issues:")
                for i in pair["details"]["structure_issues"]:
                    print(f"    - {i}")
            print()

        print("Interpretation:")
        print("  STRONG (>=80): Proceed with fusion immediately.")
        print("  FEASIBLE (60-79): Proceed with noted caveats.")
        print("  WEAK (40-59): Agent recommends against; user override required.")
        print("  REJECT (<40 or CRITICAL): Fusion would violate 1+1>=2.")


if __name__ == "__main__":
    main()
