# Board-Aware Coding Agents — Skill Definitions

## Project Overview

Structured "skill" files that give coding agents (Claude Code, Gemini, Codex, etc.) the hardware and software context needed to generate correct, compilable, board-specific embedded firmware. Skills are split into two concerns:

- **Board configs** — hardware characteristics, pin mappings, peripherals, reset procedures
- **Platform configs** — toolchain, SDK, build/flash commands, workflow guidelines

---

## Repository Structure

```
embedskill/
├── data/
│   ├── board/          # Per-board Markdown config files
│   └── framework/      # Per-platform Markdown config files
└── scripts/
    ├── install_skill.py          # Installs selected skills into a user project
    ├── quick_start.py          # Creates a starter workspace/project
    └── validate_board_config.py  # Board config linter / CI gate
```

---

## End-User Workflow

The `embedskill` repository is a reusable skill registry. End users should generate firmware in their own project directories, not inside this repository.

Recommended layout:

```text
~/embedded/embedskill/          # skill registry
~/projects/my-firmware/         # user's actual firmware project
```

### Quickstart: Create a Starter Project

For a first test, use the starter script. It creates a workspace, creates a board-specific LED blink project, installs the selected skill context, and prints the next prompt to try.

```bash
python3 scripts/quick_start.py --board uno_q
```

By default, this creates:

```text
~/embedskill_workspace/
└── arduino_uno_q_led_blink/
    ├── AGENTS.md
    └── README.md
```

Then start your coding agent from the generated project:

```bash
cd ~/embedskill_workspace/arduino_uno_q_led_blink
codex
```

Example prompt:

```text
Read AGENTS.md. Generate a minimal LED blink program for this board.
Use the correct board pin constants and build workflow from the installed skill.
Create the source files in this project directory.
```

The starter script supports custom boards, workspaces, and project names:

```bash
python3 scripts/quick_start.py \
  --board arduino_uno_q \
  --workspace ~/embedskill_workspace \
  --project-name unoq_led_blink
```

### Manual Setup: New Project

Create your own project directory first:

```bash
mkdir -p ~/projects/my-firmware
cd ~/projects/my-firmware
```

From the user's firmware project, install the selected board and platform context:

```bash
python3 ~/embedded/embedskill/scripts/install_skill.py \
  --board arduino_uno_q \
  --platform arduino
```

This creates a project-local context file:

```text
~/projects/my-firmware/AGENTS.md
```

The user should then start the coding agent from the firmware project directory:

```bash
cd ~/projects/my-firmware
codex
```

Generated code, sketches, build files, and tests stay in the user's project directory. The `embedskill` repository remains only the source of reusable board and platform skills.

### Existing Project Integration

For an existing firmware project, run `install_skill.py` from that project directory:

```bash
cd ~/projects/existing-firmware
python3 ~/embedded/embedskill/scripts/install_skill.py --board uno_q
```

This adds `AGENTS.md` to the existing project without moving source code into the `embedskill` repository. Existing output files are not overwritten unless `--force` is passed.

### Installing Skills

List available boards and platforms:

```bash
python3 scripts/install_skill.py --list
```

Install an Arduino UNO Q skill into the current directory:

```bash
python3 /path/to/embedskill/scripts/install_skill.py --board uno_q
```

Install into a specific project directory:

```bash
python3 /path/to/embedskill/scripts/install_skill.py \
  --board arduino_uno_q \
  --platform arduino \
  --project-dir ~/projects/my-firmware
```

By default, the script writes `AGENTS.md`. Use `--output` to target another agent context file:

```bash
python3 /path/to/embedskill/scripts/install_skill.py \
  --board arduino_uno_q \
  --output CLAUDE.md
```

Existing output files are not overwritten unless `--force` is passed.

---

## Board Configurations (`data/board/`)

Each file follows the naming convention `board_arduino_<name>.md` or `board_idf_<name>.md`.

| File | Board | MCU |
|------|-------|-----|
| `board_arduino_uno_r4_minima.md` | Arduino UNO R4 Minima (ABX00080) | Renesas R7FA4M1AB3CFM — Arm Cortex-M4 @ 48 MHz |
| `board_arduino_nano_r4.md` | Arduino Nano R4 (ABX00143) | Renesas RA4M1 — Arm Cortex-M4 @ 48 MHz |
| `board_arduino_nano33_ble_rev2.md` | Arduino Nano 33 BLE Rev2 (ABX00071/72) | Nordic nRF52840 — Arm Cortex-M4F @ 64 MHz |
| `board_arduino_nano_esp32.md` | Arduino Nano ESP32 (ABX00083) | ESP32-S3 — Xtensa LX7 dual-core @ 240 MHz |
| `board_arduino_nano_matter.md` | Arduino Nano Matter (ABX00112/137) | Silicon Labs MGM240SD22VNA — Arm Cortex-M33 @ 78 MHz |
| `board_idf_esp32_c3.md` | ESP32-C3-DevKit-RUST-1 | ESP32-C3 — RISC-V single-core @ 160 MHz |

Each board file covers: Board Overview metadata, Project Setup, Supported Platforms, Pin Reference tables, On-Board Peripherals, Factory Reset steps, Power Notes, and Additional Resources.

---

## Platform Configurations (`data/framework/`)

| File | Description |
|------|-------------|
| `platform_config.md` | Master config — toolchain selection logic and general agent workflow |
| `platform_arduino.md` | Arduino workflow guide using `arduino-cli` |
| `platform_esp32.md` | ESP32 workflow guide using ESP-IDF (`idf.py`) and `esptool.py` |

---

## Validating Board Configs (`scripts/validate_board_config.py`)

A linter that checks board config Markdown files against the required format before they are merged. Exits `0` if all files pass, `1` if any errors are found — usable as a CI gate.

### Usage

```bash
# Single file
python3 scripts/validate_board_config.py data/board/board_arduino_nano_r4.md

# All boards in a directory
python3 scripts/validate_board_config.py data/board/

# Multiple specific files
python3 scripts/validate_board_config.py file1.md file2.md
```

### Checks

**Structural (hard errors):**

1. Filename starts with `board_arduino_` or `board_idf_`
2. H1 title present (warning if it doesn't end with `Board Notes`)
3. `## Project Setup` present — with `**Build system**`, `**Project structure**`, `**Build/Flash commands**`
4. `## Supported Platforms` present and non-empty
5. `## Board Overview` present
6. `## Pin Reference` present — with at least one `|`-delimited table
7. `## Factory Reset` present (any suffix) — with at least one numbered step
8. `## Power Notes` present
9. `## Additional Resources` present — with at least one `https://` URL

**Metadata fields within `## Board Overview` (hard errors):**

10. `` `board` `` field present and non-empty
11. `` `model` `` field present and non-empty
12. `` `fqbn` `` present — Arduino boards only (detected from filename prefix)
13. `` `core` `` present — Arduino boards only

**Warnings (soft):**

14. H1 title doesn't end with `Board Notes`
15. `## On-Board Peripherals` section missing
