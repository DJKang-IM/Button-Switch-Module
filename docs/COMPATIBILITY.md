# 벤더별 호환성

BSM이 지원하는 내시경 콘솔 및 게이트웨이 환경입니다.

---

## 지원 벤더

| 벤더 | 콘솔 시리즈 | Short 트리거 동작 | BSM 상태 |
|------|-------------|-------------------|----------|
| **Olympus** | EVIS LUCERA / ELITE / X1 | Release, Print, DVR Start | ✅ 지원 |
| **Fujifilm** | ELUXEO / ELUXEO 7000 | Release, Print | ✅ 지원 |
| **Pentax** | EPK-i / EPK-i7010 | External Record | ✅ 지원 |

> 핀 매핑은 벤더 · 모델 · 펌웨어 버전별로 다릅니다. 공개 저장소에 포함되지 않습니다.

---

## 게이트웨이 SW 호환성

| 게이트웨이 | 캡처 단축키 | BSM 설정 |
|------------|-------------|----------|
| Olympus IPLEX Gateway | F11 | `KEY_F11` (기본) |
| Fujifilm GW-SU | F11 | `KEY_F11` (기본) |
| Pentax nStream | F11 | `KEY_F11` (기본) |
| 기타 (커스텀) | 설정 확인 필요 | `CAPTURE_KEY` 변경 |

---

## Freeze vs Short 트리거

| 동작 | 모니터 Freeze | Short 출력 | BSM 캡처 |
|------|---------------|------------|----------|
| Freeze only | ✅ | ❌ (대부분) | ❌ |
| Freeze + Release | ✅ | ✅ | ✅ |
| DVR Record Start | — | ✅ | ✅ |
| Print | — | ✅ | ✅ |

**핵심:** BSM은 short 신호가 발생하는 트리거 동작에 연동됩니다. 벤더별로 Freeze 버튼 하나만으로 short + freeze가 동시에 발생하도록 **콘솔 설정 또는 핀 매핑**이 구성됩니다.

---

## 테스트 환경

| 항목 | 내용 |
|------|------|
| MCU | Arduino Pro Micro (ATmega32U4, 16 MHz) |
| Optocoupler | PC816 |
| OS | Windows 10/11 64-bit |
| USB | USB 2.0, HID Keyboard |

---

## 미지원 / 주의

| 항목 | 사유 |
|------|------|
| Short 출력 없는 구형 콘솔 | 외부 기록 단자 미탑재 |
| All-in-one 내시경 (일体型) | Short 핀 접근 불가 |
| USB 3.0 hub 경유 | HID 지연 가능 — PC 직결 권장 |
| macOS / Linux 게이트웨이 | HID 동작 확인 필요 (Windows 기준 개발) |

---

## 호환성 확인 요청

새로운 콘솔 모델의 BSM 호환성 확인은 GitHub Issues에 다음 정보를 등록해 주세요.

- 벤더 · 모델명
- 콘솔 펌웨어 버전
- 서비스 매뉴얼상 External Recorder / Print 단자 유무
- 현재 사용 중인 게이트웨이 SW
