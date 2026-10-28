"""Shared motherboard Direct-mode color control; importing it never touches hardware."""
import time


def set_led_color(rgb, client_name, label):
    try:
        from openrgb import OpenRGBClient
        from openrgb.utils import RGBColor, ZoneType, DeviceType
    except Exception as error:
        print('openrgb-python missing:', error)
        return 3

    color = RGBColor(*rgb)
    last = None
    for _ in range(12):
        try:
            client = OpenRGBClient(name=client_name)
            break
        except Exception as error:
            last = error
            time.sleep(1.5)
    else:
        print('Could not connect to OpenRGB server on 127.0.0.1:6742:', last)
        return 2

    time.sleep(1)
    print('Detected devices:', [device.name for device in client.devices])
    targets = [device for device in client.devices if device.type == DeviceType.MOTHERBOARD]
    if not targets:
        print('No motherboard device matched; falling back to ALL devices.')
        targets = list(client.devices)
    for device in targets:
        try:
            if 'Direct' in [mode.name for mode in device.modes]:
                try:
                    device.set_mode('Direct')
                except Exception as error:
                    print('  set Direct skip', device.name, error)
            for zone in device.zones:
                try:
                    if zone.type in (ZoneType.LINEAR, ZoneType.MATRIX):
                        before = len(zone.leds)
                        try:
                            zone.resize(120)  # OpenRGB clamps to the actual header maximum.
                            print("  resized zone '%s' %d -> %d LEDs" % (zone.name, before, len(zone.leds)))
                        except Exception as error:
                            print('  resize skip', zone.name, error)
                    try:
                        zone.set_color(color)
                    except Exception as error:
                        print('  zone color skip', zone.name, error)
                except Exception as error:
                    print('  zone skip', device.name, getattr(zone, 'name', '?'), error)
            try:
                device.set_color(color)
            except Exception:
                pass
            print(label + ':', device.name)
        except Exception as error:
            print('  device skip', device.name, error)
    print('Done. Keep OpenRGB running in the tray (Direct mode needs OpenRGB to keep driving the headers).')
    return 0
