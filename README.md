# Button Switch Module (BSM)

**Endoscope Freeze → Gateway Auto-Capture Module**

Automatically captures PACS-ready images from the endoscope console Freeze action — no capture pedal required.

---

## Problem

In endoscopy suites, console video is routed to two destinations:

```
Endoscope Console
    ├─► Endoscope Monitor  (physician view)
    └─► Gateway PC           (capture · PACS storage)
```

The conventional capture workflow uses a **gateway foot pedal**. When pressed, a USB HID module sends `F11` (or a vendor-specific hotkey) to trigger capture.

| Issue | Cause |
|-------|-------|
| Back / knee strain | Maintaining pedal position throughout the procedure |
| Image shake | Post-freeze posture collapse while stepping on the pedal |
| Redundant motion | Freeze with fingers → pedal with foot (dual operation) |

---

## Solution

The **Button Switch Module (BSM)** detects the endoscope console's **external recorder trigger (short) signal** and automatically sends a capture keystroke to the gateway PC.

```
Endoscope Console ── short signal ──► [PC816 isolation] ──► Arduino ──► USB HID ──► F11 ──► Gateway capture
         ▲
    Short occurs on Freeze / Release / Print
    (external recorder output pins)
```

The physician only needs to press **Freeze**. The pedal is no longer required.

---

## How It Works

1. Olympus, Fujifilm, Pentax, and other endoscope consoles output a **dry-contact short signal** on specific pins during DVR recording, Release (print), and similar actions.
2. A plain Freeze action often does **not** produce a short — **vendor/model-specific pin mapping** is the core of BSM.
3. A `PC816` optocoupler provides galvanic isolation between the medical device and the MCU.
4. The Arduino detects the short edge and sends `F11` via USB HID.
5. Gateway software captures and stores to PACS as before.

> ⚠️ **Pin mapping tables are proprietary.** They vary by vendor, model, and console firmware version, and require on-site calibration.

---

## Kit Contents

| Component | Role |
|-----------|------|
| BSM unit (Arduino Pro Micro / Leonardo) | Short detection · HID key injection |
| PC816 × N | Endoscope ↔ MCU galvanic isolation |
| Signal cable (vendor-specific connector) | Console short pins → BSM input |
| USB cable | BSM → Gateway PC |

Full specifications: [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)

---

## Quick Start

1. Connect BSM to a USB port on the gateway PC.
2. Wire the console short output pins through PC816 to the BSM input. ([`docs/WIRING.md`](docs/WIRING.md))
3. Upload the Arduino firmware. ([`firmware/arduino/button_switch_module.ino`](firmware/arduino/button_switch_module.ino))
4. Confirm the gateway capture hotkey is `F11` (modify firmware if different).
5. Verify Freeze → auto-capture behavior.

Installation details: [`docs/INSTALLATION.md`](docs/INSTALLATION.md)

---

## Compatibility

| Vendor | Status | Notes |
|--------|--------|-------|
| Olympus | ✅ Tested | Pin mapping varies by model |
| Fujifilm | ✅ Tested | Pin mapping varies by model |
| Pentax | ✅ Tested | Pin mapping varies by model |

Details: [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md)

---

## Repository Structure

```
button-switch-module/
├── README.md
├── docs/
│   ├── PRODUCT_SPEC.md      # Product specification
│   ├── INSTALLATION.md      # Installation guide
│   ├── WIRING.md            # Wiring & isolation guide
│   └── COMPATIBILITY.md     # Vendor compatibility
├── firmware/
│   └── arduino/
│       └── button_switch_module.ino
└── assets/
    └── block_diagram.svg
```

---

## Safety & Compliance

- BSM performs **signal detection and key injection only** — it does not modify the endoscope video path.
- PC816 optocoupler isolates the medical device power domain from the MCU. ([IEC 60601-1 concept](docs/WIRING.md#electrical-isolation))
- Verify hospital medical device management policies and IT requirements before installation.

---

## License

MIT License — [`LICENSE`](LICENSE)

---

## Contact

GitHub Issues: [https://github.com/DJKang-IM/Button-Switch-Module/issues](https://github.com/DJKang-IM/Button-Switch-Module/issues)
