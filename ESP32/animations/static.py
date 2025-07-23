from animations.base import LEDAnimation

class StaticColor(LEDAnimation):
    def __init__(self, led_strip, color, standby_color=(5, 5, 5)):
        super().__init__(led_strip)
        self.color = color
        self.standby_color = standby_color

    def start(self):
        super().start()
        self.led_strip.set_group_color(list(self.led_strip.group_map.keys()), self.color)

    def update(self):
        pass

    def stop(self):
        super().stop()

    def standby(self):
        self.led_strip.set_group_color(list(self.led_strip.group_map.keys()), self.standby_color)
