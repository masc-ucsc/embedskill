# Arduino UNO Q Board Notes

## Project Setup
- **Build system**: `arduino-cli`
- **Project structure**: Standard Arduino sketch project
  - Sketch directory: `<sketch_name>/`
  - Main file: `<sketch_name>.ino`
- **Build/Flash commands**:
  - Compile: `arduino-cli compile --fqbn arduino:zephyr:unoq <sketch_name>`
  - Upload: `arduino-cli upload -p <PORT> --fqbn arduino:zephyr:unoq <sketch_name>`
  - Monitor: `arduino-cli monitor -p <PORT>`

## Supported Platforms
- **Arduino** (targets the STM32 MCU only)
- **Debian Linux** (targets the Qualcomm MPU via Arduino App Lab)

## Board Overview
- `board`: uno_q
- `model`: Arduino UNO Q
- `fqbn`: arduino:zephyr:unoq
- `core`: arduino:zephyr
- **Microprocessor (MPU)**: Qualcomm® QRB2210, quad-core Arm® Cortex®-A53 at 2.0 GHz, Adreno™ 702 GPU (845 MHz), runs Debian Linux OS
- **Microcontroller (MCU)**: STMicroelectronics® STM32U585, Arm® Cortex®-M33 up to 160 MHz, 2 MB Flash, 786 KB SRAM, runs Zephyr OS
- **Wireless**: WCBN3536A module — dual-band Wi-Fi® 5 (2.4/5 GHz) + Bluetooth® 5.1, onboard antennas
- **Memory**: 2 GB or 4 GB LPDDR4 RAM; 16 GB or 32 GB eMMC storage
- **Multimedia**: ANX7625 codec for video/audio over USB-C (DisplayPort)
- **Power Management**: Qualcomm® PM4145 PMIC
- USB-C® connector for power, programming, and display output (USB 3.1 Gen 1, 5 V 3 A)
- Classic UNO form factor — compatible with UNO shields

> **Note:** This is a dual-processor design. The Arduino IDE / arduino-cli targets only the STM32 MCU (via `arduino:zephyr` core). To program the Qualcomm MPU, use Arduino App Lab. The two processors communicate over RPC via the `Arduino_RouterBridge` library; `/dev/ttyHS1` (Linux) and `Serial1` (MCU) are reserved for this — do not use them directly.

## On-Board Peripherals

### LED Matrix

| Feature | Value |
| ------- | ----- |
| Size | 8×13 blue LEDs |
| Controller | STM32 MCU |
| Library | `Arduino_LED_Matrix.h` |
| Frame format | Flat `uint8_t[104]` array (8 rows × 13 cols) |
| Grayscale | 3-bit (8 levels) or 8-bit input mapped to 3-bit |

Key API:
```cpp
#include <Arduino_LED_Matrix.h>
Arduino_LED_Matrix matrix;
matrix.begin();
matrix.setGrayscaleBits(3); // 8 brightness levels (0–7)
matrix.draw(frameArray);    // frameArray is uint8_t[104]
```

### RGB LEDs

The board has 4× RGB LEDs. LEDs are active low on the MCU side.

| LED | Controller | Interface |
| --- | ---------- | --------- |
| LED 1 | MPU (Qualcomm) | `/sys/class/leds/red:user`, `green:user`, `blue:user` |
| LED 2 | MPU (Qualcomm) | `/sys/class/leds/red:panic`, `green:wlan`, `blue:bt` (also user-controllable) |
| LED 3 | MCU (STM32) | `LED3_R`, `LED3_G`, `LED3_B` — active low GPIO |
| LED 4 | MCU (STM32) | `LED4_R`, `LED4_G`, `LED4_B` — active low GPIO |

MPU LED control (Linux / Python):
```python
from arduino.app_utils import Leds
Leds.set_led1_color(1, 0, 0)  # R, G, B
```

MCU LED control (Arduino):
```cpp
pinMode(LED3_R, OUTPUT);
digitalWrite(LED3_R, LOW);   // LOW = ON (active low)
```

### Other On-Board GPIO

| Function | Reference |
| -------- | --------- |
| Built-in LED | `LED_BUILTIN` (D13) |
| Power Button | Long press 5 s+ to reboot Linux |

## Pin Reference

### Digital Header (JDIGITAL)

| Pin | Function | Type | Description |
| --- | -------- | ---- | ----------- |
| 1 | SCL / D21 | Digital | I²C Serial Clock (Wire, PB10) |
| 2 | SDA / D20 | Digital | I²C Serial Data (Wire, PB11) |
| 3 | AREF | Analog | Analog Reference Voltage |
| 4 | GND | Power | Ground |
| 5 | D13 / SCK | Digital | GPIO / SPI Clock / LED_BUILTIN (PB13) |
| 6 | D12 / MISO | Digital | GPIO / SPI MISO (PB14) |
| 7 | D11 / MOSI | Digital | GPIO (PWM~) / SPI MOSI (PB15) |
| 8 | D10 / SS | Digital | GPIO (PWM~) / SPI SS (PB9) |
| 9 | D9 | Digital | GPIO (PWM~) (PB8) |
| 10 | D8 | Digital | GPIO (PB4) |
| 11 | D7 | Digital | GPIO (PB2) |
| 12 | D6 | Digital | GPIO (PWM~) (PB1) |
| 13 | D5 / FDCAN1_RX | Digital | GPIO (PWM~) / CAN Bus RX (PA11) |
| 14 | D4 / FDCAN1_TX | Digital | GPIO / CAN Bus TX (PA12) |
| 15 | D3 | Digital | GPIO (PWM~) / OPAMP OUT (PB0) |
| 16 | D2 | Digital | GPIO (PB3) |
| 17 | D1 / TX | Digital | GPIO / UART TX (PB6) |
| 18 | D0 / RX | Digital | GPIO / UART RX (PB7) |

