#!/usr/bin/env python3
"""Generate static, print-ready QR codes for flyer batches.

Each tag becomes its own QR code pointing at BASE_URL?src=TAG, so every
flyer batch shows up as a separate row in GoatCounter.

Usage:
    pip install "qrcode[pil]"
    python tools/make_qr.py https://YOURNAME.github.io/AI-QR-Code-Flier-Counter/ \
        library-march coffeeshop-march bulletin-board

Writes qr-codes/qr-<tag>.png for each tag. Test-scan every code with a
phone before printing — the URL is baked in permanently.
"""

import sys
import urllib.parse
from pathlib import Path

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_Q
except ImportError:
    sys.exit('Missing dependency. Install with:  pip install "qrcode[pil]"')

OUT_DIR = Path(__file__).resolve().parent.parent / "qr-codes"


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} BASE_URL TAG [TAG ...]\n\n{__doc__}")

    base_url = sys.argv[1].rstrip("/") + "/"
    tags = sys.argv[2:]
    OUT_DIR.mkdir(exist_ok=True)

    for tag in tags:
        url = base_url + "?src=" + urllib.parse.quote(tag)
        # Error correction Q (25%) survives print smudges and worn paper;
        # box_size 20 yields roughly 1000px, crisp at typical flyer sizes.
        qr = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=20, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        out = OUT_DIR / f"qr-{tag}.png"
        qr.make_image(fill_color="black", back_color="white").save(out)
        print(f"{out}  ->  {url}")

    print(f"\n{len(tags)} code(s) written to {OUT_DIR}/. Test-scan before printing!")


if __name__ == "__main__":
    main()
