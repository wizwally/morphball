import time
import math
from animations.base import LEDAnimation

class PulseAnimation(LEDAnimation):
    def __init__(self, led_strip, brightness=0.8, speed=0.02):
        super().__init__(led_strip)
        self.brightness = brightness
        self.speed = speed
        self.i = 0
        self.direction = 1
        self.last_update = time.ticks_ms()

    def update(self):
        if not self.running:
            return

        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_update) < int(self.speed * 1000):
            return

        self.last_update = now
        self.i += self.direction * 2

        if self.i >= 200:
            self.direction = -1
            self.i = 200
        elif self.i <= 0:
            self.direction = 1
            self.i = 0

        factor = math.pow(math.sin(self.i * math.pi / 200), 2) * self.brightness
        self.led_strip._apply_brightness(factor)
