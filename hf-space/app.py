"""
Button Switch Module (BSM) — Hugging Face Space
Interactive documentation and signal flow demo.
"""

import gradio as gr

OVERVIEW = """
## Button Switch Module (BSM)

**Endoscope Freeze → Gateway Auto-Capture Module**

Automatically captures PACS-ready images from the endoscope console Freeze action — no capture pedal required.

### Problem
- Gateway **pedal** capture → physician posture collapse, back strain, **image shake**
- Redundant dual operation: Freeze (hand) + pedal (foot)

### Solution
Detect endoscope console **external recorder short signal** via PC816 optocoupler → Arduino sends USB HID `F11` → gateway auto-capture

### Signal Flow
```
Endoscope Console ── short ──► PC816 ──► Arduino BSM ── USB HID ──► Gateway PC (F11) ──► PACS
```

### Supported Vendors
| Vendor | Status |
|--------|--------|
| Olympus | ✅ |
| Fujifilm | ✅ |
| Pentax | ✅ |

> Pin mapping is proprietary per vendor/model. On-site calibration required.

### Links
- 📦 [GitHub Repository](https://github.com/DJKang-IM/Button-Switch-Module)
- 📄 [Product Specification](https://github.com/DJKang-IM/Button-Switch-Module/blob/main/docs/PRODUCT_SPEC.md)
- 🔧 [Installation Guide](https://github.com/DJKang-IM/Button-Switch-Module/blob/main/docs/INSTALLATION.md)
- ⚡ [Arduino Firmware](https://github.com/DJKang-IM/Button-Switch-Module/blob/main/firmware/arduino/button_switch_module.ino)
"""

SPEC_TABLE = """
| Parameter | Specification |
|-----------|---------------|
| Input | Dry contact short (endoscope console) |
| Isolation | PC816 photocoupler ≥ 2.5 kVrms |
| MCU | ATmega32U4 (Pro Micro / Leonardo) |
| Output | USB HID Keyboard — F11 |
| Response | ≤ 100 ms |
| Power | USB 5 V bus |
"""

COMPARISON = """
| | Pedal | BSM |
|---|-------|-----|
| Operation | Freeze + pedal | **Freeze only** |
| Posture | Foot operation → shake | Hands only → **stable** |
| Installation | USB HID pedal | BSM + short wiring |
| Console mod | None | **None** |
"""


def simulate_capture(freeze_pressed: bool, pedal_pressed: bool, mode: str):
    """Simulate capture behavior for pedal vs BSM mode."""
    if mode == "Pedal (legacy)":
        if freeze_pressed and pedal_pressed:
            return (
                "✅ Capture OK — but **posture collapse and image shake** from stepping on pedal",
                "🔴 Posture stability: low",
            )
        elif freeze_pressed:
            return "⏸ Frozen — pedal required for capture", "🟡 Waiting"
        else:
            return "▶ Live video", "⚪ Idle"
    else:  # BSM
        if freeze_pressed:
            return (
                "✅ **Auto capture** — short detected → F11 → PACS (no pedal)",
                "🟢 Posture stability: high",
            )
        else:
            return "▶ Live video", "⚪ Idle"


with gr.Blocks(title="Button Switch Module", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔬 Button Switch Module (BSM)")
    gr.Markdown(OVERVIEW)

    with gr.Tab("📋 Specifications"):
        gr.Markdown(SPEC_TABLE)

    with gr.Tab("⚖️ Pedal vs BSM"):
        gr.Markdown(COMPARISON)
        with gr.Row():
            freeze = gr.Checkbox(label="Freeze button pressed", value=False)
            pedal = gr.Checkbox(label="Pedal pressed (legacy)", value=False)
        mode = gr.Radio(
            choices=["Pedal (legacy)", "BSM (Button Switch Module)"],
            value="BSM (Button Switch Module)",
            label="Capture method",
        )
        result = gr.Textbox(label="Capture result", interactive=False)
        stability = gr.Textbox(label="Posture stability", interactive=False)

        inputs = [freeze, pedal, mode]
        for inp in inputs:
            inp.change(simulate_capture, inputs, [result, stability])

        gr.Examples(
            examples=[
                [True, True, "Pedal (legacy)"],
                [True, False, "Pedal (legacy)"],
                [True, False, "BSM (Button Switch Module)"],
                [False, False, "BSM (Button Switch Module)"],
            ],
            inputs=inputs,
            outputs=[result, stability],
        )

    with gr.Tab("🔗 Resources"):
        gr.Markdown(
            """
            - [GitHub — source, docs, firmware](https://github.com/DJKang-IM/Button-Switch-Module)
            - [Product Specification (PRODUCT_SPEC.md)](https://github.com/DJKang-IM/Button-Switch-Module/blob/main/docs/PRODUCT_SPEC.md)
            - [Wiring Guide (WIRING.md)](https://github.com/DJKang-IM/Button-Switch-Module/blob/main/docs/WIRING.md)
            - [Vendor Compatibility (COMPATIBILITY.md)](https://github.com/DJKang-IM/Button-Switch-Module/blob/main/docs/COMPATIBILITY.md)
            """
        )

if __name__ == "__main__":
    demo.launch()
