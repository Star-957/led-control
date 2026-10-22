# Turn ON motherboard ARGB-header LEDs to white via the OpenRGB SDK.
# Same Direct-mode / resize approach as fans_off.py, just a different target color.
import sys, time
try:
    from openrgb import OpenRGBClient
    from openrgb.utils import RGBColor, ZoneType, DeviceType
except Exception as e:
    print("openrgb-python missing:", e); sys.exit(3)

WHITE = RGBColor(255, 255, 255)
RESIZE_TO = 120  # legacy assumption; verify actual controller and LED count first

def connect(retries=12):
    last = None
    for _ in range(retries):
        try:
            return OpenRGBClient(name="led-control-leds-white")
        except Exception as e:
            last = e; time.sleep(1.5)
    print("Could not connect to OpenRGB server on 127.0.0.1:6742:", last)
    sys.exit(2)

cli = connect()
time.sleep(1)
print("Detected devices:", [d.name for d in cli.devices])

targets = [d for d in cli.devices if d.type == DeviceType.MOTHERBOARD]
if not targets:
    print("No motherboard device matched; falling back to ALL devices.")
    targets = list(cli.devices)

for d in targets:
    try:
        modes = [m.name for m in d.modes]
        if "Direct" in modes:
            try: d.set_mode("Direct")
            except Exception as me: print("  set Direct skip", d.name, me)
        for z in d.zones:
            try:
                if z.type in (ZoneType.LINEAR, ZoneType.MATRIX):
                    before = len(z.leds)
                    try:
                        z.resize(RESIZE_TO)
                        print("  resized zone '%s' %d -> %d LEDs" % (z.name, before, len(z.leds)))
                    except Exception as re:
                        print("  resize skip", z.name, re)
                try: z.set_color(WHITE)
                except Exception as ce: print("  zone color skip", z.name, ce)
            except Exception as ze:
                print("  zone skip", d.name, getattr(z, "name", "?"), ze)
        try: d.set_color(WHITE)
        except Exception: pass
        print("WHITE:", d.name)
    except Exception as de:
        print("  device skip", d.name, de)

print("Done. Keep OpenRGB running in the tray (Direct mode needs OpenRGB to keep driving the headers).")
