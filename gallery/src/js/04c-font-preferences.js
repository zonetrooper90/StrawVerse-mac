/* v82 — Consistent English-only, non-interactive typography specimens. */
const PREVIEW_LATIN_UPPER='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const PREVIEW_LATIN_LOWER='abcdefghijklmnopqrstuvwxyz';
function fontPreviewMarkupTile(){
 return `<span class="settings-font-sample-pair"><span class="settings-font-sample-label">Uppercase</span><span class="settings-font-glyphs">${PREVIEW_LATIN_UPPER}</span></span><span class="settings-font-sample-pair"><span class="settings-font-sample-label">Lowercase</span><span class="settings-font-glyphs">${PREVIEW_LATIN_LOWER}</span></span><span class="settings-font-sample-pair"><span class="settings-font-sample-label">Numbers &amp; symbols</span><span class="settings-font-glyphs">0123456789 · ! ? @ # &amp; % ( ) / + = — € $</span></span><span class="settings-font-sample-pair"><span class="settings-font-sample-label">Similar-looking characters</span><span class="settings-font-glyphs">I l 1 | O 0 o · b d p q · 6 9</span></span>`;
}

const supportedGalleryFonts=['system','atkinson','inter'];
function readGalleryFont(){try{const stored=localStorage.getItem('gallery.font');return supportedGalleryFonts.includes(stored)?stored:'system';}catch{return 'system';}}
state.font=readGalleryFont();
document.body.dataset.font=state.font;
function setGalleryFont(name){
 if(!supportedGalleryFonts.includes(name))return;
 state.font=name;
 document.body.dataset.font=name;
 try{localStorage.setItem('gallery.font',name);}catch{}
 if(settingsPage?.isConnected){
  for(const b of settingsPage.querySelectorAll('[data-font-choice]'))b.setAttribute('aria-pressed',String(b.dataset.fontChoice===name));
  updateGalleryFontNotice();
 }
 saveDesktopPreferences();
}
function galleryFontAvailable(family){
 if(family==='system')return true;
 try{
  // FontFaceSet.check() alone returns true for absent families, so compare metrics.
  const sample='WMWMWM il1I O0 bdqp ÆØÅ æøå Readability 0123456789';
  const canvas=document.createElement('canvas');const ctx=canvas.getContext('2d');
  if(!ctx)return false;
  const base=generic=>{ctx.font='32px '+generic;return ctx.measureText(sample).width;};
  const test=generic=>{ctx.font='32px "'+family+'",'+generic;return ctx.measureText(sample).width;};
  return ['monospace','serif','sans-serif'].some(generic=>Math.abs(test(generic)-base(generic))>1.2);
 }catch{return false;}
}
function updateGalleryFontNotice(){
 const notice=settingsPage?.querySelector('#settings-font-missing');if(!notice)return;
 const name=state.font==='atkinson'?'Atkinson Hyperlegible Next':state.font==='inter'?'Inter':'';
 const missing=name&&!galleryFontAvailable(name);
 notice.hidden=!missing;
 notice.textContent=missing?'“'+name+'” is not installed on this Mac, so Gallery is showing the system font as a fallback. Install the font locally to see the selection applied throughout the app.':'';
}
