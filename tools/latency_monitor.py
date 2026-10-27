# /// script
# dependencies = ["hidapi"]
# ///
# Print the firmware's LATENCY_DEBUG timing output.
#
# The firmware prints over the Teensy "serial emulation" HID interface (vendor usage page
# 0xFFC9); this reads that interface directly.
#
#   uv run tools/latency_monitor.py      # until Ctrl+C
#   uv run tools/latency_monitor.py 10   # stop after 10 seconds
import sys
import time

import hid

TEENSY_VID, KEYBOARD_PID = 0x16C0, 0x04D0
SEREMU_USAGE_PAGE = 0xFFC9

seconds = float(sys.argv[1]) if len(sys.argv) > 1 else None

dev = next((d for d in hid.enumerate(TEENSY_VID, KEYBOARD_PID)
            if d["usage_page"] == SEREMU_USAGE_PAGE), None)
if not dev:
    sys.exit("no Teensy keyboard serial emulation interface found")

h = hid.device()
h.open_path(dev["path"])
buf = b""
end = time.time() + seconds if seconds else None
try:
    while end is None or time.time() < end:
        data = h.read(65, 200)
        if not data:
            continue
        buf += bytes(b for b in data if b)  # reports are zero padded
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            print(line.decode(errors="replace"), flush=True)
except KeyboardInterrupt:
    pass
finally:
    h.close()
