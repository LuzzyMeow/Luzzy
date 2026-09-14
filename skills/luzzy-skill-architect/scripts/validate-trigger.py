#!/usr/bin/env python3
"""
L1 Trigger Validation Script for Agent Skills.

Validates that a skill's description correctly matches expected trigger phrases.
Run: python scripts/validate-trigger.py <skill-directory>

The script:
1. Reads the skill's SKILL.md and extracts the description.
2. Loads test cases from a triggers.json file (if present) or uses built-in heuristics.
3. Compares each trigger phrase against the description.
4. Reports activation rate and suggests improvements.

Requires: Python 3.8+ (stdlib only, no external dependencies)
"""

import json
import re
import sys
import argparse
from pathlib import Path


def extract_frontmatter(skill_dir: Path) -> dict:
    """Extract YAML frontmatter from SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: {skill_md} not found.")
        sys.exit(1)

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        print("ERROR: SKILL.md missing YAML frontmatter (must start with ---).")
        sys.exit(1)

    parts = content.split("---", 2)
    if len(parts) < 3:
        print("ERROR: SKILL.md frontmatter not properly closed (missing second ---).")
        sys.exit(1)

    frontmatter_text = parts[1].strip()
    metadata = {}
    current_multiline_key = None

    for line in frontmatter_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        # Check if this line starts a new key (not indented)
        if not line.startswith(" ") and ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value in (">", "|"):
                current_multiline_key = key
                metadata[key] = ""
            elif value:
                metadata[key] = value
                current_multiline_key = None
            else:
                current_multiline_key = None
        elif current_multiline_key:
            # Continuation of a multiline value
            metadata[current_multiline_key] = metadata.get(current_multiline_key, "") + " " + stripped

    # Clean up multiline values: collapse whitespace
    for key in metadata:
        if isinstance(metadata[key], str):
            metadata[key] = " ".join(metadata[key].split())

    if "description" not in metadata:
        metadata["description"] = content.split("---", 2)[2].split("\n")[0].strip()
    return metadata


def load_triggers(skill_dir: Path) -> list:
    """Load trigger test cases from triggers.json or return empty list."""
    triggers_file = skill_dir / "triggers.json"
    if triggers_file.exists():
        try:
            return json.loads(triggers_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERROR: triggers.json contains invalid JSON: {e}")
            sys.exit(1)
    return []


def check_activation(description: str, trigger_phrase: str) -> bool:
    """
    Heuristic check: does the trigger phrase match the description?
    
    Uses keyword overlap: extracts significant words from both and
    calculates a similarity score. Not a replacement for actual agent
    testing, but provides a quick first-pass filter.
    """
    desc_lower = description.lower()
    phrase_lower = trigger_phrase.lower()
    
    # Extract keywords (3+ char words, excluding stop words)
    stop_words = {
        "the", "and", "for", "use", "when", "not", "this", "that",
        "with", "from", "your", "you", "are", "was", "has", "have",
        "does", "did", "can", "will", "should", "would", "could"
    }
    
    desc_words = set(w for w in re.findall(r'\b\w{3,}\b', desc_lower) if w not in stop_words)
    phrase_words = set(w for w in re.findall(r'\b\w{3,}\b', phrase_lower) if w not in stop_words)
    
    if not phrase_words:
        return False
    
    overlap = len(desc_words & phrase_words)
    score = overlap / len(phrase_words)
    
    # Also check for negative trigger exclusion
    negative_match = False
    if "do not use for" in desc_lower:
        neg_section = desc_lower.split("do not use for")[1]
        neg_words = set(w for w in re.findall(r'\b\w{3,}\b', neg_section) if w not in stop_words)
        neg_overlap = len(neg_words & phrase_words)
        if neg_overlap > 0:
            negative_match = True
    
    if negative_match:
        return False
    
    return score >= 0.25


def analyze_description(description: str) -> list:
    """Check description quality and return improvement suggestions."""
    suggestions = []
    
    # Check for execution steps in description (anti-pattern AP-1)
    # Only flag execution words that appear outside user-speech context
    # (i.e., NOT inside quoted trigger phrases like '"audit this skill"')
    execution_indicators = [
        "first", "then", "next", "finally", "step", "run", "execute",
        "verify", "write", "read", "modify", "delete"
    ]
    # Split away quoted user-speech patterns (between double quotes)
    desc_lower = description.lower()
    clean_desc = re.sub(r'"[^"]*"', '', desc_lower)
    found_indicators = [w for w in execution_indicators if re.search(rf'\b{w}\b', clean_desc)]
    if found_indicators:
        suggestions.append(
            f"AP-1: Description may contain execution steps "
            f"(outside quoted trigger patterns). "
            f"Indicators found: {', '.join(found_indicators)}. "
            f"Move these to the body."
        )
    
    # Check for negative triggers
    if "do not use" not in desc_lower:
        suggestions.append(
            "AP-5: No negative triggers found. Add 'Do NOT use for...' "
            "to prevent false activations."
        )
    
    # Check description length
    if len(description) < 50:
        suggestions.append(
            f"Description is short ({len(description)} chars). "
            f"Add more trigger keywords and synonyms."
        )
    if len(description) > 1024:
        suggestions.append(
            f"Description exceeds 1024 chars ({len(description)}). "
            f"Trim to fit the spec limit."
        )
    
    # Check for second-person
    if re.search(r'\byou\b', desc_lower):
        suggestions.append(
            "AP-3: Description uses second-person ('you'). "
            "Rewrite in third person or imperative."
        )
    
    # Check name format
    return suggestions


def validate_name(name: str, dir_name: str) -> list:
    """Validate the name field against agentskills.io spec."""
    issues = []
    
    if not name:
        issues.append("Missing 'name' field in frontmatter.")
        return issues
    
    if len(name) < 1 or len(name) > 64:
        issues.append(f"Name length ({len(name)}) outside 1-64 character range.")
    
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name):
        if name.startswith('-') or name.endswith('-'):
            issues.append("Name must not start or end with a hyphen.")
        if '--' in name:
            issues.append("Name must not contain consecutive hyphens.")
        if not re.match(r'^[a-z0-9-]+$', name):
            issues.append("Name must contain only lowercase letters, digits, and hyphens.")
    
    if name != dir_name:
        issues.append(f"Name '{name}' does not match directory name '{dir_name}'.")
    
    return issues


def main():
    parser = argparse.ArgumentParser(
        description="L1 Trigger Validation for Agent Skills"
    )
    parser.add_argument(
        "skill_dir",
        help="Path to the skill directory to validate"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all test results, not just failures"
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    verbose = args.verbose
    
    if not skill_dir.is_dir():
        print(f"ERROR: {skill_dir} is not a directory.")
        sys.exit(1)
    
    print(f"=== Luzzy-Skill Architect: Trigger Validation ===")
    print(f"Skill: {skill_dir.name}")
    print(f"Path: {skill_dir}")
    print()
    
    # Extract metadata
    metadata = extract_frontmatter(skill_dir)
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    
    print(f"Name: {name}")
    print(f"Description ({len(description)} chars): {description[:120]}{'...' if len(description) > 120 else ''}")
    print()
    
    # Validate name
    print("--- Name Validation ---")
    name_issues = validate_name(name, skill_dir.name)
    if name_issues:
        for issue in name_issues:
            print(f"  FAIL: {issue}")
    else:
        print("  PASS: Name format is valid.")
    print()
    
    # Analyze description
    print("--- Description Analysis ---")
    desc_suggestions = analyze_description(description)
    if desc_suggestions:
        for s in desc_suggestions:
            print(f"  SUGGEST: {s}")
    else:
        print("  PASS: Description looks good.")
    print()
    
    # Trigger tests
    triggers = load_triggers(skill_dir)
    
    if not triggers:
        print("--- Trigger Test (Default) ---")
        print("No triggers.json found. Add test cases in this format:")
        print("""
