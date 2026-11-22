# Game Night Guide

Board games for beginners, couples and families, in plain English.
English only, USA only. No Bangla, no Bangladesh content.

- **Site (live):** https://raihanlite.github.io/gamenightguide/
  Hosted on GitHub Pages, repo `raihanlite/gamenightguide`.
- **How deploy works (22 Nov 2026):** GitHub Pages serves the
  `gh-pages` branch (built output only). Two pushes per update:
  source → `main`, then the built `_site/` folder → `gh-pages`.
  The API token used to push has only the `repo` scope, so it
  **cannot** push files under `.github/workflows/` (GitHub answers
  404 for workflow paths without the `workflow` scope). That is
  why there is no Actions auto-deploy yet. A ready-made
  `.github/workflows/deploy.yml` is kept in the local source only
  (not in the repo). To switch to Actions builds later: either add
  that file through the GitHub web UI, or regenerate the token
  with the `workflow` scope and push it via the API; then change
  the Pages source to GitHub Actions and delete the `gh-pages`
  branch workflow.
- **Custom domain:** not set yet. `gamenightguide.com` is still only a
  placeholder idea, not bought. When a real domain is bought, change
  `url` (and `email`) in `src/_data/site.json` and remove
  `pathPrefix: "/gamenightguide/"` from `eleventy.config.js` (a custom
  domain serves the site at the root, so the prefix must go).
- **Stack:** Eleventy 3 (11ty), no framework, no tracking, no build-time
  network calls. One small CSS file, one small vanilla JS file (Finder only).
- **Source of truth for topics and facts:**
  `~/workspace/board-games-topic-research.md` (outside this repo).

## Build & serve

```bash
npm install
npm run build    # writes _site/
npm run serve    # build + local server with live reload
npm run images   # regenerate OG images (needs Python + PIL)
```

Node v24 / npm 10 used here. Output is a plain static folder (`_site/`).
It can be hosted anywhere that serves static files.

## Structure

```text
src/
  _data/site.json        site name, tagline, URL placeholder
  _data/games.json       22 games: players, time, age, price (only where
                         verified), BGG rating (only where verified)
  _includes/layouts/     base.njk, post.njk (Article + Breadcrumb JSON-LD),
                         page.njk
  assets/style.css       the only stylesheet (system fonts)
  assets/finder.js       Board Game Finder logic (vanilla JS)
  index.md               home
  finder.md              Board Game Finder tool
  guides.md              guides index (/guides/)
  guides/*.md            6 articles, 1,400–1,500 words each
  about.md contact.md privacy.md disclaimer.md affiliate-disclosure.md
  sitemap.njk feed.njk robots.njk
scripts/make_images.py   generates 1200×630 OG PNGs with PIL
```

## How to add an article

1. Copy a file in `src/guides/`, keep the front matter fields:
   `title`, `description`, `date` (YYYY-MM-DD), `image`
   (`/images/og-<slug>.png`), `imageAlt`.
2. Add the OG image: add an entry to `scripts/make_images.py` and run
   `npm run images`, or reuse an existing image.
3. Every article needs: a key-facts table, a comparison table, a
   checklist, an FAQ, and a `Last checked: …` line.
4. Run `npm run build` and check the new page in `_site/guides/`.

## How to change the domain

1. Edit `url` in `src/_data/site.json` (and `email` if it changes).
2. Rebuild. Canonical URLs, Open Graph URLs, JSON-LD, sitemap and RSS
   all read from that one value, nothing else needs editing.

## How facts are handled (read this before editing content)

- **Prices:** only three prices were verified on 22 Nov 2026:
  Spirit Island $57.99, Terraforming Mars $79.99, Mage Knight $79.99.
  Every other price in the site is explicitly marked “not verified”.
  Never invent a price. Re-check a price at the store, date-stamp it,
  and only then publish it.
- **BGG ratings:** only publish a rating that is in the research file
  (Patchwork 7.6, Jaipur 7.5, 7 Wonders Duel 8.1, Spirit Island 8.4,
  Terraforming Mars 8.4, Mage Knight 8.1, Dune: Imperium 8.4).
  Everything else is blank on purpose.
- **Players / time / age:** from the research file only.

## Writing style

No em dashes anywhere. Use commas for natural pauses, periods to
separate thoughts, and colons to introduce explanations. Hyphens are
only for compound words, and en dashes only for ranges.

Keep paragraphs short, usually 2 to 4 lines. Break long paragraphs
into smaller sections. Tables, lists, headings, checklists and FAQs
stay as they are.

## What is NOT verified yet

- Exact search volume / KD per keyword. The research file gives verified
  numbers only for “board games” (broad, ~410,000/month USA),
  single game names (high KD), and “board games for adults”
  (5,400/month, KD 40) / “best board games for adults” (4,400/month,
  KD 54). Tier 1 order was ranked on competition evidence, not KD.
  Before writing new articles, run one keyword-tool export
  (Ahrefs / Semrush / KWFinder) for the exact keyword.
- Amazon Associates commission % for board games: not verified.
  Do not quote a commission rate anywhere on the site.
- Live prices for 19 of the 22 games in `games.json`, marked null.
- Affiliate programme sign-ups (Amazon, Target, Barnes &amp; Noble)
  are not done. Links currently go to public store pages without an
  affiliate tag; the disclosure page says so.

## Decisions still needed from Md

- **Domain name:** gamenightguide.com is a placeholder, not bought.
  Site is live on the GitHub Pages URL above until a domain is decided.
- **Affiliate account sign-ups** (Amazon Associates, Target, Barnes &amp; Noble).
- **AdSense:** apply only after the site has content and traffic history;
  no ad code is installed.
- **Google Search Console:** not added yet; add after the domain
  decision, per Md.

## v2 visual redesign (22 Nov 2026)

Warm game night identity: deep green #1E4D3B, warm cream #FBF9F4,
warm ink #23201C, amber #E8A317 for calls to action only. Serif
display headings (Georgia stack), clean sans body. One small CSS file,
no new frameworks, no tracking.

- **Photos:** all real photographs from Pexels (free licence), no AI
  images. See `src/photo-credits.md` for every photographer and source
  URL. Originals are downloaded at 1600px and optimised with
  `scripts/make_photos.py` (1200x630 guide photos, 600x375 card
  thumbs, 1600x900 home hero, all under 200KB).
- **OG images:** 1200x630, photo on top with a deep green band and the
  guide title in cream serif, built by `scripts/make_photos.py` in the
  same layout as the Canva home OG design.
- **Canva:** home OG design "Game Night Guide OG social sharing image",
  https://canva.link/0zoz23l3t0ns5o1 (design DAHbn8g9fqM, hero photo
  asset MAHbn64d9oQ). Two Canva limits found while making it: the
  create-design API always returns a 940x788 canvas even when asked
  for 1200x630, and its export endpoint answers "permission denied"
  for these agent-created designs, so the design can be opened and
  exported in the Canva editor by Md, but the shipped 1200x630 files
  are the PIL versions in the same layout. The resize-design tool also
  broke the layout (design DAHbn6m1BDM, do not use).
- **Writing rules (Md, 22 Nov 2026):** no em dashes; commas, periods
  and colons; hyphens only for compound words; en dashes only for
  ranges; short paragraphs, usually 2 to 4 lines.
- **Performance:** homepage images are lazy loaded below the fold
  (hero is eager). Homepage total is under 1MB.
