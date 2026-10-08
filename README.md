# Robert Wydra — wydra.dev

A small, English-language personal profile. Plain HTML, one stylesheet, one
small script, and two-colour images. No build step, framework, CDN, analytics,
or third-party requests on page load.

## Local preview

From the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open <http://127.0.0.1:8080/>. Stop the server with Ctrl+C.

The repository root is ready to serve directly with GitHub Pages. `CNAME`
retains the custom domain `wydra.dev`; `.nojekyll` skips Jekyll processing.

## Editing

- `index.html`: content, links, page metadata, and accessible structure.
- `styles.css`: all styles, the locally hosted font, responsive layout, and the
  entrance animation. `prefers-reduced-motion` disables the animation.
- `script.js`: displays the email link and its arrow immediately on page load.
  It also inserts the current year in the copyright notice; without JavaScript,
  the notice displays the author name without a year.
  The address is assembled from encoded fragments. Without JavaScript, the page
  shows `eczajnik [at] gmail [dot] com`. This deters simple email harvesters; it
  cannot prevent determined crawlers from decoding a public address.
- `assets/`: the two-colour images, monogram favicon, and Space Grotesk WOFF2.

Space Grotesk is hosted locally and uses `font-display: swap`. The font is
unmodified, downloaded from the [official repository](https://github.com/floriankarsten/space-grotesk),
and distributed with its [SIL Open Font License](assets/fonts/OFL.txt).

Section headings use inline SVGs from the [Heroicons outline set](https://heroicons.com/outline),
version 2.1.5: briefcase, wrench-screwdriver, cpu-chip, book-open, and rocket-launch.
They use the text colour, are hidden from assistive technology as decorative
icons, and need no library or additional requests. The [MIT licence](assets/icons/HEROICONS-LICENSE.txt)
is included locally.

## Reprocessing the images

Only this optional, offline step needs Pillow; the website itself has no runtime
dependencies. Use Python 3.10 or later:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/process_images.py \
  --portrait /Users/robert/Downloads/Robert.png \
  --logo /Users/robert/develop/ottershot-logo/ottershot-favicon.png
```

Replace the input paths if your originals live elsewhere. The script preserves
the source files and overwrites only `assets/robert.png` and `assets/ottershot.png`.
The portrait crop is tailored to the supplied photograph.

Images are resized, flattened to white for luminance processing, and converted
with Floyd–Steinberg dithering. The resulting one-bit indexed PNGs use only
`#155e9a` and `#eef7ff`; transparency becomes the light palette colour.
The portrait is 480 × 560 pixels and the OtterShot logo is 192 × 192 pixels.

## Verification

Checked in Chromium at 320, 375, 768, and 1440 px, including immediate email display,
keyboard activation and focus, in-page navigation, reduced motion, and disabled
JavaScript. No horizontal overflow or console errors; every loaded resource
comes from the same origin. All supplied recommendation/profile URLs are present.

Lighthouse reports 100 for accessibility, best practices, and SEO, with no failed
audits. The foreground/background contrast is 6.25:1, above WCAG AA for ordinary text. Both
raster assets have exactly two colours and one-bit PNG palettes.

The complete page payload is approximately **92.7 KiB before HTTP compression**,
including HTML, CSS, JS, font, both images, and favicon (budget: 150 KiB).
Developer scripts, the font licence, README, and preview screenshots are not
requested by the page and are excluded from this runtime budget.

Representative full-page screenshots: [desktop, 1440 px](docs/preview/desktop.png)
and [mobile, 375 px](docs/preview/mobile.png).
