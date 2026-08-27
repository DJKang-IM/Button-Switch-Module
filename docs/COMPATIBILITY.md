# Vendor Compatibility

Supported endoscope consoles and gateway environments for BSM.

---

## Supported Vendors

| Vendor | Console Series | Short Trigger Actions | BSM Status |
|--------|----------------|----------------------|------------|
| **Olympus** | EVIS LUCERA / ELITE / X1 | Release, Print, DVR Start | ✅ Supported |
| **Fujifilm** | ELUXEO / ELUXEO 7000 | Release, Print | ✅ Supported |
| **Pentax** | EPK-i / EPK-i7010 | External Record | ✅ Supported |

> Pin mapping varies by vendor, model, and firmware version. Not included in this public repository.

---

## Gateway Software Compatibility

| Gateway | Capture Hotkey | BSM Config |
|---------|----------------|------------|
| Olympus IPLEX Gateway | F11 | `KEY_F11` (default) |
| Fujifilm GW-SU | F11 | `KEY_F11` (default) |
| Pentax nStream | F11 | `KEY_F11` (default) |
| Other (custom) | Verify in settings | Change `CAPTURE_KEY` |

---

## Freeze vs Short Trigger

| Action | Monitor Freeze | Short Output | BSM Capture |
|--------|----------------|--------------|-------------|
| Freeze only | ✅ | ❌ (most models) | ❌ |
| Freeze + Release | ✅ | ✅ | ✅ |
| DVR Record Start | — | ✅ | ✅ |
| Print | — | ✅ | ✅ |

**Key point:** BSM triggers on actions that produce a short signal. Vendor-specific console configuration or pin mapping ensures Freeze alone produces both freeze and short simultaneously.

---

## Test Environment

| Item | Details |
|------|---------|
| MCU | Arduino Pro Micro (ATmega32U4, 16 MHz) |
| Optocoupler | PC816 |
| OS | Windows 10/11 64-bit |
| USB | USB 2.0, HID Keyboard |

---

## Unsupported / Caution

| Item | Reason |
|------|--------|
| Legacy consoles without short output | No external recorder terminals |
| All-in-one endoscope systems | Short pins not accessible |
| USB 3.0 hub passthrough | Possible HID latency — direct PC connection recommended |
| macOS / Linux gateway | HID behavior unverified (developed for Windows) |

---

## Compatibility Requests

To request BSM compatibility for a new console model, open a GitHub Issue with:

- Vendor and model name
- Console firmware version
- Whether External Recorder / Print terminals exist (per service manual)
- Current gateway software in use
