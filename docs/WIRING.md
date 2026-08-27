# 배선 · 절연 가이드

BSM과 내시경 콘솔 간의 전기적 연결 방법입니다.

---

## 전기적 절연

내시경 콘솔은 Class I/II 의료기기로, 외부 MCU와 **반드시 절연**하여 연결해야 합니다.

### PC816 Photocoupler

| PC816 Pin | 연결 |
|-----------|------|
| 1 (Anode) | 콘솔 short(+) |
| 2 (Cathode) | 콘솔 short(−) |
| 3 (Emitter) | Arduino GND |
| 4 (Collector) | Arduino INPUT_PIN (D2) |

- 입력측(1–2): LED + current limiting resistor (330 Ω – 1 kΩ)
- 출력측(3–4): Arduino `INPUT_PULLUP` — short 시 LOW

### 절연 사양

| 항목 | 값 |
|------|-----|
| Isolation voltage | ≥ 2.5 kVrms |
| CTR (Current Transfer Ratio) | 50 – 600 % |
| Response time | ≤ 4 μs |

---

## Arduino 핀 배치

```
                    ┌─────────────────┐
    PC816 Col (4) ──►│ D2  (INPUT)     │
    PC816 Emm (3) ──►│ GND             │
                    │                 │
    USB ────────────►│ USB (5V power)  │
                    └─────────────────┘
                         Pro Micro
```

### 확장 채널 (BSM-4, 계획)

| 채널 | Arduino Pin | 용도 |
|------|-------------|------|
| CH1 | D2 | Primary short (Freeze/Release) |
| CH2 | D3 | Secondary trigger |
| CH3 | D4 | DVR Start |
| CH4 | D5 | Print |

---

## 신호 극성

내시경 콘솔 short 신호는 대부분 **dry contact (무극성 접점)** 입니다.

펌웨어 기본값:

```cpp
#define ACTIVE_LOW  true   // short → LOW (pull-up 해제)
```

일부 콘솔에서 active-high인 경우 `ACTIVE_LOW false`로 변경합니다.

---

## 케이블

| 구간 | 권장 사양 |
|------|-----------|
| 콘솔 → PC816 | 차폐 2-core, AWG 24, ≤ 3 m |
| PC816 → Arduino | 2-core, AWG 26, ≤ 0.5 m |
| Arduino → PC (USB) | USB 2.0, ferrite bead 권장 |

### 접지

- Arduino GND와 콘솔 GND는 **PC816을 통해서만** 연결됩니다.
- 직접 GND 공유(ground loop) 금지.

---

## 배선 다이어그램

```
  내시경 콘솔                    BSM 본체
 ┌────────────┐               ┌─────────────┐
 │            │               │             │
 │  Short(+) ─┼──┐            │             │
 │  Short(−) ─┼──┤            │             │
 │            │  │  ┌──────┐  │  ┌────────┐ │
 └────────────┘  └──┤ PC816├──┼──┤Arduino │─┼── USB ──► 게이트웨이 PC
                    │      │  │  │Pro Micro│ │
                    └──────┘  │  └────────┘ │
                              │             │
                              └─────────────┘
```

---

## 주의사항

1. **콘솔 전원 OFF** 후 배선 작업
2. short 핀에 **전압을 인가하지 않음** — dry contact tap only
3. PC816 LED 전류: 5 – 20 mA (330 Ω – 1 kΩ 저항 필수)
4. 케이블 길이 3 m 초과 시 차폐 케이블 필수
5. 핀 매핑은 벤더별로 상이 — [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §6 참고
