import esp32
import machine
import time
import _thread
from ledstrip import LEDStrip  # Assicurati di avere ledstrip.py caricato
from machine import Pin


# CONFIGURAZIONE
LED_PIN    = 18   # GPI18 → DIN strip WS2812
NUM_LEDS   = 32
MOTION_PIN = 8    # GPIO7 ← segnale da MG24
ALIVE_PIN  = 7    # GPIO8 → segnale animation on a MG24
 
SLEEP_TIMEOUT_MS = 20_000  # 30 secondi
STANDBY_WAIT_MS  = 20_000   # 30 secondi extra prima di deep sleep


# Gruppi LED
GROUPS = {
    0: [0, 19, 20, 25, 26, 31],
    1: [1, 2, 17, 18, 21, 22, 23, 24, 27, 28, 29, 30],
    2: list(range(3, 17))
}

# Stato condiviso
active = True
last_motion_time = time.ticks_ms()
anim_thread_started = False
 
# GPIO setup
alive_pin = machine.Pin(ALIVE_PIN, machine.Pin.OUT)
alive_pin.on()  # subito HIGH all'avvio

motion_pin = machine.Pin(MOTION_PIN, machine.Pin.IN)
esp32.wake_on_ext1(pins=(Pin(MOTION_PIN,),), level=esp32.WAKEUP_ANY_HIGH)

# LEDStrip init
leds = LEDStrip(LED_PIN, NUM_LEDS, GROUPS)

# ISR per impulsi da MG24
def motion_interrupt(pin):
    global last_motion_time, active, anim_thread_started
    last_motion_time = time.ticks_ms()
    if not active:
        print("📡 Movimento durante standby → riattivo animazione")
        active = True
        if not anim_thread_started:
            anim_thread_started = True
            _thread.start_new_thread(animation_loop, ())

motion_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=motion_interrupt)

# Thread animazione LED
def animation_loop():
    global active, anim_thread_started
    print("Starting animation thread")
    
    # Colori iniziali
    leds.set_group_color(0, (0, 230, 100))  # Core grills
    leds.set_group_color(1, (0, 255, 30))   # Inner
    leds.set_group_color(2, (0, 255, 30))   # Ring
    
    while active:
        leds.pulse(duration=1)
    leds.clear()
    # Fade solo del gruppo 0
    leds.fade_in(duration = 1, group_id = 0)
    # Core grills soft standby
    anim_thread_started = False

# Thread monitor timeout → standby → deep sleep
def motion_monitor():
    global active
    print("Starting monitor thread")
    while True:
        delta = time.ticks_diff(time.ticks_ms(), last_motion_time)
        if delta > SLEEP_TIMEOUT_MS:
            print("🏁 Timeout: stop animazione, standby")
            active = False
            t0 = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), t0) < STANDBY_WAIT_MS:
                if active:
                    print("🔄 Movimento durante standby → annullo sleep")
                    break
                time.sleep(0.5)
            if not active:
                print("💤 Deep sleep")
                alive_pin.off()
                leds.fade_out(duration = 1, group_id = 0)
                time.sleep_ms(100)  # tempo per MG24 di leggere LOW
                machine.deepsleep()
        time.sleep(0.5)

# Avvio thread
_thread.start_new_thread(animation_loop, ())
_thread.start_new_thread(motion_monitor, ())

# Loop principale
while True:
    time.sleep(1)
