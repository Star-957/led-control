# Existing black/off entrypoint; implementation shared with the white launcher.
from led_control import set_led_color

if __name__ == '__main__':
    raise SystemExit(set_led_color((0, 0, 0), 'led-control-fans-off', 'OFF'))
