# 🔮 Metroid Morph Ball

3D printed Metroid Morph Ball action figure with LED animations controlled by ESP32 and IMU motion sensor.

![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-ESP32--S3-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

🇬🇧 English Version | [🇮🇹 Versione Italiana](docs/README_IT.md)

## 📋 Table of Contents

- [Panoramica](#panoramica)
- [Caratteristiche](#caratteristiche)
- [Hardware](#hardware)
- [Software](#software)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Sviluppo Futuro](#sviluppo-futuro)
- [Contribuire](#contribuire)
- [Licenza](#licenza)

## 🎮 Panoramica

Questo progetto ricrea la leggendaria **Morph Ball** della serie Metroid come action figure interattiva stampata in 3D. La sfera si illumina con 32 LED WS2812B programmabili e risponde al movimento grazie a un sensore IMU, entrando automaticamente in deep sleep quando è ferma per risparmiare batteria.

### Due Versioni Disponibili

Il progetto offre due implementazioni complete:

1. **MicroPython** (`/ESP32` + `/MG24`) - Versione standalone originale
2. **ESPHome** (`/ESPHome`) - Integrazione completa con Home Assistant

## ✨ Caratteristiche

- 🎨 **32 LED RGB WS2812B** con animazioni customizzabili
- 🏃 **Rilevamento movimento** tramite accelerometro LSM6DS3
- 💤 **Deep sleep automatico** per risparmio energetico
- 🔋 **Wake su movimento** per attivazione istantanea
- 🏠 **Integrazione Home Assistant** (versione ESPHome)
- 📱 **Controllo WiFi** con selezione effetti e configurazione
- 🎯 **Gruppi LED personalizzati** che riproducono l'estetica Metroid
- ⚡ **Architettura dual-MCU** (ESP32-S3 + MG24) per ottimizzazione consumi

## 🔧 Hardware

### Perché Architettura Dual-MCU?

Questo progetto usa **due microcontrollori** invece di uno per ragioni strategiche:

1. **🔋 Power Management Ottimizzato**
   - MG24 funziona in modalità ultra-low power monitorando continuamente l'IMU
   - ESP32 può andare in deep sleep (~10µA) mentre MG24 fa da "sentinella" per il movimento
   - Wake-on-motion con latenza minima e massima durata batteria

2. **📡 ESP32-S3 Tiny Non Ha IMU Integrato**
   - Il form factor compatto dell'ESP32-S3 Tiny non include sensori di movimento
   - XIAO MG24 ha accelerometro LSM6DS3 già integrato on-board
   - Non servono moduli IMU esterni e cablaggi aggiuntivi

3. **⚡ Separazione Task & Performance Real-Time**
   - **MG24**: Dedicato al polling real-time dell'IMU (20Hz) e rilevamento movimento
   - **ESP32**: Gestisce animazioni LED, WiFi, integrazione Home Assistant
   - Nessuna contesa di risorse - ogni MCU fa ciò per cui è ottimizzato

4. **🎯 Monitoraggio Continuo Senza Impatto**
   - MG24 esegue polling IMU continuo a 20Hz senza impattare performance ESP32
   - Animazioni LED fluide su ESP32 senza overhead polling IMU
   - Separazione pulita delle responsabilità nel codice

**Svantaggi approccio single-MCU:**
- ❌ ESP32 che fa polling IMU = alto consumo (no vero deep sleep)
- ❌ Wake-on-timer = alta latenza (100-500ms) e spreco energia
- ❌ Modulo IMU esterno = cablaggio più complesso, ingombro maggiore

**Vantaggi Dual-MCU:**
- ✅ Massima efficienza energetica (~100µA media in standby)
- ✅ Wake istantaneo su movimento (<50ms latenza)
- ✅ Architettura modulare (upgrade/swap MCU indipendenti)
- ✅ Entrambi MCU in form factor XIAO (stack back-to-back)

### Componenti Principali

| Componente | Modello | Quantità | Note |
|------------|---------|----------|------|
| Microcontroller principale | ESP32-S3 Tiny | 1 | Controllo LED e WiFi |
| Microcontroller IMU | Seeed XIAO MG24 | 1 | Rilevamento movimento |
| LED Strip | WS2812B | 32 LED | Divisi in 3 gruppi |
| IMU | LSM6DS3 | 1 | Integrato nel MG24 |
| Batteria | LiPo 3.7V | 1 | Capacità da definire |
| Switch | ON/OFF | 1 | Alimentazione |

### Schema Connessioni

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
└─────────────┘       └──────────┘        │ +5V ◄───┤ Batteria
                                          └─────────┘
```

### Dettagli Pin

**ESP32-S3 Tiny:**
- `GPIO18`: DIN del LED strip WS2812B
- `GPIO8`: Input da MG24 (HIGH quando c'è movimento)
- `GPIO7`: Output verso MG24 (HIGH quando animazioni attive)

**MG24 (XIAO):**
- `D4`: Output verso ESP32 (pulse su movimento)
- `D5`: Input da ESP32 (stato animazioni)
- `SDA/SCL`: I2C per LSM6DS3 (interno)

### Disposizione LED

I 32 LED sono organizzati in 3 gruppi per ricreare l'estetica Metroid:

- **Gruppo 0** (6 LED): Core grills - Verde acqua `(0, 230, 100)`
  - Posizioni: `[0, 19, 20, 25, 26, 31]`
  
- **Gruppo 1** (12 LED): Inner ring - Verde brillante `(0, 255, 30)`
  - Posizioni: `[1, 2, 17, 18, 21, 22, 23, 24, 27, 28, 29, 30]`
  
- **Gruppo 2** (14 LED): Outer ring - Verde brillante `(0, 255, 30)`
  - Posizioni: `[3-16]`

## 💾 Software

### Struttura Repository

```
morphball/
├── 3D model/                # Modello 3D stampabile
│   └── MorphBall.3mf
├── ESP32/                   # Versione MicroPython standalone
│   ├── main.py             # Entry point
│   ├── ledstrip.py         # Gestione LED
│   └── animations/         # Effetti LED
│       ├── base.py
│       ├── pulse.py
│       ├── rotation.py
│       └── static.py
├── MG24/                    # Codice sensore movimento
│   └── mg24_imu.ino        # Arduino sketch per IMU
├── ESPHome/                 # Versione Home Assistant
│   ├── morphball.yaml      # Config ESPHome
│   ├── README.md           # Guida setup
│   ├── lovelace-card.yaml  # Dashboard HA
│   └── secrets.yaml.example
└── docs/                    # Documentazione (questa cartella)
```

### Versione MicroPython

**Caratteristiche:**
- Standalone, non richiede connessione WiFi
- Animazione pulse automatica
- Sleep dopo 20 secondi di inattività
- Deep sleep dopo ulteriori 20 secondi in standby

**Files principali:**
- `main.py`: Loop principale, gestione thread, sleep management
- `ledstrip.py`: Classe per controllo WS2812B con gruppi
- `animations/`: Moduli con diversi effetti LED

### Versione ESPHome

**Caratteristiche:**
- Integrazione nativa con Home Assistant
- 11 effetti LED selezionabili
- Configurazione timeout via dashboard
- OTA updates
- Diagnostica completa (WiFi, uptime, IP)

**Vantaggi:**
- Nessuna app mobile necessaria
- Configurazione via interfaccia web
- Automazioni HA disponibili
- Sincronizzazione con altri dispositivi

Vedi [ESPHome/README.md](ESPHome/README.md) per dettagli completi.

## 🚀 Installazione

### Requisiti Software

**Per versione MicroPython:**
- Python 3.7+
- `esptool` per flash
- `mpremote` o `ampy` per upload files

**Per versione ESPHome:**
- ESPHome CLI o addon Home Assistant
- Home Assistant (ovviamente!)

### Setup Versione MicroPython

1. **Flash MicroPython su ESP32-S3:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 esp32s3-micropython.bin
```

2. **Upload codice:**
```bash
cd ESP32
mpremote connect /dev/ttyUSB0 cp -r . :
```

3. **Flash MG24:**
```bash
# Usa Arduino IDE
# Board: Seeed XIAO MG24
# Upload: MG24/mg24_imu.ino
```

### Setup Versione ESPHome

Vedi documentazione completa in [ESPHome/README.md](ESPHome/README.md)

**Quick start:**
```bash
cd ESPHome
cp secrets.yaml.example secrets.yaml
# Edita secrets.yaml con le tue credenziali
esphome run morphball.yaml
```

## 🎯 Utilizzo

### Versione MicroPython

La Morph Ball si attiva automaticamente:
1. **Movimento rilevato** → LED si accendono con effetto pulse
2. **20s di inattività** → Entra in standby (solo core grills accesi)
3. **Altri 20s ferma** → Deep sleep completo
4. **Nuovo movimento** → Wake automatico e riattivazione

### Versione ESPHome

**Dashboard Home Assistant:**
1. Accendi/spegni LED
2. Seleziona effetto dal dropdown
3. Regola timeout sleep con slider
4. Abilita/disabilita deep sleep mode
5. Monitora stato movimento e diagnostica

**Automazioni esempio:**

```yaml
# Attiva Rainbow al tramonto
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

## 🔮 Sviluppo Futuro

### Roadmap

- [ ] **Riconoscimento gesti** - Shake, roll, tilt trigger effetti diversi
- [ ] **Batteria monitoring** - Indicatore livello carica
- [ ] **Modalità gioco** - Mini-game interattivi
- [ ] **Sincronizzazione multi-ball** - Più Morph Ball che comunicano
- [ ] **Audio feedback** - Speaker per suoni Metroid
- [ ] **Charging dock** - Base di ricarica wireless
- [ ] **App mobile** - Per versione MicroPython standalone
- [ ] **Effetti audio-reactive** - Sync con musica

### Idee per Contributi

- Nuove animazioni LED
- Ottimizzazione consumi energetici
- Miglioramenti modello 3D
- Porting su altri microcontroller
- Integrazione con altri smart home systems (Alexa, Google Home)

## 🤝 Contribuire

Contributi benvenuti! Ecco come:

1. **Fork** il repository
2. Crea un **branch** per la tua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. Apri una **Pull Request**

### Linee Guida

- Commenta il codice (possibilmente in italiano)
- Testa le modifiche prima del commit
- Aggiorna la documentazione se necessario
- Segui lo stile di codice esistente

## 📄 Licenza

Questo progetto è rilasciato sotto licenza **GPL-3.0**. Vedi [LICENSE](LICENSE) per dettagli.

## 🙏 Ringraziamenti

- **Nintendo/Retro Studios** per l'ispirazione Metroid
- **Comunità ESPHome** per il framework fantastico
- **Home Assistant** per la piattaforma domotica
- **Seeed Studio** per il XIAO MG24
- Tutti i contributor che miglioreranno questo progetto!

## 📞 Contatti

**Gualtiero Saderis** - [@wizwally](https://github.com/wizwally)

Project Link: [https://github.com/wizwally/morphball](https://github.com/wizwally/morphball)

---

**Fatto con ❤️ e nostalgia per i classici Nintendo**
