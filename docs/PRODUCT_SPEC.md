# Button Switch Module — 제품 사양서

**문서 버전:** 1.0  
**최종 수정:** 2026-08-27  
**제품명:** Button Switch Module (BSM)  
**분류:** 내시경 게이트웨이 캡처 자동화 하드웨어

---

## 1. 개요

Button Switch Module(BSM)은 내시경 콘솔의 외부 기록 트리거(short) 신호를 감지하여, 게이트웨이 PC에 캡처 단축키(`F11`)를 USB HID로 자동 전송하는 신호 변환 모듈입니다.

기존 페달 기반 캡처 방식을 대체하여, 의사의 Freeze 조작만으로 PACS 저장용 이미지 캡처를 수행합니다.

---

## 2. 적용 분야

- ERCP / EGD / Colonoscopy 등 소화기 내시경 검사실
- Olympus · Fujifilm · Pentax 내시경 콘솔 + 게이트웨이(PACS 연동) 환경
- 페달 캡처로 인한 자세 불안정 · 허리 부담 개선이 필요한 검사실

---

## 3. 기능 사양

| 항목 | 사양 |
|------|------|
| 입력 | 내시경 콘솔 short 신호 (접점, dry contact) |
| 입력 채널 | 1ch (확장 시 최대 4ch) |
| 절연 | PC816 photocoupler, 입력–출력 간 ≥ 2.5 kVrms |
| MCU | ATmega32U4 (Arduino Pro Micro / Leonardo 호환) |
| 출력 | USB HID Keyboard — `F11` 키 press + release |
| 디바운스 | 50 ms (펌웨어 설정 가능) |
| 응답 지연 | Short 감지 → 키 전송 ≤ 100 ms |
| 전원 | USB 5 V (게이트웨이 PC 버스 전원) |
| 소비 전류 | ≤ 50 mA (typical) |
| 동작 온도 | 10 – 40 °C |
| 크기 (본체) | 60 × 40 × 20 mm (케이스 포함, 예상) |
| 무게 | ≤ 80 g |

---

## 4. 동작 시퀀스

```
[1] 의사: 내시경 Freeze 버튼 누름
         ↓
[2] 내시경 콘솔: 모니터 화면 freeze + (설정된 동작 시) short 신호 출력
         ↓
[3] PC816: short 신호를 절연하여 Arduino GPIO로 전달
         ↓
[4] Arduino: falling/rising edge 감지 → debounce → F11 HID 전송
         ↓
[5] 게이트웨이 SW: F11 수신 → 현재 화면 캡처 → PACS 저장
```

### 기존 페달 방식과 비교

| | 페달 방식 | BSM |
|---|-----------|-----|
| 조작 | Freeze + 페달 | Freeze only |
| 자세 안정성 | 낮음 (발 조작) | 높음 (손만 사용) |
| 캡처 타이밍 | Freeze 후 별도 | Freeze와 동시 |
| 설치 | USB HID 페달 | BSM + short 배선 |
| 내시경 개조 | 없음 | 없음 (신호 탭만) |

---

## 5. 하드웨어 블록 다이어그램

```
┌─────────────────┐     short      ┌──────────┐    GPIO    ┌──────────────┐
│  내시경 콘솔     │ ──────────────►│  PC816   │──────────►│   Arduino    │
│  (Olympus/      │   (dry contact) │ Optocoupl│           │  ATmega32U4  │
│   Fujifilm/     │                 │   er     │           │              │
│   Pentax)       │                 └──────────┘           └──────┬───────┘
└─────────────────┘                                               │ USB HID
                                                                  ▼
                                                         ┌──────────────┐
                                                         │  게이트웨이   │
                                                         │  PC (F11)    │
                                                         │  → PACS      │
                                                         └──────────────┘
```

---

## 6. 핀 매핑 (비공개)

내시경 콘솔의 short 출력 핀은 **벤더 · 모델 · 콘솔 펌웨어 버전**에 따라 다릅니다.

| 벤더 | 트리거 동작 | 핀 위치 |
|------|-------------|---------|
| Olympus | Release / Print / DVR Start | 🔒 비공개 |
| Fujifilm | Release / Print | 🔒 비공개 |
| Pentax | External Record | 🔒 비공개 |

> 핀 매핑 정보는 현장 설치 시 제공됩니다. 본 공개 저장소에는 포함되지 않습니다.

---

## 7. 펌웨어

- **파일:** `firmware/arduino/button_switch_module.ino`
- **보드:** Arduino Leonardo / Pro Micro (ATmega32U4, native USB)
- **라이브러리:** `Keyboard.h` (Arduino built-in)
- **설정 가능 파라미터:**
  - `CAPTURE_KEY` — 캡처 단축키 (기본 `F11`)
  - `DEBOUNCE_MS` — 디바운스 시간 (기본 50 ms)
  - `INPUT_PIN` — short 감지 GPIO (기본 pin 2)
  - `ACTIVE_LOW` — short 극성 (기본 true)

---

## 8. 설치 요구사항

### 게이트웨이 PC
- Windows 10/11 (64-bit)
- USB 2.0 이상 포트 1개
- 게이트웨이 캡처 단축키: `F11` (또는 펌웨어에서 변경)

### 내시경 콘솔
- 외부 기록(short) 출력 단자 보유
- 콘솔 서비스 매뉴얼상 "External Recorder" / "Print" / "DVR" 트리거 핀 확인

### 도구
- Arduino IDE 2.x 또는 PlatformIO
- 멀티미터 (short 핀 확인용)
- 벤더별 신호 케이블 (현장 제공)

---

## 9. 품질 · 안전

| 항목 | 내용 |
|------|------|
| 전기적 절연 | PC816 photocoupler, 내시경 전원계와 MCU 완전 분리 |
| Fail-safe | Short 미감지 시 기존 페달 방식 병행 사용 가능 |
| EMI | 케이블 차폐 권장, Arduino USB ferrite bead 권장 |
| 내시경 영향 | 신호 탭(tap)만 수행, 콘솔 펌웨어 · 영상 경로 무변경 |

---

## 10. 제품 변형 (로드맵)

| 모델 | 설명 | 상태 |
|------|------|------|
| BSM-1 | Single channel, F11 고정 | ✅ 현재 |
| BSM-4 | 4ch 입력, 다중 트리거 | 🔜 계획 |
| BSM-PRO | OLED 상태 표시, 캡처 로그 | 🔜 계획 |

---

## 11. 개정 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| 1.0 | 2026-08-27 | 최초 공개 |
