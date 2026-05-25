#!/usr/bin/env python3
"""
Create a starter embedded workspace and install board-aware skills.

This is a convenience wrapper for first-time users. It creates a new firmware
project outside the embedskill repository, installs AGENTS.md using
install_skill.py, and prints a prompt the user can try with their coding agent.

Examples:
  python3 scripts/quick_start.py
  python3 scripts/quick_start.py --board uno_q
  python3 scripts/quick_start.py --board uno_q --peripheral ssd1306_oled_i2c
  python3 scripts/quick_start.py --board arduino_uno_q --workspace ~/embedskill_workspace
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Optional

import install_skill


DEFAULT_BOARD = "arduino_uno_q"
DEFAULT_WORKSPACE = "~/embedskill_workspace"
DEFAULT_OUTPUT = "AGENTS.md"
DEFAULT_EXAMPLE = "led_blink"


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def render_project_readme(board_id: str, peripheral_ids: List[str], output_name: str) -> str:
    peripheral_text = ""
    if peripheral_ids:
        joined = ", ".join(f"`{peripheral}`" for peripheral in peripheral_ids)
        peripheral_text = f"\nInstalled peripheral skills: {joined}.\n"

    return f"""# {board_id}_{DEFAULT_EXAMPLE}

Starter firmware project created by `embedskill/scripts/quick_start.py`.

## Board Skill

This project has a local `{output_name}` file generated from the embedskill
board and platform skills.
{peripheral_text}

## How to Use

Start your coding agent from this directory, then ask it to read `{output_name}`
before generating code.

Example prompt:

```text
Read {output_name}. Generate a minimal LED blink program for this board.
Use the correct board pin constants and build workflow from the installed skill.
Create the source files in this project directory.
```

Generated firmware should stay in this project directory.
"""


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a starter firmware project with embedskill context installed."
    )
    parser.add_argument(
        "--board",
        default=DEFAULT_BOARD,
        help=f"Board id or alias. Default: {DEFAULT_BOARD}.",
    )
    parser.add_argument(
        "--platform",
        help="Platform id. If omitted, inferred from the board filename when possible.",
    )
    parser.add_argument(
        "--peripheral",
        action="append",
        default=[],
        help="Peripheral id or alias to include. Can be passed multiple times.",
    )
    parser.add_argument(
        "--workspace",
        default=DEFAULT_WORKSPACE,
        help=f"Workspace directory to create/use. Default: {DEFAULT_WORKSPACE}.",
    )
    parser.add_argument(
        "--project-name",
        help="Project directory name. Default: <board>_led_blink.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Agent context filename to create. Default: {DEFAULT_OUTPUT}.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated context/README files if they already exist.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available boards and platforms, then exit.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    root = install_skill.repo_root()

    if args.list:
        install_skill.print_available(root)
        return 0

    try:
        board_path = install_skill.resolve_board(root, args.board)
        board_id = install_skill.board_id_from_filename(board_path)
        platform = args.platform or install_skill.infer_platform_from_board(board_path)
        if not platform:
            print(
                "ERROR: --platform is required because it could not be inferred from the board.",
                file=sys.stderr,
            )
            return 2
        platform_path = install_skill.resolve_platform(root, platform)
        peripheral_paths = [
            install_skill.resolve_peripheral(root, peripheral)
            for peripheral in args.peripheral
        ]
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    workspace = Path(args.workspace).expanduser().resolve()
    project_name = args.project_name or f"{normalize_name(board_id)}_{DEFAULT_EXAMPLE}"
    project_dir = workspace / project_name
    output_path = project_dir / args.output
    readme_path = project_dir / "README.md"

    project_dir.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not args.force:
        print(
            f"ERROR: {output_path} already exists. Use --force to overwrite it.",
            file=sys.stderr,
        )
        return 1

    if readme_path.exists() and not args.force:
        print(
            f"ERROR: {readme_path} already exists. Use --force to overwrite it.",
            file=sys.stderr,
        )
        return 1

    context = install_skill.render_context(
        root,
        board_path,
        platform_path,
        peripheral_paths,
        args.output,
    )
    install_skill.write_text(output_path, context)
    peripheral_ids = [
        install_skill.peripheral_id_from_filename(path)
        for path in peripheral_paths
    ]
    install_skill.write_text(
        readme_path,
        render_project_readme(board_id, peripheral_ids, args.output),
    )

    print("Your new embedskill workspace is ready.")
    print("")
    print(f"Workspace: {workspace}")
    print(f"Project:   {project_dir}")
    print(f"Context:   {output_path}")
    if peripheral_ids:
        print(f"Peripherals: {', '.join(peripheral_ids)}")
    print("")
    print("Next steps:")
    print(f"  cd {project_dir}")
    print("  Start your preferred coding agent from this directory.")
    print("")
    print("Try this prompt:")
    print(f"  Read {args.output}. Generate a minimal LED blink program for this board.")
    print("  Use the correct board pin constants and build workflow from the installed skill.")
    print("  Create the source files in this project directory.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
