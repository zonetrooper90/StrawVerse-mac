# Gallery × daisyUI — Full-App Preview 03: live component integration

Date: 2026-11-05. **Standalone design experiment, not Gallery v104.** The approved stable build remains **v103**, unchanged.

## User direction

After reviewing Preview 02, the user concluded that seeing only palette changes plus a separate component showcase wasn't a fair test of daisyUI. They **approved changing selected controls inside the real Gallery interface** to genuine daisyUI components, preserving Gallery's positions and behavior and keeping the prototype separate from the stable version.

## Recovery

- Full working **Gallery-daisyUI-Full-App-Preview-03.html**: ChatGPT Library at `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Full-App-Preview-03.html`.
  - Exact length: **6,862,193 bytes**, SHA256 `8a135aa431d8ba6f61f1a1fdcb81c499be6a4fa4cd6ddb7345431044a8f24e8f`.
- GitHub source recovery: [v103 → Full-App Preview 03 reproducible patch](Gallery-v103-to-daisyUI-Full-App-Preview-03.patch) committed on `gallery/design-checkpoints`.
  - Patch: **44,811 bytes**, SHA256 `68b5b12b6341fd53f472fb12b8228efd74d7676a9204857d408b29252d7e5b62`.
  - Reconstruct: copy the Library `/Gallery Backups/2026-11-04/Gallery-v103.html` into a working folder as `Gallery-v103.html`; run `patch -p0 < Gallery-v103-to-daisyUI-Full-App-Preview-03.patch`; rename the patched copy to `Gallery-daisyUI-Full-App-Preview-03.html`. `patch --dry-run` succeeded, and the applied file was **byte-identical** to the archived prototype. Do not patch the archived stable source.
- Existing Preview 01, Preview 02, and Component Labs 01–03 remain archived.

## What is genuinely daisyUI now

Unlike Preview 02 (which used official palette tokens but left native controls intact), **Preview 03 renders real daisyUI v5.7.48 component classes in the actual Gallery UI**:

1. Main three-tab navigation: a **real `tabs` / `tab` / `tab-active` component in a ShadowRoot** over the exact native Gallery nav footprint; original `nav.tabs` stays in the DOM for existing route/paging logic and original grid dimensions. The real tabs forward clicks to the native navigation, including keyboard arrow navigation. Experimental **Boxed / Bordered / Lifted** tab selection in the floating panel.
2. Live action buttons: page-header, detail, collection, dialog and download actions acquire ShadowRoot-mounted **real `btn`, `btn-primary`, `btn-outline`, `btn-ghost`** surfaces; their native Gallery button DOM elements, children, click handlers, layout/intrinsic measurements and state remain in place. Original content remains part of layout but becomes visually hidden while the vendor skin is active.
3. Live Settings navigation: the five Settings section buttons and Back button use the same genuine vendor-styled button surfaces inside their original Gallery button elements.
4. Live Settings fields: the two actual selectors for **Subtitles when playback starts** and **Autoplay next episode** are visually represented by real daisyUI `select` controls in separate ShadowRoots. They forward selection via the native underlying select's **change event**, preserving its original Gallery settings logic. The original selects remain present in the layout but visually hidden while enhanced.

The original floating palette selector from Preview 02 remains and includes two new experiment controls: **Use real daisyUI components** (on/off for immediate comparison) and **Navigation component style** (three real tab variants). Seven daisyUI-compatible palettes, three original Gallery themes and optional corner-shape toggle remain available. **No new persistent Gallery settings are written by the experiment controller.**

**Vendor CSS availability / accuracy:** genuine, version-pinned `https://cdn.jsdelivr.net/npm/daisyui@5.7.48/daisyui.css`, with `unpkg.com` fallback, loaded via per-control ShadowRoot `<link rel=stylesheet>`. No third-party JavaScript, no React or runtime Tailwind dependency. Browser requires **internet to obtain daisyUI CSS**; this experiment is **not an offline bundle**. If neither host loads, original controls stay visible and floating panel displays an honest failure status. Component CSS can't leak to the global document and conflict with Gallery's pre-existing `.tabs`, `.tab`, or `.btn` classes.

Actual Gallery nav and app behavior remains from v103, but its *visible styling/interaction affordance* has changed in experiment mode (e.g., selected daisyUI tab vs original sliding Gallery capsule). This is intentional for fair visual assessment, not a promise to adopt daisyUI wholesale.

## Validation

- Chromium, test widths **1440, 620, 390 and 320px**: tested main nav→Library, open Settings, switch Settings section, actual select proxy → original Autoplay value, switch real component mode off → original Gallery styles. No JavaScript exceptions and no document horizontal overflow.
- Geometry compared to baseline v103 at **1440, 1050, 620, 390 and 320px**: app frame, header, brand, native nav, native tabs, and workspace rects showed **zero differences**. Same pixels are used to position the ShadowRoot overlays.
- Simulated complete CDN failure: verified vendorReady=false, native nav opacity 1, no enhanced buttons/selects, status **"Could not load daisyUI CSS · showing unchanged Gallery controls"**, zero JS errors.
- **Important visual verification limit:** automated Chromium's offline environment used a deterministic stand-in stylesheet to test events and the isolation. It could **not fetch real daisyUI CSS**; the user should inspect actual daisyUI component aesthetics in a browser that loads the vendor stylesheet. The prototype's CSS uses real vendor URLs/classes, not manually approximated visual components.
- The full app HTML and all embedded original artwork are preserved; no images generated or edited.

## Next step

User evaluates the real component skins, tab styles, and palette choices and identifies which actually improve Gallery. Possible corrections to this experiment should be discussed before creating another named Gallery app version. **Do not integrate Preview 03 into v103 or label it v104 without explicit approval.**
