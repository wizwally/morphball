# 🛠️ Complete Tutorial - Build Your Morph Ball

Step-by-step guide from 3D printing to first boot.

## 📋 Prerequisites

### What You Need

**Hardware:**
- [ ] 3D Printer (min volume: 150x150x150mm)
- [ ] Soldering iron + solder
- [ ] Multimeter
- [ ] Pliers, wire cutters
- [ ] Precision screwdrivers
- [ ] Hot glue gun (optional)

**Software:**
- [ ] 3D Slicer (PrusaSlicer / Cura)
- [ ] Python 3.7+ (for MicroPython) or ESPHome
- [ ] Arduino IDE (for MG24)
- [ ] USB-Serial drivers (CP2102/CH340)
- [ ] Git (to clone repo)

**Skill Level:**
- 🟢 3D Printing: Beginner
- 🟡 Electronics: Intermediate
- 🟡 Programming: Intermediate
- 🟢 Assembly: Beginner

## 🖨️ Phase 2: 3D Printing

### 2.1 Model Preparation

```bash
# Open the 3D model
cd "3D model"
# Import MorphBall.3mf into your slicer
```

### 2.2 Print Settings

**Recommended Material:** Transparent PETG

**Profile:**
```
Layer Height: 0.2mm
Wall Thickness: 1.2mm (3 perimeters)
Infill: 15-20% (Gyroid)
Supports: YES (auto-generate)
Brim/Raft: NO (if bed leveling ok)
Temperature: 240°C (PETG)
Bed Temp: 80°C
Speed: 50mm/s
Retraction: 2mm @ 40mm/s
```

**Important notes:**
- 🔴 **Supports essential** for LED mounting holes
- 🟡 **First layer critical** - verify adhesion
- 🟢 **Z-seam**: position at back for aesthetics

**Print time:** 8-12 hours (depends on size)

## 🔌 Phase 3: Electronics

### 3.1 Test Individual Components

Before soldering, **test everything separately!**

#### Test ESP32-S3

```bash
# Install esptool
pip install esptool

# Test connection
esptool.py --port /dev/ttyUSB0 chip_id

# Expected output:
# Chip is ESP32-S3 (revision X)
```

#### Test LED Strip

```python
# Test with Arduino/base ESP32
#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel strip(32, 18, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();
}

void loop() {
  strip.fill(strip.Color(0, 255, 30));  // Green
  strip.show();
  delay(1000);
}
```

✅ All 32 LEDs should light up green

### 3.2 Soldering

**⚠️ IMPORTANT: Test EVERYTHING before permanent soldering!**

#### Soldering Order

1. **ESP32 ↔ MG24 Stack**

Solder:
- MG24 D5 → ESP32 GPIO7
- MG24 D4 → ESP32 GPIO8  
- MG24 3V3 → ESP32 3V3
- MG24 GND → ESP32 GND

**Technique:**
- Short wires (<3cm)
- 28-30 AWG silicone
- Colors: Red=3V3, Black=GND, Yellow=D5, Green=D4

2. **LED Strip → ESP32**

```
LED Strip          ESP32
DIN  ─────────────► GPIO18 (+ 330Ω R optional)
5V   ─────────────► 5V (or battery+)
GND  ─────────────► GND
```

3. **Battery + Power Circuit**

```
3.7V LiPo Battery
    ├─ (+) ─► Switch ─► TP4056 IN+ ─► 5V (LEDs + ESP32)
    └─ (-) ─────────────► TP4056 IN- ─► GND
                              │
                          USB charging
```

**⚠️ Polarity Warning!**
- Red = +
- Black = -
- Reversal = 💥 fried components

### 3.3 Insulation

```
After soldering:
1. Heat shrink on ALL connections
2. Verify NO shorts with multimeter
3. Test continuity with beeper
4. Hot glue on critical points (stress relief)
```

## 💻 Phase 4: Software

### Option A: MicroPython (Standalone)

#### 4.1 Flash MicroPython

```bash
# Download firmware
wget https://micropython.org/download/esp32s3/

# Flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash

esptool.py --chip esp32s3 --port /dev/ttyUSB0 \
  write_flash -z 0x0 esp32s3-micropython.bin
```

#### 4.2 Upload Code

```bash
# Install mpremote
pip install mpremote

# Upload files
cd ESP32
mpremote connect /dev/ttyUSB0 cp main.py :
mpremote connect /dev/ttyUSB0 cp ledstrip.py :
mpremote connect /dev/ttyUSB0 cp -r animations :
```

#### 4.3 Flash MG24

```bash
# Arduino IDE
1. Install board: Seeed XIAO SAMD
2. Open: MG24/mg24_imu.ino
3. Select: Tools > Board > XIAO MG24
4. Select: Tools > Port > /dev/ttyUSB1
5. Upload (Ctrl+U)

# Verify serial monitor:
✅ IMU ready — reading accelerations
```

### Option B: ESPHome (Home Assistant)

#### 4.1 Setup ESPHome

```bash
# Install
pip install esphome

# Or use HA addon
```

#### 4.2 Config Secrets

```bash
cd ESPHome
cp secrets.yaml.example secrets.yaml
nano secrets.yaml

# Fill:
wifi_ssid: "YourWiFi"
wifi_password: "YourPassword"
api_key: "<generate with: openssl rand -base64 32>"
```

#### 4.3 Compile & Flash

