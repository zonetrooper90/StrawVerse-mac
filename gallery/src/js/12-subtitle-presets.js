/* v82 — Subtitle customization design preview (CSS rendering, not mpv).
   ARTWORK FOLLOW-UPS (deferred, no image edits in v82): soften lantern-light pool
   irregularity and refine fine day/night foliage alignment. */
const SHRINE_DAY_IMAGE='__GALLERY_SHRINE_DAY_DATA_URL__';
const SHRINE_NIGHT_IMAGE='__GALLERY_SHRINE_NIGHT_DATA_URL__';
const SUBTITLE_PREVIEW_TEXT='The quick brown fox\njumps over the lazy dog.';
/* v93 — Five user-facing, named relative subtitle sizes. The values below are
   reference units at a 1080-high displayed video area (not physical display
   pixels, not source-video dimensions). Only the names appear in the UI.
   Persist stable preset IDs, never a resolution-specific font size. */
const SUBTITLE_SIZES=Object.freeze([
 {id:'extra-small',label:'Extra Small',reference:28},
 {id:'small',label:'Small',reference:36},
 {id:'normal',label:'Normal',reference:44},
 {id:'large',label:'Large',reference:54},
 {id:'extra-large',label:'Extra Large',reference:64}
]);
const SUBTITLE_DEFAULTS=Object.freeze({font:'system',size:'normal',color:'#f8f8f8',colorMode:'white',customColor:'#ffffff',customColorSet:false,outline:3,outlineColor:'#08080b',shadow:3,shadowColor:'#08080b',boxOpacity:65,boxColor:'#08080b',effect:'outline',outlinePreset:'normal',shadowPreset:'normal',boxPreset:'normal',});
const SUBTITLE_TEXT_COLOR_PRESETS=Object.freeze({white:'#f8f8f8',yellow:'#ffe066'});
// Three intensity levels: Low and Medium unchanged, High uses the former Max.
// The UI offers named effect presets, while the renderer still uses numbers.
// Outline values respect the existing font-size-dependent maximum.
const SUBTITLE_EFFECT_PRESETS=Object.freeze({
 outline:{light:1,normal:3,strong:6},
  shadow:{light:1.5,normal:3,strong:10},
  box:{light:35,normal:65,strong:100}
});
const SUBTITLE_EFFECT_LABELS=Object.freeze(['Low','Medium','High']);
function subtitlePresetValue(effect,preset,size){
 const n=SUBTITLE_EFFECT_PRESETS[effect]?.[preset]??SUBTITLE_EFFECT_PRESETS[effect]?.normal??0;
 return effect==='outline'?Math.min(maximumSubtitleOutline(size),n):n;
}
function assignSubtitlePresetNumbers(prefs){
 for(const [effect,key,presetKey] of [['outline','outline','outlinePreset'],['shadow','shadow','shadowPreset'],['box','boxOpacity','boxPreset']]){
  prefs[key]=subtitlePresetValue(effect,prefs[presetKey],prefs.size);
 }
}

function normalizeSubtitleSize(size){
 return typeof size==='string' && SUBTITLE_SIZES.some(entry=>entry.id===size)?size:SUBTITLE_DEFAULTS.size;
}
function subtitleReferenceSize(size){
 return (SUBTITLE_SIZES.find(entry=>entry.id===size)||SUBTITLE_SIZES[2]).reference;
}
// Same proportional cap as v88: one eighth of the reference font size,
// rounded down to half-steps and never above six reference units.
function maximumSubtitleOutline(size){return Math.min(6,Math.floor(subtitleReferenceSize(size)/4)/2)}
const SUBTITLE_FONTS=Object.freeze({system:'-apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif',atkinson:'"Atkinson Hyperlegible Next", -apple-system, sans-serif',inter:'Inter, -apple-system, sans-serif'});
