# 🔌 Documentazione Hardware - Metroid Morph Ball

Guida completa all'hardware del progetto Morph Ball.

## 🎯 Razionale Architettura Dual-MCU

### Perché Due Microcontrollori?

Questo design usa **ESP32-S3 + MG24** invece di un singolo MCU per prestazioni e efficienza energetica ottimali:

**🔋 Eccellenza nel Power Management**
- MG24 monitora continuamente l'IMU in modalità ultra-low power (~50µA)
- ESP32 in deep sleep a ~10µA quando inattivo
- **Totale standby: ~100µA** (vs. ~5000µA se ESP32 dovesse fare polling IMU)
- Autonomia batteria in standby: **400+ giorni** vs. ~30 giorni single-MCU

**⚡ Performance Real-Time**
- **MG24**: Polling IMU dedicato a 20Hz, rilevamento movimento <50ms
- **ESP32**: Animazioni LED a 60fps, WiFi, zero overhead interrupt
- Zero contesa risorse = animazioni fluide + wake istantaneo

**🎯 Specializzazione Task**
| Task | ESP32-S3 | MG24 |
|------|----------|------|
| Controllo LED | ✅ Primario | - |
| WiFi/BLE | ✅ Primario | - |
| Polling IMU | - | ✅ Primario |
| Rilevamento Movimento | - | ✅ Primario |
| Deep Sleep | ✅ Ultra-basso | ✅ Low power |
| Wake Trigger | Riceve | Invia |

**📐 Integrazione Fisica**
- Entrambi in form factor XIAO (21x17.5mm)
- Stack back-to-back con 4 fili
- Stesso ingombro di un singolo MCU più grande
- Modulare: swap/upgrade indipendenti

**vs. Alternative Single-MCU:**

| Approccio | Consumo (Standby) | Latenza Wake | Complessità |
|-----------|-------------------|--------------|-------------|
| **ESP32 + IMU Esterno** | ~5mA | 100-500ms | Cablaggio complesso |
| **ESP32 wake-on-timer** | ~500µA | 200-1000ms | Media |
| **Dual-MCU (Questo)** | **~100µA** | **<50ms** | Bassa (4 fili) |

## 📦 Bill of Materials (BOM)

### Componenti Elettronici

| Componente | Specifiche | Quantità | Prezzo Est. | Link/Note |
|------------|------------|----------|-------------|-----------|
| **ESP32-S3 Tiny** | Dual-core, WiFi, BLE | 1 | €8-12 | Piccolo form factor ideale |
| **Seeed XIAO MG24** | ARM Cortex-M33, LSM6DS3 integrato | 1 | €10-15 | Include IMU on-board |
| **LED Strip WS2812B** | 5V, IP30, 60 LED/m | 32 LED (~53cm) | €5-8 | Tagliabile ogni LED |
| **Batteria LiPo** | 3.7V, 500-1000mAh | 1 | €8-12 | Dimensioni da verificare |
| **Modulo ricarica** | TP4056 o simile | 1 | €2-3 | Con protezione |
| **Switch ON/OFF** | Slide switch 3 pin | 1 | €0.50 | Miniatura |
| **Connettori JST** | 2.54mm pitch | Vari | €2-3 | Per collegamenti modulari |
| **Fili** | AWG 22-26, silicone | 1m | €2-3 | Rosso/Nero/Dati |
| **Heat shrink** | Guaina termorestringente | 10cm | €1 | Varie misure |

### Componenti Meccanici

| Componente | Specifiche | Quantità | Note |
|------------|------------|----------|------|
| **Filamento PETG** | Trasparente/Verde | 100-150g | Per il guscio principale |
| **Filamento PLA/ASA** | Opaco/Nero | 50g | Per supporti interni |
| **Viti M2** | 6-10mm | 4-8 | Fissaggio componenti |
| **Dadi M2** | Standard | 4-8 | O inserti termici |

**Costo totale stimato:** €50-80

## 🔧 Specifiche Tecniche

### ESP32-S3 Tiny

```
MCU: Xtensa® dual-core 32-bit LX7
Clock: fino a 240 MHz
Flash: 4MB
PSRAM: 2MB
WiFi: 802.11 b/g/n
BLE: 5.0
GPIO: 27 disponibili
ADC: 12-bit, 20 canali
Alimentazione: 3.3V (regolatore integrato da 5V)
Dimensioni: 21mm x 17.5mm
```

**Vantaggi:**
- Form factor minuscolo
- WiFi + BLE integrati
- Sufficiente memoria per OTA
- Deep sleep ultra-low power (~10µA)

### Seeed XIAO MG24

```
MCU: Silicon Labs EFR32MG24
Core: ARM Cortex-M33 @ 78 MHz
Flash: 1536 KB
RAM: 256 KB
IMU: LSM6DS3 (I2C integrato)
Alimentazione: 3.3V
Dimensioni: 21mm x 17.5mm (compatibile XIAO)
```

