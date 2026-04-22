# 💻 Architettura Software - Metroid Morph Ball

Guida completa all'architettura software del progetto.

## 📊 Panoramica Architettura

```
┌─────────────────────────────────────────────┐
│           HOME ASSISTANT (opzionale)        │
│  ┌────────────────────────────────────┐    │
│  │  Dashboard Lovelace                │    │
│  │  - Controllo LED                   │    │
│  │  - Selezione effetti               │    │
│  │  - Config sleep                    │    │
│  └────────────────────────────────────┘    │
│                    │                        │
│                    │ WiFi / API             │
└────────────────────┼────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│              ESP32-S3 TINY                   │
│  ┌──────────────────────────────────────┐  │
│  │  VERSIONE A: MicroPython             │  │
│  │  - main.py (event loop, threads)     │  │
│  │  - ledstrip.py (WS2812B driver)      │  │
│  │  - animations/* (effects)            │  │
│  └──────────────────────────────────────┘  │
│               OR                            │
│  ┌──────────────────────────────────────┐  │
│  │  VERSIONE B: ESPHome                 │  │
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

## 🐍 Versione MicroPython

### Architettura Multi-Thread

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

**Responsabilità:**
- Setup iniziale GPIO
- Gestione interrupt motion sensor
- Coordinamento thread
- Sleep state machine

**Componenti chiave:**

```python
# State globals
active = True                    # Animazione attiva/standby
last_motion_time = ticks_ms()   # Timestamp ultimo movimento
anim_thread_started = False     # Flag thread animazione

# Hardware setup
alive_pin = Pin(ALIVE_PIN, Pin.OUT)
motion_pin = Pin(MOTION_PIN, Pin.IN)
leds = LEDStrip(LED_PIN, NUM_LEDS, GROUPS)

# ISR - Interrupt Service Routine
def motion_interrupt(pin):
    """
    Chiamata su RISING edge di motion_pin.
    Wake da standby se necessario.
    """
    global last_motion_time, active
    last_motion_time = time.ticks_ms()
    if not active:
        active = True
        start_animation_thread()

# Thread functions
def animation_loop():
    """Esegue animazioni LED in loop"""
    
def motion_monitor():
    """Monitora timeout e gestisce sleep"""
```

**State Machine:**

```
┌─────────┐  movimento   ┌────────────┐
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

**Classe principale:**

```python
class LEDStrip:
    def __init__(self, pin, num_leds, groups):
        self.np = NeoPixel(Pin(pin), num_leds)
        self.groups = groups
        self.num_leds = num_leds
    
    # Metodi per gruppi
    def set_group_color(self, group_id, color)
    def clear_group(self, group_id)
    
    # Animazioni base
    def pulse(self, duration=1)
    def fade_in(self, duration=1, group_id=None)
    def fade_out(self, duration=1, group_id=None)
    
    # Utility
    def clear()
    def show()
```

**Design pattern:**
- Astrazione gruppi LED (nasconde mapping fisico)
- Animazioni non-blocking (controllo durata via parametri)
- Thread-safe (importante per multi-threading)

### File: animations/

Directory con moduli animazioni:

**base.py** - Classe base astratta:
```python
class Animation:
    def __init__(self, ledstrip):
        self.ledstrip = ledstrip
    
    def run(self):
        """Override in subclass"""
        pass
```

**pulse.py** - Breathing effect:
```python
class PulseAnimation(Animation):
    def run(self, duration=1):
        # Fade in/out sinusoidale
```

**rotation.py** - Effetto rotazione:
```python
class RotationAnimation(Animation):
    def run(self, speed=50):
        # Shift circolare dei colori
```

**static.py** - Colori fissi:
```python
class StaticAnimation(Animation):
    def run(self, colors):
        # Set e hold
```

### Deep Sleep & Wake

```python
# Setup wake pin
esp32.wake_on_ext1(
    pins=(Pin(MOTION_PIN),), 
    level=esp32.WAKEUP_ANY_HIGH
)

# Entrare in deep sleep
machine.deepsleep()

# All'uscita dal deep sleep:
# - ESP32 fa RESET completo
# - main.py riparte da capo
# - Stato non persistente (RAM azzerata)
```

**Wake flow:**

```
MG24 rileva movimento
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
                             └─► Animazione avviata
```

## 🏠 Versione ESPHome

### Architettura Event-Driven

ESPHome usa un'architettura basata su **componenti** e **automazioni**.

```yaml
# Struttura concettuale

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

**Sezioni principali:**

#### 1. Configurazione Base

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
            // C++ code qui
```

**Lambda Effects - Dettaglio:**

