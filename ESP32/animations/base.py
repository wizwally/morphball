class LEDAnimation:
    def __init__(self, led_strip):
        self.led_strip = led_strip
        self.running = False

    def start(self):
        self.running = True

    def update(self):
        raise NotImplementedError

    def stop(self):
        self.running = False

    def is_finished(self):
        return False

    def standby(self):
        self.led_strip.clear()
