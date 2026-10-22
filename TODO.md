# TODO

## backlight and brightness

The backlight is a separate two-wire series LED string (about 26.9V at 10mA), not on the FPC.

- [x] Identify the backlight leads (red +, black -) and forward voltage (~26.9V at 10mA).
- [ ] Build the driver: 5V -> boost module (set ~32V) -> ~470 ohm -> string, low-side
      >= 50V N-MOSFET on Teensy pin 33.
- [ ] Basic backlight on/off.
- [ ] Backlight brightness levels via PWM, with up/down keys (and/or the MX brightness keys).
- [ ] Optional: auto-dim/idle-off after no keypresses.

### Proximity sensor

The keyboard has a separate cable for the hand-proximity sensor (the one that wakes the backlight when hands approach).

It is a single brown wire, so it is almost certainly a bare capacitive electrode: Logitech's sensing chip was on the removed main board.

The Teensy might be able to measure it with the Teensyduino `CapacitiveSensor` library (supports Teensy 4):

```
Teensy pin 34 (send) --> 1-10M ohm resistor --> Teensy pin 35 (receive) --> brown wire
```

- [ ] Check if a bigger resistor senses from farther away but reacts more slowly (1M ~ touch, ~10M for a few cm).
- [ ] Confirm what the brown wire connects to inside the keyboard (copper pad, foil, plate).
- [ ] Check it is isolated: brown wire to the backlight black wire and to a few FPC pins should all read OL.
- [ ] Get resistors in the 1M-10M range (many cheap kits stop at 1M).
- [ ] Test sketch `tools/Proximity_Probe`: print raw `CapacitiveSensor` readings over serial while moving a hand closer/farther; try 1M, 4.7M and 10M to pick the range.
- [ ] Pick a threshold with automatic baseline tracking (so slow drift from temperature and humidity is ignored).
- [ ] Use it: backlight on when hands are near, fade out after a timeout.
- [] Check whether the same cable also carries the ambient-light sensor (MX Keys adjusts the backlight to room light); if so, scale brightness with it. - I think Ambient light sensor is in origina board under the power-on/power-off button.

## persistence and polish

- [x] Persist `fn_lock` and `os_mode` to the Teensy EEPROM so settings survive a reboot.
- [ ] Optional: NKRO instead of 6KRO for full n-key rollover.
- [ ] Optional: a build/config flag block at the top of the sketch for the above toggles.

## Notes

- Keep the matrix (`normal` / `modifier` / `media`) and pin arrays as the single source of truth; new layers (fn-lock default, os-mode remap) should transform on top of them rather than duplicating the tables.
- Verify every MX function-key legend against the physical unit before mapping; layouts differ between MX Keys, MX Keys S, and MX Keys Mini.
