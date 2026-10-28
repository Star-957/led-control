# Existing white/on entrypoint; implementation shared with the off launcher.
from led_control import set_led_color

if __name__ == '__main__':
    raise SystemExit(set_led_color((255, 255, 255), 'led-control-leds-white', 'WHITE'))