```cpp
// Lambda effect con accesso diretto ai LED

it[index] = Color(R, G, B);

// Variabili static per stato persistente
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

# Entità esposte automaticamente:
# - light.morphball_light
# - select.morphball_effect
# - number.morphball_sleep_timeout
# - binary_sensor.morphball_motion
# - sensor.morphball_wifi_signal
```

### Component Lifecycle

```
Boot
 │
 ├─► on_boot actions
 │    └─► alive_pin.on()
 │         light.turn_on()
 │
 ├─► Setup loops
 │    └─► interval timers start
 │
 └─► Main loop
      │
      ├─► WiFi management
      ├─► API communication
      ├─► Component updates
      └─► Event handling
           │
           ├─► binary_sensor triggers
           ├─► light effect updates
           └─► interval callbacks
```

### OTA Updates

```yaml
ota:
  platform: esphome
  password: !secret ota_password

# Workflow:
# 1. esphome run morphball.yaml --device morphball.local
# 2. Compila nuovo firmware
# 3. Upload via WiFi (no cable!)
# 4. Auto-reboot
```

## 🤖 MG24 - Motion Detection

### File: mg24_imu.ino

**Architettura:**

```cpp
// Setup
void setup() {
    pinMode(PIN_ALIVE, INPUT);
    pinMode(PIN_MOTION_OUT, OUTPUT);
    IMU.begin();
}

// Loop
void loop() {
    // 1. Leggi stato ESP32
    check_alive_signal();
    
    // 2. Leggi IMU
    aX = IMU.readFloatAccelX();
    aY = IMU.readFloatAccelY();
    aZ = IMU.readFloatAccelZ();
    
    // 3. Calcola magnitude
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
// Somma delle accelerazioni assolute
float aSum = fabs(aX) + fabs(aY) + fabs(aZ);

// Threshold statico
const float threshold = 2.5;  // G

// Debouncing temporale
static unsigned long lastMove = 0;
if (millis() - lastMove > 200) {  // Min 200ms tra pulse
    digitalWrite(PIN_MOTION_OUT, HIGH);
    lastMove = millis();
}
```

**Possibili Miglioramenti:**

```cpp
// 1. Riconoscimento gesti
enum Gesture {
    SHAKE,      // Oscillazione rapida
    ROLL,       // Rotazione continua
    TILT,       // Inclinazione statica
    TAP,        // Colpo singolo
    DOUBLE_TAP  // Doppio colpo
};

// 2. Soglia adattativa
float adaptive_threshold = 
    baseline_noise * 1.5 + offset;

// 3. Comunicazione I2C/UART invece di GPIO
// Inviare tipo di gesto + intensità
```

## 🔄 Comunicazione Inter-MCU

### Protocollo GPIO Attuale

**Segnale ALIVE (ESP32 → MG24):**

```
HIGH (3.3V)
  │     ┌───────────────────────┐
  │     │  Animazioni attive    │
  │     │  MG24 polling normale │
  │     └───────────────────────┘
  │
  └─► LOW (0V)
        │  ESP32 in deep sleep
        │  MG24 può ridurre polling
        │  o andare in low power
        └───────────────────────┘
```

**Segnale MOTION (MG24 → ESP32):**

```
Movimento rilevato
  │
  ├─► Pulse HIGH (200ms)
  │    │
  │    └─► ESP32 wake (se in deep sleep)
  │         o reset timeout (se attivo)
  │
  └─► Return LOW
```

### Protocolli Alternativi (Future)

#### Opzione A: UART

```cpp
// MG24 invia
Serial.write('S');  // Shake
Serial.write('R');  // Roll
Serial.write('T');  // Tilt

// ESP32 riceve
char gesture = Serial.read();
switch(gesture) {
    case 'S': trigger_shake_effect(); break;
    // ...
}
```

#### Opzione B: I2C

```cpp
// MG24 come slave I2C
#define MG24_I2C_ADDR 0x42

// ESP32 read
Wire.requestFrom(MG24_I2C_ADDR, 2);
uint8_t gesture = Wire.read();
uint8_t intensity = Wire.read();
```

#### Opzione C: Multiple GPIO

```cpp
// 3 GPIO per 8 combinazioni
GPIO_BIT0 = shake_detected;
GPIO_BIT1 = roll_detected;
GPIO_BIT2 = tap_detected;

// ESP32 read as 3-bit value
uint8_t gesture = (bit2 << 2) | (bit1 << 1) | bit0;
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
Config embedded: ~10KB
Runtime: ~150KB
OTA partition: ~2MB
```

### Ottimizzazioni

#### LED Performance

