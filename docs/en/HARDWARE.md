# 🔌 Hardware Documentation - Metroid Morph Ball

Complete hardware guide for the Morph Ball project.

## 📦 Bill of Materials (BOM)

### Electronic Components

| Component | Specifications | Qty | Est. Price | Link/Notes |
|-----------|---------------|-----|------------|-----------|
| **ESP32-S3 Tiny** | Dual-core, WiFi, BLE | 1 | €8-12 | Ideal small form factor |
| **Seeed XIAO MG24** | ARM Cortex-M33, LSM6DS3 integrated | 1 | €10-15 | Includes on-board IMU |
| **LED Strip WS2812B** | 5V, IP30, 60 LED/m | 32 LED (~53cm) | €5-8 | Cuttable per LED |
| **LiPo Battery** | 3.7V, 500-1000mAh | 1 | €8-12 | Size TBD |
| **Charging Module** | TP4056 or similar | 1 | €2-3 | With protection |
| **ON/OFF Switch** | Slide switch 3 pin | 1 | €0.50 | Miniature |
| **JST Connectors** | 2.54mm pitch | Various | €2-3 | For modular connections |
| **Wires** | AWG 22-26, silicone | 1m | €2-3 | Red/Black/Data |
| **Heat shrink** | Heat shrink tubing | 10cm | €1 | Various sizes |

### Mechanical Components

| Component | Specifications | Qty | Notes |
|-----------|---------------|-----|-------|
| **PETG Filament** | Transparent/Green | 100-150g | For main shell |
| **PLA/ASA Filament** | Opaque/Black | 50g | For internal supports |
| **M2 Screws** | 6-10mm | 4-8 | Component mounting |
| **M2 Nuts** | Standard | 4-8 | Or heat-set inserts |

**Total estimated cost:** €50-80

## 🔧 Technical Specifications

### ESP32-S3 Tiny

```
MCU: Xtensa® dual-core 32-bit LX7
Clock: up to 240 MHz
Flash: 4MB
PSRAM: 2MB
WiFi: 802.11 b/g/n
BLE: 5.0
GPIO: 27 available
ADC: 12-bit, 20 channels
Power: 3.3V (integrated 5V regulator)
Dimensions: 21mm x 17.5mm
```

**Advantages:**
- Tiny form factor
- Integrated WiFi + BLE
- Sufficient memory for OTA
- Ultra-low power deep sleep (~10µA)

### Seeed XIAO MG24

```
MCU: Silicon Labs EFR32MG24
Core: ARM Cortex-M33 @ 78 MHz
Flash: 1536 KB
RAM: 256 KB
IMU: LSM6DS3 (integrated I2C)
Power: 3.3V
Dimensions: 21mm x 17.5mm (XIAO compatible)
```

**Advantages:**
- LSM6DS3 already integrated (no external wiring!)
- Ultra low power
- Same form factor as ESP32-S3
- Dedicated I2C for IMU

### WS2812B LED Strip

```
Type: Addressable RGB LED
Protocol: WS2812/NeoPixel
Voltage: 5V
Current per LED: ~60mA @ white full brightness
Current 32 LEDs: ~1.92A @ 100% (rarely needed)
PWM Frequency: 800 kHz
Colors: 24-bit (16.7M colors)
```

**Notes:**
- 5V power, but 3.3V DATA works (ESP32 out = 3.3V)
- Recommended 100-1000µF capacitor on power
- 330Ω resistor on DATA line (optional but recommended)

## 🔌 Detailed Circuit Diagram

### ESP32-S3 Connections

```
ESP32-S3 Tiny
┌─────────────────────┐
│                     │
│ 5V  ────────┬───────┼──── Battery+ (via switch)
│             │       │
│             └───────┼──── LED Strip +5V
│                     │
│ GND ────────┬───────┼──── Battery-
│             │       │
│             ├───────┼──── LED Strip GND
│             │       │
│             └───────┼──── MG24 GND
│                     │
│ GPIO18 ─────────────┼──── LED Strip DIN
│ (LED_PIN)           │     (optional: 330Ω R)
│                     │
│ GPIO8  ◄────────────┼──── MG24 D4 (Motion OUT)
│ (MOTION_PIN)        │
│                     │
│ GPIO7  ─────────────┼──► MG24 D5 (Alive IN)
│ (ALIVE_PIN)         │
│                     │
│ 3V3 ────────────────┼──── MG24 3V3
│                     │
└─────────────────────┘
```

### MG24 Connections

```
Seeed XIAO MG24
┌──────────────────┐
│                  │
│ 3V3 ◄────────────┼──── ESP32 3V3
│                  │
│ GND ◄────────────┼──── ESP32 GND
│                  │
│ D4  ─────────────┼──► ESP32 GPIO8
│ (PIN_MOTION_OUT) │
│                  │
│ D5  ◄────────────┼──── ESP32 GPIO7
│ (PIN_ALIVE)      │
│                  │
│ SDA ─────┐       │
│          │ LSM6DS3 (internal)
│ SCL ─────┘       │
│                  │
└──────────────────┘
```

### Signal Logic

**ALIVE (ESP32 GPIO7 → MG24 D5):**
- `HIGH`: ESP32 running animations, MG24 continues monitoring
- `LOW`: ESP32 in deep sleep, MG24 can reduce polling or go low power

**MOTION (MG24 D4 → ESP32 GPIO8):**
- `HIGH` (200ms pulse): Motion detected (acceleration > 2.5G)
- `LOW`: No movement
- Wake pin for ESP32 deep sleep

### Power Supply

```
LiPo Battery 3.7V (500-1000mAh)
       │
       ├──► TP4056 (USB charging)
       │      │
       │      └──► LED charge status
       │
       └──► ON/OFF Switch
              │
              └──► 5V Boost converter (optional)
                   │
                   ├──► ESP32-S3 (has internal 3.3V regulator)
                   │
                   └──► LED Strip WS2812B (5V)
```