**Vantaggi:**
- LSM6DS3 già integrato (no cablaggio esterno!)
- Ultra low power
- Form factor identico a ESP32-S3
- I2C dedicato per IMU

### WS2812B LED Strip

```
Tipo: RGB LED indirizzabili
Protocollo: WS2812/NeoPixel
Tensione: 5V
Corrente per LED: ~60mA @ bianco full brightness
Corrente 32 LED: ~1.92A @ 100% (raramente necessario)
Frequenza PWM: 800 kHz
Colori: 24-bit (16.7M colori)
```

**Note:**
- Alimentazione 5V, ma DATA a 3.3V funziona (ESP32 out = 3.3V)
- Consigliato condensatore 100-1000µF sulla alimentazione
- Resistenza 330Ω sulla linea DATA (opzionale ma consigliata)

## 🔌 Schema Circuitale Dettagliato

### Connessioni ESP32-S3

```
ESP32-S3 Tiny
┌─────────────────────┐
│                     │
│ 5V  ────────┬───────┼──── Batteria+ (via switch)
│             │       │
│             └───────┼──── LED Strip +5V
│                     │
│ GND ────────┬───────┼──── Batteria-
│             │       │
│             ├───────┼──── LED Strip GND
│             │       │
│             └───────┼──── MG24 GND
│                     │
│ GPIO18 ─────────────┼──── LED Strip DIN
│ (LED_PIN)           │     (opzionale: R 330Ω)
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

### Connessioni MG24

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
│          │ LSM6DS3 (interno)
│ SCL ─────┘       │
│                  │
└──────────────────┘
```

### Logica Segnali

**ALIVE (ESP32 GPIO7 → MG24 D5):**
- `HIGH`: ESP32 sta eseguendo animazioni, MG24 continua a monitorare
- `LOW`: ESP32 in deep sleep, MG24 può andare in low power

**MOTION (MG24 D4 → ESP32 GPIO8):**
- `HIGH` (pulse 200ms): Movimento rilevato (accelerazione > 2.5G)
- `LOW`: Nessun movimento
- Wake pin per deep sleep dell'ESP32

### Alimentazione

```
Batteria LiPo 3.7V (500-1000mAh)
       │
       ├──► TP4056 (ricarica USB)
       │      │
       │      └──► LED status carica
       │
       └──► Switch ON/OFF
              │
              └──► Boost converter 5V (opzionale)
                   │
                   ├──► ESP32-S3 (ha regolatore 3.3V interno)
                   │
                   └──► LED Strip WS2812B (5V)
```

**Opzioni alimentazione:**

1. **Semplice (consigliato per prototipo):**
   - Batteria → ESP32 diretto (accetta 3.7V su pin 5V)
   - LED a 3.7V (funzionano, meno luminosi)

2. **Boost a 5V (produzione):**
   - Batteria → Boost 5V → ESP32 + LED
   - LED a piena luminosità
   - Boost esempio: MT3608

## 🎨 Layout Fisico 3D

### Disposizione Componenti

```
Vista sezione trasversale:

        ╔════════════════╗  ← Guscio superiore PETG trasparente
        ║   LED Ring     ║  
     ┌──╫────────────────╫──┐
     │  ║  ┌──────────┐  ║  │
     │  ║  │          │  ║  │ ← LED gruppo 2 (ring esterno)
     │  ╠══╪══════════╪══╣  │
     │  ║  │  ESP32   │  ║  │
     │  ║  │   +      │  ║  │ ← LED gruppo 1 (inner)
     │  ║  │  MG24    │  ║  │
     │  ╠══╪══════════╪══╣  │
     │  ║  │          │  ║  │ ← LED gruppo 0 (core grills)
     │  ║  └──────────┘  ║  │
     │  ║                ║  │
     ├──╫────────────────╫──┤
     │  ║    Batteria    ║  │
     │  ║                ║  │
     └──╨────────────────╨──┘
        ╚════════════════╝  ← Guscio inferiore

        [●]  ← Switch ON/OFF
```

### Vincoli Dimensionali

- **Diametro interno:** ~60-80mm (da verificare con modello 3D)
- **Altezza componenti:** max 15mm (stack ESP32+MG24)
- **Spazio batteria:** ~40x30x10mm
- **LED strip:** curvatura raggio min 20mm

## ⚡ Consumi e Autonomia

### Analisi Consumi

**ESP32-S3:**
- Active (WiFi ON, LED ON): ~150-200mA
- Light sleep: ~3-5mA
- Deep sleep: ~10µA

**MG24:**
- Active (IMU polling): ~5-10mA
- Low power: ~50µA

