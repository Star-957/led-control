# Windows RGB LED Control — OpenRGB and Lian Li LCD Notes

Windows helpers for motherboard RGB / ARGB lighting through [OpenRGB](https://openrgb.org/), plus a technical report on **Lian Li TL Wireless LCD fan lighting and LCD backlights with L-Connect 3**.

[繁體中文](README-繁體.md) · [Lian Li LCD lighting report](docs/lian-li-tl-wireless-lcd-lighting.md)

## Choose the right control path

| Goal | What this repository provides |
|---|---|
| Set OpenRGB-detected motherboard lighting black or white | Legacy Python scripts and Windows launchers |
| Turn off TL Wireless LCD fan rings, fan displays and an 8.8-inch screen | A version-specific [L-Connect 3 report](docs/lian-li-tl-wireless-lcd-lighting.md), not a universal driver |
| Keep original LCD images when turning lights back on | Report explains backlight-only changes; legacy OpenRGB scripts do not control LCD content |

The report documents a separately tested local adapter. That machine-specific adapter, device identifiers, backups and vendor binaries are **not** bundled here. These legacy launchers do not control every RGB device or any Lian Li LCD.

## Legacy OpenRGB helpers

- `leds-off.cmd` invokes `fans_off.py`: requests black on motherboard devices, falling back to all detected devices if none are classified as a motherboard.
- `leds-white.cmd` invokes `leds_white.py`: requests white using the same selection.
- `setup-once.cmd` requests UAC, attempts OpenRGB installation through winget if missing, then lists detected devices. Its winget command automatically accepts package/source agreements; read those terms before choosing to run it, or install OpenRGB yourself.

Requirements: Windows, Python 3, `openrgb-python`, and a running OpenRGB SDK server on `127.0.0.1:6742`. The setup script does not install the Python package or explicitly enable the SDK server. Configure those separately. The two daily wrappers only call Python; they do not themselves elevate.

## Important limitations before running

The legacy code attempts Direct mode, requests **120 LEDs** for LINEAR/MATRIX zones, then writes color to zones and devices. This fixed resize request is not validated against each controller's supported limits. Inspect the actual LED count and back up profiles before use; no universal clamping or hardware-compatibility guarantee is made.

Many errors are caught and execution continues. A final `Done` message, a zero exit code or a detected device is **not** proof that all lighting changed. These scripts have not been newly hardware-tested as part of the report publication.

"Off" requests black on selected devices; it does not power down fans, controllers or LCD decoders. Unsupported keyboards and vendor-specific displays need their own controls. Lighting commands use localhost; setup/package installation needs network access, and third-party software has its own behavior and policies.

## Lian Li TL Wireless LCD report

The [technical report](docs/lian-li-tl-wireless-lcd-lighting.md) covers separate RGB/backlight commands, the wrong-renderer default that left TL fan rings black, preserving loaded images, and the difference between service acceptance and physical verification. It includes the tested version and explicit limits rather than claiming universal support.

## License

[MIT](LICENSE). No vendor binaries, decompiled vendor source or original LCD artwork are redistributed.
