// LED probe for the unused FPC pins (26-30), to find the Caps Lock and computer 1/2/3
// indicator LEDs without a multimeter.
//
// Steps through every ordered pair of probe pins: the "anode" pin is pulled up through the
// Teensy's internal pullup (~22k) and the "cathode" pin is driven low. The pullup limits the
// current to tens of microamps, so this is safe for any LED and any wiring, but the glow is
// faint - watch the keys in a dark room. All other pins stay high impedance.
//
// Build with USB type serial and open the serial monitor to see which pair is active:
//   arduino-cli compile --fqbn teensy:avr:teensy41:usb=serial tools/LED_Probe
//   arduino-cli upload  -p usb:<port> --fqbn teensy:avr:teensy41:usb=serial tools/LED_Probe
//   arduino-cli monitor -p usb:<port>
// Reflash the controller (usb=keyboard) afterwards.
//
#define HOLD_MS 3000 // how long each pair is held
#define GAP_MS  500  // all-off gap between pairs so changes are easy to spot
//
// FPC 26..30 map straight across to Teensy 26..30 (see README wiring table)
const byte probe_pins[] = {26, 27, 28, 29, 30};
const byte probe_count = sizeof(probe_pins);
//
// Function to float every probe pin (no pullup, not driven)
void all_off() {
  for (int i = 0; i < probe_count; i++) {
    pinMode(probe_pins[i], INPUT);
  }
}
//
void setup() {
  all_off();
  Serial.begin(9600);
  while (!Serial && millis() < 4000) {} // wait briefly for the serial monitor
  Serial.println("LED probe: FPC 26-30, anode = pullup, cathode = low");
}
//
void loop() {
  for (int a = 0; a < probe_count; a++) {
    for (int c = 0; c < probe_count; c++) {
      if (a == c) continue;
      all_off();
      delay(GAP_MS);
      pinMode(probe_pins[a], INPUT_PULLUP); // anode side: weak pullup to 3.3V
      pinMode(probe_pins[c], OUTPUT);       // cathode side: driven low
      digitalWrite(probe_pins[c], LOW);
      Serial.printf("anode FPC %d  ->  cathode FPC %d\n", probe_pins[a], probe_pins[c]);
      delay(HOLD_MS);
    }
  }
  all_off();
  Serial.println("---- cycle done, repeating ----");
}
