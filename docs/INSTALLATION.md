# 설치 가이드

Button Switch Module(BSM)을 검사실에 설치하는 절차입니다.

---

## 사전 준비

- [ ] BSM 본체 + PC816 모듈 + 신호 케이블
- [ ] Arduino IDE 2.x 설치
- [ ] 게이트웨이 PC 관리자 권한
- [ ] 내시경 콘솔 서비스 매뉴얼 (short 핀 위치 확인용)
- [ ] 멀티미터

---

## Step 1 — 펌웨어 업로드

1. Arduino IDE에서 `firmware/arduino/button_switch_module.ino`를 엽니다.
2. 보드: **Arduino Leonardo** (또는 Pro Micro, ATmega32U4)
3. 포트: BSM USB 포트 선택
4. **Upload** 클릭

### 캡처 키 변경 (필요 시)

게이트웨이 SW의 캡처 단축키가 `F11`이 아닌 경우, 펌웨어 상단의 `CAPTURE_KEY`를 수정합니다.

```cpp
#define CAPTURE_KEY  KEY_F11   // KEY_F10, KEY_F12 등으로 변경
```

---

## Step 2 — BSM → 게이트웨이 PC 연결

1. BSM USB를 게이트웨이 PC에 연결합니다.
2. Windows 장치 관리자에서 **HID Keyboard Device**로 인식되는지 확인합니다.
3. 메모장을 열고 short 신호를 인위적으로 발생시켜 `F11` 입력이 들어오는지 확인합니다.

> ⚠️ BSM이 연결된 상태에서 다른 키보드와 동시 사용에 문제가 없습니다. HID composite로 동작합니다.

---

## Step 3 — 내시경 콘솔 배선

1. **콘솔 전원 OFF** 상태에서 작업합니다.
2. 서비스 매뉴얼 또는 현장 핀 매핑 문서에 따라 short 출력 핀을 확인합니다.
3. PC816 입력측(핀 1–2)을 short 핀에 연결합니다.
4. PC816 출력측(핀 3–4)을 BSM INPUT 핀 + GND에 연결합니다.

```
콘솔 short(+) ──► PC816 pin 1
콘솔 short(−) ──► PC816 pin 2
PC816 pin 3   ──► Arduino D2 (INPUT_PULLUP)
PC816 pin 4   ──► Arduino GND
```

상세: [`WIRING.md`](WIRING.md)

---

## Step 4 — 동작 확인

### 4-1. Short 신호 확인 (멀티미터)

1. 콘솔 전원 ON
2. Freeze + Release (또는 해당 벤더 트리거 동작) 수행
3. short 핀 간 저항: open → **0 Ω (short)** 전환 확인

### 4-2. 캡처 확인

1. 게이트웨이 SW 실행, 내시경 영상 수신 확인
2. Freeze 버튼 누름
3. 게이트웨이 SW에서 캡처 이미지 생성 확인
4. PACS 저장 확인

### 4-3. 타이밍 확인

Freeze 직후 100 ms 이내에 캡처가 발생해야 합니다. 지연이 크면:

- 디바운스 값(`DEBOUNCE_MS`) 조정
- 케이블 길이 · 접지 노이즈 점검

---

## Step 5 — 기존 페달 처리

BSM 설치 후 기존 USB HID 페달은 **백업용**으로 보관하거나 분리합니다.

동시 연결 시 BSM + 페달 모두 `F11`을 전송할 수 있으므로, BSM 정상 동작 확인 후 페달을 분리하는 것을 권장합니다.

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| Freeze해도 캡처 안 됨 | short 핀 미연결 / 핀 매핑 오류 | 멀티미터로 short 발생 확인, 핀 재확인 |
| 캡처가 2번 됨 | 디바운스 부족 / rising+falling 모두 트리거 | `DEBOUNCE_MS` 증가, edge 설정 확인 |
| 간헐적 미캡처 | 노이즈 / 케이블 접촉 불량 | 차폐 케이블 교체, PC816 재납땜 |
| F11 대신 다른 키 입력 | 펌웨어 키 설정 오류 | `CAPTURE_KEY` 확인 |
| Arduino 미인식 | USB 케이블 / 드라이버 | 다른 포트, 케이블 교체 |

---

## 유지보수

- **월 1회:** short 핀 접점 저항 측정 (open circuit 확인)
- **분기 1회:** PC816 동작 확인 (LED on/off)
- **콘솔 펌웨어 업데이트 시:** short 핀 변경 여부 확인
