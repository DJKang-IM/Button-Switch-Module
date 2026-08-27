/*
 * Button Switch Module (BSM) — Arduino Firmware
 *
 * Detects endoscope console short (dry contact) signal via PC816
 * optocoupler and sends USB HID capture key to gateway PC.
 *
 * Board: Arduino Leonardo / Pro Micro (ATmega32U4)
 * Library: Keyboard.h (built-in)
 *
 * (c) 2026 DJKang-IM — MIT License
 */

#include "Keyboard.h"

// ── Configuration ──────────────────────────────────────────────
#define INPUT_PIN       2          // Short signal input (via PC816)
#define CAPTURE_KEY     KEY_F11    // Gateway capture hotkey
#define DEBOUNCE_MS     50         // Debounce interval (ms)
#define ACTIVE_LOW      true       // true: short pulls pin LOW

// Optional: status LED on pin 13 (built-in)
#define STATUS_LED      LED_BUILTIN

// ── State ──────────────────────────────────────────────────────
volatile bool  signalActive  = false;
volatile bool  triggerPending = false;
unsigned long  lastTriggerMs  = 0;
unsigned long  lastDebounceMs = 0;
bool           lastPinState   = HIGH;

// ── Setup ──────────────────────────────────────────────────────
void setup() {
  pinMode(INPUT_PIN, INPUT_PULLUP);
  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(STATUS_LED, LOW);

  Keyboard.begin();
  delay(1000);  // Allow USB enumeration before first key press
}

// ── Main Loop ──────────────────────────────────────────────────
void loop() {
  bool currentState = digitalRead(INPUT_PIN);

  // Detect edge (short onset)
  if (currentState != lastPinState) {
    lastDebounceMs = millis();
  }

  if ((millis() - lastDebounceMs) > DEBOUNCE_MS) {
    bool isActive = ACTIVE_LOW ? (currentState == LOW) : (currentState == HIGH);

    if (isActive && !signalActive) {
      signalActive = true;
      triggerPending = true;
    } else if (!isActive && signalActive) {
      signalActive = false;
    }
  }

  lastPinState = currentState;

  // Fire capture key on short onset (rising edge of trigger)
  if (triggerPending && (millis() - lastTriggerMs) > DEBOUNCE_MS) {
    sendCaptureKey();
    triggerPending = false;
    lastTriggerMs = millis();
  }
}

// ── Send HID capture keystroke ─────────────────────────────────
void sendCaptureKey() {
  digitalWrite(STATUS_LED, HIGH);

  Keyboard.press(CAPTURE_KEY);
  delay(30);
  Keyboard.release(CAPTURE_KEY);

  delay(50);
  digitalWrite(STATUS_LED, LOW);
}
