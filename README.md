# QR Code Flyer Counter

Print QR codes that send people to **any website** (yours or anyone else's,
like `pauseai.info`) while **counting every scan** — with no company in the
middle, nothing that expires, no ads, and no one who can hold your printed
codes hostage later.

## How it works

A QR code pointed straight at `pauseai.info` can't be counted — the scan goes
phone → their site, and you're not in the path. So every QR code points at
**this site instead**, which counts the scan and instantly forwards the
visitor on:

```
phone scans code qr-017
   → your page (github.io) — records the scan in GoatCounter, ~a quarter second
   → forwards to wherever qr-017 is assigned (e.g. pauseai.info)
```

This is exactly what paid "dynamic QR" services do; here you own the middle
step. Because printed codes point at *your* page, you can change where any
code leads later **without reprinting anything**.

## The pieces

| File | What it is |
|---|---|
| [`manager.html`](manager.html) | **The control panel** — interactive table of all 500 codes: name, location, destination, notes, status, live scan counts. |
| [`codes.json`](codes.json) | The registry: 500 code slots (`qr-001` … `qr-500`). Edited via the manager. |
| [`index.html`](index.html) | The redirect page every QR code points at. Counts, then forwards. You never edit this. |
| [`tools/make_qr.py`](tools/make_qr.py) | Optional: generates print-ready QR code PNGs offline. |

Scan counting is [GoatCounter](https://www.goatcounter.com) (open source,
free for non-commercial use) — dashboard at
<https://stealthsilent.goatcounter.com>, already wired in.

## Setup

### 1. Turn on GitHub Pages (~2 min)

**Settings → Pages** → Source **Deploy from a branch** → default branch,
`/ (root)` → save. A minute later the site is live:

- Manager: `https://stealthsilent1.github.io/AI-QR-Code-Flier-Counter/manager.html`
- Redirect page (what QR codes encode): `https://stealthsilent1.github.io/AI-QR-Code-Flier-Counter/?src=qr-001`

### 2. Assign your codes in the manager (~2 min per batch)

Open the manager. Each row is one QR code:

| Column | Editable? | Meaning |
|---|---|---|
| **ID / slug** | no — permanent | What the printed code encodes (`qr-001`…`qr-500`). Never changes, so printed codes never break. |
| **Name** | click to edit | Your label, rename anytime ("PauseAI spring run"). |
| **Owner** | click to edit | Who's responsible for this code / who posted it. |
| **Location** | click to edit | Where you physically posted it ("Main St library board"). |
| **Venue type** | click to edit | library / coffee shop / transit stop / … (suggestions offered, free text allowed). |
| **Posted** | date picker | The day you put the flyer up. |
| **Flyer ver.** | click to edit | Which design/print run this flyer is ("v1", "spring-2026"). |
| **Destination** | click to edit | The website this code forwards to. |
| **Scans** | automatic | Live count from GoatCounter. Click it to open that code's full scan history and graphs in the dashboard. |
| **Last scan** | automatic | How long since the last scan. Inferred: the manager notices when a count rises between checks, so it fills in as you use the page (`?` = scans predate tracking; exact times are one click away in GoatCounter). |
| **Prev. check** | via **Record check** button | The scan count as of your last check-in, with date — and a green `+N` showing growth since. |
| **Conv.** | click to edit | Conversions, entered by hand (see Notes below on why this can't be automatic). |
| **Verified** | date picker | The day you last physically confirmed the flyer is still up. |
| **Status** | dropdown | `retired` stops a code from forwarding (scans still counted). |
| **Notes** | click to edit | Anything ("re-postered 3/12", "taken down"). |
| **Copy URL** | button | Copies the exact URL to paste into a QR generator. |

Plus search, filters (assigned / unassigned / edited), CSV export of every
column, a **Load all scan counts** button (500 codes takes a couple of
minutes — it goes gently to respect GoatCounter's rate limit), and **Record
check**, which stamps today's counts into every code's "Prev. check" column
so next visit you can see growth per location at a glance.

**Saving:** edits apply instantly in your browser, but a static site can't
write to itself — to make them live for scanners, click **Download
codes.json**, then in the GitHub repo use *Add file → Upload files* to
replace `codes.json` and commit. (Takes ~30 seconds; Pages redeploys
automatically.)

### 3. Make the physical QR codes

For each code you want to print, **Copy URL** in the manager (e.g.
`…/AI-QR-Code-Flier-Counter/?src=qr-001`), paste it into
[QR Code Monkey](https://www.qrcode-monkey.com) (free, static, no account),
and download at 1000px+. Or generate any number offline:

```sh
pip install "qrcode[pil]"
python tools/make_qr.py https://stealthsilent1.github.io/AI-QR-Code-Flier-Counter/ --range 1 50
```

writes print-ready `qr-001.png` … `qr-050.png` into `qr-codes/`.

**Test-scan every code with your phone before printing.**

### 4. Watch the numbers

Scan counts appear in the manager's **Scans** column and, with graphs over
time, at <https://stealthsilent.goatcounter.com> (one row per code, e.g.
`/qr-017`).

> If the Scans column shows "–", log in to GoatCounter → Settings and enable
> **"Allow adding visitor counts on your website"** (the public counter
> endpoint the manager reads).

## Notes

- **Scans of unassigned, retired, or mistyped codes are never lost** — they
  count under `/untagged/…` and the visitor sees a page listing your known
  destinations instead of being stranded.
- **The forward is fast** (typically under half a second) and never waits
  more than 1.5s on counting — if GoatCounter is unreachable, visitors are
  forwarded anyway.
- **Physical location is whatever you type in the Location column** — a QR
  scan carries no GPS. You know where a scan happened because you know where
  you posted that code. (GoatCounter separately shows visitors' rough
  country/region.)
- **Why conversions are manual:** a conversion (signing up, donating) happens
  on the destination site — e.g. pauseai.info — which you don't control and
  can't see into. No QR service can measure that either. The scan→visit is
  what's countable from outside; record conversions you learn about by hand.
- **"Last scan" precision:** GoatCounter's public counter endpoint returns
  totals only, so the manager infers recency by noticing count increases
  between checks (per browser). For exact per-scan timestamps, click the
  scan count — the GoatCounter dashboard has the full history.
- **Privacy:** GoatCounter uses no cookies and collects no personal data, so
  no cookie banner is needed.
- **Need more than 500?** Add more entries to `codes.json` — the pattern is
  obvious in the file. Everything else adjusts automatically.
