# ESP32 Platform Guide (`idf.py`)

Use ESP-IDF (`idf.py`) and `esptool.py` for boards that target the ESP-IDF
workflow.

## Required Tools

- ESP-IDF installed and exported in the shell environment
- `idf.py`
- `esptool.py`
- The chip target from the board skill, such as `esp32`, `esp32c3`, or `esp32s3`

## Typical Workflow

1. Confirm the target board from the installed project context file.
2. Confirm the ESP-IDF chip target from the board skill.
3. Create or open an ESP-IDF project.
4. Set the target with `idf.py set-target <target>`.
5. Build with `idf.py build`.
6. Put the board into the required bootloader mode if needed.
7. Flash with `idf.py -p <PORT> flash`.
8. Monitor serial output with `idf.py -p <PORT> monitor`.

## Common Commands

```bash
idf.py set-target <target>
idf.py menuconfig
idf.py build
idf.py -p <PORT> flash
idf.py -p <PORT> monitor
esptool.py --chip <chip> --port <PORT> chip_id
```

## Workflow Guidelines

- Keep generated application code in the user's project directory.
- Use the board skill's pin mappings and bootloader instructions.
- Ask the user to confirm the serial port before flashing if it is not obvious.
- Do not erase or reinitialize an existing ESP-IDF project unless the user
  explicitly asks for that.
- If the board is not detected, ask the user to confirm cabling, drivers, and
  bootloader mode.

## Common Troubleshooting

- **ESP-IDF environment missing:** Ask the user to source the ESP-IDF export
  script for their installation before running `idf.py`.
- **Wrong target:** Run `idf.py set-target <target>` using the target specified
  by the board skill.
- **Flash failure:** Follow the board skill's bootloader entry procedure, then
  retry `idf.py -p <PORT> flash`.
- **Monitor exit:** ESP-IDF monitor usually exits with `Ctrl+]`.
