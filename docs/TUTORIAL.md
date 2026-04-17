# 🛠️ Tutorial Completo - Build Your Morph Ball

Guida passo-passo dalla stampa 3D al primo avvio.

## 📋 Prerequisiti

### Cosa Ti Serve

**Hardware:**
- [ ] Stampante 3D (volume min: 150x150x150mm)
- [ ] Saldatore + stagno
- [ ] Multimetro
- [ ] Pinze, tronchesine
- [ ] Cacciaviti precisione
- [ ] Hot glue gun (opzionale)

**Software:**
- [ ] Slicer 3D (PrusaSlicer / Cura)
- [ ] Python 3.7+ (per MicroPython) o ESPHome
- [ ] Arduino IDE (per MG24)
- [ ] Driver USB-Serial (CP2102/CH340)
- [ ] Git (per clonare repo)

**Skill Level:**
- 🟢 Stampa 3D: Beginner
- 🟡 Elettronica: Intermediate
- 🟡 Programmazione: Intermediate
- 🟢 Assembly: Beginner

## 📦 Fase 1: Preparazione

### 1.1 Ordinare i Componenti

Segui la [BOM completa](HARDWARE.md#bill-of-materials-bom) e ordina tutto.

**Store consigliati:**
- **AliExpress**: ESP32-S3, MG24, LED strip, batterie
- **Amazon**: Cavi, connettori, tools
- **LCSC/DigiKey**: Componenti specifici (condensatori, etc.)

**Tempo:** 1-3 settimane per spedizioni

### 1.2 Clonare il Repository

```bash
git clone https://github.com/wizwally/morphball.git
cd morphball
```

### 1.3 Studiare la Documentazione

Leggi:
- [ ] [HARDWARE.md](HARDWARE.md) - Schema circuitale
- [ ] [SOFTWARE.md](SOFTWARE.md) - Architettura software
- [ ] [ESPHome/README.md](../ESPHome/README.md) - Se usi ESPHome

## 🖨️ Fase 2: Stampa 3D

### 2.1 Preparazione Modello

```bash
# Apri il modello 3D
cd "3D model"
# Importa MorphBall.3mf nel tuo slicer
```

### 2.2 Settings Stampa

**Materiale Consigliato:** PETG trasparente

**Profile:**
```
Layer Height: 0.2mm
Wall Thickness: 1.2mm (3 perimetri)
Infill: 15-20% (Gyroid)
Supports: SI (generare automaticamente)
Brim/Raft: NO (se bed leveling ok)
Temperature: 240°C (PETG)
Bed Temp: 80°C
Speed: 50mm/s
Retraction: 2mm @ 40mm/s
```

**Note importanti:**
- 🔴 **Supporti essenziali** per LED mounting holes
- 🟡 **Prima layer critica** - verifica adesione
- 🟢 **Z-seam**: posiziona sul retro per estetica

### 2.3 Post-Processing

```bash
# Dopo stampa:
1. Rimuovi supporti con cura (pinze)
2. Sbavatura con cutter
3. Leviga superfici con carta vetro 400-800
4. (Opzionale) Acetone vapor per smoothing PETG
```

**Tempo stampa:** 8-12 ore (dipende da dimensioni)

## 🔌 Fase 3: Elettronica

### 3.1 Test Componenti Individuali

Prima di saldare, **testa tutto separatamente!**

#### Test ESP32-S3

```bash
# Installa esptool
pip install esptool

# Test connessione
esptool.py --port /dev/ttyUSB0 chip_id

# Output atteso:
# Chip is ESP32-S3 (revision X)
```

#### Test LED Strip

```python
# Test con Arduino/ESP32 base
#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel strip(32, 18, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();
}

void loop() {
  strip.fill(strip.Color(0, 255, 30));  // Verde
  strip.show();
  delay(1000);
}
```

✅ Tutti i 32 LED devono accendersi verde

#### Test MG24 IMU

```cpp
// Sketch di test LSM6DS3
#include <LSM6DS3.h>
#include <Wire.h>

LSM6DS3 IMU(I2C_MODE, 0x6A);

void setup() {
  Serial.begin(115200);
  IMU.begin();
}

void loop() {
  float aX = IMU.readFloatAccelX();
  Serial.print("X: "); Serial.println(aX);
  delay(100);
}
```

✅ Valori X ~0.0 fermo, cambiano se muovi la board

### 3.2 Saldature

**⚠️ IMPORTANTE: Testa TUTTO prima di saldare definitivamente!**

#### Ordine Saldature

1. **ESP32 ↔ MG24 Stack**

```
           MG24 (sopra)
            ║ ║ ║ ║
      ┌─────╨─╨─╨─╨──────┐
      │ D5 D4 3V3 GND     │
      │                   │
      │                   │
      └─────┬─┬─┬─┬───────┘
            ║ ║ ║ ║
       ESP32 (sotto)
```

Salda:
- MG24 D5 → ESP32 GPIO7
- MG24 D4 → ESP32 GPIO8  
- MG24 3V3 → ESP32 3V3
- MG24 GND → ESP32 GND

**Tecnica:**
- Fili corti (<3cm)
- 28-30 AWG silicone
- Colori: Rosso=3V3, Nero=GND, Giallo=D5, Verde=D4

2. **LED Strip → ESP32**

```
LED Strip          ESP32
DIN  ─────────────► GPIO18 (+ R 330Ω opzionale)
5V   ─────────────► 5V (o batteria+)
GND  ─────────────► GND
```

3. **Batteria + Circuito Alimentazione**

```
Batteria 3.7V LiPo
    ├─ (+) ─► Switch ─► TP4056 IN+ ─► 5V (LED + ESP32)
    └─ (-) ─────────────► TP4056 IN- ─► GND
                              │
                          USB charging
```

**⚠️ Attenzione Polarità!**
- Rosso = +
- Nero = -
- Inversione = 💥 componenti fritti

### 3.3 Isolamento

```
Dopo saldature:
1. Heat shrink su TUTTE le giunzioni
2. Verifica NO corti con multimetro
3. Test continuità con beeper
4. Hot glue su punti critici (anti-stress)
```

### 3.4 Test Assembly Elettronico

**Prima di chiudere nel guscio:**

```bash
# Power up test
1. Collega batteria
2. Accendi switch
3. Verifica:
   ✓ ESP32 LED status lampeggia
   ✓ MG24 LED (se presente) acceso
   ✓ LED strip verde (animazione base)
   ✓ NO fumo! 😅

# Motion test
4. Muovi delicatamente
5. Verifica:
   ✓ LED reagiscono (o serial monitor mostra "Motion")
   ✓ Animazioni continuano
```

## 💻 Fase 4: Software

### Opzione A: MicroPython (Standalone)

#### 4.1 Flash MicroPython

```bash
# Download firmware
wget https://micropython.org/download/esp32s3/

# Flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash

esptool.py --chip esp32s3 --port /dev/ttyUSB0 \
  write_flash -z 0x0 esp32s3-20231005-v1.21.0.bin
```

#### 4.2 Upload Code

```bash
# Installa mpremote
pip install mpremote

# Upload files
cd ESP32
mpremote connect /dev/ttyUSB0 cp main.py :
mpremote connect /dev/ttyUSB0 cp ledstrip.py :
mpremote connect /dev/ttyUSB0 cp -r animations :
```

#### 4.3 Test

```bash
# REPL
mpremote connect /dev/ttyUSB0

>>> import main
# LED dovrebbero accendersi!
```

#### 4.4 Flash MG24

```bash
# Arduino IDE
1. Installa board: Seeed XIAO SAMD
2. Apri: MG24/mg24_imu.ino
3. Seleziona: Tools > Board > XIAO MG24
4. Seleziona: Tools > Port > /dev/ttyUSB1
5. Upload (Ctrl+U)

# Verifica serial monitor:
✅ IMU pronta — lettura accelerazioni
```

### Opzione B: ESPHome (Home Assistant)

#### 4.1 Setup ESPHome

```bash
# Installa
pip install esphome

# O usa HA addon
```

#### 4.2 Config Secrets

```bash
cd ESPHome
cp secrets.yaml.example secrets.yaml
nano secrets.yaml

# Compila:
wifi_ssid: "TuoWiFi"
wifi_password: "TuaPassword"
api_key: "<genera con: openssl rand -base64 32>"
```

#### 4.3 Compile & Flash

```bash
# Prima volta (via USB)
esphome run morphball.yaml

# Seleziona la porta seriale
# Attendi compilazione (~5 min prima volta)
# Flash automatico
```

#### 4.4 Aggiungi a Home Assistant

```
1. Impostazioni > Dispositivi e servizi
2. ESPHome > Configura
3. Host: morphball.local
4. Encryption key: <dalla secrets.yaml>
5. Fatto! 🎉
```

#### 4.5 Lovelace Card

```bash
# Copia card config
cat lovelace-card-simple.yaml

# Incolla in:
# Dashboard > Edit > Add Card > Manual
```

## 🔧 Fase 5: Assembly Finale

### 5.1 Preparazione Guscio

```bash
1. Pulisci interno con alcool isopropilico
2. Rimuovi polvere da stampa
3. Test fit componenti (NO glue ancora!)
4. Segna posizioni LED con marker
```

### 5.2 Installazione LED

```
LED Strip 32 LED disposizione:

    Top view (schematico)
    
      0           19
        1  [ESP]  18
    31    2    17   20
          3  16
    26  ...    ... 21
          14 4
    25    13   5   22
        12     6
      11       7  23
        10   8
           9       24
```

**Procedura:**
1. Taglia strip a misura (conserva connettori!)
2. Curva delicatamente (raggio min 2cm)
3. Fissa con hot glue ogni 8-10 LED
4. Routing DIN cable pulito verso ESP32

### 5.3 Montaggio Elettronica

```
Layout interno (sezione):

[Guscio superiore]
    │
    ├─ LED ring (incollati)
    │
[Shelf 3D print]
    │
    ├─ ESP32 + MG24 stack (viti M2)
    │
    ├─ Switch (snap fit o glue)
    │
[Shelf inferiore]
    │
    └─ Batteria (velcro o foam double-side)
```

**Ordine montaggio:**
1. LED strip (già fatto)
2. ESP32+MG24 stack con viti M2
3. Routing cavi (usa cable ties mini)
4. Switch nel foro dedicato
5. Batteria nell'alloggiamento
6. Verifica tutto si muove senza tirare cavi

### 5.4 Test Pre-Chiusura

```bash
✓ Power on
✓ LED check (tutti i 32)
✓ Motion test (muovi la ball)
✓ Serial monitor OK
✓ WiFi connect (se ESPHome)
✓ Home Assistant entity visible
```

### 5.5 Chiusura Finale

```
1. Allinea guscio superiore + inferiore
2. Viti M2 x 4-6 nei fori previsti
   
   ┌─────────────┐
   │      ●      │  ← Vite
   │   ┌───┐    │
   │ ● │   │ ●  │
   │   └───┘    │
   │      ●      │
   └─────────────┘

3. Serraggio graduale (no overtightening!)
4. Test finale rotazione/shake
5. Se tutto OK: applica O-ring (opzionale)
```

## 🎮 Fase 6: Testing & Calibrazione

### 6.1 Test Movimento

```bash
Test checklist:

□ Shake delicato → LED reagiscono
□ Roll continuo → Animazioni fluide
□ Fermo 20s → Standby (core only)
□ Fermo 40s → Deep sleep (tutto off)
□ Nuovo shake → Wake immediato
□ Nessun rumore meccanico interno
```

### 6.2 Calibrazione IMU

Se motion detection troppo sensibile/insensibile:

```cpp
// MG24/mg24_imu.ino

// Modifica questa linea:
const float accelerationThreshold = 2.5;  // Default

// Valori tipici:
// 1.5 = Molto sensibile (anche respiro)
// 2.5 = Medio (default)
// 4.0 = Poco sensibile (serve shake deciso)
```

Re-upload e testa!

### 6.3 Tuning Animazioni

**MicroPython:**

```python
# ESP32/main.py

# Timeout sleep
SLEEP_TIMEOUT_MS = 20_000   # Aumenta se troppo veloce
STANDBY_WAIT_MS  = 20_000   # Idem

# Colori gruppi
leds.set_group_color(0, (R, G, B))  # Modifica colori
```

**ESPHome:**

```yaml
# ESPHome/morphball.yaml

# Timeout via HA dashboard (dinamico!)
number:
  - platform: template
    name: "Sleep Timeout"
    initial_value: 20  # Secondi
```

### 6.4 Test Autonomia

```bash
Batteria test (750mAh esempio):

1. Carica completa (LED TP4056 verde)
2. Uso normale (shake ogni ~30s)
3. Monitor tempo fino a spegnimento

Autonomia attesa: ~45-90 minuti

Se troppo breve:
- ✓ Verifica brightness LED (riduci a 50-70%)
- ✓ Controlla consumi parassiti (multimetro)
- ✓ Batteria più grande (1000mAh+)
```

## 🎨 Fase 7: Customizzazione

### 7.1 Effetti LED Custom

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

**MicroPython:**

```python
# ESP32/animations/rainbow.py
class RainbowAnimation(Animation):
    def run(self, speed=10):
        for hue in range(360):
            rgb = hsv_to_rgb(hue / 360.0, 1.0, 1.0)
            self.ledstrip.np.fill(rgb)
            self.ledstrip.show()
            time.sleep_ms(speed)
```

### 7.2 Automazioni HA

```yaml
# configuration.yaml o automations.yaml

automation:
  # Al tramonto → Rainbow
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

  # Su notifica → Strobe rosso
  - alias: "Morphball Alert Flash"
    trigger:
      platform: state
      entity_id: binary_sensor.front_door
      to: 'on'
    action:
      - service: light.turn_on
        target:
          entity_id: light.metroid_morph_ball_leds
        data:
          rgb_color: [255, 0, 0]
          effect: "Strobe"
```

### 7.3 Voice Control

**Google Assistant:**

```yaml
# Esponi entità in HA
google_assistant:
  entity_config:
    light.metroid_morph_ball_leds:
      name: "Morph Ball"
      room: Living Room

# Comandi vocali:
"Ok Google, accendi Morph Ball"
"Ok Google, imposta Morph Ball su verde"
"Ok Google, Morph Ball effetto rainbow"
```

## 🐛 Troubleshooting Common Issues

### Issue: LED non si accendono

**Debug:**
```bash
1. Verifica alimentazione: 
   multimetro su 5V rail → deve essere ~5V

2. Verifica DIN signal:
   oscilloscopio/logic analyzer → deve esserci data

3. Test singolo LED:
   scollega strip, prova con 1 LED solo

4. Verifica library:
   MicroPython: from neopixel import NeoPixel
   ESPHome: platform: neopixelbus
```

**Fix comuni:**
- ❌ DIN disconnesso → risalda
- ❌ 5V troppo basso (<4.5V) → batteria scarica o regolatore fail
- ❌ LED strip invertito → DIN va sul primo LED del strip!
- ❌ DOUT del primo LED rotto → salta primo LED, usa il secondo

### Issue: Motion non rilevato

**Debug:**
```cpp
// MG24 serial monitor
void loop() {
  float aSum = fabs(aX) + fabs(aY) + fabs(aZ);
  Serial.print("Accel: "); Serial.println(aSum);
  // Deve cambiare quando muovi!
}
```

**Fix comuni:**
- ❌ Threshold troppo alto → riduci a 1.5
- ❌ GPIO8 non connesso → verifica continuità
- ❌ IMU not inizializzato → check I2C address (0x6A o 0x6B?)

### Issue: Deep sleep non funziona

**Debug:**
```python
# main.py
print(f"Last motion: {time.ticks_diff(time.ticks_ms(), last_motion_time)}ms ago")
print(f"Active: {active}")
```

**Fix comuni:**
- ❌ Motion continuo impedisce sleep → normale! Aspetta 20s fermo
- ❌ Timeout troppo breve → aumenta SLEEP_TIMEOUT_MS
- ❌ Wake pin mal configurato → check `esp32.wake_on_ext1()`

### Issue: WiFi non si connette (ESPHome)

**Debug:**
```bash
esphome logs morphball.yaml

# Cerca linee tipo:
[W][wifi:xxx] No WiFi SSID set!
[E][wifi:xxx] WiFi connection failed!
```

**Fix comuni:**
- ❌ SSID/password errati in secrets.yaml
- ❌ WiFi 5GHz → ESP32 supporta solo 2.4GHz!
- ❌ Segnale debole → antenna ESP32 posizionata male
- ❌ MAC filtering router → aggiungi ESP32 MAC

## 📸 Showcase & Share

### 📷 Photo Tips

```
Best angles:
1. Top-down (mostra LED pattern)
2. Side 45° (mostra forma sferica)
3. Dark room + long exposure (LED trails!)
4. Slow-motion video (LED effects)
```

### 🎥 Video Demo

Mostra:
- ✨ LED effects showcase (tutti i 11)
- 🏃 Motion detection (shake test)
- 💤 Sleep/wake cycle
- 🏠 Home Assistant control

### 🌐 Community

Condividi il tuo build!

- **Reddit**: r/3Dprinting, r/ESP32, r/homeassistant
- **Discord**: ESPHome, Home Assistant
- **YouTube**: Tutorial + showcase
- **GitHub**: Issues & Pull Requests su questo repo!

---

## 🎉 Congratulazioni!

Hai completato la tua Metroid Morph Ball! 🔮

**Prossimi step:**
- [ ] Fine-tuning animazioni
- [ ] Setup automazioni HA
- [ ] Considera PCB custom per v2.0
- [ ] Stampa altre ball e fai effetti sincronizzati!

**Enjoy your build!** 🎮

---

**Build time totale stimato:** 2-3 giorni (non consecutivi)

- Stampa 3D: 8-12h
- Elettronica: 3-4h
- Software: 1-2h
- Assembly: 2-3h
- Testing/tuning: 2-4h

**Ultimo aggiornamento:** Aprile 2026