```bash
# First time (via USB)
esphome run morphball.yaml

# Select serial port
# Wait for compilation (~5 min first time)
# Auto-flash
```

#### 4.4 Add to Home Assistant

```
1. Settings > Devices & Services
2. ESPHome > Configure
3. Host: morphball.local
4. Encryption key: <from secrets.yaml>
5. Done! 🎉
```

## 🔧 Phase 5: Final Assembly

### 5.1 Shell Preparation

```bash
1. Clean inside with isopropyl alcohol
2. Remove print dust
3. Test fit components (NO glue yet!)
4. Mark LED positions with marker
```

### 5.2 LED Installation

**Procedure:**
1. Cut strip to size (preserve connectors!)
2. Bend gently (min radius 2cm)
3. Secure with hot glue every 8-10 LEDs
4. Clean DIN cable routing to ESP32

### 5.3 Electronics Mounting

```
Internal layout (section):

[Upper shell]
    │
    ├─ LED ring (glued)
    │
[3D print shelf]
    │
    ├─ ESP32 + MG24 stack (M2 screws)
    │
    ├─ Switch (snap fit or glue)
    │
[Lower shelf]
    │
    └─ Battery (velcro or foam double-side)
```

### 5.4 Pre-Closure Test

```bash
✓ Power on
✓ LED check (all 32)
✓ Motion test (shake the ball)
✓ Serial monitor OK
✓ WiFi connect (if ESPHome)
✓ Home Assistant entity visible
```

### 5.5 Final Closure

```
1. Align upper + lower shell
2. M2 screws x 4-6 in provided holes
3. Gradual tightening (no overtightening!)
4. Final rotation/shake test
5. If all OK: apply O-ring (optional)
```

## 🎮 Phase 6: Testing & Calibration

### 6.1 Movement Test

```bash
Test checklist:

□ Gentle shake → LEDs react
□ Continuous roll → Smooth animations
□ Stationary 20s → Standby (core only)
□ Stationary 40s → Deep sleep (all off)
□ New shake → Immediate wake
□ No internal mechanical noise
```

### 6.2 IMU Calibration

If motion detection too sensitive/insensitive:

```cpp
// MG24/mg24_imu.ino

// Modify this line:
const float accelerationThreshold = 2.5;  // Default

// Typical values:
// 1.5 = Very sensitive (even breathing)
// 2.5 = Medium (default)
// 4.0 = Less sensitive (needs firm shake)
```

Re-upload and test!

### 6.3 Animation Tuning

**MicroPython:**

```python
# ESP32/main.py

# Sleep timeout
SLEEP_TIMEOUT_MS = 20_000   # Increase if too fast
STANDBY_WAIT_MS  = 20_000   # Same

# Group colors
leds.set_group_color(0, (R, G, B))  # Modify colors
```

**ESPHome:**

```yaml
# ESPHome/morphball.yaml

# Timeout via HA dashboard (dynamic!)
number:
  - platform: template
    name: "Sleep Timeout"
    initial_value: 20  # Seconds
```

## 🎨 Phase 7: Customization

### 7.1 Custom LED Effects

**ESPHome Lambda:**

```yaml
- addressable_lambda:
    name: "My Custom Effect"
    update_interval: 50ms
    lambda: |-
      static float hue = 0;
      for (int i = 0; i < it.size(); i++) {
        it[i] = Color::from_hsv((hue + i * 10), 1.0, 1.0);
      }
      hue += 1;
      if (hue > 360) hue = 0;
```

### 7.2 HA Automations

```yaml
# configuration.yaml or automations.yaml

automation:
  # At sunset → Rainbow
  - alias: "Morphball Sunset Rainbow"
    trigger:
      platform: sun
      event: sunset
    action:
      service: select.select_option
      target:
        entity_id: select.metroid_morph_ball_effect
      data:
        option: "Rainbow"
```

## 🐛 Troubleshooting Common Issues

### Issue: LEDs don't light up

**Debug:**
```bash
1. Verify power: 
   multimeter on 5V rail → should be ~5V

2. Verify DIN signal:
   oscilloscope/logic analyzer → should have data

3. Test single LED:
   disconnect strip, try with 1 LED only
```

**Common fixes:**
- ❌ DIN disconnected → re-solder
- ❌ 5V too low (<4.5V) → dead battery or regulator fail
- ❌ LED strip reversed → DIN goes to first LED!
- ❌ First LED DOUT broken → skip first LED, use second

### Issue: Motion not detected

**Debug:**
```cpp
// MG24 serial monitor
void loop() {
  float aSum = fabs(aX) + fabs(aY) + fabs(aZ);
  Serial.print("Accel: "); Serial.println(aSum);
  // Should change when you move!
}
```

**Common fixes:**
- ❌ Threshold too high → reduce to 1.5
- ❌ GPIO8 not connected → verify continuity
- ❌ IMU not initialized → check I2C address (0x6A or 0x6B?)

## 🎉 Congratulations!

You've completed your Metroid Morph Ball! 🔮

**Next steps:**
- [ ] Fine-tune animations
- [ ] Setup HA automations
- [ ] Consider custom PCB for v2.0
- [ ] Print more balls and make synchronized effects!

**Enjoy your build!** 🎮

---

**Total build time estimate:** 2-3 days (non-consecutive)

- 3D printing: 8-12h
- Electronics: 3-4h
- Software: 1-2h
- Assembly: 2-3h
- Testing/tuning: 2-4h

**Last updated:** April 2026
