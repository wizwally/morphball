# 🔮 Metroid Morph Ball - ESPHome Edition

Configurazione ESPHome per controllare la Morph Ball via Home Assistant!

## 📋 Hardware Requirements

- **ESP32-S3 Tiny**
- **MG24** con LSM6DS3 IMU (per motion detection)
- **32x WS2812B LEDs**
- Connessioni:
  - GPIO18 → DIN LED strip
  - GPIO8 ← Motion signal dal MG24
  - GPIO7 → Alive signal al MG24

## 🚀 Setup Iniziale

### 1. Preparare secrets.yaml

```bash
cd ESPHome
cp secrets.yaml.example secrets.yaml
nano secrets.yaml  # Edita con le tue credenziali
```

Compila i seguenti campi:
- `wifi_ssid`: Nome della tua rete WiFi
- `wifi_password`: Password WiFi
- `api_key`: Genera con `openssl rand -base64 32`
- `ota_password`: Password per aggiornamenti OTA

### 2. Installare ESPHome

Se non hai ancora ESPHome:

```bash
pip install esphome
```

Oppure usa l'addon di Home Assistant.

### 3. Compilare e Flashare

**Prima volta (via USB):**

```bash
cd ESPHome
esphome run morphball.yaml
```

Seleziona la porta USB dell'ESP32-S3.

**Successivamente (via OTA):**

```bash
esphome run morphball.yaml
# Seleziona l'opzione wireless (morphball.local)
```

### 4. Aggiungere a Home Assistant

1. Vai in **Impostazioni** → **Dispositivi e servizi**
2. Home Assistant dovrebbe rilevare automaticamente il dispositivo
3. Clicca su **Configura** e inserisci l'`api_key` da `secrets.yaml`

### 5. Aggiungere la Dashboard Card

**Opzione A - Con Mushroom Cards (consigliato):**

1. Installa "Mushroom" da HACS
2. Dashboard → Modifica → Aggiungi Card → Manuale
3. Copia il contenuto di `lovelace-card.yaml`

**Opzione B - Senza custom cards:**

1. Dashboard → Modifica → Aggiungi Card → Manuale
2. Copia il contenuto di `lovelace-card-simple.yaml`

## 🎮 Funzionalità

### Controllo LED

11 effetti disponibili:
- **Pulse**: Classico breathing
- **Breathing**: Più lento e smooth
- **Strobe**: Effetto stroboscopico
- **Rainbow**: Arcobaleno scorrevole
- **Color Wipe**: Riempimento a colori
- **Scan**: Scanner tipo K.I.T.T.
- **Twinkle**: Scintillio casuale
- **Fireworks**: Fuochi d'artificio
- **Flicker**: Effetto candela
- **Original Groups**: Animazione originale con 3 gruppi LED

### Sleep Management

- **Sleep Mode**: On/Off per abilitare deep sleep
- **Sleep Timeout**: Tempo di inattività prima dello standby (5-300s)
- **Standby Duration**: Tempo in standby prima del deep sleep (5-120s)

### Motion Detection

Il MG24 rileva movimento tramite IMU e invia segnale all'ESP32:
- Wake automatico dal deep sleep
- Reset del timer di sleep
- Sensore binary_sensor in Home Assistant

## 🔧 Configurazione Avanzata

### Modificare i Colori

Edita il lambda effect "Original Groups" in `morphball.yaml`:

```cpp
// Gruppo 0 - Core grills
Color(R, G, B)  // Modifica questi valori
```

### Aggiungere Nuovi Effetti

Gli effetti ESPHome sono configurabili in `morphball.yaml` sotto `light:` → `effects:`.

Documentazione: https://esphome.io/components/light/index.html#light-effects

### Automazioni Home Assistant

Esempio - Attiva effetto Rainbow al tramonto:

```yaml
automation:
  - alias: "Morphball Rainbow al tramonto"
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: select.select_option
        target:
          entity_id: select.metroid_morph_ball_effect
        data:
          option: "Rainbow"
      - service: light.turn_on
        target:
          entity_id: light.metroid_morph_ball_leds
```

## 🐛 Troubleshooting

### Non si connette al WiFi

1. Controlla `secrets.yaml`
2. L'ESP32 crea un AP fallback: `morphball Fallback`
3. Connettiti e configura WiFi via captive portal

### LED non si accendono

1. Verifica connessione GPIO18 → DIN
2. Controlla alimentazione LED strip (5V, GND)
3. Guarda i log: `esphome logs morphball.yaml`

### Deep sleep non funziona

1. Verifica che Sleep Mode sia ON in Home Assistant
2. Controlla timeout configurati
3. Il movimento continuo previene il deep sleep (corretto!)

### MG24 non invia segnali

1. Verifica connessione GPIO8 ← MG24 D4
2. Controlla che MG24 riceva alimentazione
3. Verifica segnale ALIVE (GPIO7 → MG24 D5)

## 📚 Riferimenti

- [ESPHome Documentation](https://esphome.io)
- [WS2812B Light Effects](https://esphome.io/components/light/index.html#light-effects)
- [Deep Sleep](https://esphome.io/components/deep_sleep.html)
- [Home Assistant ESPHome Integration](https://www.home-assistant.io/integrations/esphome/)

## 🎯 Prossimi Sviluppi

Idee per il futuro:
- [ ] Distinzione tipi di movimento (shake, roll, tilt) sul MG24
- [ ] Effetti LED sincronizzati con musica
- [ ] Integrazione con Alexa/Google Assistant
- [ ] Notifiche push su movimento rilevato
- [ ] Storico attività e statistiche

## 📝 Note

- I gruppi LED originali sono mantenuti nell'effetto "Original Groups"
- Il comportamento di sleep replica il codice MicroPython originale
- Tutte le configurazioni sono persistenti (sopravvivono ai reboot)

---

**Fatto con ❤️ per Home Assistant**
