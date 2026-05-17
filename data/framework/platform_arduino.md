# Arduino Platform Guide (`arduino-cli`)

Use `arduino-cli` or the Arduino IDE for boards that target the Arduino
framework.

## Required Tools

- `arduino-cli`
- The board's Arduino core, identified by the board skill's `core` field
- The board's fully qualified board name (FQBN), identified by the board skill's
  `fqbn` field
- Any libraries required by the generated sketch

## Typical Workflow

1. Confirm the target board from the installed project context file.
2. Confirm the FQBN from the board skill.
3. Create a standard Arduino sketch directory where the folder name matches the
   `.ino` file name.
4. Compile with `arduino-cli compile --fqbn <FQBN> <sketch_name>`.
5. Connect the board and identify the serial port with `arduino-cli board list`.
6. Upload with `arduino-cli upload -p <PORT> --fqbn <FQBN> <sketch_name>`.
7. Monitor serial output with `arduino-cli monitor -p <PORT>`.

## Common Commands

```bash
arduino-cli core update-index
arduino-cli core install <core>
arduino-cli lib install <library-name>
arduino-cli board list
arduino-cli compile --fqbn <FQBN> <sketch_name>
arduino-cli upload -p <PORT> --fqbn <FQBN> <sketch_name>
arduino-cli monitor -p <PORT>
```

## Sketch Structure

Arduino projects must follow the standard sketch structure:

```text
<sketch_name>/
└── <sketch_name>.ino
```

For example:

```text
blink/
└── blink.ino
```

## Workflow Guidelines

- Do not assume an AVR-based Arduino UNO unless the board skill explicitly says
  the target MCU is AVR.
- Prefer the board skill's named constants for pins, LEDs, and peripherals.
- Use the board skill's documented FQBN and core.
- Do not use reserved interfaces listed in the board skill.
- If upload fails, ask the user to confirm the port, cable, and bootloader/reset
  procedure for the board.

## Common Troubleshooting

- **Board not found:** Run `arduino-cli board list` and ask the user to confirm
  the board is connected with a data-capable cable.
- **Missing core:** Install the core listed in the board skill with
  `arduino-cli core install <core>`.
- **Missing library:** Install the library named by the compiler error or board
  skill with `arduino-cli lib install <library-name>`.
- **Bootloader mode:** Follow the board skill's factory reset or bootloader
  procedure.