```python
# ❌ Lento - aggiorna ogni LED
for i in range(32):
    np[i] = color
    np.write()  # 32 write() calls!

# ✅ Veloce - batch update
for i in range(32):
    np[i] = color
np.write()  # 1 write() call
```

#### Sleep Aggressiveness

```python
# Risparmio energia - riduci polling

# ❌ CPU busy
while True:
    check_something()
    # No delay!

# ✅ CPU sleep tra check
while True:
    check_something()
    time.sleep_ms(100)  # 90% CPU idle
```

## 🧪 Testing & Debug

### MicroPython REPL

```python
# Connetti via USB
screen /dev/ttyUSB0 115200

# Test interattivo
>>> from ledstrip import LEDStrip
>>> leds = LEDStrip(18, 32, GROUPS)
>>> leds.set_group_color(0, (255, 0, 0))
>>> leds.show()
```

### ESPHome Logs

```bash
# Monitor live
esphome logs morphball.yaml

# Log levels
logger:
  level: DEBUG  # VERBOSE, DEBUG, INFO, WARN, ERROR
  
# Custom log
ESP_LOGD("tag", "Motion: %d", value);
```

### Debug GPIO

```python
# Oscilloscopio software
from machine import Pin, time_pulse_us

pin = Pin(8, Pin.IN)
duration = time_pulse_us(pin, 1)  # Misura HIGH pulse
print(f"Pulse: {duration}µs")
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
# Chiamabile da HA automations

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

## 🔗 Riferimenti Esterni

- [MicroPython Docs](https://docs.micropython.org/)
- [ESPHome Docs](https://esphome.io/)
- [NeoPixel Guide](https://learn.adafruit.com/adafruit-neopixel-uberguide)
- [ESP32-S3 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf)

---

## 📋 BACKLOG — Lavoro UART da Fare

Questa sezione traccia il lavoro pianificato per sostituire il protocollo GPIO binario (MOTION/ALIVE) con una comunicazione UART strutturata su **MG24 D6 (TX) / D7 (RX)** ↔ **ESP32 Serial1**.

---

### [ ] 1. Definire il protocollo messaggi strutturati MG24 → ESP32

Il protocollo deve essere leggero (adatto a 115200 baud, nessun allocator dinamico sul MG24) e facilmente decodificabile in MicroPython.

**Formato proposto — frame binario fisso 4 byte:**

```
┌────────┬────────┬────────┬────────┐
│  0xAA  │  TYPE  │ INTENS │  0x55  │
│ (sync) │ (gesto)│ (0-255)│ (end)  │
└────────┴────────┴────────┴────────┘
```

| Campo    | Valore         | Descrizione                              |
|----------|----------------|------------------------------------------|
| `0xAA`   | sync byte      | Marker di inizio frame                   |
| `TYPE`   | enum 1 byte    | Tipo movimento (vedi tabella sotto)      |
| `INTENS` | 0–255          | Intensità normalizzata (0 = minimo, 255 = massimo) |
| `0x55`   | end byte       | Marker di fine frame (sanity check)      |

**Tipi di movimento (`TYPE`):**

| Valore | Nome          | Trigger                                     |
|--------|---------------|---------------------------------------------|
| `0x01` | `MOTION`      | Movimento generico (rimpiazza GPIO pulse)   |
| `0x02` | `SHAKE`       | Oscillazione rapida su ≥2 assi             |
| `0x03` | `ROLL`        | Rotazione continua (aSum > soglia per >500ms) |
| `0x04` | `TAP`         | Picco singolo breve (< 100ms)              |
| `0x05` | `DOUBLE_TAP`  | Due picchi entro 300ms                     |
| `0x06` | `TILT`        | Inclinazione statica (asse Z fuori range)  |
| `0xFF` | `HEARTBEAT`   | Keep-alive ogni 2s (nessun movimento)      |

---

### [ ] 2. Encoder lato Arduino (MG24 — `mg24_imu.ino`)

Modifiche al loop Arduino per inviare frame UART invece di (o in aggiunta a) il pulse GPIO:

```cpp
// Aggiungi a mg24_imu.ino

#define UART_BAUD   115200
#define FRAME_SYNC  0xAA
#define FRAME_END   0x55

// Enum tipi gesto
enum GestureType : uint8_t {
  MOTION     = 0x01,
  SHAKE      = 0x02,
  ROLL       = 0x03,
  TAP        = 0x04,
  DOUBLE_TAP = 0x05,
  TILT       = 0x06,
  HEARTBEAT  = 0xFF,
};

