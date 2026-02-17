# Board-Aware Coding Agents - Initial Skill Definitions

## Project Overview

This project aims to develop a stand-alone infrastructure for board-aware coding agents. The core idea is to create structured "skills" that describe specific embedded boards and software platforms. These skills provide coding agents (like Gemini, Claude Code, or Codex) with the necessary hardware and software context to generate correct, compilable, and board-specific embedded software for a given task.

This initial phase focuses on defining these skill structures for two key components:

1.  **Board Skill**: Describes the hardware characteristics of a specific development board.
2.  **Platform Skill**: Defines the software environment (toolchain, SDK, RTOS, build/flash commands) used for that board.

## Current Progress

We have defined initial Markdown-based skill files for an **ESP32-C3-DevKit-Rust-1 v1.2** board using the **ESP-IDF** software platform.

### 1. Board Skill: `data/board/esp32_board_skill.md`

This file provides a detailed description of the `ESP3-C3-DevKit-Rust-1 v1.2` board. It focuses on the essential information an AI agent needs to interact with the hardware:

*   **`board_name`**: "ESP3-C3-DevKit-Rust-1 v1.2"
*   **`mcu`**: "ESP3-C3-MINI-1"
*   **`core_architecture`**: "RISC-V single-core"
*   **`gpio_mappings`**: A list of GPIO pins, their primary functions, and any specific notes (e.g., connected to onboard components, ADC capabilities, I2C/UART roles). For example, it identifies GPIO7 for the onboard LED and GPIO10/GPIO8 for I2C SDA/SCL.
*   **`onboard_components`**: Descriptions of integrated components like the WS2812 LED, Built-in LED, Boot Button, and USB-UART Bridge, along with their connected GPIOs.
*   **`flashing_boot_constraints`**: Instructions on how to enter bootloader mode and reset the board, crucial for programming.

### 2. Platform Skill: `data/framework/esp_idf_platform_skill.md`

This file defines the software development environment for boards using the Espressif IoT Development Framework (ESP-IDF):

*   **`platform_name`**: "ESP-IDF"
*   **`version`**: This field is currently a placeholder and should be updated with the specific ESP-IDF version in use (e.g., `v5.1`).
*   **`supported_boards`**: Lists boards compatible with this platform, currently including `ESP3-C3-DevKit-Rust-1 v1.2`.
*   **`rtos`**: Identifies FreeRTOS as the default Real-Time Operating System.
*   **`toolchain_info`**: Provides general details about the necessary compiler and tools.
*   **`environment_setup`**: Commands required to set up the ESP-IDF environment (e.g., sourcing `export.sh`).
*   **`build_commands`**: Standard build commands (e.g., `idf.py build`, `idf.py clean`).
*   **`flash_commands`**: Commands for flashing firmware and monitoring serial output (e.g., `idf.py -p /dev/ttyUSB0 flash`). The serial port (`/dev/ttyUSB0`) is a common placeholder and may need adjustment for your specific system.
*   **`configuration_options`**: Command for accessing SDK configuration (`idf.py menuconfig`).

## How Coding Agents Utilize These Skills

The separation of board and platform details allows a coding agent to understand abstract tasks and generate specific code:

1.  **Parsing:** The agent first ingests both the board and platform skill Markdown files to build a comprehensive understanding of the target hardware and software stack.
2.  **Reasoning for Board-Independent Benchmarks:**
    *   **Example Task: "Blink the onboard LED."**
        *   The agent queries the **board skill** to find which GPIO is connected to the "Built-in LED" (e.g., GPIO7 for the ESP32-C3-DevKit-Rust-1 v1.2).
        *   It then consults the **platform skill** to understand the ESP-IDF framework, identifying relevant API calls (e.g., `gpio_set_direction`, `gpio_set_level` from `driver/gpio.h`).
        *   Combining this, the agent generates C/C++ code that includes the correct headers, configures GPIO7 as an output, and toggles its level with delays using FreeRTOS tasks.

This modular approach ensures that tasks can be defined generically, while the agent, armed with the appropriate skills, can translate them into correct, compilable code for a diverse range of embedded systems.

## Next Steps

*   Review the content and structure of `data/board/esp32_board_skill.md` and `data/framework/esp_idf_platform_skill.md` for accuracy and completeness.
*   Populate the `version` field in `data/framework/esp_idf_platform_skill.md` with the exact ESP-IDF version being used.
*   Verify and adjust the serial port in `flash_commands` within `data/framework/esp_idf_platform_skill.md` if `/dev/ttyUSB0` is not correct for your environment.
*   Begin exploring initial benchmark tasks (e.g., GPIO toggle, button interrupt, I2C sensor read) to test the agent's ability to utilize these skills.
