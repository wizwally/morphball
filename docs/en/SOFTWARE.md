# 💻 Software Architecture - Metroid Morph Ball

Complete guide to the project's software architecture.

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────┐
│           HOME ASSISTANT (optional)         │
│  ┌────────────────────────────────────┐    │
│  │  Lovelace Dashboard                │    │
│  │  - LED Control                     │    │
│  │  - Effect selection                │    │
│  │  - Sleep config                    │    │
│  └────────────────────────────────────┘    │
│                    │                        │
│                    │ WiFi / API             │
└────────────────────┼────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│              ESP32-S3 TINY                   │
│  ┌──────────────────────────────────────┐  │
│  │  VERSION A: MicroPython              │  │
│  │  - main.py (event loop, threads)     │  │
│  │  - ledstrip.py (WS2812B driver)      │  │
│  │  - animations/* (effects)            │  │
│  └──────────────────────────────────────┘  │
│               OR                            │
│  ┌──────────────────────────────────────┐  │
│  │  VERSION B: ESPHome                  │  │
│  │  - morphball.yaml (config)           │  │
│  │  - Built-in effects library          │  │
│  │  - OTA updates                       │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  GPIO Management:                           │
│  - GPIO18 → LED Strip DIN                  │
│  - GPIO8  ← Motion signal (wake pin)       │
│  - GPIO7  → Alive signal                   │
└───────┬─────────────────────────┬───────────┘
        │                         │
        │ WS2812 Protocol         │ Digital I/O
        ▼                         ▼
┌───────────────┐         ┌──────────────────┐
│  LED STRIP    │         │  SEEED MG24      │
│  32x WS2812B  │         │                  │
│               │         │  - mg24_imu.ino  │
│  3 Groups:    │         │  - LSM6DS3 IMU   │
│  - Core (6)   │         │  - Motion detect │
│  - Inner (12) │         │                  │
│  - Ring (14)  │         │  Acceleration    │
└───────────────┘         │  threshold: 2.5G │
                          └──────────────────┘
```

## 🐍 MicroPython Version

### Multi-Thread Architecture

```python
# Thread Model

Main Thread (REPL)
    │
    ├─► Animation Thread
    │   │
    │   └─► while active:
    │           leds.pulse()
    │           fade_in/out()
    │
    └─► Motion Monitor Thread
        │
        └─► while True:
                check_timeout()
                sleep_management()
                deep_sleep()
```

### File: main.py

**Responsibilities:**
- Initial GPIO setup
- Motion sensor interrupt management
- Thread coordination
- Sleep state machine

**Key components:**

```python
# State globals
active = True                    # Animation active/standby
last_motion_time = ticks_ms()   # Last movement timestamp
anim_thread_started = False     # Animation thread flag

# Hardware setup
alive_pin = Pin(ALIVE_PIN, Pin.OUT)
motion_pin = Pin(MOTION_PIN, Pin.IN)
leds = LEDStrip(LED_PIN, NUM_LEDS, GROUPS)

# ISR - Interrupt Service Routine
def motion_interrupt(pin):
    """
    Called on RISING edge of motion_pin.
    Wake from standby if necessary.
    """
    global last_motion_time, active
    last_motion_time = time.ticks_ms()
    if not active:
        active = True
        start_animation_thread()

# Thread functions
def animation_loop():
    """Executes LED animations in loop"""
    
def motion_monitor():
    """Monitors timeout and manages sleep"""
```

**State Machine:**

```
┌─────────┐  movement    ┌────────────┐
│  ACTIVE │ ◄────────────┤   STANDBY  │
│         │              │            │
│ LED ON  │              │ Core only  │
└────┬────┘              └─────┬──────┘
     │                         │
     │ timeout 20s            │ timeout 20s
     │                         │
     ▼                         ▼
┌────────────┐          ┌─────────────┐
│  STANDBY   │          │ DEEP SLEEP  │
│            │          │             │
│ Core fade  │          │ Wake on GPIO│
└────────────┘          └─────────────┘
```

### File: ledstrip.py

**Main class:**

```python
class LEDStrip:
    def __init__(self, pin, num_leds, groups):
        self.np = NeoPixel(Pin(pin), num_leds)
        self.groups = groups
        self.num_leds = num_leds
    
    # Group methods
    def set_group_color(self, group_id, color)
    def clear_group(self, group_id)
    
    # Base animations
    def pulse(self, duration=1)
    def fade_in(self, duration=1, group_id=None)
    def fade_out(self, duration=1, group_id=None)
    
    # Utility
    def clear()
    def show()
```

**Design pattern:**
- LED group abstraction (hides physical mapping)
- Non-blocking animations (duration control via parameters)
- Thread-safe (important for multi-threading)

### Deep Sleep & Wake

```python
# Setup wake pin
esp32.wake_on_ext1(
    pins=(Pin(MOTION_PIN),), 
    level=esp32.WAKEUP_ANY_HIGH
)

# Enter deep sleep
machine.deepsleep()

# On deep sleep wake:
# - ESP32 does complete RESET
# - main.py restarts from beginning
# - Non-persistent state (RAM cleared)
```

**Wake flow:**

```
MG24 detects movement
    │
    └─► GPIO8 = HIGH (200ms pulse)
         │
         └─► ESP32 wake
              │
              └─► Boot sequence
                   │
                   └─► main.py restart
                        │
                        └─► alive_pin.on()
                             │
                             └─► Animation started
```

## 🏠 ESPHome Version

### Event-Driven Architecture

ESPHome uses a **component** and **automation** based architecture.

```yaml
# Conceptual structure

esphome:
  on_boot: [actions]

binary_sensor:        # Input events
  on_press: [actions]
  on_release: [actions]

light:                # Output control
  effects: [...]

interval:             # Periodic tasks
  - interval: 1s
    then: [actions]

script:               # Reusable actions
  - id: script_name
    then: [actions]
```

### File: morphball.yaml

**Main sections:**

#### 1. Base Configuration

```yaml
substitutions:
  device_name: morphball
  friendly_name: "Metroid Morph Ball"

esp32:
  board: esp32-s3-devkitc-1
  framework:
    type: arduino

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
```

#### 2. GPIO Setup

```yaml
# Output ALIVE
output:
  - platform: gpio
    pin: GPIO7
    id: alive_output

# Input MOTION
binary_sensor:
  - platform: gpio
    pin: GPIO8
    id: motion_sensor
    on_press:
      - script.execute: reset_sleep_timer
      - if: [wake logic]
```

#### 3. LED Control

```yaml
light:
  - platform: neopixelbus
    pin: GPIO18
    num_leds: 32
    id: morphball_light
    effects:
      - pulse:
          name: "Pulse"
      - addressable_lambda:
          name: "Custom"
          lambda: |-
            // C++ code here
```

**Lambda Effects - Detail:**

```cpp
// Lambda effect with direct LED access

it[index] = Color(R, G, B);

// Static variables for persistent state
static float brightness = 0.5;
static uint32_t last_update = 0;

// Logic
if (millis() - last_update > interval) {
    // Update colors
}
```

#### 4. Sleep Management

```yaml
globals:
  - id: last_motion_time
    type: uint32_t
  - id: sleep_mode_enabled
    type: bool

interval:
  - interval: 1s
    then:
      - if:
          condition:
            lambda: 'return check_timeout();'
          then:
            - light.turn_off
            - delay
            - deep_sleep.enter
```

#### 5. Home Assistant Integration

```yaml
api:
  encryption:
    key: !secret api_key

# Automatically exposed entities:
# - light.morphball_light
# - select.morphball_effect
# - number.morphball_sleep_timeout
# - binary_sensor.morphball_motion
# - sensor.morphball_wifi_signal
```

### OTA Updates

```yaml
ota:
  platform: esphome
  password: !secret ota_password

# Workflow:
# 1. esphome run morphball.yaml --device morphball.local
# 2. Compile new firmware
# 3. Upload via WiFi (no cable!)
# 4. Auto-reboot
```

## 🤖 MG24 - Motion Detection

### File: mg24_imu.ino

**Architecture:**

```cpp
// Setup
void setup() {
    pinMode(PIN_ALIVE, INPUT);
    pinMode(PIN_MOTION_OUT, OUTPUT);
    IMU.begin();
}

// Loop
void loop() {
    // 1. Read ESP32 status
    check_alive_signal();
    
    // 2. Read IMU
    aX = IMU.readFloatAccelX();
    aY = IMU.readFloatAccelY();
    aZ = IMU.readFloatAccelZ();
    
    // 3. Calculate magnitude
    aSum = abs(aX) + abs(aY) + abs(aZ);
    
    // 4. Threshold check
    if (aSum >= 2.5) {
        pulse_motion_pin();
    }
    
    delay(50);  // 20 Hz polling
}
```

**Detection Algorithm:**

```cpp
// Sum of absolute accelerations
float aSum = fabs(aX) + fabs(aY) + fabs(aZ);

// Static threshold
const float threshold = 2.5;  // G

// Temporal debouncing
static unsigned long lastMove = 0;
if (millis() - lastMove > 200) {  // Min 200ms between pulses
    digitalWrite(PIN_MOTION_OUT, HIGH);
    lastMove = millis();
}
```

**Possible Improvements:**

```cpp
// 1. Gesture recognition
enum Gesture {
    SHAKE,      // Rapid oscillation
    ROLL,       // Continuous rotation
    TILT,       // Static inclination
    TAP,        // Single hit
    DOUBLE_TAP  // Double hit
};

// 2. Adaptive threshold
float adaptive_threshold = 
    baseline_noise * 1.5 + offset;

// 3. I2C/UART communication instead of GPIO
// Send gesture type + intensity
```

## 🔄 Inter-MCU Communication

### Current GPIO Protocol

**ALIVE Signal (ESP32 → MG24):**

```
HIGH (3.3V)
  │     ┌───────────────────────┐
  │     │  Animations active    │
  │     │  MG24 normal polling  │
  │     └───────────────────────┘
  │
  └─► LOW (0V)
        │  ESP32 in deep sleep
        │  MG24 can reduce polling
        │  or go low power
        └───────────────────────┘
```

**MOTION Signal (MG24 → ESP32):**

```
Movement detected
  │
  ├─► Pulse HIGH (200ms)
  │    │
  │    └─► ESP32 wake (if in deep sleep)
  │         or reset timeout (if active)
  │
  └─► Return LOW
```

## 📊 Performance & Optimization

### Timing Analysis

**MicroPython:**
```
Animation frame time: ~20-50ms
Thread context switch: ~1-5ms
GPIO interrupt latency: <1ms
Deep sleep current: ~10µA
Wake time: ~100-300ms
```

**ESPHome:**
```
Effect update: 16-50ms (configurable)
API response: <100ms (LAN)
OTA update: ~30-60s
Component loop: 16ms (60 Hz)
```

### Memory Usage

**MicroPython ESP32-S3:**
```
Firmware: ~1.5MB flash
User code: ~50KB
Runtime RAM: ~100KB
Free heap: ~150KB
```

**ESPHome ESP32-S3:**
```
Firmware: ~2MB flash
Embedded config: ~10KB
Runtime: ~150KB
OTA partition: ~2MB
```

## 🧪 Testing & Debug

### MicroPython REPL

```python
# Connect via USB
screen /dev/ttyUSB0 115200

# Interactive test
>>> from ledstrip import LEDStrip
>>> leds = LEDStrip(18, 32, GROUPS)
>>> leds.set_group_color(0, (255, 0, 0))
>>> leds.show()
```

### ESPHome Logs

```bash
# Live monitor
esphome logs morphball.yaml

# Log levels
logger:
  level: DEBUG  # VERBOSE, DEBUG, INFO, WARN, ERROR
  
# Custom log
ESP_LOGD("tag", "Motion: %d", value);
```

## 📚 API Reference

### MicroPython LEDStrip API

```python
class LEDStrip:
    def __init__(self, pin: int, num_leds: int, 
                 groups: dict)
    
    def set_group_color(self, group_id: int, 
                       color: tuple[int, int, int])
    
    def pulse(self, duration: float = 1.0)
    
    def fade_in(self, duration: float = 1.0, 
                group_id: int = None)
    
    def fade_out(self, duration: float = 1.0, 
                 group_id: int = None)
    
    def clear(self, group_id: int = None)
    
    def show(self)
```

### ESPHome Services

```yaml
# Callable from HA automations

service: light.turn_on
target:
  entity_id: light.morphball_light
data:
  effect: "Rainbow"
  brightness: 200

service: select.select_option
target:
  entity_id: select.morphball_effect
data:
  option: "Pulse"
```

## 🔗 External References

- [MicroPython Docs](https://docs.micropython.org/)
- [ESPHome Docs](https://esphome.io/)
- [NeoPixel Guide](https://learn.adafruit.com/adafruit-neopixel-uberguide)
- [ESP32-S3 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf)

---

**Last updated:** April 2026
