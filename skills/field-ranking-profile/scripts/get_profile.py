#!/usr/bin/env python3
"""Resolve field-specific ranking profiles for authority-aware ranking."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_profiles(profile_file: str | None = None) -> dict:
    """Load bundled or custom field ranking profiles."""
    default_path = Path(__file__).resolve().parent.parent / "references" / "default_profiles.json"
    path = Path(profile_file) if profile_file else default_path
    with open(path, encoding="utf-8") as handle:
        return json.load(handle).get("profiles", {})


def get_profile(name: str = "cs", profile_file: str | None = None) -> dict:
    """Resolve one profile by name."""
    profiles = load_profiles(profile_file)
    if name not in profiles:
        available = ", ".join(sorted(profiles))
        raise SystemExit(f"Unknown profile '{name}'. Available: {available}")
    return profiles[name]


def main():
    parser = argparse.ArgumentParser(description="Resolve a field ranking profile")
    parser.add_argument("--profile", default="cs", help="Profile name (default: cs)")
    parser.add_argument("--profile-file", help="Optional custom profile JSON")
    parser.add_argument("--output", "-o", help="Write profile JSON to a file")
    args = parser.parse_args()

    profile = get_profile(args.profile, args.profile_file)
    payload = json.dumps(profile, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
