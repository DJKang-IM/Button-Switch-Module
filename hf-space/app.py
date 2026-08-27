"""
Button Switch Module (BSM) — Hugging Face Space
Interactive documentation and signal flow demo.
"""

import gradio as gr

OVERVIEW = """
## Button Switch Module (BSM)

**내시경 Freeze → 게이트웨이 자동 캡처 모듈**

페달 없이 내시경 콘솔의 Freeze 동작만으로 PACS 저장용 이미지를 자동 캡처합니다.

### 문제
- 게이트웨이 **페달** 캡처 → 의사 자세 붕괴 · 허리 부담 · **화면 흔들림**
- Freeze(손) + 페달(발) **이중 조작** 불필요

### 해결
내시경 콘솔의 **외부 기록 short 신호**를 PC816 광절연으로 감지 → Arduino가 USB HID `F11` 전송 → 게이트웨이 자동 캡처

### 신호 흐름
```
내시경 콘솔 ── short ──► PC816 ──► Arduino BSM ── USB HID ──► 게이트웨이 PC (F11) ──► PACS
```

### 호환 벤더
| 벤더 | 상태 |
|------|------|
| Olympus | ✅ |
| Fujifilm | ✅ |
| Pentax | ✅ |

> 핀 매핑은 벤더·모델별 비공개. 현장 캘리브레이션 필요.

### 링크
- 📦 [GitHub Repository](https://github.com/DJKang-IM/button-switch-module)
- 📄 [제품 사양서](https://github.com/DJKang-IM/button-switch-module/blob/main/docs/PRODUCT_SPEC.md)
- 🔧 [설치 가이드](https://github.com/DJKang-IM/button-switch-module/blob/main/docs/INSTALLATION.md)
- ⚡ [Arduino 펌웨어](https://github.com/DJKang-IM/button-switch-module/blob/main/firmware/arduino/button_switch_module.ino)
"""

SPEC_TABLE = """
| 항목 | 사양 |
|------|------|
| 입력 | Dry contact short (내시경 콘솔) |
| 절연 | PC816 photocoupler ≥ 2.5 kVrms |
| MCU | ATmega32U4 (Pro Micro / Leonardo) |
| 출력 | USB HID Keyboard — F11 |
| 응답 | ≤ 100 ms |
| 전원 | USB 5 V bus |
"""

COMPARISON = """
| | 페달 방식 | BSM |
|---|-----------|-----|
| 조작 | Freeze + 페달 | **Freeze only** |
| 자세 | 발 조작 → 흔들림 | 손만 사용 → **안정** |
| 설치 | USB HID 페달 | BSM + short 배선 |
| 내시경 개조 | 없음 | **없음** |
"""


def simulate_capture(freeze_pressed: bool, pedal_pressed: bool, mode: str):
    """Simulate capture behavior for pedal vs BSM mode."""
    if mode == "페달 방식 (기존)":
        if freeze_pressed and pedal_pressed:
            return (
                "✅ 캡처 성공 — 그러나 페달 밟으며 **자세 붕괴 · 화면 흔들림** 발생",
                "🔴 자세 안정성: 낮음",
            )
        elif freeze_pressed:
            return "⏸ Freeze됨 — 페달을 밟아야 캡처", "🟡 대기 중"
        else:
            return "▶ Live 영상", "⚪ 대기"
    else:  # BSM
        if freeze_pressed:
            return (
                "✅ **자동 캡처** — short 감지 → F11 → PACS 저장 (페달 불필요)",
                "🟢 자세 안정성: 높음",
            )
        else:
            return "▶ Live 영상", "⚪ 대기"


with gr.Blocks(title="Button Switch Module", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔬 Button Switch Module (BSM)")
    gr.Markdown(OVERVIEW)

    with gr.Tab("📋 제품 사양"):
        gr.Markdown(SPEC_TABLE)

    with gr.Tab("⚖️ 페달 vs BSM"):
        gr.Markdown(COMPARISON)
        with gr.Row():
            freeze = gr.Checkbox(label="Freeze 버튼 누름", value=False)
            pedal = gr.Checkbox(label="페달 밟음 (기존 방식)", value=False)
        mode = gr.Radio(
            choices=["페달 방식 (기존)", "BSM (Button Switch Module)"],
            value="BSM (Button Switch Module)",
            label="캡처 방식",
        )
        result = gr.Textbox(label="캡처 결과", interactive=False)
        stability = gr.Textbox(label="자세 안정성", interactive=False)

        inputs = [freeze, pedal, mode]
        for inp in inputs:
            inp.change(simulate_capture, inputs, [result, stability])

        gr.Examples(
            examples=[
                [True, True, "페달 방식 (기존)"],
                [True, False, "페달 방식 (기존)"],
                [True, False, "BSM (Button Switch Module)"],
                [False, False, "BSM (Button Switch Module)"],
            ],
            inputs=inputs,
            outputs=[result, stability],
        )

    with gr.Tab("🔗 리소스"):
        gr.Markdown(
            """
            - [GitHub — 소스 · 문서 · 펌웨어](https://github.com/DJKang-IM/button-switch-module)
            - [제품 사양서 (PRODUCT_SPEC.md)](https://github.com/DJKang-IM/button-switch-module/blob/main/docs/PRODUCT_SPEC.md)
            - [배선 가이드 (WIRING.md)](https://github.com/DJKang-IM/button-switch-module/blob/main/docs/WIRING.md)
            - [벤더 호환성 (COMPATIBILITY.md)](https://github.com/DJKang-IM/button-switch-module/blob/main/docs/COMPATIBILITY.md)
            """
        )

if __name__ == "__main__":
    demo.launch()
