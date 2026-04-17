# 🤝 Contributing to Morphball

Thank you for your interest in contributing to the Metroid Morph Ball project!

## 🌟 How You Can Contribute

### 1. 🐛 Report Bugs

If you find a problem:

1. **Search first** among [existing Issues](https://github.com/wizwally/morphball/issues)
2. If it doesn't exist, open a new Issue with:
   - ✅ Clear problem description
   - ✅ Steps to reproduce
   - ✅ Hardware/software used
   - ✅ Logs/screenshots if possible
   - ✅ Expected vs. observed behavior

**Issue Template:**

```markdown
**Description:**
[Describe the bug]

**Steps to reproduce:**
1. 
2. 
3. 

**Expected behavior:**
[What should happen]

**Observed behavior:**
[What happens instead]

**Environment:**
- Version: MicroPython/ESPHome X.Y
- Hardware: ESP32-S3 / MG24
- OS: [if relevant]

**Logs/Screenshots:**
[Add here]
```

### 2. 💡 Propose New Features

Have an idea?

1. Open an Issue with `enhancement` tag
2. Describe:
   - Problem it solves
   - Proposed solution
   - Alternatives considered
   - Mockups/sketches if relevant

### 3. 📝 Improve Documentation

Documentation is never enough!

**Areas to help:**
- Translations (IT, ES, DE, FR)
- Additional tutorials
- Troubleshooting tips
- Video guides
- Improved diagrams/schematics

**Process:**
1. Fork repo
2. Modify files in `/docs`
3. Pull Request

### 4. 💻 Contribute Code

#### Development Environment Setup

```bash
# Clone
git clone https://github.com/wizwally/morphball.git
cd morphball

# Branch for feature
git checkout -b feature/feature-name

# Work on code
# ...

# Commit
git add .
git commit -m "feat: clear description"

# Push
git push origin feature/feature-name

# Open PR on GitHub
```

#### Code Style

**Python (MicroPython):**

```python
# PEP 8 style
# Descriptive names
# Comments in English preferred

class LEDStrip:
    """Manages WS2812B LED strip."""
    
    def set_color(self, color: tuple) -> None:
        """
        Sets RGB color.
        
        Args:
            color: Tuple (R, G, B) with values 0-255
        """
        pass
```

**YAML (ESPHome):**

```yaml
# 2-space indentation
# Descriptive comments
# snake_case naming

sensor:
  - platform: template
    name: "Descriptive Name"
    # Explanatory comment if complex logic
    lambda: |-
      return value;
```

**C++ (MG24):**

```cpp
// Camel case for functions
// UPPER_CASE for constants
// English comments preferred

const float ACCELERATION_THRESHOLD = 2.5;

void readIMU() {
    // Reads accelerometer data
}
```

#### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adds rainbow LED effect
fix: corrects deep sleep wake
docs: updates README with new instructions
refactor: optimizes animation loop
test: adds test for motion detection
```

**Common types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no logic change)
- `refactor`: Code refactoring
- `test`: Add/modify tests
- `chore`: Maintenance tasks

#### Testing

**Before PR:**

```bash
# Test MicroPython
mpremote connect /dev/ttyUSB0
>>> import main
>>> # Verify works

# Test ESPHome
esphome compile morphball.yaml
# ✓ No compilation errors

# Hardware test
# ✓ LEDs work
# ✓ Motion detection OK
# ✓ Sleep cycle correct
```

**Test checklist:**
- [ ] Code compiles without errors
- [ ] Feature works as expected
- [ ] Doesn't break existing functionality
- [ ] Documentation updated if necessary

### 5. 🎨 Contribute LED Animations

New animations always welcome!

**MicroPython:**

```python
# ESP32/animations/my_effect.py
from animations.base import Animation
import time

class MyEffectAnimation(Animation):
    """Effect description."""
    
    def run(self, param1=default):
        """
        Args:
            param1: Parameter description
        """
        # Implementation
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
        // Comments on logic
```

## 📋 Pull Request Process

### 1. Clear Description

```markdown
**Type:** [Feature/Bugfix/Docs/Refactor]

**Description:**
[What this PR does]

**Motivation:**
[Why it's necessary]

**Testing:**
[How you tested]

**Screenshots/Video:**
[If applicable]

**Breaking Changes:**
[If present, list here]

**Checklist:**
- [ ] Code tested
- [ ] Docs updated
- [ ] Clear commit messages
- [ ] No conflicts with main
```

### 2. Code Review

- Respond to feedback constructively
- Update code if requested
- Squash commits if requested

### 3. Merge

After approval:
- Maintainer merges
- Feature branch deleted
- Celebrate! 🎉

## 🎯 Priority Areas

Contributions especially welcome in:

**High priority:**
- [ ] **Gesture recognition** - Shake, roll, tilt detection
- [ ] **Battery monitoring** - Voltage/percentage
- [ ] **Alexa/Google Home** integration
- [ ] **Mobile app** (React Native/Flutter)
- [ ] **Multi-ball sync** - Communication protocol

**Medium priority:**
- [ ] **Audio feedback** - Speaker integration
- [ ] **Charging dock** design
- [ ] **Alternative animations**
- [ ] **Power optimization**
- [ ] **PCB design**

**Low priority (but welcome!):**
- [ ] Documentation translations
- [ ] Video tutorials
- [ ] Case studies / build logs
- [ ] Alternative form factors

## 💬 Communication

**Where to discuss:**

- **GitHub Issues**: Bugs, feature requests
- **GitHub Discussions**: General questions, show & tell
- **Discord**: Real-time chat (link TBD)
- **Reddit**: r/homeassistant, r/esp32

**Communication rules:**

✅ **DO:**
- Be respectful and constructive
- Provide context and details
- Share logs/screenshots when useful
- Search before asking
- Help others when you can

❌ **DON'T:**
- Flame/troll/spam
- Ask "does it work on Arduino Uno?" (no, needs ESP32)
- Demand immediate support
- Off-topic noise

## 📜 License

By contributing, you agree that your code will be released under **GPL-3.0 License** like the rest of the project.

**Means:**
- ✅ Open source code
- ✅ Modifications must remain open source
- ✅ Attribution required
- ❌ No proprietary use without sharing modifications

See [LICENSE](../../LICENSE) for complete details.

## ❓ Questions?

Not sure about something?

1. Read [FAQ](#) (TBD)
2. Search closed Issues
3. Open Discussion on GitHub
4. Ask on Discord

**There are no stupid questions!** We're all here to learn. 🚀

---

## 🙏 Thank You!

Every contribution, big or small, is appreciated!

From fixing typos to architecting new features, **you make this project better**. ❤️

Happy hacking! 🔮

---

**Last updated:** April 2026
