# Installation Guide

Step-by-step procedure for installing the Button Switch Module (BSM) in an endoscopy suite.

---

## Prerequisites

- [ ] BSM unit + PC816 module + signal cable
- [ ] Arduino IDE 2.x installed
- [ ] Administrator access on gateway PC
- [ ] Endoscope console service manual (for short pin location)
- [ ] Multimeter

---

## Step 1 — Upload Firmware

1. Open `firmware/arduino/button_switch_module.ino` in Arduino IDE.
2. Board: **Arduino Leonardo** (or Pro Micro, ATmega32U4)
3. Port: select BSM USB port
4. Click **Upload**

### Change Capture Key (if needed)

If the gateway capture hotkey is not `F11`, modify `CAPTURE_KEY` at the top of the firmware:

```cpp
#define CAPTURE_KEY  KEY_F11   // Change to KEY_F10, KEY_F12, etc.
```

---

## Step 2 — Connect BSM to Gateway PC

1. Connect BSM USB to the gateway PC.
2. In Windows Device Manager, confirm it appears as **HID Keyboard Device**.
3. Open Notepad and manually trigger a short signal to verify `F11` input.

> ⚠️ BSM coexists with other keyboards without conflict. It operates as an HID composite device.

---

## Step 3 — Wire Endoscope Console

1. Work with **console power OFF**.
2. Identify short output pins per service manual or on-site pin mapping document.
3. Connect PC816 input side (pins 1–2) to the short pins.
4. Connect PC816 output side (pins 3–4) to BSM INPUT pin + GND.

```
Console short(+) ──► PC816 pin 1
Console short(−) ──► PC816 pin 2
PC816 pin 3      ──► Arduino D2 (INPUT_PULLUP)
PC816 pin 4      ──► Arduino GND
```

Details: [`WIRING.md`](WIRING.md)

---

## Step 4 — Verify Operation

### 4-1. Short Signal Check (Multimeter)

1. Console power ON
2. Perform Freeze + Release (or vendor-specific trigger action)
3. Verify resistance across short pins: open → **0 Ω (short)**

### 4-2. Capture Check

1. Launch gateway software, confirm endoscope video feed
2. Press Freeze button
3. Confirm capture image appears in gateway software
4. Confirm PACS storage

### 4-3. Timing Check

Capture should occur within 100 ms of freeze. If latency is high:

- Adjust debounce value (`DEBOUNCE_MS`)
- Check cable length and ground noise

---

## Step 5 — Retire Existing Pedal

After BSM installation, keep the existing USB HID pedal as **backup** or disconnect it.

If both BSM and pedal are connected simultaneously, both may send `F11`. Disconnect the pedal after confirming BSM operation.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No capture on freeze | Short pin not wired / wrong pin mapping | Verify short with multimeter, recheck pins |
| Double capture | Insufficient debounce / both edges trigger | Increase `DEBOUNCE_MS`, check edge config |
| Intermittent miss | Noise / poor cable contact | Replace shielded cable, re-solder PC816 |
| Wrong key injected | Firmware key misconfiguration | Check `CAPTURE_KEY` |
| Arduino not recognized | USB cable / driver | Try different port and cable |

---

## Maintenance

- **Monthly:** Measure short pin contact resistance (verify open circuit at rest)
- **Quarterly:** Verify PC816 operation (LED on/off)
- **On console firmware update:** Confirm short pin assignments unchanged