void sendGestureFrame(GestureType type, uint8_t intensity) {
  Serial1.write(FRAME_SYNC);
  Serial1.write((uint8_t)type);
  Serial1.write(intensity);
  Serial1.write(FRAME_END);
}

// Nel setup():
//   Serial1.begin(UART_BAUD);  // D6=TX, D7=RX

// Nel loop(), sostituire il pulse GPIO con:
//   uint8_t intensity = (uint8_t)constrain(map(aSum * 100, 0, 500, 0, 255), 0, 255);
//   sendGestureFrame(MOTION, intensity);
//   (mantenere anche il GPIO D4 per compatibilità con deep-sleep wake)

// Heartbeat separato ogni 2s:
//   static unsigned long lastHeartbeat = 0;
//   if (millis() - lastHeartbeat > 2000) {
//     sendGestureFrame(HEARTBEAT, 0);
//     lastHeartbeat = millis();
//   }
```

**Note implementative:**
- `Serial1` su XIAO MG24 usa fisicamente `D6` (TX) e `D7` (RX) — verificare pinout con `Serial1.begin()` nella libreria Seeed
- Mantenere il pulse su `D4` (GPIO) per continuare a fare wake dall'ESP32 deep sleep (il UART non può wakeup da deep sleep senza hardware UART wakeup)
- `intensity` = `aSum` scalata su 0–255 (`map(aSum, 0, 5.0, 0, 255)`)

---

### [ ] 3. Decoder lato MicroPython (ESP32 — `ESP32/main.py`)

Aggiungere un thread o ISR che legge i frame UART e aggiorna lo stato delle animazioni:

```python
# Aggiungere in main.py o in un nuovo file uart_receiver.py

from machine import UART
import struct

UART_BAUD     = 115200
FRAME_SYNC    = 0xAA
FRAME_END     = 0x55
FRAME_LEN     = 4

GESTURE_NAMES = {
    0x01: "MOTION",
    0x02: "SHAKE",
    0x03: "ROLL",
    0x04: "TAP",
    0x05: "DOUBLE_TAP",
    0x06: "TILT",
    0xFF: "HEARTBEAT",
}

# Inizializzazione (scegliere i pin UART corretti per ESP32-S3 Tiny)
uart = UART(1, baudrate=UART_BAUD, tx=PIN_UART_TX, rx=PIN_UART_RX)

def read_gesture_frame():
    """
    Legge un frame da 4 byte. Ritorna (gesture_type, intensity) o None.
    Cerca il sync byte 0xAA per risincronizzarsi in caso di rumore.
    """
    while uart.any():
        b = uart.read(1)[0]
        if b != FRAME_SYNC:
            continue
        rest = uart.read(3)
        if len(rest) < 3 or rest[2] != FRAME_END:
            continue
        return rest[0], rest[1]   # (type, intensity)
    return None

def uart_monitor_loop():
    """Thread che processa i frame UART e aggiorna lo stato globale."""
    global last_motion_time, active, current_gesture
    while True:
        frame = read_gesture_frame()
        if frame:
            gesture_type, intensity = frame
            if gesture_type != 0xFF:   # ignora heartbeat
                last_motion_time = time.ticks_ms()
                current_gesture = gesture_type
                # TODO: mappare tipo gesto → animazione specifica
                #   0x02 SHAKE  → effetto "esplosione" rapido
                #   0x03 ROLL   → effetto rotazione
                #   0x04 TAP    → flash singolo
        time.sleep_ms(10)
```

**Note implementative:**
- Identificare i pin UART1 fisici sull'ESP32-S3 Tiny (controllare lo schema della board)
- Il frame sync `0xAA` + end `0x55` permette di risincronizzarsi senza buffer circolare complesso
- Il `HEARTBEAT` serve a rilevare se il MG24 si è bloccato (assenza per >5s = errore)
- Fase successiva: mappare `current_gesture` a effetti animazione diversi in `animations/`

---

### [ ] 4. Mapping gesti → animazioni (fase successiva)

Dopo aver validato il canale UART, collegare i tipi di gesto alle animazioni:

| Gesto         | Animazione LED suggerita                          |
|---------------|---------------------------------------------------|
| `MOTION`      | Comportamento attuale (pulse verde)               |
| `SHAKE`       | Flash bianco rapido + burst intensità             |
| `ROLL`        | `RotationAnimation` con velocità proporzionale a `intensity` |
| `TAP`         | Singolo flash del gruppo core (group 0)           |
| `DOUBLE_TAP`  | Cambio effetto ciclico                            |
| `TILT`        | Colore base cambia (verde → ciano → blu) in base all'asse |

---

**Ultimo aggiornamento:** Aprile 2026