[
  {"phrase": "generate a commit message", "should_activate": true},
  {"phrase": "add a button to the page", "should_activate": false}
]
        """)
        
        # Run a default heuristic check
        print("Running heuristic keyword analysis on description...")
        desc_words = set(re.findall(r'\b\w{3,}\b', description.lower()))
        print(f"  Keywords in description: {', '.join(sorted(desc_words)[:20])}...")
        print(f"  Total unique keywords: {len(desc_words)}")
        if len(desc_words) < 10:
            print("  SUGGEST: Description has few keywords. Add more trigger terms and synonyms.")
        else:
            print("  PASS: Sufficient keyword coverage.")
        print()
    else:
        print(f"--- Trigger Test ({len(triggers)} cases) ---")
        passed = 0
        failed = 0
        false_positives = 0
        false_negatives = 0
        
        for i, case in enumerate(triggers):
            phrase = case.get("phrase", "")
            should_activate = case.get("should_activate", True)
            activated = check_activation(description, phrase)
            
            status = "PASS"
            if should_activate and not activated:
                status = "FAIL (false negative: should activate but didn't)"
                false_negatives += 1
                failed += 1
            elif not should_activate and activated:
                status = "FAIL (false positive: shouldn't activate but did)"
                false_positives += 1
                failed += 1
            else:
                passed += 1
            
            if verbose or status != "PASS":
                print(f"  [{status}] \"{phrase}\"")
        
        total = len(triggers)
        pass_rate = passed / total * 100 if total > 0 else 0
        print()
        print(f"  Results: {passed}/{total} passed ({pass_rate:.0f}%)")
        print(f"  False negatives: {false_negatives}")
        print(f"  False positives: {false_positives}")
        
        if pass_rate >= 80:
            print("  PASS: Trigger activation rate meets the 80% threshold.")
        else:
            print("  FAIL: Trigger activation rate below 80%. Adjust the description.")
            print("  Suggestions:")
            if false_negatives > 0:
                print("    - Add more trigger keywords and synonyms to description.")
                print("    - Check if your test phrases use terminology not in the description.")
            if false_positives > 0:
                print("    - Add negative triggers: 'Do NOT use for...'")
                print("    - Narrow the trigger conditions in the description.")
    
    print()
    print("=== Validation Complete ===")


if __name__ == "__main__":
    main()
