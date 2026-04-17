# 🤝 Contributing to Morphball

Grazie per l'interesse nel contribuire al progetto Metroid Morph Ball! 

## 🌟 Come Puoi Contribuire

### 1. 🐛 Segnalare Bug

Se trovi un problema:

1. **Cerca prima** tra le [Issues esistenti](https://github.com/wizwally/morphball/issues)
2. Se non esiste, apri una nuova Issue con:
   - ✅ Descrizione chiara del problema
   - ✅ Steps per riprodurlo
   - ✅ Hardware/software usati
   - ✅ Log/screenshot se possibile
   - ✅ Comportamento atteso vs. comportamento osservato

**Template Issue:**

```markdown
**Descrizione:**
[Descrivi il bug]

**Steps per riprodurre:**
1. 
2. 
3. 

**Comportamento atteso:**
[Cosa dovrebbe succedere]

**Comportamento osservato:**
[Cosa succede invece]

**Environment:**
- Versione: MicroPython/ESPHome X.Y
- Hardware: ESP32-S3 / MG24
- OS: [se rilevante]

**Log/Screenshot:**
[Aggiungi qui]
```

### 2. 💡 Proporre Nuove Feature

Hai un'idea?

1. Apri una Issue con tag `enhancement`
2. Descrivi:
   - Problema che risolve
   - Proposta soluzione
   - Alternative considerate
   - Mockup/sketch se pertinente

### 3. 📝 Migliorare Documentazione

La documentazione non è mai troppa!

**Aree dove aiutare:**
- Traduzioni (EN, ES, DE, FR)
- Tutorial addizionali
- Troubleshooting tips
- Video guides
- Diagrammi/schemi migliorati

**Processo:**
1. Fork repo
2. Modifica files in `/docs`
3. Pull Request

### 4. 💻 Contribuire Codice

#### Setup Ambiente Sviluppo

```bash
# Clone
git clone https://github.com/wizwally/morphball.git
cd morphball

# Branch per feature
git checkout -b feature/nome-feature

# Lavora sul codice
# ...

# Commit
git add .
git commit -m "feat: descrizione chiara"

# Push
git push origin feature/nome-feature

# Apri PR su GitHub
```

#### Code Style

**Python (MicroPython):**

```python
# PEP 8 style
# Nomi descrittivi
# Commenti in italiano OK

class LEDStrip:
    """Gestisce il LED strip WS2812B."""
    
    def set_color(self, color: tuple) -> None:
        """
        Imposta colore RGB.
        
        Args:
            color: Tupla (R, G, B) con valori 0-255
        """
        pass
```

**YAML (ESPHome):**

```yaml
# Indentazione 2 spazi
# Commenti descrittivi
# Naming snake_case

sensor:
  - platform: template
    name: "Descriptive Name"
    # Commento esplicativo se logica complessa
    lambda: |-
      return value;
```

**C++ (MG24):**

```cpp
// Camel case per funzioni
// UPPER_CASE per costanti
// Commenti in italiano OK

const float ACCELERATION_THRESHOLD = 2.5;

void readIMU() {
    // Legge dati accelerometro
}
```

#### Commit Messages

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: aggiunge effetto LED rainbow
fix: corregge deep sleep wake
docs: aggiorna README con nuove istruzioni
refactor: ottimizza loop animazione
test: aggiunge test per motion detection
```

**Tipi comuni:**
- `feat`: Nuova feature
- `fix`: Bug fix
- `docs`: Solo documentazione
- `style`: Formattazione (no logic change)
- `refactor`: Refactoring codice
- `test`: Aggiunge/modifica test
- `chore`: Maintenance tasks

#### Testing

**Prima di PR:**

```bash
# Test MicroPython
mpremote connect /dev/ttyUSB0
>>> import main
>>> # Verifica funziona

# Test ESPHome
esphome compile morphball.yaml
# ✓ No errori compilazione

# Hardware test
# ✓ LED funzionano
# ✓ Motion detection OK
# ✓ Sleep cycle corretto
```

**Test checklist:**
- [ ] Codice compila senza errori
- [ ] Feature funziona come previsto
- [ ] Non rompe funzionalità esistenti
- [ ] Documentazione aggiornata se necessario

### 5. 🎨 Contribuire Animazioni LED

Nuove animazioni sempre benvenute!

**MicroPython:**

```python
# ESP32/animations/my_effect.py
from animations.base import Animation
import time

class MyEffectAnimation(Animation):
    """Descrizione effetto."""
    
    def run(self, param1=default):
        """
        Args:
            param1: Descrizione parametro
        """
        # Implementazione
        pass
```

**ESPHome:**

```yaml
# ESPHome/morphball.yaml
effects:
  - addressable_lambda:
      name: "My Effect"
      update_interval: 50ms
      lambda: |-
        // C++ code
        // Commenti su logica
```

**Aggiungi anche:**
- Descrizione in README
- GIF/video demo (crea Issue per link)
- Parameters documentati

### 6. 🔧 Hardware Improvements

Modifiche hardware:

**Modello 3D:**
- Files STL/3MF in `/3D model`
- Changelog con modifiche
- Test print consigliati

**Schemi Elettronici:**
- Fritzing/KiCAD files
- Export PNG per documentazione
- BOM aggiornata se nuovi componenti

**PCB Custom:**
- Gerber files
- Assembly guide
- Test report

## 📋 Pull Request Process

### 1. Descrizione Chiara

```markdown
**Tipo:** [Feature/Bugfix/Docs/Refactor]

**Descrizione:**
[Cosa fa questa PR]

**Motivazione:**
[Perché è necessaria]

**Testing:**
[Come hai testato]

**Screenshots/Video:**
[Se applicabile]

**Breaking Changes:**
[Se presenti, lista qui]

**Checklist:**
- [ ] Codice testato
- [ ] Docs aggiornate
- [ ] Commit messages chiari
- [ ] No conflitti con main
```

### 2. Code Review

- Rispondi a feedback costruttivamente
- Aggiorna codice se richiesto
- Squash commits se richiesto

### 3. Merge

Dopo approval:
- Maintainer fa merge
- Branch feature cancellato
- Celebra! 🎉

## 🎯 Aree Prioritarie

Contributi particolarmente graditi in:

**Alta priorità:**
- [ ] **Gesture recognition** - Shake, roll, tilt detection
- [ ] **Battery monitoring** - Voltage/percentage
- [ ] **Alexa/Google Home** integration
- [ ] **Mobile app** (React Native/Flutter)
- [ ] **Multi-ball sync** - Communication protocol

**Media priorità:**
- [ ] **Audio feedback** - Speaker integration
- [ ] **Charging dock** design
- [ ] **Alternative animations**
- [ ] **Power optimization**
- [ ] **PCB design**

**Bassa priorità (ma gradite!):**
- [ ] Traduzioni documentazione
- [ ] Tutorial video
- [ ] Case studies / build logs
- [ ] Alternative form factors

## 🏆 Contributors Hall of Fame

Tutti i contributor saranno riconosciuti nel README!

```markdown
## Contributors

- [@wizwally](https://github.com/wizwally) - Creator
- [@tu_username](https://github.com/tu_username) - [Contributo]
```

## 💬 Comunicazione

**Dove discutere:**

- **GitHub Issues**: Bug, feature requests
- **GitHub Discussions**: Domande generali, show & tell
- **Discord**: Real-time chat (link TBD)
- **Reddit**: r/homeassistant, r/esp32

**Regole comunicazione:**

✅ **DO:**
- Sii rispettoso e costruttivo
- Fornisci contesto e dettagli
- Condividi log/screenshot quando utile
- Cerca prima di chiedere
- Help others when you can

❌ **DON'T:**
- Flame/troll/spam
- Chiedere "funziona su Arduino Uno?" (no, serve ESP32)
- Pretendere support immediato
- Off-topic noise

## 📜 Licenza

Contribuendo, accetti che il tuo codice sia rilasciato sotto **GPL-3.0 License** come il resto del progetto.

**Significa:**
- ✅ Codice open source
- ✅ Modifiche devono restare open source
- ✅ Attribution richiesta
- ❌ No uso proprietario senza condividere modifiche

Vedi [LICENSE](../LICENSE) per dettagli completi.

## ❓ Domande?

Non sicuro di qualcosa?

1. Leggi [FAQ](#) (TBD)
2. Cerca nelle Issues chiuse
3. Apri Discussion su GitHub
4. Chiedi su Discord

**Non esistono domande stupide!** Siamo tutti qui per imparare. 🚀

---

## 🙏 Grazie!

Ogni contributo, grande o piccolo, è apprezzato!

From fixing typos to architecting new features, **you make this project better**. ❤️

Happy hacking! 🔮

---

**Ultimo aggiornamento:** Aprile 2026