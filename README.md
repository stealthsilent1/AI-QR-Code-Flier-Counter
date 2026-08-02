# QR Code Flyer Counter

Print QR codes that send people to **any website** (yours or anyone else's,
like `pauseai.info`) while **counting every scan** — with no company in the
middle, nothing that expires, no ads, and no one who can hold your printed
codes hostage later.

## How it works

A QR code pointed straight at `pauseai.info` can't be counted — the scan goes
phone → their site, and you're not in the path. So the QR code points at
**this page instead**, which counts the scan and instantly forwards the
visitor on:

```
phone scans code
   → your page (github.io) — records the scan in GoatCounter, ~a quarter second
   → forwards to the destination (e.g. pauseai.info)
```

This is exactly what paid "dynamic QR" services do; here you own the middle
step. Bonus: because the printed code points at *your* page, you can change
where any batch of flyers leads later — by editing one line — **without
reprinting anything**.

The pieces:

1. **[QR Code Monkey](https://www.qrcode-monkey.com)** — makes the static
   codes for free, no account. Static is what you want: the URL it encodes is
   this page, which never needs to change.
2. **This repo on GitHub Pages** — the free counting-and-forwarding page.
3. **[GoatCounter](https://www.goatcounter.com)** — open source, free for
   non-commercial use. Already wired in:
   dashboard at <https://stealthsilent.goatcounter.com>.

## Setup

### 1. Add your flyer batches (~2 min)

Open [`index.html`](index.html) and find the `DESTINATIONS` map near the top
of the script — the only part you ever edit:

```js
var DESTINATIONS = {
  "pauseai-library":    "https://pauseai.info",
  "pauseai-coffeeshop": "https://pauseai.info",
  "example-batch":      "https://example.org"
};
```

One line per flyer batch: a short tag (lowercase, no spaces) and the website
that batch should lead to. Two batches may share a destination — they're
still counted separately, so you can compare which locations pull.

### 2. Turn on GitHub Pages (~2 min)

1. In this repo on GitHub: **Settings → Pages**.
2. Under **Build and deployment**: Source **Deploy from a branch**, pick your
   default branch, folder `/ (root)`, save.
3. After a minute the page is live at:

   ```
   https://stealthsilent1.github.io/AI-QR-Code-Flier-Counter/
   ```

4. Test it: open
   `https://stealthsilent1.github.io/AI-QR-Code-Flier-Counter/?src=pauseai-library`
   — you should land on pauseai.info a moment later, and the scan should
   appear at <https://stealthsilent.goatcounter.com> as `/pauseai-library`.

### 3. Make the QR codes (~5 min)

1. Go to <https://www.qrcode-monkey.com> and enter the URL **for this page
   with the batch's tag** — *not* the destination site:

   ```
   https://stealthsilent1.github.io/AI-QR-Code-Flier-Counter/?src=pauseai-library
   ```

2. Download as **PNG at 1000px or larger** (or SVG) so it prints crisply.
3. Repeat with a different `?src=` tag for each batch.
4. **Test-scan every code with your phone before printing.**

(Or generate them offline: `pip install "qrcode[pil]"` then
`python tools/make_qr.py https://stealthsilent1.github.io/AI-QR-Code-Flier-Counter/ pauseai-library pauseai-coffeeshop`
— writes print-ready PNGs into `qr-codes/`.)

### 4. Read your numbers

Open <https://stealthsilent.goatcounter.com>. Each batch is its own row:

```
/pauseai-library      42
/pauseai-coffeeshop   17
```

## Changing where printed flyers point

Edit the destination URL in the `DESTINATIONS` map and commit. Every flyer
already out in the world now forwards to the new address. This is the
"dynamic QR" feature the paid services charge for — except nothing expires
and nobody can turn it off but you.

## Notes

- **Scans with a mistyped or removed tag are never lost** — they're counted
  under `/untagged/...`, and the visitor sees a page listing all known
  destinations instead of being stranded.
- **The forward is fast** (typically under half a second) and never waits
  more than 1.5s on counting — if GoatCounter is unreachable, visitors are
  forwarded anyway.
- **Privacy:** GoatCounter uses no cookies and collects no personal data, so
  no cookie banner is needed.
- **Why not point codes straight at the destination?** You'd get zero data,
  and you could never change where a printed flyer leads.
