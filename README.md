# led-control

One-click RGB off / RGB white for a PC with no bundled RGB software, using [OpenRGB](https://openrgb.org/) as the engine.

## Why this exists

My motherboard (ASUS ROG STRIX X870-A) and case fans (Lian Li SL V3) light up by default and there's no first-party app installed to turn that off — just the default rainbow cycling on the board's ARGB header. I'm a night-owl who wants the room dark to actually sleep, and didn't want to install a vendor's bloated RGB suite just to hit "off" once a day. OpenRGB already solves "control any RGB device from one place" — this repo is just two scripts and two double-click shortcuts wrapped around it so the daily action is one click, not a GUI hunt.

## What it does

- `leds-off.cmd` → turns all detected motherboard/ARGB-header LEDs off (black)
- `leds-white.cmd` → turns them all to plain white
- `setup-once.cmd` → one-time setup: installs OpenRGB via `winget` if missing, elevates once (UAC) so OpenRGB can see the board, and lists what it detected

Both `.cmd` files just call the matching Python script (`fans_off.py` / `leds_white.py`), which talks to the OpenRGB SDK over `127.0.0.1:6742`.

## Requirements

- Windows
- [OpenRGB](https://openrgb.org/) (the `setup-once.cmd` script installs it for you via `winget`)
- Python 3 with the `openrgb-python` package (`pip install openrgb-python`)
- A motherboard/ARGB header that OpenRGB actually detects — check with `setup-once.cmd` first

## Usage

1. Run `setup-once.cmd` once. It self-elevates (UAC prompt) because ASUS board LEDs need one admin pass to be controllable, installs OpenRGB if it isn't there, and prints the detected devices.
2. Keep OpenRGB running in the system tray — it has to stay open to keep driving the header in Direct mode.
3. Day to day: double-click `leds-off.cmd` or `leds-white.cmd`. Each pops one UAC prompt.

## How it works, briefly

OpenRGB exposes zones per device. Addressable (LINEAR/MATRIX) zones need to be in **Direct mode** before they can be resized or driven, and `openrgb-python`'s zone wrapper doesn't expose a "max LEDs" property — so both scripts force Direct mode, resize each addressable zone up to a generous count (OpenRGB clamps it to the header's real max), then set every zone and the whole device to the target color. That two-step "resize then color" order is the part that isn't obvious from the OpenRGB docs and is the main reason this isn't just a three-line script.

## Notes

- "Off" means every detected LED is set to black — if something still glows faintly, that device probably needs its own profile; not all RGB hardware responds identically to "black."
- Keyboards vary — if yours doesn't show up in `setup-once.cmd`'s device list, it's not controllable through this tool; most keyboards have a manual `Fn` + lighting key instead.
- Everything here is local: OpenRGB talks to your hardware over localhost, nothing leaves your machine.
- A Traditional Chinese version of this README is at [`README-繁體.md`](README-繁體.md).

## License

MIT
