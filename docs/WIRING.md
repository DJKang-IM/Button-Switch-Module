# Wiring & Isolation Guide

Electrical connection between the BSM and the endoscope console.

---

## Electrical Isolation

Endoscope consoles are Class I/II medical devices. External MCUs **must be galvanically isolated**.

### PC816 Photocoupler

| PC816 Pin | Connection |
|-----------|------------|
| 1 (Anode) | Console short(+) |
| 2 (Cathode) | Console short(−) |
| 3 (Emitter) | Arduino GND |
| 4 (Collector) | Arduino INPUT_PIN (D2) |

- Input side (1–2): LED + current limiting resistor (330 Ω – 1 kΩ)
- Output side (3–4): Arduino `INPUT_PULLUP` — goes LOW on short

### Isolation Specifications

| Parameter | Value |
|-----------|-------|
| Isolation voltage | ≥ 2.5 kVrms |
| CTR (Current Transfer Ratio) | 50 – 600 % |
| Response time | ≤ 4 μs |

---

## Arduino Pin Layout

```
                    ┌─────────────────┐
    PC816 Col (4) ──►│ D2  (INPUT)     │
    PC816 Emm (3) ──►│ GND             │
                    │                 │
    USB ────────────►│ USB (5V power)  │
                    └─────────────────┘
                         Pro Micro
```

### Expansion Channels (BSM-4, planned)

| Channel | Arduino Pin | Purpose |
|---------|---------------|---------|
| CH1 | D2 | Primary short (Freeze/Release) |
| CH2 | D3 | Secondary trigger |
| CH3 | D4 | DVR Start |
| CH4 | D5 | Print |

---

## Signal Polarity

Endoscope console short signals are typically **dry contact (non-polarized)**.

Firmware default:

```cpp
#define ACTIVE_LOW  true   // short → LOW (pull-up released)
```

For active-high consoles, set `ACTIVE_LOW false`.

---

## Cabling

| Segment | Recommended Spec |
|---------|------------------|
| Console → PC816 | Shielded 2-core, AWG 24, ≤ 3 m |
| PC816 → Arduino | 2-core, AWG 26, ≤ 0.5 m |
| Arduino → PC (USB) | USB 2.0, ferrite bead recommended |

### Grounding

- Arduino GND and console GND connect **only through PC816**.
- Direct GND sharing (ground loop) is prohibited.

---

## Wiring Diagram

```
  Endoscope Console              BSM Unit
 ┌────────────┐               ┌─────────────┐
 │            │               │             │
 │  Short(+) ─┼──┐            │             │
 │  Short(−) ─┼──┤            │             │
 │            │  │  ┌──────┐  │  ┌────────┐ │
 └────────────┘  └──┤ PC816├──┼──┤Arduino │─┼── USB ──► Gateway PC
                    │      │  │  │Pro Micro│ │
                    └──────┘  │  └────────┘ │
                              │             │
                              └─────────────┘
```

---

## Precautions

1. Work with **console power OFF**
2. Do **not apply voltage** to short pins — dry contact tap only
3. PC816 LED current: 5 – 20 mA (330 Ω – 1 kΩ resistor required)
4. Use shielded cable if length exceeds 3 m
5. Pin mapping varies by vendor — see [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §6
