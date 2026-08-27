# Button Switch Module (BSM)

**내시경 Freeze → 게이트웨이 자동 캡처 모듈**

페달 캡처 없이, 내시경 콘솔의 Freeze 동작만으로 PACS 저장용 이미지를 자동 캡처합니다.

---

## 문제

내시경 검사실에서는 콘솔 영상이 두 경로로 송출됩니다.

```
내시경 콘솔
    ├─► 내시경 모니터  (의사 시야)
    └─► 게이트웨이 PC    (캡처 · PACS 저장)
```

기존 캡처 방식은 **게이트웨이 페달**을 밟아 USB HID 모듈이 `F11`(또는 벤더별 캡처 단축키)을 전송하는 구조입니다.

| 문제 | 원인 |
|------|------|
| 허리 · 무릎 부담 | 검사 내내 페달 위치 유지 |
| 화면 흔들림 | Freeze 후 페달을 밟으며 자세 붕괴 |
| 불필요한 동작 | 손가락으로 Freeze → 발로 페달 (이중 조작) |

---

## 해결

**Button Switch Module(BSM)** 은 내시경 콘솔의 **외부 기록 트리거(short) 신호**를 감지하여, 게이트웨이 PC에 캡처 키 입력을 자동 전송합니다.

```
내시경 콘솔 ── short signal ──► [PC816 절연] ──► Arduino ──► USB HID ──► F11 ──► 게이트웨이 캡처
         ▲
    Freeze / Release / Print 시
    외부 기록장비용 핀 short 발생
```

의사는 **Freeze 버튼만** 누르면 됩니다. 페달은 더 이상 필요하지 않습니다.

---

## 핵심 원리

1. 올림푸스 · 후지필름 · 펜탁스 등 내시경 콘솔은 DVR 녹화, Release(프린트) 등 특정 동작 시 **외부 기록장치용 short 신호**를 핀으로 출력합니다.
2. 일반 Freeze 동작만으로는 short가 나오지 않는 경우가 많습니다 — **벤더·모델별 핀 매핑**이 BSM의 핵심입니다.
3. `PC816` 광절연(optocoupler)으로 의료기기와 MCU를 전기적으로 분리합니다.
4. Arduino가 short edge를 감지하면 USB HID로 `F11` 키를 전송합니다.
5. 게이트웨이 소프트웨어가 기존과 동일하게 캡처 → PACS 저장을 수행합니다.

> ⚠️ **핀 매핑 테이블은 비공개**입니다. 벤더·모델·콘솔 펌웨어 버전에 따라 상이하며, 현장 캘리브레이션이 필요합니다.

---

## 제품 구성

| 구성품 | 역할 |
|--------|------|
| BSM 본체 (Arduino Pro Micro / Leonardo 계열) | Short 감지 · HID 키 전송 |
| PC816 × N | 내시경 ↔ MCU 전기적 절연 |
| 신호 케이블 (벤더별 커넥터) | 콘솔 short 핀 → BSM 입력 |
| USB 케이블 | BSM → 게이트웨이 PC |

자세한 사양은 [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)를 참고하세요.

---

## 빠른 시작

1. BSM을 게이트웨이 PC USB 포트에 연결합니다.
2. 내시경 콘솔 short 출력 핀을 PC816 경유하여 BSM 입력에 배선합니다. ([`docs/WIRING.md`](docs/WIRING.md))
3. Arduino 펌웨어를 업로드합니다. ([`firmware/arduino/button_switch_module.ino`](firmware/arduino/button_switch_module.ino))
4. 게이트웨이 캡처 단축키가 `F11`인지 확인합니다. (다를 경우 펌웨어 수정)
5. Freeze → 자동 캡처 동작을 확인합니다.

설치 상세: [`docs/INSTALLATION.md`](docs/INSTALLATION.md)

---

## 호환성

| 벤더 | 지원 상태 | 비고 |
|------|-----------|------|
| Olympus | ✅ 테스트됨 | 모델별 핀 매핑 상이 |
| Fujifilm | ✅ 테스트됨 | 모델별 핀 매핑 상이 |
| Pentax | ✅ 테스트됨 | 모델별 핀 매핑 상이 |

상세: [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md)

---

## 저장소 구조

```
button-switch-module/
├── README.md
├── docs/
│   ├── PRODUCT_SPEC.md      # 제품 사양서
│   ├── INSTALLATION.md      # 설치 가이드
│   ├── WIRING.md            # 배선 · 절연 가이드
│   └── COMPATIBILITY.md     # 벤더별 호환성
├── firmware/
│   └── arduino/
│       └── button_switch_module.ino
└── assets/
    └── block_diagram.svg
```

---

## 안전 · 규정

- BSM은 **신호 감지 · 키 입력 변환**만 수행하며, 내시경 영상 경로를 변경하지 않습니다.
- PC816 광절연으로 의료기기 전원계와 MCU를 분리합니다. ([IEC 60601-1 개념 준수](docs/WIRING.md#전기적-절연))
- 현장 설치 시 의료기기 관리 규정 및 병원 IT 정책을 확인하세요.

---

## 라이선스

MIT License — [`LICENSE`](LICENSE)

---

## Hugging Face Space

데모 · 문서: [https://huggingface.co/spaces/DJKang-IM/button-switch-module](https://huggingface.co/spaces/DJKang-IM/button-switch-module)

---

## 문의

GitHub Issues: [https://github.com/DJKang-IM/button-switch-module/issues](https://github.com/DJKang-IM/button-switch-module/issues)
