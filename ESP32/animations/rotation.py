import time
from animations.base import LEDAnimation

class RotationAnimation(LEDAnimation):
    def __init__(self, led_strip, group_id=2, brightness=0.8, speed=0.05):
        super().__init__(led_strip)
        self.group_id = group_id
        self.brightness = brightness
        self.speed = speed
        self.index = 0
        self.last_update = time.ticks_ms()
        self.leds = list(self.led_strip.group_map[group_id])

    def update(self):
        if not self.running:
            return

        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_update) < int(self.speed * 1000):
            return

        self.last_update = now
        num = len(self.leds)

        for i, led_index in enumerate(self.leds):
            dist = (i - self.index) % num
            factor = max(0.1, (1 - dist / num)) * self.brightness
            base_color = self.led_strip.group_colors.get(self.group_id, (50, 0, 50))
            r = int(base_color[0] * factor)
            g = int(base_color[1] * factor)
            b = int(base_color[2] * factor)
            self.led_strip.strip[led_index] = (r, g, b)

        self.led_strip.strip.write()
        self.index = (self.index + 1) % num