### Analog Header (JANALOG)

| Pin | Function | Type | Description |
| --- | -------- | ---- | ----------- |
| 1 | BOOT | Mode | Mode selection |
| 2 | IOREF | Reference | Digital logic voltage reference |
| 3 | RESET | Reset | Active-low reset |
| 4 | +3V3 | Power Out | 3.3 V power rail |
| 5 | +5V | Power Out | 5 V power rail |
| 6 | GND | Power | Ground |
| 7 | GND | Power | Ground |
| 8 | VIN | Power In | Voltage input (7–24 V) |
| 9 | A0 / DAC0 | Analog | ADC / DAC (PA4) |
| 10 | A1 / DAC1 | Analog | ADC / DAC (PA5) |
| 11 | A2 | Analog | ADC / OPAMP IN+ (PA6) |
| 12 | A3 | Analog | ADC / OPAMP IN− (PA7) |
| 13 | A4 / SDA2 | Analog | ADC / I²C SDA — D18 (PC1) |
| 14 | A5 / SCL2 | Analog | ADC / I²C SCL — D19 (PC0) |

## Analog Features

| Feature | Pin | Notes |
| ------- | --- | ----- |
| ADC (14-bit) | A0–A5 | Configurable 8/10/12/14-bit via `analogReadResolution()` |
| DAC | DAC0 (A0), DAC1 (A1) | 8–12-bit via `analogWriteResolution()` |
| ADC Reference | AREF | Default 3.3 V; configurable via `analogReference()` |

ADC reference options: `AR_INTERNAL1V5`, `AR_INTERNAL1V8`, `AR_INTERNAL2V05`, `AR_INTERNAL2V5`, `AR_EXTERNAL`.

## Communication Interfaces

| Interface | Pins | Notes |
| --------- | ---- | ----- |
| UART (Serial) | D0 (RX/PB7), D1 (TX/PB6) | |
| SPI | D10 (SS), D11 (MOSI), D12 (MISO), D13 (SCK) | |
| I2C (Wire) | D20 (SDA/PB11), D21 (SCL/PB10) | UNO-style header |
| I2C (Wire1) | Qwiic connector (I2C4) | 3.3 V only; PD13 SDA, PD12 SCL |
| CAN | D4 (FDCAN1_TX), D5 (FDCAN1_RX) | External transceiver required |
| PWM | D3, D5, D6, D9, D10, D11 | Fixed 500 Hz |

> **Reserved:** `Serial1` (MCU) and `/dev/ttyHS1` (Linux) are locked by the `arduino-router` service for MPU↔MCU RPC. Do not use them in your code.

## Bridge / RPC (MPU ↔ MCU)

The `Arduino_RouterBridge` library enables the STM32 MCU and Qualcomm MPU to call each other's functions transparently.

```cpp
// MCU sketch — expose a function to Linux
#include <Arduino_RouterBridge.h>
Bridge.begin();
Bridge.provide_safe("my_func", myFunc);
```

```python
# Python on MPU — call the MCU function
from arduino.app_utils import *
Bridge.call("my_func", arg)
```

Use `Monitor.println()` instead of `Serial.println()` to print to the Arduino App Lab console.

## Hardware Debug UART (JCTL)

- **Logic level**: 1.8 V — requires a 1.8 V USB-to-TTL converter
- **Baud rate**: 115200 bps
- Provides access to bootloader (SPL/U-Boot) logs and a Linux shell before SSH/ADB are available

## Power Notes
- **USB-C input**: 5 V 3 A (15 W)
- **VIN pin / Barrel jack**: 7–24 V
- **3V3 pin**: Output only — do not use as power input
- **5V pin**: 5 V output rail

## Factory Reset / Board Recovery

1. Double-tap the **RESET** button to enter bootloader mode.
2. Re-flash via `arduino-cli upload` or Arduino IDE.
3. For a full Linux image reflash, enter Emergency Download Mode (EDL) — refer to the flashing guide.

## Additional Resources
- Arduino UNO Q Product Page: https://store.arduino.cc/products/uno-q
- UNO Q User Manual: https://docs.arduino.cc/tutorials/uno-q/user-manual/
- Arduino App Lab: https://www.arduino.cc/en/software/#app-lab-section
- Arduino Zephyr Core Docs: https://docs.arduino.cc/learn/programming/zephyr-intro
- Arduino_RouterBridge Library: https://github.com/arduino-libraries/Arduino_RouterBridge
- Full Pinout PDF: https://docs.arduino.cc/resources/pinouts/ABX00162-full-pinout.pdf
- Datasheet PDF: https://docs.arduino.cc/resources/datasheets/ABX00162-datasheet.pdf
