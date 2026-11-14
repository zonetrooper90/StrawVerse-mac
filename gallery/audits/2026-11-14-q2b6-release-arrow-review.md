# Q2-B6 — Anime release arrow hover partial-rule review (2026-11-14)

Read-only review approved; implementation requires separate explicit approval. Verified baseline build `043eb6b22011e4540c5c843fb8b7d12b297ba913`, checkpoint `2026-11-14-q2b5-typography`, full SHA-256 `3df19003fa0e0b1bbe2a4d47bca65835223052fc5e7e1222bf955fd3c63b1aa8` (6,902,957 bytes), lightweight `b01c98b76d195b7d00d180f2fae92ed086e9a6e5e21eef2380e3a68581e2bde1` (587,267 bytes). Both exact-build checks 43603010191 and 43603012740 passed. Current documentation head `5700c4ba718e0518eb7acccfafdd52ded9ffbbd4` checks 43603907321 and 43603907289 passed; integrity logs verify archive, exact full/lightweight bytes and deterministic source reconstruction. Pointer and manifest agree. User reported no visual change in Q2-B5 with unbundled custom fonts; custom-font appearance remains unverified, no claim of native typography validation. User authorized this read-only review separately.

## Rescan
Verified assembled lightweight style block, lexical scanner respecting comments, quotes, escaped characters, parentheses/brackets, enclosing conditions and selector branches; excludes keyframes/non-qualified at-rules, requires identical value/priority across branch/property/context chain and later complete selector match. 2,075 qualified rules, 7,080 declarations, 54 identical-value and 239 differing-value chains, 38 distinct earlier candidates in 20 partial rules; no scanner errors. Exactly one release-arrow candidate; remaining 37 held (18 Settings, 8 Player, 11 Search). Lexical equivalence is not universal runtime proof.

## Exact proposal
`gallery/src/styles/07-anime-detail-refinements.css`, source blob `7de22f2c9de4ab0fa46d44d6758d9e70cf7a82ac`, earlier lines 89–91 (assembled 734–736), later line 105 (assembled 750). Both are unconditional identical full selectors. Remove only `color:var(--accent);` from the earlier hover rule. Unique exact full snippet confirmed in both source and assembled lightweight HTML.

```css
.inline-release-fade .inline-arrow:hover{
  color:var(--accent);background:transparent;border:0;box-shadow:none;
}
```

Becomes:

```css
.inline-release-fade .inline-arrow:hover{
  background:transparent;border:0;box-shadow:none;
}
```

Keep later `.inline-release-fade .inline-arrow:hover{color:var(--accent)}`, all other declarations and rules, base ink color, transparent button chrome, icon shadow/rotation, focus outline, disabled states, full-height edge hit shields, gradients, 560px edge-width and 460px generic-arrow media rules, fade timings/reduced motion, chronological card order, selection and episode availability. 20 ASCII bytes only; expected full 6,902,937 bytes, lightweight 587,247 bytes.

## Actual behavior and verification required after approval
`11a-anime-detail.js` mounts .inline-release-viewport with #inline-installment-rail, [data-inline-scroll="-1"/"1"] arrows and real release cards. refreshInstallmentArrows derives can-left/right, guard-left/right and disabled state from rail scroll position/overflow and pointer presence. setupInstallmentEdgeGuards retains invisible edge hit shield until pointer leaves (not touch). `11i-core-render.js` advances exactly one release offset, clamped to rail max, smooth normally/instant reduced; clicks on guard consumed. selectInlineInstallment retains actual rail DOM/scroll, updates selected card and dependent sections. Representative actual fixtures: Attack on Titan eight chronological releases (seasons, specials, film and OAD), Quintessential Quintuplets five (seasons, film, specials), Solo Leveling two; single-release title has no rail.

- Guard both baseline HTML digests, source blob and exact unique earlier rule, prove only 20 CSS bytes removed and non-CSS content unchanged. Source-first build, exact candidate tree, four mandatory mode/motion shards with exact counts, three standard groups, immutable checkpoint and both independent checks.
- Actual mounted Anime Details across six themes and both motions/build modes. Desktop, narrow 370px, both sides of 560px and 460px, and real overflow/no-overflow cases (measure rail geometry; use fixture-dependent sizes where needed). Compare all enumerable computed properties/pseudo styles and geometry of rail, arrows/icons, fades, cards/descendants and layout ancestors. Check resting, real left/right hover (accent color), keyboard focus, combined hover/focus, disabled/hidden and both guard states after reaching limits with stationary pointer. Confirm gradients, visibility/opacity, pointer hit target, focus outline, one-card advance in both directions, scroll behavior and no accidental card activation when clicking guard; release guard on pointer exit. Test actual season/related card selection, retained rail and correct selected/episode state; no-overflow/single-release checks. Compare settled states, avoid nondeterministic mid-animation samples; verify declared normal/reduced transitions and real interaction. Preserve existing standard regressions. Stop on mismatch; visual approval separate.
- No application, asset, font, native or numbered-release changes during audit.
