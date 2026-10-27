# Make the Teensy 4 core poll the media-key interface at 8000Hz.
#
# The core's usb=keyboard descriptor (USB_KEYBOARDONLY in cores/teensy4/usb_desc.h) asks for
# the keyboard endpoint every microframe (bInterval 1 = 125us) but the media-key endpoint
# only every 8 (bInterval 4 = 1ms). The macro is defined there unconditionally, so a -D build
# flag can't override it; this edits it to 1. Re-run after every Teensyduino core update,
# then compile with --clean so the cached core is rebuilt.
#
#   uv run tools/patch_teensy_core.py                  # find the installed core(s)
#   uv run tools/patch_teensy_core.py <path/to/usb_desc.h>
import os
import re
import sys
from pathlib import Path


def find_cores():
    roots = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Arduino15",  # Windows
        Path.home() / ".arduino15",                               # Linux
        Path.home() / "Library" / "Arduino15",                    # macOS
    ]
    for root in roots:
        yield from (root / "packages" / "teensy" / "hardware" / "avr").glob(
            "*/cores/teensy4/usb_desc.h")


def patch(path):
    text = path.read_text()
    # the KEYMEDIA_INTERVAL line inside the USB_KEYBOARDONLY block only
    block = re.search(r"#elif defined\(USB_KEYBOARDONLY\)(.*?)#elif", text, re.S)
    if not block:
        print(f"{path}: no USB_KEYBOARDONLY block, skipped")
        return
    new_block, n = re.subn(r"(#define KEYMEDIA_INTERVAL\s+)\d+", r"\g<1>1", block.group(1))
    if n != 1:
        print(f"{path}: KEYMEDIA_INTERVAL not found, skipped")
        return
    if new_block == block.group(1):
        print(f"{path}: already patched")
        return
    path.write_text(text[:block.start(1)] + new_block + text[block.end(1):])
    print(f"{path}: media keys now poll every microframe (8000Hz)")


paths = [Path(p) for p in sys.argv[1:]] or list(find_cores())
if not paths:
    sys.exit("no Teensy core found; pass the path to cores/teensy4/usb_desc.h")
for p in paths:
    patch(p)
