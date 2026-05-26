# BME280 Environmental Sensor Peripheral Notes

## Device Overview

- `peripheral`: bme280
- `model`: BME280 temperature, humidity, and barometric pressure sensor module
- `example_product`: BME280 breakout module, such as common GY-BME280 style boards sold for Arduino and ESP32 projects
- `sensor`: Bosch Sensortec BME280
- `measurements`: temperature, relative humidity, barometric pressure, approximate altitude
- `interfaces`: I2C and SPI on the sensor; many breakout modules expose I2C only or make SPI optional
- `typical_i2c_address`: 0x76
- `alternate_i2c_address`: 0x77
- `supply_voltage`: usually 3.3 V on the bare sensor; some breakout modules support 3.3 V to 5 V through an onboard regulator
- `pins_i2c`: VCC, GND, SDA, SCL
- `pins_spi_optional`: VCC, GND, SCK, SDI/MOSI, SDO/MISO, CS

Use this skill for BME280 environmental sensor modules used to measure
temperature, humidity, and pressure. For the capstone benchmarks, prefer I2C
mode so that the sensor can share the same bus as an SSD1306 OLED display.

## Protocol / Behavior

- The BME280 is a digital environmental sensor with factory calibration data.
- It supports I2C and SPI at the sensor level, but the available interface
  depends on the breakout board.
- I2C modules commonly use address `0x76` or `0x77`.
- The sensor must be initialized before reading values.
- Temperature, humidity, and pressure readings should be checked for reasonable
  ranges before using them in runtime tests.
- Approximate altitude can be calculated from pressure if a sea-level reference
  pressure is provided.
- Some low-cost modules sold as BME280 may actually be BMP280 modules. BMP280
  measures temperature and pressure only and does not provide humidity.

## Wiring

### I2C Wiring

| BME280 Pin | Connect To | Notes |
| --- | --- | --- |
| GND | Board GND | Common ground is required |
| VCC / VIN | Board 3.3 V or supported module voltage | Prefer 3.3 V unless the breakout explicitly supports 5 V |
| SCL | Board I2C SCL | Use board skill for the correct SCL pin |
| SDA | Board I2C SDA | Use board skill for the correct SDA pin |

### Optional SPI Wiring

| BME280 Pin | Connect To | Notes |
| --- | --- | --- |
| SCK / SCL | Board SPI SCK | SPI clock |
| SDI / SDA / MOSI | Board SPI MOSI | Data from MCU to sensor |
| SDO / MISO | Board SPI MISO | Data from sensor to MCU |
| CS / CSB | Board GPIO chip select | Keep unique per SPI device |

## Board Integration Guidance

- Do not guess SDA/SCL or SPI pins. Use the selected board skill.
- Prefer I2C for benchmarks that also use an SSD1306 OLED display.
- BME280 and SSD1306 can share the same I2C bus because they normally use
  different addresses: BME280 is usually `0x76` or `0x77`, and SSD1306 is
  usually `0x3C` or `0x3D`.
- If initialization fails, run an I2C scanner and try the detected address.
- If humidity readings are missing or the chip ID does not match BME280, check
  whether the module is actually a BMP280.
- For 3.3 V boards such as ESP32, power the module from 3.3 V unless the module
  documentation clearly says otherwise.

## Arduino Usage

Recommended Arduino libraries:

```bash
arduino-cli lib install "Adafruit BME280 Library"
arduino-cli lib install "Adafruit Unified Sensor"
```

Required includes:

```cpp
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
```

Initialization pattern for I2C:

```cpp
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define BME280_ADDR 0x76

Adafruit_BME280 bme;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!bme.begin(BME280_ADDR)) {
    Serial.println("Could not find BME280. Check wiring/address.");
    while (true) {
      delay(100);
    }
  }
}

void loop() {
  float temperatureC = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressureHpa = bme.readPressure() / 100.0F;

  Serial.print("Temp C: ");
  Serial.println(temperatureC);
  Serial.print("Humidity %: ");
  Serial.println(humidity);
  Serial.print("Pressure hPa: ");
  Serial.println(pressureHpa);

  delay(1000);
}
```

When combining BME280 with an SSD1306 OLED, initialize the I2C bus once, then
initialize both devices on the same bus using their own addresses.

## ESP-IDF Usage

- Use the ESP-IDF I2C driver to configure the selected I2C controller, SDA pin,
  SCL pin, clock speed, and pull-up behavior.
- Use a BME280 ESP-IDF component or a small BME280 driver module rather than
  writing the compensation algorithm from scratch.
- The driver must read and apply Bosch calibration coefficients before returning
  compensated temperature, humidity, and pressure values.
- If using the ESP-IDF component manager, document the selected BME280 component
  and version in the project.
- If initialization fails, scan the I2C bus and retry with address `0x76` or
  `0x77`.

Expected ESP-IDF configuration facts:

```text
sensor: BME280
interface: I2C
address: 0x76 or 0x77
sda: board-specific
scl: board-specific
measurements: temperature, humidity, pressure
```

## MicroPython Usage

- Use `machine.I2C` to initialize the board's I2C bus.
- Use a BME280 MicroPython driver module.
- Initialize the driver with the selected I2C object and address.
- Read temperature, humidity, and pressure, then print or display the values.

Expected MicroPython pattern:

```python
from machine import Pin, I2C
import bme280

i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
sensor = bme280.BME280(i2c=i2c, address=0x76)

temperature, pressure, humidity = sensor.values
print(temperature, pressure, humidity)
```

## Common Failure Modes

- Wrong I2C address (`0x76` vs `0x77`)
- SDA and SCL swapped
- Missing pull-ups on the I2C bus
- Powering a 3.3 V-only module from 5 V
- Missing Arduino libraries or ESP-IDF component
- Treating a BMP280 module as a BME280 and expecting humidity readings
- Forgetting to initialize `Wire` or the ESP-IDF I2C controller
- Using SPI code with a module wired for I2C
- Reinitializing the I2C bus separately for the OLED and BME280 instead of
  sharing one bus

## Benchmark Ideas

1. Print temperature, humidity, and pressure to the serial monitor once per
   second.
2. Display BME280 readings on an SSD1306 OLED over the same I2C bus.
3. Send BME280 readings from ESP32-C3 to Arduino UNO Q over UART.
4. Compare baseline and skill-enabled code generation for correct address,
   libraries, I2C wiring, and display update behavior.

## Additional Resources

- Bosch Sensortec BME280 product page: https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/
- Bosch Sensortec BME280 datasheet: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf
- Adafruit BME280 library: https://github.com/adafruit/Adafruit_BME280_Library
- ESP-IDF component registry BME280 search: https://components.espressif.com/components?q=bme280
- Example Amazon product page: https://www.amazon.com/dp/B0CLCRF1QS
