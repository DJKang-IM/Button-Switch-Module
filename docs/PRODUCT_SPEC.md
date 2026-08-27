# Button Switch Module — Product Specification

**Document Version:** 1.0  
**Last Updated:** 2026-08-27  
**Product Name:** Button Switch Module (BSM)  
**Category:** Endoscopy gateway capture automation hardware

---

## 1. Overview

The Button Switch Module (BSM) is a signal conversion device that detects the endoscope console's external recorder trigger (short) signal and automatically sends a capture hotkey (`F11`) to the gateway PC via USB HID.

It replaces pedal-based capture, allowing physicians to capture PACS-ready images with a Freeze action alone.

---

## 2. Applications

- GI endoscopy suites (ERCP, EGD, colonoscopy)
- Olympus · Fujifilm · Pentax console + gateway (PACS-integrated) environments
- Suites where pedal capture causes posture instability or back strain

---

## 3. Functional Specifications

| Parameter | Specification |
|-----------|---------------|
| Input | Endoscope console short signal (dry contact) |
| Input channels | 1ch (expandable to 4ch) |
| Isolation | PC816 photocoupler, ≥ 2.5 kVrms input–output |
| MCU | ATmega32U4 (Arduino Pro Micro / Leonardo compatible) |
| Output | USB HID Keyboard — `F11` press + release |
| Debounce | 50 ms (configurable in firmware) |
| Response latency | Short detection → key injection ≤ 100 ms |
| Power | USB 5 V (gateway PC bus power) |
| Current draw | ≤ 50 mA (typical) |
| Operating temperature | 10 – 40 °C |
| Dimensions (unit) | 60 × 40 × 20 mm (with enclosure, estimated) |
| Weight | ≤ 80 g |

---

## 4. Operation Sequence

```
[1] Physician: presses endoscope Freeze button
         ↓
[2] Console: monitor freeze + (when configured) short signal output
         ↓
[3] PC816: isolates short signal, passes to Arduino GPIO
         ↓
[4] Arduino: edge detect → debounce → F11 HID injection
         ↓
[5] Gateway SW: receives F11 → captures frame → stores to PACS
```

### Comparison with Pedal Capture

| | Pedal | BSM |
|---|-------|-----|
| Operation | Freeze + pedal | Freeze only |
| Posture stability | Low (foot operation) | High (hands only) |
| Capture timing | Separate step after freeze | Simultaneous with freeze |
| Installation | USB HID pedal | BSM + short wiring |
| Console modification | None | None (signal tap only) |

---

## 5. Hardware Block Diagram

```
┌─────────────────┐     short      ┌──────────┐    GPIO    ┌──────────────┐
│ Endoscope       │ ──────────────►│  PC816   │──────────►│   Arduino    │
│ Console         │   (dry contact) │ Optocoupl│           │  ATmega32U4  │
│ (Olympus/       │                 │   er     │           │              │
│  Fujifilm/       │                 └──────────┘           └──────┬───────┘
│  Pentax)         │                                               │ USB HID
└─────────────────┘                                                ▼
                                                          ┌──────────────┐
                                                          │   Gateway    │
                                                          │  PC (F11)    │
                                                          │  → PACS      │
                                                          └──────────────┘
```

---

## 6. Pin Mapping (Proprietary)

Console short output pins vary by **vendor, model, and firmware version**.

| Vendor | Trigger Action | Pin Location |
|--------|----------------|--------------|
| Olympus | Release / Print / DVR Start | 🔒 Proprietary |
| Fujifilm | Release / Print | 🔒 Proprietary |
| Pentax | External Record | 🔒 Proprietary |

> Pin mapping is provided during on-site installation. Not included in this public repository.

---

## 7. Firmware

- **File:** `firmware/arduino/button_switch_module.ino`
- **Board:** Arduino Leonardo / Pro Micro (ATmega32U4, native USB)
- **Library:** `Keyboard.h` (Arduino built-in)
- **Configurable parameters:**
  - `CAPTURE_KEY` — capture hotkey (default `F11`)
  - `DEBOUNCE_MS` — debounce interval (default 50 ms)
  - `INPUT_PIN` — short detection GPIO (default pin 2)
  - `ACTIVE_LOW` — short polarity (default true)

---

## 8. Installation Requirements

### Gateway PC
- Windows 10/11 (64-bit)
- One USB 2.0+ port
- Gateway capture hotkey: `F11` (or modify firmware)

### Endoscope Console
- External recorder (short) output terminals
- Confirm "External Recorder" / "Print" / "DVR" trigger pins in service manual

### Tools
- Arduino IDE 2.x or PlatformIO
- Multimeter (for short pin verification)
- Vendor-specific signal cable (provided on-site)

---

## 9. Quality & Safety

| Item | Details |
|------|---------|
| Galvanic isolation | PC816 photocoupler; endoscope and MCU fully isolated |
| Fail-safe | Pedal capture can remain as backup if short is not detected |
| EMI | Shielded cables recommended; ferrite bead on Arduino USB recommended |
| Console impact | Signal tap only; no firmware or video path modification |

---

## 10. Product Variants (Roadmap)

| Model | Description | Status |
|-------|-------------|--------|
| BSM-1 | Single channel, fixed F11 | ✅ Current |
| BSM-4 | 4ch input, multi-trigger | 🔜 Planned |
| BSM-PRO | OLED status display, capture log | 🔜 Planned |

---

## 11. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-08-27 | Initial public release |