**Power options:**

1. **Simple (recommended for prototype):**
   - Battery → ESP32 direct (accepts 3.7V on 5V pin)
   - LEDs at 3.7V (work, less bright)

2. **Boost to 5V (production):**
   - Battery → 5V Boost → ESP32 + LEDs
   - LEDs at full brightness
   - Boost example: MT3608

## 🎨 3D Physical Layout

### Component Placement

```
Cross-section view:

        ╔════════════════╗  ← Upper shell PETG transparent
        ║   LED Ring     ║  
     ┌──╫────────────────╫──┐
     │  ║  ┌──────────┐  ║  │
     │  ║  │          │  ║  │ ← LED group 2 (outer ring)
     │  ╠══╪══════════╪══╣  │
     │  ║  │  ESP32   │  ║  │
     │  ║  │   +      │  ║  │ ← LED group 1 (inner)
     │  ║  │  MG24    │  ║  │
     │  ╠══╪══════════╪══╣  │
     │  ║  │          │  ║  │ ← LED group 0 (core grills)
     │  ║  └──────────┘  ║  │
     │  ║                ║  │
     ├──╫────────────────╫──┤
     │  ║    Battery     ║  │
     │  ║                ║  │
     └──╨────────────────╨──┘
        ╚════════════════╝  ← Lower shell

        [●]  ← ON/OFF Switch
```

### Dimensional Constraints

- **Internal diameter:** ~60-80mm (verify with 3D model)
- **Component height:** max 15mm (ESP32+MG24 stack)
- **Battery space:** ~40x30x10mm
- **LED strip:** minimum bend radius 20mm

## ⚡ Power Consumption & Battery Life

### Consumption Analysis

**ESP32-S3:**
- Active (WiFi ON, LEDs ON): ~150-200mA
- Light sleep: ~3-5mA
- Deep sleep: ~10µA

**MG24:**
- Active (IMU polling): ~5-10mA
- Low power: ~50µA

**LEDs (32x WS2812B):**
- 1 LED @ 100%: ~60mA
- 32 LEDs @ 100%: ~1920mA (!)
- Typical (pulse effect, 50% avg): ~500-800mA

**Average total in use:** ~650-1000mA  
**Total deep sleep:** ~100µA

### Battery Life Estimate

With **500mAh** battery:
- Continuous use (animations): ~30-45 minutes
- Standby (core only): ~2-3 hours
- Deep sleep: ~200+ days

With **1000mAh** battery:
- Continuous use: ~1-1.5 hours
- Standby: ~4-6 hours
- Deep sleep: ~400+ days

**Recommendation:** 750-1000mAh battery to balance size/autonomy.

## 🛠️ Assembly Guide

### Step 1: Component Preparation

1. **Cut LED strip** to 32 LEDs
2. **Solder wires** to DIN, 5V, GND
3. **Prepare JST connectors** for modularity
4. **Test LED strip** with separate Arduino/ESP32

### Step 2: ESP32-MG24 Soldering

```
ESP32 GPIO7  ──────► MG24 D5
ESP32 GPIO8  ◄────── MG24 D4
ESP32 3V3    ──────► MG24 3V3
ESP32 GND    ──────► MG24 GND
```

**Tip:** Solder ESP32 and MG24 **back-to-back** to save space!

### Step 3: LED Connection

1. Solder **DIN** to ESP32 GPIO18 (330Ω resistor recommended)
2. **5V** and **GND** directly to battery (with switch)
3. 470µF capacitor between 5V-GND near LEDs

### Step 4: Functionality Test

```python
# Test code for ESP32
from machine import Pin
from neopixel import NeoPixel

np = NeoPixel(Pin(18), 32)
np.fill((0, 255, 30))  # Green
np.write()
```

### Step 5: Shell Mounting

1. **Position LEDs** following 3D model guide
2. **Secure ESP32+MG24** with M2 screws or hot glue
3. **Insert battery** and charging module
4. **Clean cable routing** and secure
5. **Mount switch** in dedicated hole

### Step 6: Final Closure & Test

1. **Close shell** with screws or clips
2. **Motion test** in all directions
3. **Verify waterproofing** (if required)
4. **Battery life test** with timer

## 🔍 Hardware Troubleshooting

### LEDs don't light up

- ✓ Verify 5V power (multimeter)
- ✓ Check DIN signal continuity
- ✓ Test with single LED
- ✓ Verify LED strip polarity

### ESP32 won't connect

- ✓ Stable 3.3-5V power
- ✓ Try reset button
- ✓ USB cable with data (not just power!)
- ✓ CP2102/CH340 drivers installed

### MG24 doesn't detect motion

- ✓ IMU LSM6DS3 initialized (serial monitor)
- ✓ Acceleration threshold (2.5G default)
- ✓ I2C connection working
- ✓ Stable 3.3V power

### Excessive consumption

- ✓ LED brightness too high
- ✓ WiFi always active (disable if standalone)
- ✓ IMU polling too frequent
- ✓ Deep sleep not activating

### WiFi interference

- ✓ LED strip can generate EMI noise
- ✓ Add 100nF capacitor near ESP32
- ✓ Physically separate LEDs from WiFi antenna
- ✓ Use less crowded WiFi channels

## 🔗 References

- [ESP32-S3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
- [WS2812B Datasheet](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf)
- [LSM6DS3 Datasheet](https://www.st.com/resource/en/datasheet/lsm6ds3.pdf)
- [XIAO MG24 Wiki](https://wiki.seeedstudio.com/xiao_mg24/)

---

**Last updated:** April 2026
