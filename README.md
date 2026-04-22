# 🔮 Metroid Morph Ball

3D printed Metroid Morph Ball action figure with LED animations controlled by ESP32 and IMU motion sensor.

![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-ESP32--S3-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

[🇮🇹 Versione Italiana](README.md) | 🇬🇧 English Version

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware](#hardware)
- [Software](#software)
- [Installation](#installation)
- [Usage](#usage)
- [Future Development](#future-development)
- [Contributing](#contributing)
- [License](#license)

## 🎮 Overview

This project recreates the legendary **Morph Ball** from the Metroid series as an interactive 3D printed action figure. The sphere illuminates with 32 programmable WS2812B LEDs and responds to movement thanks to an IMU sensor, automatically entering deep sleep when stationary to save battery.

### Two Available Versions

The project offers two complete implementations:

1. **MicroPython** (`/ESP32` + `/MG24`) - Original standalone version
2. **ESPHome** (`/ESPHome`) - Full Home Assistant integration

## ✨ Features

- 🎨 **32 RGB WS2812B LEDs** with customizable animations
- 🏃 **Motion detection** via LSM6DS3 accelerometer
- 💤 **Automatic deep sleep** for energy saving
- 🔋 **Wake on movement** for instant activation
- 🏠 **Home Assistant integration** (ESPHome version)
- 📱 **WiFi control** with effect selection and configuration
- 🎯 **Custom LED groups** that reproduce the Metroid aesthetic
- ⚡ **Dual-MCU architecture** (ESP32-S3 + MG24) for optimized power consumption

## 🔧 Hardware

### Why Dual-MCU Architecture?

This project uses **two microcontrollers** instead of one for strategic reasons:

1. **🔋 Optimized Power Management**
   - MG24 runs in ultra-low power mode continuously monitoring the IMU
   - ESP32 can deep sleep (~10µA) while MG24 acts as motion "sentinel"
   - Wake-on-motion with minimal latency and maximum battery life

2. **📡 ESP32-S3 Tiny Has No Integrated IMU**
   - The compact ESP32-S3 Tiny form factor doesn't include motion sensors
   - XIAO MG24 has LSM6DS3 accelerometer already integrated on-board
   - No need for external IMU breakout boards and extra wiring

3. **⚡ Task Separation & Real-Time Performance**
   - **MG24**: Dedicated to real-time IMU polling (20Hz) and motion detection
   - **ESP32**: Handles LED animations, WiFi, Home Assistant integration
   - No resource contention - each MCU does what it does best

4. **🎯 Continuous Monitoring Without Impact**
   - MG24 polls IMU continuously at 20Hz without affecting ESP32 performance
   - LED animations run smoothly on ESP32 without IMU polling overhead
   - Clean separation of concerns in the codebase

**Alternative single-MCU approach drawbacks:**
- ❌ ESP32 polling IMU = high power consumption (no true deep sleep)
- ❌ Wake-on-timer = high latency (100-500ms) and still wastes power
- ❌ External IMU module = more complex wiring, larger footprint

**Dual-MCU benefits:**
- ✅ Best-in-class power efficiency (~100µA average in standby)
- ✅ Instant wake on motion (<50ms latency)
- ✅ Modular architecture (can upgrade/swap MCUs independently)
- ✅ Both MCUs in same XIAO form factor (stack back-to-back)

### Main Components

| Component | Model | Quantity | Est. Price | Link/Notes |
|-----------|-------|----------|------------|------------|
| **ESP32-S3 Tiny** | Dual-core, WiFi, BLE | 1 | €8-12 | Ideal small form factor |
| **Seeed XIAO MG24** | ARM Cortex-M33, integrated LSM6DS3 | 1 | €10-15 | Includes on-board IMU |
| **LED Strip WS2812B** | 5V, IP30, 60 LED/m | 32 LED (~53cm) | €5-8 | Cuttable every LED |
| **LiPo Battery** | 3.7V, 500-1000mAh | 1 | €8-12 | Size TBD |
| **Charging Module** | TP4056 or similar | 1 | €2-3 | With protection |
| **ON/OFF Switch** | Slide switch 3 pin | 1 | €0.50 | Miniature |
| **JST Connectors** | 2.54mm pitch | Various | €2-3 | For modular connections |
| **Wires** | AWG 22-26, silicone | 1m | €2-3 | Red/Black/Data |
| **Heat shrink** | Heat shrink tubing | 10cm | €1 | Various sizes |

### Connection Diagram

```
ESP32-S3 Tiny          MG24 (XIAO)         LED Strip
┌─────────────┐       ┌──────────┐        ┌─────────┐
│             │       │          │        │         │
│ GPIO18 ─────┼───────┼──────────┼────────┤ DIN     │
│             │       │          │        │         │
│ GPIO8  ◄────┼───────┤ D4 (OUT) │        │         │
│ (MOTION IN) │       │          │        │         │
│             │       │          │        │         │
│ GPIO7  ─────┼───────► D5 (IN)  │        │         │
│ (ALIVE OUT) │       │ LSM6DS3  │        │         │
│             │       │   IMU    │        │         │
│ 3V3    ─────┼───────┤ 3V3      │        │         │
│ GND    ─────┼───────┤ GND      ├────────┤ GND     │
│             │       │          │        │         │
└─────────────┘       └──────────┘        │ +5V ◄───┤ Battery
                                          └─────────┘
```

### Pin Details

**ESP32-S3 Tiny:**
- `GPIO18`: DIN of WS2812B LED strip
- `GPIO8`: Input from MG24 (HIGH when motion detected)
- `GPIO7`: Output to MG24 (HIGH when animations active)

**MG24 (XIAO):**
- `D4`: Output to ESP32 (pulse on movement)
- `D5`: Input from ESP32 (animation status)
- `D6`: Serial1 TX → ESP32 RX (future UART, structured IMU messages)
- `D7`: Serial1 RX ← ESP32 TX (future UART, configuration commands)
- `D11/D12`: SAMD11 debug bridge — **DO NOT TOUCH**
- `SDA/SCL`: I2C for LSM6DS3 (internal)

### LED Layout

The 32 LEDs are organized in 3 groups to recreate the Metroid aesthetic:

- **Group 0** (6 LEDs): Core grills - Aqua green `(0, 230, 100)`
  - Positions: `[0, 19, 20, 25, 26, 31]`
  
- **Group 1** (12 LEDs): Inner ring - Bright green `(0, 255, 30)`
  - Positions: `[1, 2, 17, 18, 21, 22, 23, 24, 27, 28, 29, 30]`
  
- **Group 2** (14 LEDs): Outer ring - Bright green `(0, 255, 30)`
  - Positions: `[3-16]`

## 💾 Software

### Repository Structure

```
morphball/
├── 3D model/                # 3D printable model
│   └── MorphBall.3mf
├── ESP32/                   # MicroPython standalone version
│   ├── main.py             # Entry point
│   ├── ledstrip.py         # LED management
│   └── animations/         # LED effects
│       ├── base.py
│       ├── pulse.py
│       ├── rotation.py
│       └── static.py
├── MG24/                    # Motion sensor code
│   └── mg24_imu.ino        # Arduino sketch for IMU
├── ESPHome/                 # Home Assistant version
│   ├── morphball.yaml      # ESPHome config
│   ├── README.md           # Setup guide
│   ├── lovelace-card.yaml  # HA Dashboard
│   └── secrets.yaml.example
└── docs/                    # Documentation
    ├── en/                  # English docs
    └── [IT docs]            # Italian docs
```

### MicroPython Version

**Features:**
- Standalone, doesn't require WiFi connection
- Automatic pulse animation
- Sleep after 20 seconds of inactivity
- Deep sleep after additional 20 seconds in standby

**Main files:**
- `main.py`: Main loop, thread management, sleep management
- `ledstrip.py`: Class for WS2812B control with groups
- `animations/`: Modules with different LED effects

### ESPHome Version

**Features:**
- Native Home Assistant integration
- 11 selectable LED effects
- Timeout configuration via dashboard
- OTA updates
- Complete diagnostics (WiFi, uptime, IP)

**Advantages:**
- No mobile app needed
- Configuration via web interface
- HA automations available
- Synchronization with other devices

See [ESPHome/README.md](ESPHome/README.md) for complete details.

## 🚀 Installation

### Software Requirements

**For MicroPython version:**
- Python 3.7+
- `esptool` for flashing
- `mpremote` or `ampy` for file upload

**For ESPHome version:**
- ESPHome CLI or Home Assistant addon
- Home Assistant (obviously!)

### MicroPython Version Setup

1. **Flash MicroPython on ESP32-S3:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 esp32s3-micropython.bin
```

2. **Upload code:**
```bash
cd ESP32
mpremote connect /dev/ttyUSB0 cp -r . :
```

3. **Flash MG24:**
```bash
# Use Arduino IDE
# Board: Seeed XIAO MG24
# Upload: MG24/mg24_imu.ino
```

### ESPHome Version Setup

See complete documentation in [ESPHome/README.md](ESPHome/README.md)

**Quick start:**
```bash
cd ESPHome
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml with your credentials
esphome run morphball.yaml
```

## 🎯 Usage

### MicroPython Version

The Morph Ball activates automatically:
1. **Motion detected** → LEDs turn on with pulse effect
2. **20s of inactivity** → Enters standby (only core grills lit)
3. **Another 20s stationary** → Complete deep sleep
4. **New movement** → Automatic wake and reactivation

### ESPHome Version

**Home Assistant Dashboard:**
1. Turn LEDs on/off
2. Select effect from dropdown
3. Adjust sleep timeout with slider
4. Enable/disable deep sleep mode
5. Monitor motion status and diagnostics

**Example automations:**

```yaml
# Activate Rainbow at sunset
automation:
  - alias: "Morphball Rainbow Sunset"
    trigger:
      platform: sun
      event: sunset
    action:
      - service: select.select_option
        target:
          entity_id: select.metroid_morph_ball_effect
        data:
          option: "Rainbow"
```

## 🔮 Future Development

### Roadmap

- [ ] **Gesture recognition** - Shake, roll, tilt trigger different effects
- [ ] **Battery monitoring** - Charge level indicator
- [ ] **Game mode** - Interactive mini-games
- [ ] **Multi-ball sync** - Multiple Morph Balls communicating
- [ ] **Audio feedback** - Speaker for Metroid sounds
- [ ] **Charging dock** - Wireless charging base
- [ ] **Mobile app** - For standalone MicroPython version
- [ ] **Audio-reactive effects** - Music synchronization

### Contribution Ideas

- New LED animations
- Power consumption optimization
- 3D model improvements
- Porting to other microcontrollers
- Integration with other smart home systems (Alexa, Google Home)

## 🤝 Contributing

Contributions welcome! Here's how:

1. **Fork** the repository
2. Create a **branch** for your feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

### Guidelines

- Comment code (English preferred for international collaboration)
- Test changes before committing
- Update documentation if necessary
- Follow existing code style

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is released under **GPL-3.0 License**. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Nintendo/Retro Studios** for Metroid inspiration
- **ESPHome Community** for the fantastic framework
- **Home Assistant** for the home automation platform
- **Seeed Studio** for XIAO MG24
- All contributors who will improve this project!

## 📞 Contact

**Gualtiero Saderis** - [@wizwally](https://github.com/wizwally)

Project Link: [https://github.com/wizwally/morphball](https://github.com/wizwally/morphball)

---

## 📚 Documentation

- **English:**
  - [Hardware Guide](docs/en/HARDWARE.md)
  - [Software Architecture](docs/en/SOFTWARE.md)
  - [Build Tutorial](docs/en/TUTORIAL.md)
  - [Contributing Guide](docs/en/CONTRIBUTING.md)

- **Italiano:**
  - [Guida Hardware](docs/HARDWARE.md)
  - [Architettura Software](docs/SOFTWARE.md)
  - [Tutorial Completo](docs/TUTORIAL.md)
  - [Come Contribuire](CONTRIBUTING.md)

---

**Made with ❤️ and nostalgia for Nintendo classics**
