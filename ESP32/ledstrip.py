import machine
import neopixel


class LEDStrip:
    def __init__(self, pin_num, num_leds, group_map):
        self.pin = machine.Pin(pin_num)
        self.n = num_leds
        self.strip = neopixel.NeoPixel(self.pin, self.n)
        self.group_map = group_map  # es: {0: [...], 1: [...], 2: [...]}
        self.group_colors = {k: (0, 0, 0) for k in group_map.keys()}
        self.brightness = 0.8

    def set_group_color(self, group_ids, color):
        """Imposta un colore statico su uno o più gruppi"""
        if isinstance(group_ids, int):
            group_ids = [group_ids]

        for gid in group_ids:
            self.group_colors[gid] = color
            for i in self.group_map[gid]:
                self.strip[i] = color
        self.strip.write()

    def clear(self):
        """Spegne tutti i LED"""
        for i in range(self.n):
            self.strip[i] = (0, 0, 0)
        self.strip.write()

    def clear_group(self, group_ids=None):
        """Spegne uno o più gruppi specifici o tutti"""
        if group_ids is None:
            target_groups = self.group_map.keys()
        elif isinstance(group_ids, int):
            target_groups = [group_ids]
        else:
            target_groups = group_ids

        for gid in target_groups:
            for i in self.group_map[gid]:
                self.strip[i] = (0, 0, 0)
        self.strip.write()

    def _apply_brightness(self, factor, group_ids=None):
        """Applica l'intensità ai LED dei gruppi specificati o a tutti"""
        if group_ids is None:
            target_groups = self.group_map.keys()
        else:
            target_groups = group_ids

        for gid in target_groups:
            color = self.group_colors.get(gid, (0, 0, 0))
            for i in self.group_map[gid]:
                r = int(color[0] * factor)
                g = int(color[1] * factor)
                b = int(color[2] * factor)
                self.strip[i] = (r, g, b)
        self.strip.write()
