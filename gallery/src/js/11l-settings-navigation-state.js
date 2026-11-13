/* v57 — Settings is a full page. Original tabs and detail DOM stay mounted,
   not rerendered, so returning preserves the active view, filters, and scroll. */
let settingsReturnScroll=0;
let settingsLastSection='appearance';
let appearanceTab='theme';
let playbackTab='general';
let settingsClosing=false;
let settingsCloseFallback=null;
let settingsReturnAnimationTimer=null;
