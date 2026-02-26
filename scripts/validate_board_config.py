#!/usr/bin/env python3
"""
Board Config Validator

Validates that a board configuration Markdown file adheres to the
required format before it is added to the embedskill config repository.

Usage:
  python3 validate_board_config.py <file.md> [file2.md ...]
  python3 validate_board_config.py configs/board/
"""

import sys
import os
import re
from typing import List, Tuple


def _get_section(heading: str, content: str) -> str:
    """Return the body of a ## section, or None if absent."""
    match = re.search(
        rf'(?:^|\n)## {re.escape(heading)}\n(.*?)(?=\n## |\Z)',
        content, re.DOTALL
    )
    return match.group(1).strip() if match else None


def _has_section(heading_pattern: str, content: str) -> bool:
    """Check whether a ## section exists (heading_pattern is a regex)."""
    return bool(re.search(rf'(?:^|\n)## {heading_pattern}', content))


def validate_file(path: str) -> Tuple[List[str], List[str]]:
    """
    Validate a single board config Markdown file.
    Returns (errors, warnings) — errors are hard failures, warnings are soft.
    """
    errors: List[str] = []
    warnings: List[str] = []

    try:
        with open(path, 'r') as f:
            content = f.read()
        lines = content.splitlines()
    except Exception as e:
        return [f"Cannot read file: {e}"], []

    filename = os.path.basename(path)

    # ------------------------------------------------------------------
    # 1. File naming convention
    # ------------------------------------------------------------------
    if not (filename.startswith('board_arduino_') or filename.startswith('board_idf_')):
        errors.append(f"Filename must start with 'board_arduino_' or 'board_idf_', got: '{filename}'")

    is_arduino = filename.startswith('board_arduino_')

    # ------------------------------------------------------------------
    # 2. H1 title
    # ------------------------------------------------------------------
    h1_lines = [l for l in lines if l.startswith('# ')]
    if not h1_lines:
        errors.append("Missing H1 title (# <Board Name> Board Notes)")
    elif not h1_lines[0].endswith('Board Notes'):
        warnings.append(f"H1 title should end with 'Board Notes': {h1_lines[0]}")

    # ------------------------------------------------------------------
    # 3. Project Setup
    # ------------------------------------------------------------------
    setup = _get_section('Project Setup', content)
    if setup is None:
        errors.append("Missing required section: ## Project Setup")
    else:
        for field in ['**Build system**', '**Project structure**', '**Build/Flash commands**']:
            if field not in setup:
                errors.append(f"## Project Setup missing field: {field}")

    # ------------------------------------------------------------------
    # 4. Supported Platforms
    # ------------------------------------------------------------------
    platforms = _get_section('Supported Platforms', content)
    if platforms is None:
        errors.append("Missing required section: ## Supported Platforms")
    elif not platforms.strip():
        errors.append("## Supported Platforms section is empty")

    # ------------------------------------------------------------------
    # 5. Board Overview — metadata fields
    # ------------------------------------------------------------------
    overview = _get_section('Board Overview', content)
    if overview is None:
        errors.append("Missing required section: ## Board Overview")
    else:
        if not re.search(r'`board`\s*:\s*\S+', overview):
            errors.append("## Board Overview missing required field: `board`")
        if not re.search(r'`model`\s*:\s*.+', overview):
            errors.append("## Board Overview missing required field: `model`")
        if is_arduino:
            if not re.search(r'`fqbn`\s*:\s*\S+', overview):
                errors.append("## Board Overview missing required Arduino field: `fqbn`")
            if not re.search(r'`core`\s*:\s*\S+', overview):
                errors.append("## Board Overview missing required Arduino field: `core`")

    # ------------------------------------------------------------------
    # 6. On-Board Peripherals (warning only — may be minimal on some boards)
    # ------------------------------------------------------------------
    if not _has_section('On-Board Peripherals', content):
        warnings.append("Missing section: ## On-Board Peripherals")

    # ------------------------------------------------------------------
    # 7. Pin Reference — must have at least one Markdown table
    # ------------------------------------------------------------------
    pin_ref = _get_section('Pin Reference', content)
    if pin_ref is None:
        errors.append("Missing required section: ## Pin Reference")
    elif '|' not in pin_ref:
        errors.append("## Pin Reference must contain at least one Markdown table (| column |)")

    # ------------------------------------------------------------------
    # 8. Factory Reset — must have numbered steps
    # ------------------------------------------------------------------
    if not _has_section(r'Factory Reset.*', content):
        errors.append("Missing required section: ## Factory Reset (or ## Factory Reset / ...)")
    else:
        factory_match = re.search(
            r'(?:^|\n)## Factory Reset.*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL
        )
        if factory_match and not re.search(r'^\s*\d+\.', factory_match.group(1), re.MULTILINE):
            errors.append("## Factory Reset section must contain numbered steps (1., 2., ...)")

    # ------------------------------------------------------------------
    # 9. Power Notes
    # ------------------------------------------------------------------
    if not _has_section('Power Notes', content):
        errors.append("Missing required section: ## Power Notes")

    # ------------------------------------------------------------------
    # 10. Additional Resources — at least one URL
    # ------------------------------------------------------------------
    resources = _get_section('Additional Resources', content)
    if resources is None:
        errors.append("Missing required section: ## Additional Resources")
    elif not re.search(r'https?://\S+', resources):
        errors.append("## Additional Resources must contain at least one URL (https://...)")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.md> [file2.md ...] or <directory>")
        sys.exit(1)

    # Collect files
    files = []
    for target in sys.argv[1:]:
        if os.path.isdir(target):
            files += sorted(
                os.path.join(target, f) for f in os.listdir(target) if f.endswith('.md')
            )
        elif os.path.isfile(target):
            files.append(target)
        else:
            print(f"Warning: '{target}' not found, skipping.", file=sys.stderr)

    if not files:
        print("No files to validate.", file=sys.stderr)
        sys.exit(1)

    total_errors = 0
    total_warnings = 0

    for path in files:
        errors, warnings = validate_file(path)
        total_errors += len(errors)
        total_warnings += len(warnings)

        status = "PASS" if not errors else "FAIL"
        print(f"\n[{status}] {os.path.basename(path)}")
        for msg in errors:
            print(f"  ERROR:   {msg}")
        for msg in warnings:
            print(f"  WARNING: {msg}")

    print(f"\n{'─' * 50}")
    print(f"Checked: {len(files)}  |  Errors: {total_errors}  |  Warnings: {total_warnings}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == '__main__':
    main()
