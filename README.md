# QR Code Flyer Counter

Count how many people scan the QR codes on your printed flyers — with **no
company in the middle**, nothing that expires, no ads, and no one who can hold
your printed codes hostage later.

The recipe:

1. **A static QR code** (never expires, encodes a plain URL you control) made
   with [QR Code Monkey](https://www.qrcode-monkey.com) — truly free, static
   codes only, no account needed.
2. **A page you control** — this repo, hosted free on GitHub Pages.
3. **[GoatCounter](https://www.goatcounter.com)** — open source, free for
   non-commercial use — counting visits via one script line in `index.html`.

Give each flyer batch its own tag (`?src=library-march`,
`?src=coffeeshop-march`) and you can compare which locations pull.

Total setup is about 15 minutes.

---

## Setup

### 1. Get a GoatCounter account (~3 min)

1. Go to <https://www.goatcounter.com> and click **Sign up**.
2. Pick a code — this becomes your dashboard address, e.g.
   `mysite.goatcounter.com`.
3. In [`index.html`](index.html), replace **both** occurrences of `MYCODE`
   with the code you picked (one in the `<script data-goatcounter=...>` line,
   one in the `<noscript>` fallback).

### 2. Turn on GitHub Pages (~2 min)

1. In this repo on GitHub: **Settings → Pages**.
2. Under **Build and deployment**, set Source to **Deploy from a branch**,
   pick your default branch and the `/ (root)` folder, and save.
3. After a minute your page is live at:

   ```
   https://YOURNAME.github.io/AI-QR-Code-Flier-Counter/
   ```

   Open it once and confirm the visit shows up in your GoatCounter dashboard.
   (GoatCounter ignores your own visits only if you enable that in its
   settings — otherwise you'll see yourself, which is a good first test.)

   If you have a custom domain (like `knightstables.net`), you can point it at
   this page instead — same setup, nicer URL on the flyer.

### 3. Make the QR code(s) (~5 min)

1. Decide on a tag for each flyer batch. Short, lowercase, no spaces:
   `library-march`, `coffeeshop-march`, `bulletin-board`.
2. Go to <https://www.qrcode-monkey.com> and enter the URL **with the tag**:

   ```
   https://YOURNAME.github.io/AI-QR-Code-Flier-Counter/?src=library-march
   ```

3. Download as **PNG at 1000px or larger** (or SVG) so it prints crisply.
4. Repeat with a different `?src=` value for each batch. One code per batch.
5. **Test-scan every code with your phone before printing.** The code is
   static — the URL is baked in permanently — so a typo means reprinting.

### 4. Read your numbers

Open `https://MYCODE.goatcounter.com`. Each batch shows up as its own row:

```
/?src=library-march      42
/?src=coffeeshop-march   17
/?src=bulletin-board      3
```

That's it. Nothing expires, and no third party sits between your printed
codes and your page.

---

## Optional: generate QR codes locally

If you'd rather not use any website at all, `tools/make_qr.py` generates the
same static QR codes offline:

```sh
pip install "qrcode[pil]"
python tools/make_qr.py https://YOURNAME.github.io/AI-QR-Code-Flier-Counter/ \
    library-march coffeeshop-march bulletin-board
```

This writes one print-ready PNG per tag into `qr-codes/`.

## Notes

- **Why static QR codes?** "Dynamic" QR codes route scans through the
  provider's redirect service. If the provider shuts down, changes pricing,
  or expires your free trial, every flyer you've printed goes dead. A static
  code encodes your URL directly — it works as long as your page exists.
- **Why the `?src=` tag works:** GoatCounter normally ignores query strings,
  so a small snippet in `index.html` folds the `src` tag back into the
  recorded path. See the comments in that file.
- **Visitors without JavaScript** are still counted via the `<noscript>`
  tracking pixel (they appear under `/noscript`, without a batch tag).
- **Privacy:** GoatCounter doesn't use cookies and doesn't collect personal
  data, so no cookie banner is needed.
