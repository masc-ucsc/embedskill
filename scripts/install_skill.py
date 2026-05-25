#!/usr/bin/env python3
"""
Install board-aware skills into an end-user firmware project.

This script is intended to be run from the user's project directory, not
from the embedskill repository. It materializes selected board and platform
skills into a project-local context file such as AGENTS.md.

Examples:
  python3 ~/embedded/embedskill/scripts/install_skill.py --list
  python3 ~/embedded/embedskill/scripts/install_skill.py --board arduino_uno_q --platform arduino
  python3 ~/embedded/embedskill/scripts/install_skill.py --board uno_q --peripheral ssd1306_oled_i2c
  python3 ~/embedded/embedskill/scripts/install_skill.py --board uno_q --output CLAUDE.md --force
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_OUTPUT = "AGENTS.md"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def board_dir(root: Path) -> Path:
    return root / "data" / "board"


def framework_dir(root: Path) -> Path:
    return root / "data" / "framework"


def peripheral_dir(root: Path) -> Path:
    return root / "data" / "peripheral"


def normalize_id(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def board_id_from_filename(path: Path) -> str:
    stem = path.stem
    if stem.startswith("board_"):
        return stem[len("board_") :]
    return stem


def platform_id_from_filename(path: Path) -> str:
    stem = path.stem
    if stem.startswith("platform_"):
        return stem[len("platform_") :]
    return stem


def peripheral_id_from_filename(path: Path) -> str:
    stem = path.stem
    if stem.startswith("peripheral_"):
        return stem[len("peripheral_") :]
    return stem


def extract_metadata_field(content: str, field: str) -> Optional[str]:
    match = re.search(rf"`{re.escape(field)}`\s*:\s*(.+)", content)
    return match.group(1).strip() if match else None


def list_board_files(root: Path) -> List[Path]:
    return sorted(board_dir(root).glob("board_*.md"))


def list_platform_files(root: Path) -> List[Path]:
    return sorted(
        path for path in framework_dir(root).glob("platform_*.md")
        if path.name != "platform_config.md"
    )


def list_peripheral_files(root: Path) -> List[Path]:
    path = peripheral_dir(root)
    if not path.exists():
        return []
    return sorted(path.glob("peripheral_*.md"))


def build_board_index(root: Path) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for path in list_board_files(root):
        content = read_text(path)
        file_id = board_id_from_filename(path)
        aliases = {
            normalize_id(file_id),
            normalize_id(path.stem),
        }

        metadata_board = extract_metadata_field(content, "board")
        metadata_model = extract_metadata_field(content, "model")
        if metadata_board:
            aliases.add(normalize_id(metadata_board))
        if metadata_model:
            aliases.add(normalize_id(metadata_model))

        for alias in aliases:
            index[alias] = path

    return index


def build_platform_index(root: Path) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for path in list_platform_files(root):
        platform_id = platform_id_from_filename(path)
        index[normalize_id(platform_id)] = path
        index[normalize_id(path.stem)] = path
    return index


def build_peripheral_index(root: Path) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for path in list_peripheral_files(root):
        content = read_text(path)
        peripheral_id = peripheral_id_from_filename(path)
        aliases = {
            normalize_id(peripheral_id),
            normalize_id(path.stem),
        }

        metadata_peripheral = extract_metadata_field(content, "peripheral")
        metadata_model = extract_metadata_field(content, "model")
        if metadata_peripheral:
            aliases.add(normalize_id(metadata_peripheral))
        if metadata_model:
            aliases.add(normalize_id(metadata_model))

        for alias in aliases:
            index[alias] = path

    return index


def resolve_board(root: Path, board: str) -> Path:
    index = build_board_index(root)
    key = normalize_id(board)
    if key in index:
        return index[key]

    available = ", ".join(sorted(board_id_from_filename(p) for p in list_board_files(root)))
    raise ValueError(f"Unknown board '{board}'. Available boards: {available}")


def resolve_platform(root: Path, platform: str) -> Path:
    index = build_platform_index(root)
    key = normalize_id(platform)
    if key in index:
        return index[key]

    available = ", ".join(sorted(platform_id_from_filename(p) for p in list_platform_files(root)))
    raise ValueError(f"Unknown platform '{platform}'. Available platforms: {available}")


def resolve_peripheral(root: Path, peripheral: str) -> Path:
    index = build_peripheral_index(root)
    key = normalize_id(peripheral)
    if key in index:
        return index[key]

    available = ", ".join(sorted(peripheral_id_from_filename(p) for p in list_peripheral_files(root)))
    if not available:
        available = "(none)"
    raise ValueError(f"Unknown peripheral '{peripheral}'. Available peripherals: {available}")


def infer_platform_from_board(board_path: Path) -> Optional[str]:
    name = board_path.name
    if name.startswith("board_arduino_"):
        return "arduino"
    if name.startswith("board_idf_"):
        return "esp32"
    return None


def available_rows(root: Path) -> Tuple[List[Tuple[str, str, str]], List[str], List[Tuple[str, str, str]]]:
    boards = []
    for path in list_board_files(root):
        content = read_text(path)
        board_id = board_id_from_filename(path)
        model = extract_metadata_field(content, "model") or "(unknown model)"
        fqbn = extract_metadata_field(content, "fqbn") or ""
        boards.append((board_id, model, fqbn))

    platforms = [platform_id_from_filename(path) for path in list_platform_files(root)]

    peripherals = []
    for path in list_peripheral_files(root):
        content = read_text(path)
        peripheral_id = peripheral_id_from_filename(path)
        model = extract_metadata_field(content, "model") or "(unknown model)"
        interface = extract_metadata_field(content, "interface") or ""
        peripherals.append((peripheral_id, model, interface))

    return boards, platforms, peripherals


def print_available(root: Path) -> None:
    boards, platforms, peripherals = available_rows(root)

    print("Available boards:")
    for board_id, model, fqbn in boards:
        suffix = f" [{fqbn}]" if fqbn else ""
        print(f"  {board_id}: {model}{suffix}")

    print("\nAvailable platforms:")
    for platform in platforms:
        print(f"  {platform}")

    print("\nAvailable peripherals:")
    if peripherals:
        for peripheral_id, model, interface in peripherals:
            suffix = f" [{interface}]" if interface else ""
            print(f"  {peripheral_id}: {model}{suffix}")
    else:
        print("  (none)")


def render_context(
    root: Path,
    board_path: Path,
    platform_path: Path,
    peripheral_paths: List[Path],
    output_name: str,
) -> str:
    platform_config_path = framework_dir(root) / "platform_config.md"

    board_content = read_text(board_path).rstrip()
    platform_config_content = read_text(platform_config_path).rstrip()
    platform_content = read_text(platform_path).rstrip()
    peripheral_sections = []
    for path in peripheral_paths:
        peripheral_sections.append(read_text(path).rstrip())

    board_id = board_id_from_filename(board_path)
    platform_id = platform_id_from_filename(platform_path)
    peripheral_ids = [peripheral_id_from_filename(path) for path in peripheral_paths]
    peripheral_profile = "\n".join(f"- Peripheral: `{pid}`" for pid in peripheral_ids)
    peripheral_sources = "\n".join(
        f"- Peripheral skill source: `{path.relative_to(root)}`"
        for path in peripheral_paths
    )
    peripheral_content = ""
    if peripheral_sections:
        peripheral_content = "\n\n---\n\n" + "\n\n---\n\n".join(peripheral_sections)

    return f"""# Embedded Project Agent Context

