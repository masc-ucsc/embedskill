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
    └── validate_board_config.py  # Board config linter / CI gate
```

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
| `platform_config.md` | Master config — tool selection logic, mandatory initialization sequence, references to board and platform files |
| `platform_arduino.md` | HAgent Arduino tool guide (`hagent.arduino`) — covers `install`, `refresh_config`, `list_boards`, `new_sketch`, `compile`, `upload`, `monitor` |
| `platform_esp32.md` | HAgent ESP32 tool guide (`hagent.esp32`) — covers `install`, `refresh_config`, `setup`, `build`, `flash`, `check_bootloader`, `monitor`, `idf` |

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
