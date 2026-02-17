# ESP32-C3-DevKit-Rust-1 v1.2 Board Skill

## Board Information
- **Board Name**: ESP3-C3-DevKit-Rust-1 v1.2
- **MCU**: ESP3-C3-MINI-1
- **Core Architecture**: RISC-V single-core

## GPIO Mappings
| Pin Number | Function                    | Notes                          |
|------------|-----------------------------|--------------------------------|
| 0          | General Purpose I/O         | ADC1-0                         |
| 1          | General Purpose I/O         | ADC1-1                         |
| 2          | WS2812 LED / General Purpose I/O | ADC1-2, Connected to onboard WS2812 LED |
| 3          | General Purpose I/O         | ADC1-3                         |
| 4          | General Purpose I/O         | ADC2-0                         |
| 5          | General Purpose I/O         | ADC2-1                         |
| 6          | General Purpose I/O         | MTCK                           |
| 7          | Built-in LED / General Purpose I/O | MTDO, Connected to onboard LED |
| 8          | I2C SCL / General Purpose I/O | Also labeled as IO9/LOG, Default SCL for I2C |
| 9          | Boot Button / General Purpose I/O | Connected to onboard Boot Button |
| 10         | I2C SDA / General Purpose I/O | Default SDA for I2C            |
| 18         | USB_D-                      | Used for USB communication     |
| 19         | USB_D+                      | Used for USB communication     |
| 20         | UART0 TX                    | U0TXD, Used for serial communication |
| 21         | UART0 RX                    | U0RXD, Used for serial communication |

## Onboard Components
- **WS2812 LED**: Addressable LED (Connected to pin 2)
- **Built-in LED**: LED (Connected to pin 7)
- **Boot Button**: Button (Connected to pin 9)
- **USB-UART Bridge**: UART (Connected to pins GPIO20 (TX), GPIO21 (RX))

## Flashing and Boot Constraints
- **Boot Mode Selection**: Press and hold the Boot button (GPIO9) while pressing and releasing the Reset button (EN) to enter bootloader mode for flashing.
- **Reset Button**: Press EN button to reset the board.

## Notes
This board skill is specifically tailored for the ESP3-C3-DevKit-Rust-1 v1.2. GPIO mappings and onboard components are based on official documentation for this board. This skill aims to provide the minimal necessary information for an AI agent to interact with the board for common tasks.
