# SSD1306 0.96 Inch I2C OLED Peripheral Notes

## Device Overview

- `peripheral`: ssd1306_oled_i2c
- `model`: 0.96 inch 128x64 SSD1306 OLED display module
- `example_product`: Hosyond 0.96 Inch OLED I2C/IIC Display Module 128x64 SSD1306
- `controller`: SSD1306
- `interface`: I2C / IIC
- `resolution`: 128 x 64 pixels
- `typical_i2c_address`: 0x3C
- `alternate_i2c_address`: 0x3D
- `supply_voltage`: 3.3 V to 5 V
- `pins`: VCC, GND, SDA, SCL

Use this skill for small 4-pin SSD1306 OLED modules with pins labeled like
`GND`, `VCC`, `SCL`, and `SDA`.

## Protocol / Behavior

- SSD1306 OLED modules expose a command/data display controller interface.
- This module uses I2C, not SPI.
- The display is framebuffer-oriented: the program draws into a memory buffer
  and then sends the buffer to the screen.
- The display must be initialized before drawing.
- Drawing text or pixels does not update the physical screen until the display
  buffer is flushed.
- Most modules use address `0x3C`; some variants use `0x3D`.
- If the display does not initialize, run an I2C scanner and retry with the
  detected address.

## Wiring

| OLED Pin | Connect To | Notes |
| --- | --- | --- |
| GND | Board GND | Common ground is required |
| VCC | 3.3 V or 5 V | Prefer 3.3 V for 3.3 V boards such as ESP32 |
| SCL | Board I2C SCL | Use board skill for the correct SCL pin |
| SDA | Board I2C SDA | Use board skill for the correct SDA pin |

## Board Integration Guidance

- Do not guess SDA/SCL pins. Use the selected board skill's I2C pin mapping.
- If the OLED is soldered onto a custom board, the board skill must document the
  exact I2C bus, SDA pin, SCL pin, address, power rail, reset pin if present,
  and any conflicts with other peripherals.
- If another I2C device is used in the same benchmark, such as an MPU-6050 or
  BME280, both devices can share SDA/SCL as long as their addresses differ.

## Arduino Usage

Recommended Arduino libraries:

```bash
arduino-cli lib install "Adafruit SSD1306"
arduino-cli lib install "Adafruit GFX Library"
```

Required includes:

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
```

Initialization pattern for a 128x64 I2C SSD1306 display:

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Wire.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    while (true) {
      delay(100);
    }
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("OLED ready");
  display.display();
}

void loop() {
}
```

Arduino display update pattern:

```cpp
display.clearDisplay();
display.setCursor(0, 0);
display.print("Temp: ");
display.println(tempC);
display.print("Humidity: ");
display.println(humidity);
display.display();
```

For ESP32 using the Arduino framework, call `Wire.begin(SDA_PIN, SCL_PIN)` if
the board uses non-default I2C pins.

## ESP-IDF Usage

- Use the ESP-IDF I2C driver to configure the selected I2C controller, SDA pin,
  SCL pin, clock speed, and pull-up behavior.
- Use an SSD1306 ESP-IDF component or a small SSD1306 driver module rather than
  writing the full display protocol from scratch.
- The driver/component should initialize the SSD1306 controller, maintain a
  framebuffer or page buffer, and send updates over I2C.
- Confirm the I2C address with an I2C scan if initialization fails.
- If using ESP-IDF component manager, document the selected component and
  version in the project.

Expected ESP-IDF configuration facts:

```text
controller: SSD1306
interface: I2C
address: 0x3C or 0x3D
width: 128
height: 64
sda: board-specific
scl: board-specific
```

## MicroPython Usage

- Use `machine.I2C` to initialize the board's I2C bus.
- Use an `ssd1306.py` driver module compatible with MicroPython.
- Initialize the display with width `128`, height `64`, and the selected I2C
  object.
- Draw text or pixels into the buffer, then call `show()` to update the display.

Expected MicroPython pattern:

```python
from machine import Pin, I2C
import ssd1306

i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
display.text("OLED ready", 0, 0)
display.show()
```

## Common Failure Modes

- Wrong I2C address (`0x3C` vs `0x3D`)
- SDA and SCL swapped
- Missing display library or graphics dependency
- Forgetting to flush the framebuffer (`display.display()` or `show()`)
- Using SPI OLED code for a 4-pin I2C OLED module
- Powering from an incompatible voltage rail
- Using the wrong I2C bus on boards with multiple I2C controllers

## Benchmark Ideas

1. Display board name and uptime counter.
2. Display BME280 temperature, humidity, and pressure readings.
3. Display MPU-6050 tilt direction and acceleration values.
4. Receive UART data from another board and display the latest message.

## Additional Resources

- Amazon product page: https://www.amazon.com/dp/B09T6SJBV5
- Adafruit SSD1306 Arduino library: https://github.com/adafruit/Adafruit_SSD1306
- Adafruit GFX library: https://github.com/adafruit/Adafruit-GFX-Library
