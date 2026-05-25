# Embedded Platform Configuration

This file provides the essential context needed before starting an embedded
development session. Read this before any board-specific or platform-specific
files are loaded.

## Tool Selection

Choose the correct toolchain based on the board's supported platform:

| Platform | Toolchain | Use When |
| -------- | --------- | -------- |
| **Arduino** | `arduino-cli` or Arduino IDE | Board uses `.ino` sketches / Arduino framework |
| **ESP-IDF / ESP32** | `idf.py` and `esptool.py` | Board uses ESP-IDF |

Refer to the board's config file (`board_*.md`). The **Supported Platforms**
section tells you which platform to use.

> **Unsupported Boards:** If no board config exists, there is no predefined
> hardware profile. Double-check all pin assignments, voltage limits, peripheral
> mappings, and build commands with the user before generating or flashing code.

---

## General Agent Workflow

1. Read the project-local context file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
   or equivalent) before generating code.
2. Keep generated firmware in the user's project directory.
3. Use the selected board skill for pin mappings, reserved interfaces, recovery
   steps, voltage limits, and supported peripherals.
4. Use the selected platform skill for build, upload, flash, and monitor
   commands.
5. If a command requires connected hardware, ask the user to confirm the board
   is connected and identify the serial port when auto-detection is unavailable.

---

## Platform-Specific Details

- Arduino workflow, APIs, and guidelines -> `platform_arduino.md`
- ESP-IDF workflow, APIs, and guidelines -> `platform_esp32.md`
