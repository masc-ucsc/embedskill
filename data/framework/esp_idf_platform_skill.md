# ESP-IDF Platform Skill

## Platform Information
- **Platform Name**: ESP-IDF
- **Version**: 
- **RTOS**: FreeRTOS

## Supported Boards
- ESP3-C3-DevKit-Rust-1 v1.2

## Toolchain Information
- **Name**: ESP-IDF Toolchain (Xtensa GCC or RISC-V GCC)
- **Version Notes**: Specific GCC version depends on ESP-IDF version and target MCU. For ESP32-C3, it's RISC-V GCC.
- **Installation Instructions**: Follow Espressif's official ESP-IDF installation guide for your OS.

## Environment Setup
- `source $IDF_PATH/export.sh`

## Build Commands
- **Default**: `idf.py build`
- **Clean**: `idf.py clean`

## Flash Commands
- **Default**: `idf.py -p /dev/ttyUSB0 flash`
- **Monitor**: `idf.py -p /dev/ttyUSB0 monitor`
- **Flash and Monitor**: `idf.py -p /dev/ttyUSB0 flash monitor`

## Configuration Options
- **Menuconfig**: `idf.py menuconfig`
- **Notes**: Allows configuration of SDK options, component settings, etc.

## Notes
This is an initial draft of the ESP-IDF platform skill. The 'version' field should be updated with the specific ESP-IDF version in use (e.g., 'v5.1', 'v4.4'). Flash commands assume a typical USB-serial port; adjust '/dev/ttyUSB0' as needed for your system.
