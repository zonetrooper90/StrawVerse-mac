function readSubtitlePrefs(){
 try{
  const raw=JSON.parse(localStorage.getItem('gallery.subtitlePreferences')||'{}');
  if(!raw||typeof raw!=='object'||Array.isArray(raw))return {...SUBTITLE_DEFAULTS};
  const v={...SUBTITLE_DEFAULTS};
  const validHex=c=>typeof c==='string' && /^#[0-9a-fA-F]{6}$/.test(c);
  if(Object.hasOwn(SUBTITLE_FONTS,raw.font))v.font=raw.font;
  v.size=normalizeSubtitleSize(raw.size);
  for(const key of ['outlineColor','shadowColor','boxColor','customColor'])
   if(validHex(raw[key]))v[key]=raw[key].toLowerCase();
  if(['white','yellow','custom'].includes(raw.colorMode))v.colorMode=raw.colorMode;
  if(typeof raw.customColorSet==='boolean')v.customColorSet=raw.customColorSet;
  v.color=v.colorMode==='custom'?v.customColor:SUBTITLE_TEXT_COLOR_PRESETS[v.colorMode];
  if(['outline','shadow','box','none'].includes(raw.effect))v.effect=raw.effect;
  for(const key of ['outlinePreset','shadowPreset','boxPreset'])
   if(['light','normal','strong'].includes(raw[key]))v[key]=raw[key];
  assignSubtitlePresetNumbers(v);
  return v;
 }catch{return {...SUBTITLE_DEFAULTS};}
}
let subtitlePrefs=readSubtitlePrefs();
let subtitleLastStyledEffect=subtitlePrefs.effect==='none'?'outline':subtitlePrefs.effect;
function persistSubtitlePrefs(){try{localStorage.setItem('gallery.subtitlePreferences',JSON.stringify(subtitlePrefs));}catch{}}
const settingsSections=[
 ['appearance','Appearance','palette'],
 ['playback','Playback','play'],
 ['downloads','Downloads','download'],
 ['sources','Sources','globe'],
 ['about','About','info']
];