This file was generated by `embedskill/scripts/install_skill.py`.

It is project-local context for coding agents. Generate and edit firmware in
this project directory. Do not write application code into the embedskill
repository.

## Selected Skill Profile

- Board: `{board_id}`
- Platform: `{platform_id}`
{peripheral_profile}
- Board skill source: `{board_path.relative_to(root)}`
- Platform skill source: `{platform_path.relative_to(root)}`
{peripheral_sources}
- Context file: `{output_name}`

## Agent Workflow Rules

1. Treat this project directory as the firmware workspace.
2. Use the board and platform notes below before generating code.
3. Respect pin mappings, reserved interfaces, voltage limits, reset steps, and toolchain commands.
4. If a requested peripheral or pin is not described here, ask the user to confirm the hardware detail before guessing.
5. Keep generated application code in this project directory.

---

{platform_config_content}

---

{platform_content}

---

{board_content}
{peripheral_content}
"""


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install embedskill board/platform context into a firmware project."
    )
    parser.add_argument(
        "--board",
        help="Board id or alias, for example: arduino_uno_q, uno_q, or 'Arduino UNO Q'.",
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
        "--project-dir",
        default=os.getcwd(),
        help="Firmware project directory where the context file should be written. Default: current directory.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Context filename to create in the project directory. Default: {DEFAULT_OUTPUT}.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available boards and platforms, then exit.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    root = repo_root()

    if args.list:
        print_available(root)
        return 0

    if not args.board:
        print("ERROR: --board is required unless --list is used.", file=sys.stderr)
        return 2

    try:
        board_path = resolve_board(root, args.board)
        platform = args.platform or infer_platform_from_board(board_path)
        if not platform:
            print(
                "ERROR: --platform is required because it could not be inferred from the board.",
                file=sys.stderr,
            )
            return 2

        platform_path = resolve_platform(root, platform)
        peripheral_paths = [
            resolve_peripheral(root, peripheral)
            for peripheral in args.peripheral
        ]
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    project_dir = Path(args.project_dir).expanduser().resolve()
    if not project_dir.exists():
        print(f"ERROR: Project directory does not exist: {project_dir}", file=sys.stderr)
        return 2
    if not project_dir.is_dir():
        print(f"ERROR: Project path is not a directory: {project_dir}", file=sys.stderr)
        return 2

    output_path = project_dir / args.output
    if output_path.exists() and not args.force:
        print(
            f"ERROR: {output_path} already exists. Use --force to overwrite it.",
            file=sys.stderr,
        )
        return 1

    content = render_context(root, board_path, platform_path, peripheral_paths, args.output)
    write_text(output_path, content)

    print(f"Installed board skill: {board_id_from_filename(board_path)}")
    print(f"Installed platform skill: {platform_id_from_filename(platform_path)}")
    for peripheral_path in peripheral_paths:
        print(f"Installed peripheral skill: {peripheral_id_from_filename(peripheral_path)}")
    print(f"Wrote context file: {output_path}")
    print("\nNext steps:")
    print(f"  cd {project_dir}")
    print("  Start your coding agent from this directory.")
    print(f"  Ask it to read {args.output} before generating embedded code.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