**LED (32x WS2812B):**
- 1 LED @ 100%: ~60mA
- 32 LED @ 100%: ~1920mA (!)
- Tipico (effetto pulse, 50% avg): ~500-800mA

**Totale medio in uso:** ~650-1000mA  
**Totale deep sleep:** ~100µA

### Stima Autonomia

Con batteria **500mAh:**
- Uso continuo (animazioni): ~30-45 minuti
- Standby (solo core): ~2-3 ore
- Deep sleep: ~200+ giorni

Con batteria **1000mAh:**
- Uso continuo: ~1-1.5 ore
- Standby: ~4-6 ore
- Deep sleep: ~400+ giorni

**Raccomandazione:** Batteria 750-1000mAh per bilanciare dimensioni/autonomia.

## 🛠️ Assembly Guide

### Step 1: Preparazione Componenti

1. **Taglia LED strip** a 32 LED
2. **Salda fili** a DIN, 5V, GND
3. **Prepara connettori JST** per modularità
4. **Test LED strip** con Arduino/ESP32 separato

### Step 2: Saldature ESP32-MG24

```
ESP32 GPIO7  ──────► MG24 D5
ESP32 GPIO8  ◄────── MG24 D4
ESP32 3V3    ──────► MG24 3V3
ESP32 GND    ──────► MG24 GND
```

**Consiglio:** Salda ESP32 e MG24 **back-to-back** per risparmiare spazio!

### Step 3: Collegamento LED

1. Salda **DIN** a ESP32 GPIO18 (resistenza 330Ω consigliata)
2. **5V** e **GND** direttamente a batteria (con switch)
3. Condensa tore 470µF tra 5V-GND vicino ai LED

### Step 4: Test Funzionalità

```python
# Test code per ESP32
from machine import Pin
from neopixel import NeoPixel

np = NeoPixel(Pin(18), 32)
np.fill((0, 255, 30))  # Verde
np.write()
```

### Step 5: Montaggio nel Guscio

1. **Posiziona LED** seguendo la guida nel modello 3D
2. **Fissa ESP32+MG24** con viti M2 o hot glue
3. **Inserisci batteria** e modulo ricarica
4. **Routing cavi** pulito e sicuro
5. **Fissa switch** nel foro dedicato

### Step 6: Chiusura e Test Finale

1. **Chiudi guscio** con viti o clip
2. **Test movimento** in tutte le direzioni
3. **Verifica impermeabilità** (se richiesta)
4. **Test autonomia** con timer

## 📏 Design Considerations

### Dissipazione Termica

- ESP32-S3: ~0.5-1W in uso intenso
- LED: ~3-10W a seconda del pattern
- Guscio PETG aiuta dissipazione
- Evitare uso continuativo a >80% luminosità

### Impermeabilità

- Versione base: **NO** (guscio snap-fit)
- Per uso esterno: O-ring nel giunto + sigillante
- Rating possibile: IPX4-IPX5

### Robustezza

- PETG: resistente a cadute da ~1m
- Rinforzi interni consigliati negli angoli di stress
- Peso totale: ~150-200g

## 🔍 Troubleshooting Hardware

### LED non si accendono

- ✓ Verifica alimentazione 5V (multimetro)
- ✓ Controlla continuità DIN, GND
- ✓ Test con singolo LED
- ✓ Verifica polarità LED strip

### ESP32 non si connette

- ✓ Alimentazione stabile 3.3-5V
- ✓ Prova reset button
- ✓ USB cable con data (non solo power!)
- ✓ Driver CP2102/CH340 installati

### MG24 non rileva movimento

- ✓ IMU LSM6DS3 inizializzato (serial monitor)
- ✓ Soglia accelerazione (2.5G default)
- ✓ Connessione I2C funzionante
- ✓ Alimentazione 3.3V stabile

### Consumo eccessivo

- ✓ LED brightness troppo alta
- ✓ WiFi sempre attivo (disattiva se standalone)
- ✓ Polling IMU troppo frequente
- ✓ Deep sleep non si attiva

### Interferenze WiFi

- ✓ LED strip può generare rumore EMI
- ✓ Aggiungi condensatore 100nF vicino ESP32
- ✓ Separa fisicamente LED da antenna WiFi
- ✓ Usa canali WiFi meno affollati

## 📐 Files Gerber/CAD

> TODO: Aggiungere PCB custom (opzionale)
> Per ora: prototipazione su breadboard/perfboard

## 🔗 Riferimenti

- [ESP32-S3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
- [WS2812B Datasheet](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf)
- [LSM6DS3 Datasheet](https://www.st.com/resource/en/datasheet/lsm6ds3.pdf)
- [XIAO MG24 Wiki](https://wiki.seeedstudio.com/xiao_mg24/)

---

**Ultimo aggiornamento:** Aprile 2026