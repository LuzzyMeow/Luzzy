#!/usr/bin/env python3
"""
Self-Update Checker for Fused Skills.

Checks whether any child skill in a Skill Family has updates available
from its registered source repository.

Usage:
    python scripts/check-updates.py --skill-dir <path-to-fused-skill>

The script reads the orchestrator SKILL.md's metadata.source_skills,
compares each source against its remote repository, and reports
available updates.

Requirements: Python 3.8+, git CLI on PATH.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def parse_metadata(skill_dir: Path) -> dict:
    """Parse YAML frontmatter metadata from orchestrator SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {"error": f"{skill_md} not found"}

    content = skill_md.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"error": "Missing YAML frontmatter"}

    return {"_raw": parts[1]}


def extract_source_skills(metadata: dict) -> list:
    """Extract source_skills entries from metadata."""
    raw = metadata.get("_raw", "")
    sources = []

    # Match source_skills list entries
    in_sources = False
    current = {}
    for line in raw.split("\n"):
        stripped = line.strip()

        if stripped.startswith("source_skills:"):
            in_sources = True
            continue
        if in_sources and stripped.startswith("- name:"):
            if current:
                sources.append(current)
            current = {}
            key, _, val = stripped[2:].partition(":")
            current[key.strip()] = val.strip().strip('"').strip("'")
            continue
        if in_sources and ":" in stripped and stripped.startswith("  "):
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key not in ["- name"]:
                current[key] = val
            continue
        if in_sources and not stripped.startswith(" ") and not stripped.startswith("-"):
            if current:
                sources.append(current)
            current = {}
            in_sources = False

    if current and "name" in current:
        sources.append(current)

    return sources


def check_git_updates(repo_url: str, current_version: str) -> dict:
    """Check a remote git repo for newer versions."""
    result = {
        "repo": repo_url,
        "current_version": current_version,
        "latest_version": None,
        "has_update": False,
        "error": None,
    }

    try:
        # Fetch remote tags
        proc = subprocess.run(
            ["git", "ls-remote", "--tags", "--sort=-version:refname", repo_url],
            capture_output=True, text=True, timeout=30
        )

        if proc.returncode != 0:
            result["error"] = f"git ls-remote failed: {proc.stderr.strip()}"
            return result

        tags = [line.split("refs/tags/")[-1] for line in proc.stdout.strip().split("\n") if "refs/tags/" in line and "^{}" not in line]
        if not tags:
            result["error"] = "No tags found in remote repository"
            return result

        latest = tags[0]
        result["latest_version"] = latest
        result["has_update"] = latest != current_version

    except FileNotFoundError:
        result["error"] = "git CLI not available on PATH"
    except subprocess.TimeoutExpired:
        result["error"] = "Timed out fetching remote tags"
    except Exception as e:
        result["error"] = str(e)

    return result


def check_http_updates(repo_url: str, current_version: str) -> dict:
    """Fallback: compare against a GitHub/GitLab API."""
    result = {
        "repo": repo_url,
        "current_version": current_version,
        "latest_version": None,
        "has_update": False,
        "error": None,
    }

    try:
        import urllib.request
        import urllib.error

        # GitHub: transform to API URL
        if "github.com" in repo_url:
            path = repo_url.split("github.com/")[-1].replace(".git", "")
            api_url = f"https://api.github.com/repos/{path}/tags"
            req = urllib.request.Request(api_url, headers={"User-Agent": "Luzzy-Skill-Architect/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                if data:
                    result["latest_version"] = data[0]["name"]
                    result["has_update"] = result["latest_version"] != current_version
                else:
                    result["error"] = "No tags found via GitHub API"
        else:
            result["error"] = "Only GitHub repos supported for HTTP fallback"
    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Check for updates in fused skills")
    parser.add_argument("--skill-dir", required=True, help="Path to the fused skill directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    if not skill_dir.is_dir():
        print(f"ERROR: {skill_dir} is not a directory.")
        sys.exit(1)

    metadata = parse_metadata(skill_dir)
    if "error" in metadata:
        print(f"ERROR: {metadata['error']}")
        sys.exit(1)

    sources = extract_source_skills(metadata)
    if not sources:
        print("No source_skills found in metadata. Not a fused skill or no sources registered.")
        sys.exit(0)

    report = {
        "skill": str(skill_dir.name),
        "checked_at": datetime.now().isoformat(),
        "total_sources": len(sources),
        "updates_available": 0,
        "sources": [],
    }

    for src in sources:
        name = src.get("name", "unknown")
        repo = src.get("repo", "")
        version = src.get("version", "unknown")

        if not repo:
            report["sources"].append({
                "name": name,
                "status": "SKIPPED",
                "reason": "No repository URL registered",
            })
            continue

        # Try git first, fall back to HTTP
        update = check_git_updates(repo, version)
        if update["error"] and "git CLI" in update["error"]:
            update = check_http_updates(repo, version)

        entry = {
            "name": name,
            "repo": repo,
            "current": version,
            "latest": update.get("latest_version", "unknown"),
            "has_update": update.get("has_update", False),
            "error": update.get("error"),
        }
        if entry["has_update"]:
            report["updates_available"] += 1
        report["sources"].append(entry)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("=" * 50)
        print("  Skill Self-Update Check")
        print("=" * 50)
        print(f"\nSkill: {report['skill']}")
        print(f"Sources: {report['total_sources']}")
        print(f"Updates available: {report['updates_available']}")
        print()

        for src in report["sources"]:
            status = "UPDATE" if src["has_update"] else "OK" if not src.get("error") else "ERROR"
            print(f"  [{status}] {src['name']}")
            print(f"    Current: {src['current']}")
            if src["has_update"]:
                print(f"    Latest:  {src['latest']} ← available!")
            elif src.get("error"):
                print(f"    Error: {src['error']}")
            print()

        if report["updates_available"] > 0:
            print("To update, re-run Luzzy-Skill-Architect and request fusion sync.")
        else:
            print("All source skills are up to date.")


if __name__ == "__main__":
    main()
