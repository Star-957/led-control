# Lian Li TL Wireless LCD: turn off RGB and screens without losing images

Technical field report, 2026-10-23. Scope: an installed L-Connect 3 **2.1.23** setup with two TL Wireless LCD fan groups (five fans total) and one Universal Screen 8.8-inch display. This is a version-specific observation, not an official API or compatibility claim for every Lian Li controller.

## Summary

RGB rings, fan LCD backlights and the separate screen use different commands. Setting RGB black does not necessarily darken displays. A lighting-only adapter can set backlights to zero, then restore visible backlights and static white RGB while leaving already-loaded images or animations in place. Cooling stays a separate control path.

The owner physically verified the result on the tested machine: all targeted lights and displays became dark; after turning on, the original images returned and the previously unlit outer fan LEDs became white. This is one-machine acceptance, not a broad hardware test matrix.

## Observed local control chain

The installed service accepted JSON POST on loopback port 11021. Discover the configured port and connected devices; do not assume stable values on another installation. Device paths are UTF-8 encoded, Base64 encoded, then URL escaped in the query.

| Purpose | Observed action/type | Important behavior |
|---|---|---|
| Enumerate controllers | `action=SyncControllerList` | Use returned identities, not guessed USB paths |
| TL fan RGB | `action=Device`, `type=FanLightingSetting` | Static TL mode, both sides, explicit unrelated-model None sentinel |
| Fan LCD backlights | `type=SetBrightness` | LCD group plus brightness; no media replacement |
| 8.8-inch backlight | `type=SetScreenBrightness` | Independent of RGB |
| 8.8-inch RGB | `type=SetLightingEffectSetting` | Static white mode separate from display content |

Do not expose the local control port to a network. Authentication and remote-access security were not audited here. Service success alone does not prove physical lighting behavior.

## Why accepted TL RGB commands can leave black LEDs

Two fields were easy to get wrong in this installed version:

1. `Speed` is an enum **3–7**, not byte-scale brightness. The corrected request used `5`.
2. TL rendering needed `SLINFWMode=34` (`None`). Omitting it selected constructor default `Rainbow=0`. The renderer checked that unrelated SL-INF effect before the TL path, producing zero TL color data in this case.

The corrected request used `TLV2Mode=3` (static), `Scope=5` (both sides), `SLINFWMode=34`, `Speed=5`, and four white color entries. RGB brightness was 255 for On and 0 for Off. These observed internal enums are **not a complete ready-to-send universal request**: inventory, model checks, validation and backups remain necessary.

Both corrected cached groups selected TL static with SL-INF None. The static effect contained 30 frames instead of the earlier zero-filled 2048-frame result. The SDK's white-color power limit was preserved; equal RGB channels do not imply unrestricted current.

## Preserve images and cooling

Each On or Off operation sends six lighting/backlight requests: two RGB groups, two fan-LCD groups, one screen backlight and one screen RGB request. The final corrected On run used this six-request plan. No image upload, animation replacement, fan-curve change, pump control, firmware flash, service stop or vendor binary modification was involved.

Visible backlights were requested at 75 on the exposed scale, not a calibrated percentage of perceived brightness. Original content stayed loaded. Off means zero requested light/backlight, not proof that panel electronics or decoders are electrically powered down.

## Verification and limits

- Pure-plan tests rejected the wrong renderer field, invalid speed, cooling commands and unsupported models.
- All six calls in the final corrected On run were accepted; separate-screen brightness and white settings were read back.
- Five fans still reported nonzero RPM. Stored device configuration hashes did not change; RPM can follow existing curves.
- Fan LCD brightness lacked equivalent hardware readback, so physical observation remained necessary.
- Exact installed binary hashes and expected device counts gated the local adapter. App/hardware updates need renewed inspection.
- Reboot persistence was not tested. No startup task or resident helper was added. Applying another GUI profile can overwrite current lighting.
- Saved-profile replay is not an exact hardware snapshot: the original saved fan brightness was zero. A separate visible/white On action was needed.

## Backups and publication boundary

Before mutation, independently copy and hash-verify settings, profiles, device configuration, generated lighting config/cache and helper scripts. Do not overwrite live vendor settings wholesale while the service runs. Restoring stored device files could also restore older cooling settings; full recovery needs a controlled procedure.

This public report excludes machine identifiers, personal paths, original LCD artwork, raw logs, settings backups, decompiled vendor source and vendor binaries. The repository's legacy OpenRGB launchers are not the tested L-Connect adapter. No universal installer is supplied.

## Troubleshooting

If a fan LCD works but outer LEDs are black, verify the exact model, RGB brightness, TL static mode, valid speed enum and explicit unrelated-model None. If RGB is dark but the screen stays visible, check its independent backlight. When an API says success but nothing changes, verify group membership and inspect the hardware.

中文摘要：聯力風扇外圍 RGB、中央 LCD 背光、8.8 吋螢幕分開控制。本文記錄 TL LCD 外圍燈冇着嘅實際原因，以及保留原圖、唔改散熱設定嘅驗證方式；唔係廠商官方 API 或通用驅動。
