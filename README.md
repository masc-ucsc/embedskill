# Board-Aware Coding Agents — Skill Definitions

## Project Overview

Structured "skill" files that give coding agents (Claude Code, Gemini, Codex, etc.) the hardware and software context needed to generate correct, compilable, board-specific embedded firmware. Skills are split into three concerns:

- **Board configs** — hardware characteristics, pin mappings, peripherals, reset procedures
- **Platform configs** — toolchain, SDK, build/flash commands, workflow guidelines
- **Peripheral configs** — external sensors/displays, wiring, libraries, and usage patterns

---

## Repository Structure

```
embedskill/
├── data/
│   ├── board/          # Per-board Markdown config files
│   ├── framework/      # Per-platform Markdown config files
│   └── peripheral/     # External sensor/display Markdown config files
└── scripts/
    ├── install_skill.py          # Installs selected skills into a user project
    ├── quick_start.py            # Creates a starter workspace/project
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

This also lists available peripheral skills.

Install an Arduino UNO Q skill into the current directory:

```bash
python3 /path/to/embedskill/scripts/install_skill.py --board uno_q
```

Install Arduino UNO Q with an SSD1306 I2C OLED peripheral skill:

```bash
python3 /path/to/embedskill/scripts/install_skill.py \
  --board uno_q \
  --platform arduino \
  --peripheral ssd1306_oled_i2c
```

Install Arduino UNO Q with BME280 and SSD1306 OLED peripheral skills:

```bash
python3 /path/to/embedskill/scripts/install_skill.py \
  --board uno_q \
  --platform arduino \
  --peripheral bme280 \
  --peripheral ssd1306_oled_i2c
```

Install into a specific project directory:

```bash
python3 /path/to/embedskill/scripts/install_skill.py \
  --board arduino_uno_q \
  --platform arduino \
  --peripheral ssd1306_oled_i2c \
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

## Custom Boards With On-Board Peripherals

For custom boards that include peripherals already soldered onto the PCB, use both
a board skill and a peripheral skill:

- **Board skill**: documents what is physically present on the board and how it
  is wired.
- **Peripheral skill**: documents reusable device behavior, driver/library
  options, protocol notes, and platform-specific usage patterns.

For example, if a custom board based on Arduino UNO Q includes an on-board
SSD1306 OLED, the custom board skill should describe board-specific wiring:

```text
On-board peripheral: SSD1306 OLED
Interface: I2C
I2C bus: Wire or Wire1
SDA: board-specific pin
SCL: board-specific pin
I2C address: 0x3C
Power rail: 3.3 V
Reset pin: none or board-specific GPIO
Conflicts/reserved pins: board-specific
```

The reusable SSD1306 behavior and platform usage remain in the peripheral skill,
such as `data/peripheral/peripheral_ssd1306_oled_i2c.md`.

---

## Board Configurations (`data/board/`)

Each file follows the naming convention `board_arduino_<name>.md` or `board_idf_<name>.md`.

| File | Board | MCU |
|------|-------|-----|
| `board_arduino_uno_q.md` | Arduino UNO Q | STM32U585 MCU + Qualcomm QRB2210 MPU |
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

## Peripheral Configurations (`data/peripheral/`)

| File | Peripheral | Interface |
|------|------------|-----------|
| `peripheral_bme280.md` | BME280 temperature, humidity, and pressure sensor | I2C preferred; SPI optional |
| `peripheral_ssd1306_oled_i2c.md` | SSD1306 128x64 OLED display | I2C |

---

## Validating Board Configs (`scripts/validate_board_config.py`)

A linter that checks board config Markdown files against the required format before they are merged. Exits `0` if all files pass, `1` if any errors are found — usable as a CI gate.

### Usage

```bash
# Single file
python3 scripts/validate_board_config.py data/board/board_arduino_uno_q.md

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
