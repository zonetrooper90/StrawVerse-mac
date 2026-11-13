
'use strict';
/* Soft Futuristic stage 01: six study palettes mapped to the v103 component tokens; no feature logic replaced. */
/* v53 — StrawVerse-style search integrated into the active Discover page. */
document.documentElement.dataset.focusModality='pointer';
document.addEventListener('pointerdown',()=>{document.documentElement.dataset.focusModality='pointer';},{capture:true});
document.addEventListener('keydown',event=>{if(event.key==='Tab')document.documentElement.dataset.focusModality='keyboard';},{capture:true});

/* Single-file, offline, self-contained design prototype. v68 connects simulated Sources to the Discover catalogue without touching Library or Downloads. All demo media availability and viewing progress are illustrative. */
/* NEXT APPLE SILICON BUILD: create a real-source smoke-test checklist (provider installation, updates, health, deduplication, and Library/Downloads preservation). */
/* FUTURE VISUAL POLISH (user-requested): Audit and resolve visual inconsistencies between full-page Settings and Gallery's other pages. Deliberately deferred; do not couple to repository functionality. */
const SVG={sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.93 4.93l1.42 1.42m11.3 11.3l1.42 1.42m0-14.14-1.42 1.42M6.35 17.65l-1.42 1.42"/>',moon:'<path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1 -9 -9z"/>',refresh:'<path d="M20 8v-5h-5M4 16v5h5M5 9a8 8 0 0 1 14-3l1 2M19 15a8 8 0 0 1 -14 3l-1-2"/>',rewind10:'<path d="M21 5v14l-8 -7l8 -7"/><path d="M10 5v14l-8 -7l8 -7"/>',forward10:'<path d="M3 5v14l8 -7l-8 -7"/><path d="M14 5v14l8 -7l-8 -7"/>',pause:'<rect x="6" y="4" width="4" height="16" rx="1" fill="currentColor"/><rect x="14" y="4" width="4" height="16" rx="1" fill="currentColor"/>',volume:'<path d="M4 9h4l5 -4v14l-5 -4H4z"/><path d="M17 8a6 6 0 0 1 0 8"/>',captions:'<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M6 11h5m-5 4h4m3 -4h5m-5 4h4"/>',maximize:'<path d="M9 3H3v6m12-6h6v6M9 21H3v-6m12 6h6v-6"/>',clapper:'<path d="M4 11h16v10H4zM4 11 2 6l17-4 3 5zM7 5l4 5m3-7 4 5"/>',search:'<circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/>',settings:'<path d="M4 7h16M4 17h16"/><circle cx="9" cy="7" r="2" fill="var(--window)"/><circle cx="15" cy="17" r="2" fill="var(--window)"/>',compass:'<circle cx="12" cy="12" r="9"/><path d="m16 8-3 5-5 3 3-5 5-3z"/>',library:'<path d="M4 4v16M8 4v16M12 6v14M16 4l4 16M2 20h20"/>',download:'<path d="M12 2v13m-5-5 5 5 5-5M4 18v3h16v-3"/>',filter:'<path d="M4 4h16v2.172a2 2 0 0 1 -.586 1.414l-4.414 4.414v7l-6 2v-8.5l-4.48 -4.928a2 2 0 0 1 -.52 -1.345v-2.227"/>',sliders:'<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="9" cy="6" r="2" fill="var(--window)"/><circle cx="16" cy="12" r="2" fill="var(--window)"/><circle cx="8" cy="18" r="2" fill="var(--window)"/>',play:'<path d="m9 6 10 6-10 6z"/>',share:'<path d="M12 16V3m-5 5 5-5 5 5M4 14v6h16v-6"/>',plus:'<path d="M12 5v14M5 12h14"/>',import:'<path d="M12 3v13m-5-5 5 5 5-5M4 20h16"/>',bookmark:'<path d="M5 3h14v18l-7-5-7 5z"/>',close:'<path d="M5 5l14 14M19 5 5 19"/>',chevron:'<path d="m9 6 6 6-6 6"/>',check:'<path d="m4 12 5 5L20 6"/>',dots:'<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',film:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16m10-16v16M3 9h4m-4 6h4m10-6h4m-4 6h4"/>',arrow:'<path d="M5 12h14m-7-7 7 7-7 7"/>',heart:'<path d="M20.8 5.9a5 5 0 0 0-7.1 0L12 7.6l-1.7-1.7a5 5 0 0 0-7.1 7.1L12 22l8.8-9a5 5 0 0 0 0-7.1z"/>',globe:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c6 5 6 13 0 18M12 3c-6 5-6 13 0 18"/>',info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.2"/>',folder:'<path d="M3 6h7l2 3h9v11H3z"/>',back:'<path d="m14 5-7 7 7 7"/>',list:'<path d="M8 6h13M8 12h13M8 18h13M3 6h.1M3 12h.1M3 18h.1"/>',headphones:'<path d="M3 14v-3a9 9 0 0 1 18 0v3M3 14h4v7H5a2 2 0 0 1-2-2zm18 0h-4v7h2a2 2 0 0 0 2-2z"/>',palette:'<circle cx="12" cy="12" r="9"/><path d="M7 11h.1M9 7h.1M14 7h.1M17 11h.1"/><path d="M12 19a2 2 0 0 0 2-2c0-1 1-2 2-2h2"/>'};
function icon(name,size=19){return `<svg class="icon" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${SVG[name]||SVG.film}</svg>`;}
function escapeHTML(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
const demo=[
{id:'demo:quints',name:'The Quintessential Quintuplets',art:'linear-gradient(152deg,#3c425f 0%,#806c98 42%,#c68d9d 73%,#e8baab 100%)',episodes:12,status:'Completed',lang:'Sub / Dub',tags:['Watching'],blurb:'Futaro Uesugi becomes tutor to five identical sisters with very different personalities. This demo groups two TV seasons, the 2022 film, and the separate 2023 and 2024 two-part specials.'},
{id:'demo:solo',name:'Solo Leveling',art:'linear-gradient(150deg,#121a35,#415078 50%,#8b6ab1)',episodes:12,status:'Completed',lang:'Sub / Dub',tags:['Watching'],blurb:'A hunter gains an unusual ability after a dangerous dungeon encounter. Connected-season relationships are illustrative; audio availability is simulated.'},
{id:'demo:long',name:'The Endless Voyage · Layout Test',art:'linear-gradient(150deg,#17333e,#437b7a 50%,#ad9481)',episodes:12,status:'Completed',lang:'Sub / Dub',tags:[],blurb:'Fictional long-running series used to stress-test the season selector. All installments and provider data are invented for this interface demonstration.'},
{id:'demo:aot',name:'Attack on Titan',art:'linear-gradient(150deg,#334447,#697b77 50%,#958c76)',episodes:25,status:'Completed',lang:'Sub / Dub',tags:['Plan to Watch'],blurb:'Humanity struggles to survive behind enormous walls. This example demonstrates split seasons, parts, and related releases.'},
{id:'demo:01',name:'Moonlit Signals',art:'linear-gradient(145deg,#322554 2%,#74548f 51%,#c48b9c 100%)',episodes:12,status:'Completed',lang:'Sub / Dub',tags:['Watching','Comfort Picks'],blurb:'A quiet science-fiction story about late-night messages between distant worlds.'},
{id:'demo:02',name:'Astra Afterlight',art:'linear-gradient(145deg,#213654,#386e88 50%,#88c2c1 100%)',episodes:12,status:'Ongoing',lang:'Sub',tags:['Watching','Downloads'],blurb:'An observatory apprentice follows a mysterious new constellation.'},
{id:'demo:03',name:'Paper Crane Days',art:'linear-gradient(150deg,#513a60,#a57696 52%,#f4b6a1)',episodes:10,status:'Completed',lang:'Sub / Dub',tags:['Comfort Picks','Plan to Watch'],blurb:'A charming slice-of-life story about a neighborhood stationery shop.'},
{id:'demo:04',name:'The Glass Harbor',art:'linear-gradient(160deg,#233955,#4b6384 52%,#b8b3ca)',episodes:13,status:'Completed',lang:'Sub',tags:['Plan to Watch'],blurb:'A coastal town reveals its secrets whenever the tide retreats.'},
{id:'demo:05',name:'Golden Orchard',art:'linear-gradient(165deg,#75506b,#aa796d 55%,#f5bf80)',episodes:24,status:'Ongoing',lang:'Sub / Dub',tags:['Weekend Queue'],blurb:'Old friends reunite to save an orchard with an unusual history.'},
{id:'demo:06',name:'Neon Reverie',art:'linear-gradient(135deg,#252a5b,#7b57a3 55%,#d277ac)',episodes:12,status:'Completed',lang:'Dub',tags:['Downloads','Comfort Picks'],blurb:'A nighttime city adventure where every streetlight remembers a wish.'},
{id:'demo:07',name:'Summer in Orbit',art:'linear-gradient(160deg,#2e5f70,#6893b1 45%,#dbbd8b)',episodes:12,status:'Completed',lang:'Sub / Dub',tags:['Plan to Watch','Weekend Queue'],blurb:'A summer school trip becomes a tiny voyage across the solar system.'},
{id:'demo:08',name:'Silent Atlas',art:'linear-gradient(150deg,#3b364c,#64778d 50%,#8e95ad)',episodes:8,status:'Ongoing',lang:'Sub',tags:['Watching'],blurb:'An archivist searches for missing places in a changing city.'},
{id:'demo:09',name:'Wisteria Nights',art:'linear-gradient(150deg,#4d3467,#8e5f95 57%,#dd9db4)',episodes:12,status:'Completed',lang:'Sub / Dub',tags:['Comfort Picks'],blurb:'A gentle mystery unfolds beneath a street of flowering trees.'},
{id:'demo:10',name:'Skyline Letters',art:'linear-gradient(160deg,#23485b,#698b8f 50%,#b9c6ad)',episodes:12,status:'Completed',lang:'Sub',tags:['Plan to Watch'],blurb:'Two childhood friends reconnect through messages left on rooftops.'}
];
function readAutoplayNextEpisode(){try{return localStorage.getItem('gallery.autoplayNextEpisode')==='on';}catch{return false;}}
/* Initial player volume uses the Gallery default or the user's starting value.
   The default is 70%; session volume is not a saved starting preference. */
const GALLERY_VOLUME_STORAGE_KEY='gallery.playback.startingVolume';
const GALLERY_INITIAL_VOLUME=70;
function galleryVolumePercent(value,fallback=GALLERY_INITIAL_VOLUME){
 const n=Number(value);
 return value!==null&&value!==undefined&&value!==''&&Number.isFinite(n)?Math.min(100,Math.max(0,Math.round(n))):fallback;
}
function readGalleryVolumePreferences(){
 try{
  const saved=JSON.parse(localStorage.getItem(GALLERY_VOLUME_STORAGE_KEY)||'null');
  if(saved&&typeof saved==='object'){
   return {
    mode:saved.mode==='user'?'user':'gallery',
    preferred:galleryVolumePercent(saved.preferred),
    precision:saved.precision==='fine'?'fine':'steps'
   };
  }
 }catch{}
 return {mode:'gallery',preferred:GALLERY_INITIAL_VOLUME,precision:'steps'};
}
const galleryVolumePreferences=readGalleryVolumePreferences();
/* This default applies once, at launch. Episode changes share the session level. */
let playerSessionVolume=galleryVolumePreferences.mode==='user'?galleryVolumePreferences.preferred:GALLERY_INITIAL_VOLUME;
let playerSessionMuted=playerSessionVolume===0;
function saveGalleryVolumePreferences(){
 try{localStorage.setItem(GALLERY_VOLUME_STORAGE_KEY,JSON.stringify(galleryVolumePreferences));}catch{}
}
/* Record the in-session volume only. Muting must not change the starting
   preference, and must not overwrite the last audible level used for unmute. */
function rememberGalleryPlayerVolume(video){
 if(!video)return;
 playerSessionVolume=galleryVolumePercent(video.volume*100);
 playerSessionMuted=!!video.muted||playerSessionVolume===0;
 if(!playerSessionMuted&&playerSessionVolume>0)playerLastAudibleVolume=video.volume;
}

const SOFT_FUTURISTIC_THEMES=['ocean','twilight','ember','slate','glacier','verdant'];
function readSoftFuturisticTheme(){
 try{const t=localStorage.getItem('gallery.softFuturistic.theme');if(SOFT_FUTURISTIC_THEMES.includes(t))return t;}catch{}
 return 'ocean';
}
const state={playback:null,playbackReturnScroll:0,view:'discover',theme:readSoftFuturisticTheme(),tag:'All Titles',filterStatus:'All',filterAudio:'All',downloadStatus:'All',query:'',tags:['Watching','Downloads','Plan to Watch','Comfort Picks','Weekend Queue'],kind:{'Watching':'system','Downloads':'system','Plan to Watch':'system','Comfort Picks':'custom','Weekend Queue':'custom'},importDoc:null,detailId:null,detailSeason:0,detailEpisode:1,detailReturnHistory:false,detailReturnView:'discover',detailReturnScroll:0,detailAudio:null,detailRelated:null,detailEpisodeFilter:'all',seasonTags:{},defaultPlayback:'sub',defaultDownload:'sub',defaultSubtitles:true,autoplayNextEpisode:readAutoplayNextEpisode()};
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
const screen=document.getElementById('screen'); const workspace=document.getElementById('workspace'); const modalHost=document.getElementById('modal-host'); const settingsPage=document.getElementById('settings-page');
// Keep page switches separate from routine in-place rerenders and tab-track motion.
// View Transitions capture the previous painted workspace before changing it;
// the shared app header and its button geometry are never part of the capture.
let galleryStageTransition=null;
let galleryStageMutating=false;
let galleryStageFadeInProgress=false;
let galleryStagePending=null;
const galleryReducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
function clearGallerySurfaceEntrance(){screen.classList.remove('surface-enter');}
// Preserve this browser snapshot transition exclusively for Anime Details ↔ Player.
// The user confirmed that route looks correct and it must not be redesigned.
function transitionGalleryPlayer(mutator){
 if(galleryStageMutating){mutator();return;}
 if(galleryStageTransition){galleryStageTransition.skipTransition();galleryStageTransition=null;}
 clearGallerySurfaceEntrance();
 // Reduced motion or browsers without the View Transitions API: switch directly.
 // A partial fallback animation would break the strict no-overlap guarantee.
 if(galleryReducedMotion.matches||!document.startViewTransition){mutator();return;}
 workspace.style.viewTransitionName='gallery-stage';
 let transition;
 try{
  transition=document.startViewTransition(()=>{
   galleryStageMutating=true;
   try{mutator();}finally{galleryStageMutating=false;}
  });
 }catch{workspace.style.viewTransitionName='';mutator();return;}
 galleryStageTransition=transition;
 transition.finished.finally(()=>{
  if(galleryStageTransition!==transition)return;
  galleryStageTransition=null;
  workspace.style.viewTransitionName='';
 }).catch(()=>{});
}
// All non-Player routes now fade actual DOM in a deliberate two-phase sequence.
// Until outgoing content *and* main navigation are fully invisible, neither
// application state nor the header/tab layout is allowed to change.
// This avoids ghosting and visible header-height jumps when tabs appear/vanish.
function transitionGalleryStage(mutator){
 if(galleryStageMutating){mutator();return;}
 if(galleryStageFadeInProgress){galleryStagePending=mutator;return;}
 if(galleryStageTransition){galleryStageTransition.skipTransition();galleryStageTransition=null;workspace.style.viewTransitionName='';}
 clearGallerySurfaceEntrance();
 if(galleryReducedMotion.matches||!Element.prototype.animate){
  galleryStageMutating=true;
  try{mutator();}finally{galleryStageMutating=false;}
  return;
 }
 galleryStageFadeInProgress=true;
 const app=document.querySelector('.app');
 const tabs=document.querySelector('.top .tabs');
 const header=document.querySelector('.top');
 const oldBorder=getComputedStyle(header).borderBottomColor;
 app.setAttribute('aria-busy','true');
 app.classList.add('gallery-route-transitioning');
 // Pause current live input; keyboard events and clicks must not mutate routes
 // during the invisible midpoint (including Settings Escape or tab hotkeys).
 let oldWorkspace=null,oldTabs=null,oldBorderAnim=null,newWorkspace=null,newTabs=null,newBorderAnim=null;
 const animate=(node,frames,timing)=>node.animate(frames,{...timing,fill:'forwards'});
 const fadeTiming={duration:150,easing:'ease-in'};
 const showTiming={duration:150,easing:'ease-out'};
 const visible=node=>Boolean(node&&node.getClientRects().length&&getComputedStyle(node).display!=='none');
 const finish=()=>{
  for(const anim of [oldWorkspace,oldTabs,oldBorderAnim,newWorkspace,newTabs,newBorderAnim])anim?.cancel();
  workspace.style.opacity='';tabs.style.opacity='';header.style.borderBottomColor='';
  app.removeAttribute('aria-busy');app.classList.remove('gallery-route-transitioning');
  galleryStageFadeInProgress=false;
  if(galleryStagePending){const next=galleryStagePending;galleryStagePending=null;queueMicrotask(()=>transitionGalleryStage(next));}
 };
 try{
  oldWorkspace=animate(workspace,[{opacity:1},{opacity:0}],fadeTiming);
  if(visible(tabs))oldTabs=animate(tabs,[{opacity:1},{opacity:0}],fadeTiming);
  oldBorderAnim=animate(header,[{borderBottomColor:oldBorder},{borderBottomColor:'transparent'}],fadeTiming);
 }catch(error){finish();galleryStageMutating=true;try{mutator();}finally{galleryStageMutating=false;}return;}
 oldWorkspace.finished.then(()=>{
  // Make the midpoint state opaque-to-input and transparent-to-view *before*
  // canceling the outgoing animations. The correct new page is mounted here.
  workspace.style.opacity='0';tabs.style.opacity='0';header.style.borderBottomColor='transparent';
  oldWorkspace.cancel();oldTabs?.cancel();oldBorderAnim?.cancel();
  galleryStageMutating=true;
  try{mutator();}finally{galleryStageMutating=false;}
  // Reading layout ensures that the new tab/header geometry is in effect
  // before either incoming opacity starts. Shared branding never moves.
  void workspace.offsetWidth;
  newWorkspace=animate(workspace,[{opacity:0},{opacity:1}],showTiming);
  if(visible(tabs))newTabs=animate(tabs,[{opacity:0},{opacity:1}],showTiming);
  header.style.borderBottomColor='';
  const incomingBorder=getComputedStyle(header).borderBottomColor;
  header.style.borderBottomColor='transparent';
  newBorderAnim=animate(header,[{borderBottomColor:'transparent'},{borderBottomColor:incomingBorder}],showTiming);
  return newWorkspace.finished;
 }).then(finish).catch(error=>{
  console.error('Gallery coordinated page fade failed',error);
  finish();
 });
}
// A route mutation must not happen while the old layout is still fading.
// Guard pointer/keyboard navigation, but retain focus and settings semantics.
function galleryRouteInputGate(event){
 if(!galleryStageFadeInProgress||galleryStageMutating)return;
 if(event.type==='click'||event.type==='keydown'){
  event.preventDefault();event.stopImmediatePropagation();
 }
}
document.querySelector('.app').addEventListener('click',galleryRouteInputGate,true);
document.querySelector('.app').addEventListener('keydown',galleryRouteInputGate,true);
// A disabled CSS animation does not fire animationend. Clean up after the
// normal animation, and when the motion preference changes in either direction.
screen.addEventListener('animationend',event=>{
 if(event.target===screen&&event.animationName==='gallery-surface-in')clearGallerySurfaceEntrance();
});
galleryReducedMotion.addEventListener('change',clearGallerySurfaceEntrance);
let modalExitTimer=null;
function countTag(t){return t==='All Titles'?demo.length:demo.filter(x=>x.tags.includes(t)).length;}
// Browser-only sliding-tab and label-anchored cursor-follow hover-pill experiment.
// No changes have been applied to the Gallery macOS application.
const tabOrder=['discover','library','downloads'];
const tabPagesViewport=document.getElementById('tab-pages-viewport');
const tabPagesTrack=document.getElementById('tab-pages-track');
const tabPages=Object.fromEntries(tabOrder.map(view=>[view,tabPagesViewport.querySelector(`[data-tab-page="${view}"]`)]));

/* v23 — One Mac-style overlay scrollbar for main tabs and anime overviews.
   It is anchored to the visible workspace rather than the hidden tabs viewport.
   No gutter is reserved; switching pages never reveals a native scrollbar. */
const tabScrollOverlay=document.getElementById('tab-scroll-overlay');
const tabScrollThumb=tabScrollOverlay.querySelector('.tab-scroll-thumb');
let tabScrollFadeTimer=null;
let tabScrollIntentUntil=0;
let tabScrollDragging=false;
function hideTabScrollOverlay(){
 clearTimeout(tabScrollFadeTimer);
 tabScrollOverlay.classList.remove('is-visible');
}
function currentScrollSurface(){
 if(document.body.classList.contains('settings-view'))return workspace;
 if(workspace.classList.contains('tab-pages-visible')){
  return tabPagesViewport.hidden?null:tabPages[state.view];
 }
 return screen.hidden?null:workspace;
}
function positionScrollOverlay(){
 const appRect=document.querySelector('.app').getBoundingClientRect();
 const workspaceRect=workspace.getBoundingClientRect();
 tabScrollOverlay.style.top=Math.round(workspaceRect.top-appRect.top+6)+'px';
 tabScrollOverlay.style.bottom=Math.round(appRect.bottom-workspaceRect.bottom+6)+'px';
}
function updateTabScrollOverlay(){
 const page=currentScrollSurface();
 if(!page){hideTabScrollOverlay();return false;}
 positionScrollOverlay();
 const maxScroll=Math.max(0,page.scrollHeight-page.clientHeight);
 const trackHeight=tabScrollOverlay.clientHeight;
 if(maxScroll<=1||trackHeight<=0){hideTabScrollOverlay();return false;}
 const thumbHeight=Math.min(trackHeight,Math.max(40,Math.round(trackHeight*page.clientHeight/page.scrollHeight)));
 const thumbY=(trackHeight-thumbHeight)*(page.scrollTop/maxScroll);
 tabScrollThumb.style.height=thumbHeight+'px';
 tabScrollThumb.style.transform=`translate3d(0,${thumbY}px,0)`;
 return true;
}
function revealTabScrollOverlay(){
 if(!updateTabScrollOverlay())return;
 tabScrollOverlay.classList.add('is-visible');
 clearTimeout(tabScrollFadeTimer);
 tabScrollFadeTimer=setTimeout(()=>{if(!tabScrollDragging)tabScrollOverlay.classList.remove('is-visible')},950);
}
function signalUserScroll(){
 tabScrollIntentUntil=performance.now()+1400;
 revealTabScrollOverlay();
}
for(const page of Object.values(tabPages)){
 page.addEventListener('wheel',()=>{if(page===tabPages[state.view])signalUserScroll()}, {passive:true});
 page.addEventListener('touchmove',()=>{if(page===tabPages[state.view])signalUserScroll()}, {passive:true});
 page.addEventListener('scroll',()=>{
  if(page!==tabPages[state.view])return;
  updateTabScrollOverlay();
  if(performance.now()<tabScrollIntentUntil||tabScrollDragging)revealTabScrollOverlay();
 }, {passive:true});
}
/* The detail overview (and player screen) scroll inside workspace itself. */
workspace.addEventListener('wheel',event=>{
 if(currentScrollSurface()!==workspace)return;
 if(Math.abs(event.deltaY)>=Math.abs(event.deltaX)&&workspace.scrollHeight>workspace.clientHeight)signalUserScroll();
},{passive:true});
workspace.addEventListener('touchmove',()=>{
 if(currentScrollSurface()===workspace)signalUserScroll();
},{passive:true});
workspace.addEventListener('scroll',()=>{
 if(currentScrollSurface()!==workspace)return;
 updateTabScrollOverlay();
 if(performance.now()<tabScrollIntentUntil||tabScrollDragging)revealTabScrollOverlay();
},{passive:true});
document.addEventListener('keydown',event=>{
 const scrollKeys=['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '];
 if(!scrollKeys.includes(event.key)||modalHost.firstChild||!currentScrollSurface())return;
 if(event.target.closest('input,select,textarea,[contenteditable="true"]'))return;
 signalUserScroll();
});
// The visible thumb may be dragged, just like a native scrollbar.
let tabScrollDragStartY=0;
let tabScrollDragStartTop=0;
tabScrollThumb.addEventListener('pointerdown',event=>{
 if(event.button!==0||!updateTabScrollOverlay())return;
 event.preventDefault();
 tabScrollDragging=true;
 tabScrollDragStartY=event.clientY;
 tabScrollDragStartTop=currentScrollSurface().scrollTop;
 tabScrollOverlay.classList.add('is-dragging');
 tabScrollThumb.setPointerCapture(event.pointerId);
 clearTimeout(tabScrollFadeTimer);
});
tabScrollThumb.addEventListener('pointermove',event=>{
 if(!tabScrollDragging)return;
 const page=currentScrollSurface();
 if(!page){endTabScrollDrag();return;}
 const maxScroll=page.scrollHeight-page.clientHeight;
 const thumbTravel=tabScrollOverlay.clientHeight-tabScrollThumb.getBoundingClientRect().height;
 if(thumbTravel>0){page.scrollTop=tabScrollDragStartTop+(event.clientY-tabScrollDragStartY)*maxScroll/thumbTravel}
 revealTabScrollOverlay();
});
function endTabScrollDrag(){
 if(!tabScrollDragging)return;
 tabScrollDragging=false;
 tabScrollOverlay.classList.remove('is-dragging');
 revealTabScrollOverlay();
}
tabScrollThumb.addEventListener('pointerup',endTabScrollDrag);
tabScrollThumb.addEventListener('pointercancel',endTabScrollDrag);
window.addEventListener('resize',()=>requestAnimationFrame(updateTabScrollOverlay));

let tabPagesReady=false;
let tabTrackAnimation=null;
let tabTrackTarget='discover';
function updateActiveTab(view){
 for(const tab of document.querySelectorAll('.tab')){
  const active=tab.dataset.view===view;
  tab.classList.toggle('active',active);
  if(active)tab.setAttribute('aria-current','page');else tab.removeAttribute('aria-current');
 }
}
function tabViewContent(view){
 return view==='discover'?discover():view==='library'?library():downloads();
}
function selectedTabScroll(){
 return workspace.classList.contains('tab-pages-visible')
  ?tabPages[state.view].scrollTop:workspace.scrollTop;
}
function syncTabPanelAccessibility(){
 for(const view of tabOrder){
  const panel=tabPages[view];const active=view===state.view;
  panel.inert=!active;
  panel.setAttribute('aria-hidden',String(!active));
 }
}
function bindTabPageEvents(view){
 const content=tabPages[view].querySelector('.tab-page-content');
 const on=(id,fn)=>{const el=content.querySelector('#'+id);if(el)el.addEventListener('click',fn)};
 for(const el of content.querySelectorAll('[data-detail]'))el.addEventListener('click',()=>{if(searchOpen)closeInlineSearch(false);showDetail(el.dataset.detail);});
 for(const el of content.querySelectorAll('[data-tag]'))el.addEventListener('click',()=>{if(searchOpen)closeInlineSearch(false);hideTabScrollOverlay();state.tag=el.dataset.tag;render();});
 for(const el of content.querySelectorAll('[data-download-filter]'))el.addEventListener('click',()=>{if(searchOpen)closeInlineSearch(false);hideTabScrollOverlay();state.downloadStatus=el.dataset.downloadFilter;render();});
 on('filters',showFilters);on('wh-view-history',whEnter);
 if(view==='discover')whSetupRecentPreview(content);
 for(const button of content.querySelectorAll('[data-wh-recent]'))button.addEventListener('click',()=>{
  const r=whRecords.find(r=>r.id===button.dataset.whRecent);
  if(!r)return;
  if(!r.galleryId||!demo.some(x=>x.id===r.galleryId)){
   modal('Sample Recently Watched entry','<p class="description">This preview record has no matching anime detail page yet.</p>','<button class="btn primary" id="wh-sample-okay">Got it</button>');
   document.getElementById('wh-sample-okay')?.addEventListener('click',closeModal);
   return;
  }
  // This card is on Discover, not inside Watch History. Back must return to Discover.
  showDetail(r.galleryId,false,r.installmentId);
 });
 on('resume',()=>showDetail('demo:02'));on('discover-browse-sources',openSourceManagerFromDiscover);
 on('import',showImport);on('newtag',showNewTag);on('sharetag',showShare);
 on('renametag',showRenameTag);on('deletetag',showDeleteTag);
 on('tag-options',()=>{
  const menu=content.querySelector('#tag-options-menu'),button=content.querySelector('#tag-options');
  if(!menu||!button)return;
  menu.hidden=!menu.hidden;
  button.setAttribute('aria-expanded',String(!menu.hidden));
 });
 on('openfolder',showFolderInfo);
 for(const el of content.querySelectorAll('[data-download-toggle]'))el.addEventListener('click',()=>setDownloadGroupExpanded(el.dataset.downloadToggle,!downloadDemo.expanded.has(el.dataset.downloadToggle)));
 for(const el of content.querySelectorAll('[data-download-dismiss]'))el.addEventListener('click',()=>dismissDownloadEpisode(el.dataset.downloadDismiss));
 for(const el of content.querySelectorAll('[data-dismiss-group]'))el.addEventListener('click',()=>dismissDownloadGroup(el.dataset.dismissGroup));
 for(const el of content.querySelectorAll('[data-download-cancel]'))el.addEventListener('click',()=>cancelDownloadEpisode(el.dataset.downloadCancel));
 for(const el of content.querySelectorAll('[data-download-retry]'))el.addEventListener('click',()=>retryDownloadEpisode(el.dataset.downloadRetry));
 for(const el of content.querySelectorAll('[data-download-pause]'))el.addEventListener('click',()=>toggleDownloadPause(el.dataset.downloadPause));
 on('dismiss-all-downloads',dismissAllFinishedDownloads);
 on('demo-next-download',simulateNextDownload);on('demo-reset-downloads',resetDownloadDemo);
}
function updateLibraryTagRail(content,revealActive=false){
 const rail=content.querySelector('.tagbar');
 const row=content.querySelector('.library-tag-row');
 if(!rail||!row)return;
const back=content.querySelector('#library-tag-prev');
 const next=content.querySelector('#library-tag-next');
 const refresh=()=>{
  const max=Math.max(0,rail.scrollWidth-rail.clientWidth);
  const overflow=max>2;
  row.classList.toggle('has-overflow',overflow);
  const left=overflow&&rail.scrollLeft>2,right=overflow&&rail.scrollLeft<max-2;
  back.disabled=!left;next.disabled=!right;
  rail.classList.toggle('can-left',left);
  rail.classList.toggle('can-right',right);
 };
 const pan=(direction)=>rail.scrollBy({left:direction*Math.max(140,rail.clientWidth*.7),behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
 back.addEventListener('click',()=>pan(-1));
 next.addEventListener('click',()=>pan(1));
 rail.addEventListener('scroll',refresh,{passive:true});
 const showActive=()=>{
  const selected=rail.querySelector('.tagchip.active');
  if(!selected)return;
  const r=rail.getBoundingClientRect(),a=selected.getBoundingClientRect();
  if(a.left<r.left+12)rail.scrollLeft-=r.left+12-a.left;
  else if(a.right>r.right-12)rail.scrollLeft+=a.right-r.right+12;
 };
 rail.galleryRefresh=(reveal=false)=>{
  // The arrows take up space when overflow begins. Measure only after
  // they've appeared, so selected tags stay visible when resizing.
  refresh();if(reveal)showActive();refresh();
 };
 rail.galleryRefresh(revealActive);
}
function renderTabPage(view){
 const panel=tabPages[view];
 const scroll=panel.scrollTop;
 const content=panel.querySelector('.tab-page-content');
 const priorTag=content.querySelector('.tagchip.active')?.dataset.tag;
 const tagScroll=content.querySelector('.tagbar')?.scrollLeft||0;
 if(view==='downloads')captureDownloadScroll();
 content.innerHTML=tabViewContent(view);
 panel.classList.toggle('search-scope-open',searchOpen&&state.view===view);
 panel.dataset.initialized='true';
 bindTabPageEvents(view);
 if(view==='downloads')restoreDownloadScroll();
 panel.scrollTop=scroll;
 requestAnimationFrame(updateTabScrollOverlay);
 if(view==='library'&&content.querySelector('.tagbar')){
  content.querySelector('.tagbar').scrollLeft=tagScroll;
  updateLibraryTagRail(content,priorTag!==state.tag);
 }
}
function measuredTrackX(){
 const transform=getComputedStyle(tabPagesTrack).transform;
 return transform==='none'?0:new DOMMatrixReadOnly(transform).m41;
}
/* v13 — The track travels in % of the *current* viewport width, rather
   than pixels captured when a tab was clicked. Percentage transforms are
   automatically recomputed by the browser on window/container resize,
   including while a WAAPI slide is running. */
function tabTrackPercent(x){
 const width=tabPagesViewport.clientWidth;
 return width>0?x/width*100:0;
}
function tabTrackTransform(percent){return `translate3d(${percent}%,0,0)`;}
function freezeTabTrack(){
 if(!tabTrackAnimation)return measuredTrackX();
 const current=measuredTrackX();
 const transform=tabTrackTransform(tabTrackPercent(current));
 tabTrackAnimation.onfinish=null;
 tabTrackAnimation.cancel();
 tabTrackAnimation=null;
 tabPagesTrack.style.transform=transform;
 return current;
}
function snapTabTrack(view){
 freezeTabTrack();
 tabTrackTarget=view;
 tabPagesTrack.style.transform=tabTrackTransform(-tabOrder.indexOf(view)*100);
}
function animateTabTrack(view){
 const width=tabPagesViewport.clientWidth;
 if(width<=0)return;
 const from=freezeTabTrack();
 const fromPercent=tabTrackPercent(from);
 const destinationPercent=-tabOrder.indexOf(view)*100;
 tabTrackTarget=view;
 const toTransform=tabTrackTransform(destinationPercent);
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||Math.abs(fromPercent-destinationPercent)<.05){
  tabPagesTrack.style.transform=toTransform;
  return;
 }
 // A single uninterrupted trajectory through intermediate pages; both
 // keyframes remain relative to the viewport width even during resizing.
 const pages=Math.abs(destinationPercent-fromPercent)/100;
 const duration=Math.round(Math.max(160,Math.min(520,310*Math.pow(pages,.68))));
 const fromTransform=tabTrackTransform(fromPercent);
 tabPagesTrack.style.transform=toTransform;
 const running=tabPagesTrack.animate(
  [{transform:fromTransform},{transform:toTransform}],
  {duration,easing:'cubic-bezier(.32,.08,.22,1)',fill:'both'}
 );
 tabTrackAnimation=running;
 running.onfinish=()=>{
  if(tabTrackAnimation!==running)return;
  tabPagesTrack.style.transform=toTransform;
  tabTrackAnimation=null;
  running.cancel();
 };
}
function showTabPages(refreshCurrent=true){
 hideTabScrollOverlay();
 const returning=!workspace.classList.contains('tab-pages-visible');
 workspace.classList.add('tab-pages-visible');
 workspace.classList.remove('library-view');
 screen.dataset.surfaceKey='';
 clearGallerySurfaceEntrance();
 tabPagesViewport.hidden=false;
 screen.hidden=true;
 if(!tabPagesReady){
  tabOrder.forEach(renderTabPage);
  tabPagesReady=true;
 }else if(returning){
  tabOrder.forEach(renderTabPage);
 }else if(refreshCurrent){renderTabPage(state.view);}
 syncTabPanelAccessibility();
 if(returning)snapTabTrack(state.view);
}
function setView(view){
 if(!tabOrder.includes(view))return;
 if(whOpen){whExit();if(view==='discover')return;}
 if(searchOpen)closeInlineSearch(false);
 const oldView=state.view;
 if(view!==oldView){hideTabScrollOverlay();document.getElementById('sf-dl-undo-global')?.remove();}
 const wasTop=!state.detailId&&!state.playback;
 if(oldView===view&&wasTop)return;
 const changeView=()=>{
  state.playback=null;state.view=view;state.detailId=null;state.query='';
  updateActiveTab(view);
  searchToggle.setAttribute('aria-label',view==='library'?'Search your library':view==='downloads'?'Search downloads':'Search anime');
 };
 if(!wasTop){
  transitionGalleryStage(()=>{changeView();render();}); // State and navigation switch at the invisible midpoint.
 }else{
  changeView();
  if(!tabPages[view].dataset.initialized)renderTabPage(view);
  syncTabPanelAccessibility();
  animateTabTrack(view); // Approved main-tab slide remains untouched.
 }

}
function artCard(item){return `<article class="poster-item"><button class="poster-button" data-detail="${escapeHTML(item.id)}" title="View ${escapeHTML(item.name)}"><div class="poster" style="background:${item.art}"><span class="art-orb"></span><span class="poster-name">${escapeHTML(item.name)}</span></div><div class="poster-title">${escapeHTML(item.name)}</div><div class="meta">${escapeHTML(item.status)} · ${escapeHTML(item.lang)}</div></button></article>`;}
function gallery(items){return items.length?`<div class="poster-grid">${items.map(artCard).join('')}</div>`:'<div class="empty">No matching anime in this sample collection.</div>';}
function searchItems(items){if(!state.query.trim())return items;let q=state.query.trim().toLowerCase();return items.filter(x=>x.name.toLowerCase().includes(q));}
function pageHeader(title, actions='', secondary='', view=''){
  // Unified minimal page titles on Discover, Library and Downloads.
  // Keep the existing page actions, filters, tags and navigation unchanged.
  const heading=`<div class="sf-page-title sf-optical-title"><h1>${escapeHTML(title)}</h1></div>`;
  return `<section class="page-header page-header-${escapeHTML(view)}" aria-label="${escapeHTML(title)} page header"><div class="page-header-primary">${heading}<div class="page-header-actions">${actions}</div></div><div class="page-header-divider" aria-hidden="true"></div>${secondary?`<div class="page-header-secondary">${secondary}</div>`:''}</section>`;
}
/* Gallery v100 · Watch History integrated from approved Layout Experiment 03.
 * UI demo records remain clearly labeled samples; local-video playback can additionally
 * produce local browser-preview records. No provider streams are fabricated. */
const whStorageKey='gallery.watchHistory.v100.preview';
function whMakeEpisodes(count, watchedCount=0, partialEpisode=null, partialSeconds=0, duration=1440){
 return Array.from({length:count},(_,i)=>{const n=i+1,watched=n<=watchedCount;return {n,watched,started:watched||n===partialEpisode,progressSeconds:watched?duration:(n===partialEpisode?partialSeconds:0),duration};});
}
const whSeed=[
 {id:'q2',library:true,group:'quints',galleryId:'demo:quints',installmentId:'quints-s2',title:'The Quintessential Quintuplets ∬',short:'Quints ∬',cover:'linear-gradient(145deg,#413759,#7e6694 48%,#cda1ba)',last:'2026-11-04',dates:['2026-11-04','2026-11-03'],episodes:whMakeEpisodes(12,7,8,872)},
 {id:'pkm',library:false,group:'pokemon',galleryId:null,installmentId:'pokemon-ind',title:'Pokémon — Indigo League',short:'Pokémon',cover:'linear-gradient(145deg,#285886,#5c8cc6 52%,#f4c36e)',last:'2026-11-03',dates:['2025-06-21','2026-11-03'],episodes:whMakeEpisodes(100,74,75,608,1320)},
 {id:'frieren',library:true,group:'frieren',galleryId:null,installmentId:'frieren-s1',title:"Frieren: Beyond Journey's End",short:'Frieren',cover:'linear-gradient(147deg,#3f6569,#8cbcb4 48%,#b9bd95)',last:'2026-10-30',dates:['2026-10-30'],episodes:whMakeEpisodes(28,16,17,914)},
 {id:'q1',library:true,group:'quints',galleryId:'demo:quints',installmentId:'quints-s1',title:'The Quintessential Quintuplets',short:'Quints',cover:'linear-gradient(145deg,#533a60,#b67f9b 52%,#ebbaa4)',last:'2026-10-28',dates:['2025-06-19','2026-10-28'],episodes:whMakeEpisodes(12,12)},
 {id:'solo',library:false,group:'solo',galleryId:'demo:solo',installmentId:'solo-s1',title:'Solo Leveling',short:'Solo',cover:'linear-gradient(148deg,#121b36,#49618e 49%,#8b6ab1)',last:'2026-09-12',dates:['2026-09-12'],episodes:whMakeEpisodes(12,8,9,430)},
 {id:'violet',library:true,group:'violet',galleryId:null,installmentId:'violet-s1',title:'Violet Evergarden',short:'Violet',cover:'linear-gradient(145deg,#465b8a,#7b99ba 51%,#cfb69b)',last:'2025-08-20',dates:['2025-08-20'],episodes:whMakeEpisodes(13,13)},
 {id:'moon',library:false,group:'moon',galleryId:'demo:01',installmentId:'moon-s1',title:'Moonlit Signals 2025',short:'Moonlit',cover:'linear-gradient(145deg,#322554,#74548f 51%,#c48b9c)',last:'2026-01-15',dates:['2026-01-15'],episodes:whMakeEpisodes(12,3,4,319)},
 {id:'aot',library:true,group:'aot',galleryId:'demo:aot',installmentId:'aot-final',title:'Attack on Titan: The Final Season',short:'AoT',cover:'linear-gradient(150deg,#334447,#697b77 50%,#958c76)',last:'2025-04-10',dates:['2025-04-10'],episodes:whMakeEpisodes(16,9,10,611)},
 {id:'astra',library:false,group:'astra',galleryId:'demo:02',installmentId:'astra-s1',title:'Astra Afterlight',short:'Astra',cover:'linear-gradient(145deg,#213654,#386e88 50%,#88c2c1)',last:'2024-12-16',dates:['2024-12-16'],episodes:whMakeEpisodes(12,12)}
];
function whLoadRecords(){
 try{const saved=JSON.parse(localStorage.getItem(whStorageKey));if(Array.isArray(saved)&&saved.every(r=>typeof r.id==='string'&&Array.isArray(r.episodes)))return saved;}
 catch{}
 return whSeed.map(r=>({...r,dates:[...r.dates],episodes:r.episodes.map(e=>({...e}))}));
}
let whRecords=whLoadRecords();let whOpen=false,whFilter='all',whSort='newest',whSearch='',whExpanded=new Set(),whPending=new Set();
let whSuspended=null,whParentView='discover';
let whInnerScrollers=new Map();
function whSave(){try{localStorage.setItem(whStorageKey,JSON.stringify(whRecords));}catch{/* Private/browser file preview may forbid storage */}}
/* Manual watched-state changes are an override, not a fake playback event:
   preserve saved duration/position separately from the status indicator. */
function whEpisodeStatus(ep){return ['never','partial','watched'].includes(ep.manualStatus)?ep.manualStatus:ep.watched?'watched':ep.started?'partial':'never';}
function whEpisodeNextStatus(ep){const status=whEpisodeStatus(ep);return status==='never'?'partial':status==='partial'?'watched':'never';}
function whEpisodeStatusLabel(status){return status==='watched'?'Watched':status==='partial'?'Partially watched':'Not watched';}
function whEpisodePress(status){return status==='watched'?'true':status==='partial'?'mixed':'false';}
function whCount(r){return r.episodes.reduce((n,e)=>n+(whEpisodeStatus(e)==='watched'?1:0),0)}
function whCompleted(r){return r.episodes.length>0&&whCount(r)===r.episodes.length}
function whFormatDate(date){const d=new Date(date+'T12:00:00');return Number.isNaN(d.getTime())?date:d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});}
function whFmt(sec){const n=Math.max(0,Math.floor(Number(sec)||0));return `${Math.floor(n/60)}:${String(n%60).padStart(2,'0')}`;}
function whLastEpisode(r){return r.episodes.find(e=>e.n===r.latestEpisode)||[...r.episodes].reverse().find(e=>e.started)||r.episodes[0]}
function whSorted(list){return [...list].sort((a,b)=>whSort==='newest'?b.last.localeCompare(a.last):a.last.localeCompare(b.last));}
const whMonths=['january','february','march','april','may','june','july','august','september','october','november','december'];
function whSearchGroups(list){
 const q=whSearch.trim().toLowerCase();if(!q)return [{label:null,items:whSorted(list)}];
 const m=q.match(/^([a-z]+)\s+((?:19|20)\d{2})$/),month=m?whMonths.indexOf(m[1]):-1;
 const year=/^(?:19|20)\d{2}$/.test(q)?q:q==='last year'?String(new Date().getFullYear()-1):m&&month!==-1?m[2]:null;
 if(year!==null){
  const byDate=whSorted(list.filter(r=>r.dates.some(d=>d.startsWith(year)&&(month===-1||Number(d.slice(5,7))===month+1))));
  const seen=new Set(byDate.map(r=>r.id));const title=whSorted(list.filter(r=>!seen.has(r.id)&&r.title.toLowerCase().includes(q)));
  const label=month===-1?`Watched in ${year}`:`Watched in ${whMonths[month].slice(0,1).toUpperCase()+whMonths[month].slice(1)} ${year}`;
  return [{label,items:byDate},{label:'Title matches',items:title}].filter(group=>group.items.length);
 }
 return [{label:null,items:whSorted(list.filter(r=>r.title.toLowerCase().includes(q)))}];
}
function whGroups(){return whSearchGroups(whRecords.filter(r=>!whPending.has(r.id)&&(whFilter==='all'||(whFilter==='completed')===whCompleted(r))));}
function whSmallIcon(name){const glyph={
  back:'<path d="m14 6-6 6 6 6"/><path d="M8 12h12"/>',
  sort:'<path d="M8 3v18m-4-4 4 4 4-4M16 21V3m-4 4 4-4 4 4"/>',
  trash:'<path d="M4 7h16M10 4h4M6 7l1 14h10l1-14M10 11v6m4-6v6"/>',
  check:'<path d="m5 12 4 4L19 6"/>',
  completed:'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
  chevron:'<path d="m6 9 6 6 6-6"/>',
  history:'<path d="M3 12a9 9 0 1 0 2.7-6.3L3 8"/><path d="M3 3v5h5M12 7v5l4 2"/>'
 };
 return `<svg class="icon" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${glyph[name]||''}</svg>`;
}
/* v102: Soft Glide + Lab 03's coordinated space transfer and pointer targeting.
 * The row gains panel-width once, then *transfers* it between covers. This avoids
 * a bouncing View History tile and prevents covers sliding under a stationary
 * pointer from silently changing the active anime. */
let whRecentController=null;
function whSetupRecentPreview(content){
 if(whRecentController){whRecentController.destroy();whRecentController=null;}
 const row=content.querySelector('.wh-recent-row');if(!row)return;
 const items=[...row.querySelectorAll('.wh-recent-item')];
 const historyTile=row.querySelector('#wh-view-history');
 if(!items.length)return;
 const options={open:550,close:375,delay:100};
 const easing={open:'cubic-bezier(.35,0,.13,1)',close:'cubic-bezier(.25,0,.22,1)'};
 const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
 let observer=null,pending=null,active=null,animation=null,frame=0,destroyed=false;
 let pointerInside=false,pointerX=0,pointerY=0,lastChosenX=null,lastChosenY=null;
 let lastMotionAt=-Infinity,panelWidth=188;
 let extras=items.map(()=>0);
 const sum=arr=>arr.reduce((total,n)=>total+n,0);
 const cancelPending=()=>{if(pending){clearTimeout(pending.timer);pending=null;}};
 const bezier=(curve,progress)=>{
  if(progress<=0)return 0;if(progress>=1)return 1;
  const c=curve.match(/cubic-bezier\(([^)]+)\)/)[1].split(',').map(Number);
  const bez=(a,b,t)=>3*a*(1-t)*(1-t)*t+3*b*(1-t)*t*t+t*t*t;
  let lo=0,hi=1;for(let i=0;i<18;i++){const mid=(lo+hi)/2;if(bez(c[0],c[2],mid)<progress)lo=mid;else hi=mid;}
  return Math.max(0,Math.min(1,bez(c[1],c[3],(lo+hi)/2)));
 };
 const paint=()=>items.forEach((item,i)=>{item.style.flexBasis=(66+Math.max(0,extras[i])).toFixed(3)+'px';});
 function sample(time,repeat=true){
  if(!animation||destroyed)return;
  const a=animation;
  const p=a.duration>0?Math.min(1,(time-a.time)/a.duration):1;
  const ease=bezier(a.toTotal>=a.fromTotal?easing.open:easing.close,p);
  const transfer=bezier(easing.open,p);
  const total=a.fromTotal+(a.toTotal-a.fromTotal)*ease;
  let weights=a.fromWeights.map((w,i)=>w+(a.toWeights[i]-w)*transfer);
  const weightSum=sum(weights);
  if(weightSum>1e-8)weights=weights.map(w=>Math.max(0,w/weightSum));
  extras=weights.map(w=>w*total);paint();
  if(p>=1){animation=null;frame=0;if(active===null)row.classList.remove('is-switching');}
  else if(repeat)frame=requestAnimationFrame(t=>sample(t));
 }
 function stop(){if(frame){cancelAnimationFrame(frame);frame=0;}if(animation)sample(performance.now(),false);}
 function activate(item){
  if(destroyed)return;
  cancelPending();
  if(active===item)return;
  stop();
  const previous=active;active=item;
  lastMotionAt=performance.now();
  const total=sum(extras);
  const from=total>1e-6?extras.map(w=>w/total):items.map(x=>x===previous?1:0);
  const to=item?items.map(x=>x===item?1:0):from;
  const switching=Boolean(item&&(previous||total>1e-6));
  row.classList.toggle('is-switching',switching);
  row.style.setProperty('--wh-hover-ms',options.open+'ms');
  items.forEach(x=>x.classList.toggle('is-active',x===item));
  if(reducedMotion.matches){animation=null;extras=items.map(x=>x===item?panelWidth:0);paint();return;}
  animation={time:performance.now(),duration:item?options.open:options.close,
    fromTotal:total,toTotal:item?panelWidth:0,fromWeights:from,toWeights:to};
  frame=requestAnimationFrame(t=>sample(t));
 }
 function enter(item,x,y){
  if(item===active){cancelPending();return;}
  const inMotion=performance.now()-lastMotionAt<Math.max(options.open,options.close)+110;
  if(active||inMotion||options.delay===0){
   cancelPending();activate(item);lastChosenX=x;lastChosenY=y;return;
  }
  if(pending?.item===item)return;
  cancelPending();
  const request={item,timer:null};pending=request;
  request.timer=setTimeout(()=>{
   if(destroyed||pending!==request||!pointerInside)return;
   const target=document.elementFromPoint(pointerX,pointerY);
   if(target?.closest('.wh-recent-item')!==item||!target?.closest('.wh-recent-card')){cancelPending();return;}
   pending=null;activate(item);lastChosenX=pointerX;lastChosenY=pointerY;
  },options.delay);
 }
 function onPointerMove(event){
  if(event.pointerType==='touch'||!event.isPrimary||destroyed)return;
  pointerInside=true;pointerX=event.clientX;pointerY=event.clientY;
  const cover=event.target.closest('.wh-recent-card');
  const item=cover?.closest('.wh-recent-item');
  if(item&&!item.classList.contains('is-preview-hidden')){
   if(active&&active!==item&&lastChosenX!==null){
    // Moving covers must not steal selection when the cursor itself hardly moved.
    if(Math.hypot(event.clientX-lastChosenX,event.clientY-lastChosenY)<18)return;
   }
   enter(item,event.clientX,event.clientY);
  }else if(event.target.closest('#wh-view-history')){cancelPending();activate(null);}
 }
 function onPointerLeave(event){
  if(event.pointerType==='touch'||destroyed)return;
  pointerInside=false;lastChosenX=lastChosenY=null;cancelPending();activate(null);
 }
 row.addEventListener('pointermove',onPointerMove);
 row.addEventListener('pointerleave',onPointerLeave);
 const focusHandlers=[];
 for(const item of items){
  const button=item.querySelector('.wh-recent-card');
  const onFocus=()=>activate(item);
  const onFocusOut=event=>{if(!item.contains(event.relatedTarget)&&active===item)activate(null);};
  button.addEventListener('focus',onFocus);item.addEventListener('focusout',onFocusOut);
  focusHandlers.push({item,button,onFocus,onFocusOut});
 }
 function fit(){
  if(destroyed)return;
  const width=row.clientWidth;if(width<1)return;
  // Leave room for the widest active panel plus the final View History tile.
  const panel=Math.min(188,Math.max(55,width-66*2-10));
  row.style.setProperty('--wh-panel-width',panel+'px');
  const maximum=Math.max(1,Math.floor((width-66-panel)/(66+10)));
  items.forEach((item,i)=>{
   const hidden=i>=maximum;item.classList.toggle('is-preview-hidden',hidden);
   if(hidden&&item===active)activate(null);
  });
  if(Math.abs(panel-panelWidth)>.1){
   stop();const ratio=panelWidth>0?panel/panelWidth:1;
   extras=extras.map(x=>x*ratio);panelWidth=panel;paint();
   if(active){
    const total=sum(extras);
    const from=total>0?extras.map(x=>x/total):items.map(x=>x===active?1:0);
    animation={time:performance.now(),duration:options.open,fromTotal:total,toTotal:panelWidth,
      fromWeights:from,toWeights:items.map(x=>x===active?1:0)};
    frame=requestAnimationFrame(t=>sample(t));
   }
  }
 }
 if(typeof ResizeObserver==='function'){
  observer=new ResizeObserver(fit);observer.observe(row);
 }else window.addEventListener('resize',fit,{passive:true});
 fit();
 whRecentController={destroy(){
  destroyed=true;cancelPending();stop();observer?.disconnect();
  if(!observer)window.removeEventListener('resize',fit);
  row.removeEventListener('pointermove',onPointerMove);
  row.removeEventListener('pointerleave',onPointerLeave);
  focusHandlers.forEach(({item,button,onFocus,onFocusOut})=>{
   button.removeEventListener('focus',onFocus);item.removeEventListener('focusout',onFocusOut);
  });
 }};
}
function whPreviewMarkup(){
 const seen=new Set();const recent=[...whRecords].sort((a,b)=>b.last.localeCompare(a.last)).filter(r=>{if(seen.has(r.group))return false;seen.add(r.group);return true;});
 return `<div class="continue-shell"><div class="continue-clip"><section class="continue wh-recent" aria-label="Recently Watched">
 <div class="wh-recent-header">Recently Watched</div>
 <div class="wh-recent-row">${recent.map(r=>`<div class="wh-recent-item"><button class="wh-recent-card" type="button" data-wh-recent="${escapeHTML(r.id)}" style="--cover:${r.cover}" aria-label="Open ${escapeHTML(r.title)}; ${whCompleted(r)?'Completed':`Episode ${whLastEpisode(r).n}`}"><span class="wh-recent-card-label">${escapeHTML(r.short)}</span></button><div class="wh-recent-info" aria-hidden="true"><strong>${escapeHTML(r.title)}</strong><span>${whCompleted(r)?'Completed':`Episode ${whLastEpisode(r).n}`}</span></div></div>`).join('')}
 <button class="wh-recent-view" type="button" id="wh-view-history">${whSmallIcon('history')}<span>View History</span></button></div></section></div></div>`;
}
function whEpisodeMarkup(r,ep){
 const status=whEpisodeStatus(ep),label=whEpisodeStatusLabel(status),next=whEpisodeStatusLabel(whEpisodeNextStatus(ep));
 return `<button type="button" class="wh-episode wh-episode-row" data-wh-episode="${escapeHTML(r.id)}:${ep.n}" aria-pressed="${whEpisodePress(status)}" aria-label="Episode ${ep.n}: ${label}. Next: ${next}" title="${label} — click to mark ${next}"><span class="wh-episode-main"><span class="wh-episode-number">Episode ${ep.n}</span>${status==='partial'&&ep.started&&ep.progressSeconds>0?`<span class="wh-episode-position">${whFmt(ep.progressSeconds)} / ${whFmt(ep.duration)}</span>`:''}</span><span class="wh-episode-toggle"><span class="wh-status-icon is-${status}">${status==='watched'?whSmallIcon('check'):''}</span><span class="wh-episode-label">${label}</span></span></button>`;
}
function whSummaryMarkup(r){
 const watched=whCount(r),total=r.episodes.length,complete=whCompleted(r),open=whExpanded.has(r.id),pct=total?watched/total*100:0;
 const last=whLastEpisode(r);
 return `<div class="wh-summary">
 <button class="wh-summary-hit" type="button" data-wh-expand="${escapeHTML(r.id)}" aria-expanded="${open}" aria-label="${open?'Collapse':'Expand'} episodes for ${escapeHTML(r.title)}" title="${open?'Collapse episodes':'View episodes'}"></button>
 <button class="wh-cover-button" type="button" data-wh-open="${escapeHTML(r.id)}" title="Open anime details"><span class="wh-cover" style="--cover:${r.cover}"><span>${escapeHTML(r.short)}</span></span></button>
 <div class="wh-info"><button class="wh-anime-title" type="button" data-wh-open="${escapeHTML(r.id)}">${escapeHTML(r.title)}</button>
 ${complete?`<div class="wh-completed">${whSmallIcon('completed')} Completed</div>`:`<div class="wh-meta">Episode ${last?.n||1} · ${whFmt(last?.progressSeconds)} / ${whFmt(last?.duration)}</div><div class="wh-meta">${watched} of ${total} episodes watched</div><div class="wh-progress gallery-split-timeline" aria-hidden="true"><div class="wh-progress-done" style="flex-basis:${galleryTimelineFill(pct)}"></div><div class="wh-progress-rest"></div></div>`}
 <div class="wh-meta">Last watched ${whFormatDate(r.last)}</div></div>
 <div class="wh-actions"><span class="wh-action wh-expand" aria-hidden="true">${whSmallIcon('chevron')}</span><button class="wh-action wh-trash" type="button" data-wh-remove="${escapeHTML(r.id)}" aria-label="Remove ${escapeHTML(r.title)} from history" title="Remove from history">${whSmallIcon('trash')}</button></div>
 </div>`;
}
function whRowMarkup(r){const open=whExpanded.has(r.id);return `<section class="wh-season ${open?'is-expanded':''}" data-wh-row="${escapeHTML(r.id)}" aria-label="${escapeHTML(r.title)}">${whSummaryMarkup(r)}<div class="wh-episodes"><div class="wh-episodes-inner" ${open?'':'inert aria-hidden="true"'}><div class="wh-episodes-content"><div class="wh-episode-head"><strong>Episodes</strong><span>${whCount(r)} / ${r.episodes.length} watched</span></div><div class="wh-episode-shell" data-wh-shell="${escapeHTML(r.id)}"><div class="wh-episode-scroll gallery-episode-scroll" role="region" tabindex="0" aria-label="Scrollable episodes for ${escapeHTML(r.title)}">${r.episodes.map(ep=>whEpisodeMarkup(r,ep)).join('')}</div><div class="wh-inner-overlay" aria-hidden="true"><div class="wh-inner-thumb"></div></div></div><p class="wh-episode-hint">Click an episode to cycle Not Watched, Partially Watched, and Watched. Saved playback position is kept separately.</p></div></div></div></section>`;}
function whPageMarkup(){
 const groups=whGroups(),total=groups.reduce((n,g)=>n+g.items.length,0),removed=whRecords.filter(r=>whPending.has(r.id));
 return `<section id="wh-root" aria-label="Watch History">
 <header class="detail-page-header wh-page-header">
  <h1 class="detail-title sf-optical-title">Watch History</h1>
  <button type="button" class="detail-back" data-wh-exit>${icon('back',18)} Back to Discover</button>
 </header>
 <div class="wh-controls"><div class="wh-segmented" role="group" aria-label="Filter Watch History">${[['all','All'],['progress','In Progress'],['completed','Completed']].map(([name,label])=>`<button type="button" data-wh-filter="${name}" aria-pressed="${whFilter===name}">${label}</button>`).join('')}</div>
 <button type="button" class="wh-sort" data-wh-sort title="Reverse watch history sorting">${whSmallIcon('sort')} ${whSort==='newest'?'Newest First':'Oldest First'}</button></div>
 ${removed.length?`<aside class="wh-undo" aria-label="Pending removals"><div class="wh-undo-top"><div><strong>${removed.length} ${removed.length===1?'season':'seasons'} removed from view</strong><div class="wh-undo-hint">Undo is available until you leave Watch History.</div></div><button type="button" class="btn small" data-wh-undo-all>Undo all</button></div><div class="wh-undo-items">${removed.map(r=>`<div class="wh-undo-item"><span>${escapeHTML(r.title)}</span><button type="button" data-wh-undo="${escapeHTML(r.id)}" aria-label="Undo removal of ${escapeHTML(r.title)}">Undo</button></div>`).join('')}</div></aside>`:''}
 <div class="wh-result-count">${total} ${total===1?'season':'seasons'} ${whSearch?'matching your search':'in this view'}</div>
 ${total?groups.map(g=>`${g.label?`<div class="wh-match-heading">${escapeHTML(g.label)}</div>`:''}<div class="wh-list">${g.items.map(whRowMarkup).join('')}</div>`).join(''):`<div class="wh-empty">Nothing to show. ${whSearch?'Try a different title or viewing date.':'Try another filter, or undo a removal.'}</div>`}
 <div class="wh-prototype-note">Gallery v103 design preview: the initial history entries and covers are sample data for testing the UI. Actual source streaming isn't yet connected in this HTML prototype. When a supported local video plays, this preview can record its progress on this device.</div>
 </section>`;
}
function whAttachInner(area,overlay){
 const thumb=overlay.querySelector('.wh-inner-thumb');let timer=null,dragging=false,dragY=0,dragTop=0,intent=0;
 const update=()=>{const max=area.scrollHeight-area.clientHeight,track=overlay.clientHeight;if(max<=1||track<=0){overlay.classList.remove('is-visible');return false}const h=Math.min(track,Math.max(40,Math.round(track*area.clientHeight/area.scrollHeight)));thumb.style.height=h+'px';thumb.style.transform=`translate3d(0,${(track-h)*area.scrollTop/max}px,0)`;return true;};
 const reveal=()=>{if(!update())return;overlay.classList.add('is-visible');clearTimeout(timer);timer=setTimeout(()=>{if(!dragging)overlay.classList.remove('is-visible');},950);};
 const intentScroll=()=>{intent=performance.now()+1400;reveal();};
 const onScroll=()=>{update();if(performance.now()<intent||dragging)reveal();};
 const onKey=e=>{if(['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(e.key))intentScroll();};
 /* Native scroll chaining through clipped, non-scrollable wrappers; no wheel interception. */
 const down=e=>{if(e.button!==0||!update())return;e.preventDefault();dragging=true;dragY=e.clientY;dragTop=area.scrollTop;overlay.classList.add('is-dragging','is-visible');clearTimeout(timer);thumb.setPointerCapture(e.pointerId);};
 const move=e=>{if(!dragging)return;const distance=overlay.clientHeight-thumb.getBoundingClientRect().height,max=area.scrollHeight-area.clientHeight;if(distance>0)area.scrollTop=dragTop+(e.clientY-dragY)*max/distance;reveal();};
 const up=()=>{if(!dragging)return;dragging=false;overlay.classList.remove('is-dragging');reveal();};
 area.addEventListener('wheel',intentScroll,{passive:true});area.addEventListener('touchmove',intentScroll,{passive:true});area.addEventListener('scroll',onScroll,{passive:true});area.addEventListener('keydown',onKey);
 thumb.addEventListener('pointerdown',down);thumb.addEventListener('pointermove',move);thumb.addEventListener('pointerup',up);thumb.addEventListener('pointercancel',up);thumb.addEventListener('lostpointercapture',up);
 return {area,update,destroy(){clearTimeout(timer);area.removeEventListener('wheel',intentScroll);area.removeEventListener('touchmove',intentScroll);area.removeEventListener('scroll',onScroll);area.removeEventListener('keydown',onKey);thumb.removeEventListener('pointerdown',down);thumb.removeEventListener('pointermove',move);thumb.removeEventListener('pointerup',up);thumb.removeEventListener('pointercancel',up);thumb.removeEventListener('lostpointercapture',up);}};
}
function whDestroyInner(){for(const scroller of whInnerScrollers.values())scroller.destroy();whInnerScrollers.clear();}
/* Expand/collapse in place so DOM, scroll position and animated height remain stable. */
function whToggleRow(id){
 const row=[...screen.querySelectorAll('[data-wh-row]')].find(el=>el.dataset.whRow===id);
 if(!row)return;
 const opening=!whExpanded.has(id);
 if(opening)whExpanded.add(id);else whExpanded.delete(id);
 row.classList.toggle('is-expanded',opening);
 const hit=row.querySelector('.wh-summary-hit');
 const record=whRecords.find(r=>r.id===id);
 hit.setAttribute('aria-expanded',String(opening));
 hit.setAttribute('aria-label',`${opening?'Collapse':'Expand'} episodes for ${record?.title||''}`);
 hit.title=opening?'Collapse episodes':'View episodes';
 const inner=row.querySelector('.wh-episodes-inner');
 inner.inert=!opening;
 if(opening)inner.removeAttribute('aria-hidden');else inner.setAttribute('aria-hidden','true');
 if(opening&&!whInnerScrollers.has(id)){
  const shell=row.querySelector('[data-wh-shell]');
  const area=shell.querySelector('.wh-episode-scroll');
  const scroller=whAttachInner(area,shell.querySelector('.wh-inner-overlay'));
  whInnerScrollers.set(id,scroller);
  const last=record&&whLastEpisode(record);
  const columns=matchMedia('(max-width:820px)').matches?1:2;
  if(record&&record.episodes.length>6*columns&&last)
   area.scrollTop=Math.max(0,(Math.floor((last.n-1)/columns)-2)*42);
 }
 if(opening)requestAnimationFrame(()=>{if(whExpanded.has(id))whInnerScrollers.get(id)?.update();});
 row.querySelector('.wh-episodes').addEventListener('transitionend',event=>{
  if(event.propertyName==='grid-template-rows')updateTabScrollOverlay();
 },{once:true});
 requestAnimationFrame(updateTabScrollOverlay);
}
function whRender({keepScroll=true}={}){
 if(!whOpen)return;
 const old=keepScroll?workspace.scrollTop:0;
 const prevPositions=new Map([...whInnerScrollers.entries()].map(([id,scroller])=>[id,scroller.area.scrollTop]));
 whDestroyInner();screen.innerHTML=whPageMarkup();
 for(const id of whExpanded){
  const shell=[...screen.querySelectorAll('[data-wh-shell]')].find(x=>x.dataset.whShell===id);if(!shell)continue;
  const area=shell.querySelector('.wh-episode-scroll');const scroller=whAttachInner(area,shell.querySelector('.wh-inner-overlay'));whInnerScrollers.set(id,scroller);
  if(prevPositions.has(id))area.scrollTop=prevPositions.get(id);
  else {const r=whRecords.find(r=>r.id===id);const ep=r&&whLastEpisode(r);const columns=matchMedia('(max-width:820px)').matches?1:2;if(r&&r.episodes.length>6*columns&&ep)area.scrollTop=Math.max(0,(Math.floor((ep.n-1)/columns)-2)*42);}
  scroller.update();
 }
 workspace.scrollTop=old;
 requestAnimationFrame(updateTabScrollOverlay);
}
function whUpdateEpisodeInPlace(button,r,ep){
 const status=whEpisodeStatus(ep),label=whEpisodeStatusLabel(status),next=whEpisodeStatusLabel(whEpisodeNextStatus(ep));
 button.setAttribute('aria-pressed',whEpisodePress(status));button.setAttribute('aria-label',`Episode ${ep.n}: ${label}. Next: ${next}`);button.title=`${label} — click to mark ${next}`;
 const mark=button.querySelector('.wh-status-icon');mark.className='wh-status-icon is-'+status;mark.innerHTML=status==='watched'?whSmallIcon('check'):'';
 button.querySelector('.wh-episode-label').textContent=label;
 const main=button.closest('.wh-episode').querySelector('.wh-episode-main');let position=main.querySelector('.wh-episode-position');
 if(status==='partial'&&ep.started&&ep.progressSeconds>0){if(!position){position=document.createElement('span');position.className='wh-episode-position';main.append(position)}position.textContent=`${whFmt(ep.progressSeconds)} / ${whFmt(ep.duration)}`;}else position?.remove();
 const row=button.closest('.wh-season');const replacement=document.createElement('template');replacement.innerHTML=whSummaryMarkup(r);row.querySelector('.wh-summary').replaceWith(replacement.content.firstElementChild);
 row.querySelector('.wh-episode-head span').textContent=`${whCount(r)} / ${r.episodes.length} watched`;
 // No rebuild of episode panel; its scrollbar, selected control and scroll position stay stationary.
}
function whEnter(){
 if(whOpen)return;
 transitionGalleryStage(()=>{
  if(searchOpen)closeInlineSearch(false);
  whParentView=state.view;whSuspended=null;whOpen=true;
  document.body.classList.add('watch-history-view');
  whFilter='all';whSort='newest';whSearch='';whExpanded.clear();whPending.clear();
  hideTabScrollOverlay();render();workspace.scrollTop=0;
 });
}
function whSuspendForDetail(){
 whSuspended={scroll:workspace.scrollTop,inner:new Map([...whInnerScrollers].map(([id,scroller])=>[id,scroller.area.scrollTop]))};
 whDestroyInner();whOpen=false;document.body.classList.remove('watch-history-view');
}
function whResumeFromDetail(){
 const saved=whSuspended;
 whOpen=true;state.playback=null;state.detailId=null;
 state.view=whParentView;updateActiveTab(state.view);
 document.body.classList.add('watch-history-view');
 render();workspace.scrollTop=saved?.scroll||0;
 for(const [id,position] of saved?.inner||[])if(whInnerScrollers.has(id))whInnerScrollers.get(id).area.scrollTop=position;
 whSuspended=null;
}
function whExit({renderAfter=true}={}){
 if(!whOpen)return;
 const exit=()=>{
  whOpen=false;whSuspended=null;document.body.classList.remove('watch-history-view');
  whDestroyInner();if(whPending.size){whRecords=whRecords.filter(r=>!whPending.has(r.id));whSave();}
  whPending.clear();whExpanded.clear();whFilter='all';whSort='newest';whSearch='';
  if(searchOpen)closeInlineSearch(false);
  if(renderAfter){state.view=whParentView;updateActiveTab(state.view);render();requestAnimationFrame(updateTabScrollOverlay);}
 };
 if(renderAfter)transitionGalleryStage(exit);else exit();
}
function whOpenTitle(r){
 if(!r.galleryId||!demo.some(x=>x.id===r.galleryId)){
  modal('Sample Watch History entry',`<p class="description">${escapeHTML(r.title)} is a layout-testing record; this HTML version has no matching anime detail page. The Watch History entry remains editable here.</p>`,`<button class="btn primary" id="wh-sample-okay">Got it</button>`);
  document.getElementById('wh-sample-okay')?.addEventListener('click',closeModal);return;
 }
 const targetView=r.library?'library':'discover';
 transitionGalleryStage(()=>{
  whSuspendForDetail();state.view=targetView;updateActiveTab(targetView);
  showDetail(r.galleryId,true);state.detailReturnScroll=tabPages[targetView].scrollTop;
  const x=demo.find(x=>x.id===r.galleryId);const index=getSeasons(x).findIndex(s=>s.id===r.installmentId);
  if(index>=0){state.detailSeason=index;state.detailRelated=null;render();}
 });
}
/* All page actions live in one delegated listener; episode toggles don't rebuild their list. */
screen.addEventListener('click',event=>{
 if(!whOpen)return;const b=event.target.closest('button');if(!b)return;
 if(b.hasAttribute('data-wh-exit')){whExit();return;}
 if(b.dataset.whFilter){whFilter=b.dataset.whFilter;whRender();return;}
 if(b.hasAttribute('data-wh-sort')){whSort=whSort==='newest'?'oldest':'newest';whRender();return;}
 if(b.dataset.whExpand){whToggleRow(b.dataset.whExpand);return;}
 if(b.dataset.whRemove){whPending.add(b.dataset.whRemove);whExpanded.delete(b.dataset.whRemove);whRender();return;}
 if(b.dataset.whUndo){whPending.delete(b.dataset.whUndo);whRender();return;}
 if(b.hasAttribute('data-wh-undo-all')){whPending.clear();whRender();return;}
 if(b.dataset.whOpen){const record=whRecords.find(r=>r.id===b.dataset.whOpen);if(record)whOpenTitle(record);return;}
 if(b.dataset.whEpisode){const divider=b.dataset.whEpisode.lastIndexOf(':'),id=b.dataset.whEpisode.slice(0,divider),n=Number(b.dataset.whEpisode.slice(divider+1));const r=whRecords.find(r=>r.id===id),ep=r?.episodes.find(ep=>ep.n===n);if(!ep)return;ep.manualStatus=whEpisodeNextStatus(ep);whUpdateEpisodeInPlace(b,r,ep);whSave();return;}
});
/* Playback tracking is limited to a user-opened local video in the HTML preview.
 * An episode becomes Watched only by continuous active playback crossing into
 * its final 20 seconds, never because the user seeks directly into that range. */
let whPlayerSession=null;
function whInitPlayerSession(){whPlayerSession={lastTime:0,hasPlayedOutsideFinal:false,lastSavedAt:0};}
function whRecordLocalPlayback(video,markWatched=false){
 if(!state.playback||!state.detailId||!Number.isFinite(video.duration)||video.duration<=0)return;
 const anime=demo.find(x=>x.id===state.detailId),installment=anime&&activeInstallment(anime);if(!anime||!installment)return;
 const id='local:'+anime.id+':'+String(installment.id||installment.label||'s1');let rec=whRecords.find(r=>r.galleryId===anime.id&&r.installmentId===(installment.id||null))||whRecords.find(r=>r.id===id);
 if(!rec){
  rec={id,group:anime.id,library:state.view==='library',galleryId:anime.id,installmentId:installment.id||null,title:installmentDisplayName(anime,installment),short:anime.name.split(' ').slice(0,2).join(' '),cover:anime.art,last:'',dates:[],latestEpisode:state.playback.episode,episodes:whMakeEpisodes(installment.total||1)};
  whRecords.unshift(rec);
 }
 const n=state.playback.episode;let ep=rec.episodes.find(e=>e.n===n);if(!ep){ep={n,watched:false,started:false,progressSeconds:0,duration:Math.floor(video.duration)};rec.episodes.push(ep);rec.episodes.sort((a,b)=>a.n-b.n);}
 delete ep.manualStatus;ep.started=true;ep.duration=Math.floor(video.duration);ep.progressSeconds=Math.floor(video.currentTime);if(markWatched)ep.watched=true;
 rec.latestEpisode=n;
 const now=new Date(),day=[now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');
 rec.last=day;if(!rec.dates.includes(day))rec.dates.push(day);
 whSave();
}
function whOnVideoTick(video){
 if(!whPlayerSession||video.paused||video.seeking||!Number.isFinite(video.duration)||video.duration<=0)return;
 const current=video.currentTime,threshold=Math.max(0,video.duration-20),past=whPlayerSession.lastTime;
 if(current<threshold)whPlayerSession.hasPlayedOutsideFinal=true;
 const completed=whPlayerSession.hasPlayedOutsideFinal&&past<threshold&&current>=threshold&&current-past<3;
 if(completed||current-whPlayerSession.lastSavedAt>=3||!whPlayerSession.lastSavedAt){whRecordLocalPlayback(video,completed);whPlayerSession.lastSavedAt=current;}
 whPlayerSession.lastTime=current;
}
function whOnVideoSeek(video){if(!whPlayerSession)return;whPlayerSession.lastTime=video.currentTime;whPlayerSession.hasPlayedOutsideFinal=false;}

/* Discover integration: Soft Futuristic visuals, v103 source/search/history behavior. */
function discover(){
 const model=getSourceCataloguePreview();
 const isSearching=searchOpen&&state.view==='discover'&&!document.body.classList.contains('settings-view');
 const matching=isSearching?searchItems(model.titles):model.titles.filter(x=>(state.filterStatus==='All'||x.status===state.filterStatus)&&(state.filterAudio==='All'||x.lang.includes(state.filterAudio)));
 const actions=model.titles.length?`<button class="btn ghost page-filter-button" id="filters">${icon('filter',18)} Filters${state.filterStatus!=='All'||state.filterAudio!=='All'?' · Active':''}</button>`:'';
 const title=isSearching&&state.query.trim()?'Search results':'Explore the universe';
 const cards=model.titles.length?(matching.length?gallery(matching):'<div class="search-empty">No matching titles in this sample catalogue.</div>'):sourceCatalogueEmptyMarkup(model);
 const note=model.catalogSources.length>1?`<p class="discover-source-note">Shared sample titles are combined into one catalogue entry, even when both sources list them.</p>`:model.cached?`<p class="discover-source-note">Previously known titles from an unavailable provider are kept visible in this simulation; availability has not been rechecked.</p>`:'';
 return `<div class="sf-discover-page">
 ${pageHeader('Discover','','','discover')}
 ${whPreviewMarkup()}
 <section class="gallery-section sf-discover-explore" id="sf-discover-explore" aria-label="Explore anime">
 <div class="section-row sf-discover-explore-heading"><div class="sf-explore-heading-text"><h2 class="discover-results-heading">${title}</h2><span class="sf-explore-star" aria-hidden="true">✦</span><span class="muted discover-result-count" aria-live="polite">${discoverSourceCount(model,matching)}</span></div>${actions}</div>
 <div class="discover-result-region">${cards}</div>${note}</section>
 </div>`;
}
// Keep unfinished JSON collection transfers for a future redesign.
const GALLERY_COLLECTION_TRANSFER_UI_ENABLED=false;
function library(){
 const isSearching=searchOpen&&state.view==='library'&&Boolean(state.query.trim());
 const visibleTag=isSearching?'All Titles':state.tag;
 // Search spans all library tags and per-installment tags; the selected tag is preserved.
 const titles=isSearching?searchItems(demo):visibleTag==='All Titles'?demo:demo.filter(x=>x.tags.includes(visibleTag));
 const isCustom=state.kind[visibleTag]==='custom';
 const isAll=visibleTag==='All Titles';
 const actions=`${GALLERY_COLLECTION_TRANSFER_UI_ENABLED?`<button class="btn" id="import">${icon('import',16)} <span>Import</span></button>`:''}<button class="btn primary" id="newtag">${icon('plus',17)} <span>New Tag</span></button>`;
 const tagChip=(tag)=>{const active=visibleTag===tag,custom=state.kind[tag]==='custom',count=countTag(tag);return `<button type="button" class="tagchip ${active?'active':''}" data-tag="${escapeHTML(tag)}" aria-pressed="${active}" aria-label="${escapeHTML(tag)}${custom?', custom tag':''}, ${count} titles" title="${custom?'Custom tag':'Built-in collection'}"><span>${escapeHTML(tag)}</span>${custom?`<span class="custom-tag-icon">${icon('bookmark',11)}</span>`:''}<span class="count">${count}</span></button>`;};
 const tags=`<div class="library-tag-row"><button type="button" class="library-tag-arrow library-tag-prev" id="library-tag-prev" aria-label="Scroll collections left">${icon('chevron',16)}</button><div class="tagbar" role="group" aria-label="Library collections">${tagChip('All Titles')}${state.tags.map(tagChip).join('')}</div><button type="button" class="library-tag-arrow library-tag-next" id="library-tag-next" aria-label="Scroll collections right">${icon('chevron',16)}</button></div>`;
 const shareAction=isAll||!GALLERY_COLLECTION_TRANSFER_UI_ENABLED?'':`<button class="btn small" id="sharetag" title="Share ${escapeHTML(state.tag)}">${icon('share',15)} <span>Share</span></button>`;
 const menu=isCustom?`<div class="collection-menu-wrap"><button class="btn small collection-options" id="tag-options" aria-label="More actions for ${escapeHTML(state.tag)}" aria-haspopup="menu" aria-expanded="false">${icon('dots',19)}</button><div class="collection-menu" id="tag-options-menu" role="menu" hidden><button type="button" role="menuitem" id="renametag">${icon('bookmark',15)} Rename tag</button><button type="button" role="menuitem" class="delete-tag-action" id="deletetag">${icon('close',15)} Delete tag</button></div></div>`:'';
 const kind=isAll?'All anime in your library':isCustom?'Custom tag':'Built-in collection';
 const label=visibleTag;
 const subtitle=isSearching?`${titles.length} ${titles.length===1?'match':'matches'} · Across all tags`: `${titles.length} ${titles.length===1?'title':'titles'} · ${kind}`;
 const cards=isSearching?`<div class="poster-grid">${titles.map(librarySearchCard).join('')}</div>`:gallery(titles);
 return `${pageHeader('My Library',actions,tags,'library')}
 <section class="library-collection" aria-label="${isSearching?'Library search results':'Selected library collection'}"><div class="collections-head"><div class="col-title-row"><div><h2>${escapeHTML(label)}</h2><div class="meta">${subtitle}</div></div></div>${isSearching?'':`<div class="collection-actions">${menu}${shareAction}</div>`}</div><div class="col-contents">${titles.length?cards:'<div class="search-empty">No matching titles in your library.</div>'}</div>${GALLERY_COLLECTION_TRANSFER_UI_ENABLED&&!isSearching&&!isAll?'<p class="tip">Shared collections include titles and identifiers only — not videos, watch history, or private settings.</p>':''}</section>`;
}
function librarySearchCard(item){
 const seasons=connectedMetadata[item.id]?.seasons||[];
 const labels=[...item.tags];
 for(const season of seasons){
  const tags=seasonTagList(item,season);
  // Show the release-specific statuses where multiple seasons differ.
  if(tags.length && (state.seasonTags[season.id]||seasons.some(s=>s.id!==season.id&&seasonTagList(item,s).join('|')!==tags.join('|')))){
   for(const tag of tags)labels.push(`${season.label}: ${tag}`);
  }
 }
 const unique=[...new Set(labels)];
 const pills=unique.length?unique.map(tag=>`<span>${escapeHTML(tag)}</span>`).join(''):'<span>Untagged</span>';
 return artCard(item).replace('</article>',`<div class="library-search-tags" aria-label="Tags for ${escapeHTML(item.name)}">${pills}</div></article>`);
}
// One fictional transfer is controllable to test the completion moment.
// The existing completed download starts with its percentage hidden.
const DOWNLOAD_ACTION_SVG={"cancel": '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon download-action-icon" aria-hidden="true" focusable="false"><path d="M18 6l-12 12" /><path d="M6 6l12 12" /></svg>', "dismiss": '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon download-action-icon" aria-hidden="true" focusable="false"><path d="M18 6l-12 12" /><path d="M6 6l12 12" /></svg>', "retry": '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon download-action-icon" aria-hidden="true" focusable="false"><path d="M19.933 13.041a8 8 0 1 1 -9.925 -8.788c3.899 -1 7.935 1.007 9.425 4.747" /><path d="M20 4v5h-5" /></svg>'};
function downloadActionIcon(action){return DOWNLOAD_ACTION_SVG[action]||'';}
const DEMO_COMPLETION_HOLD_MS=3000;
// Browser-only illustration of grouped downloads. No real transfers, files, or path reads.
function makeDemoDownloadEntries(){
 const items=[];
 for(let ep=1;ep<=10;ep++)items.push({id:`quints-${ep}`,animeId:'demo:quints',release:'Season 1',episode:ep,audio:'Sub',totalBytes:350+ep*13,status:ep<=8?'Completed':'Downloading',progress:ep<=8?100:ep===9?61:36});
 items.push(
  {id:'astra-01',animeId:'demo:02',release:'Season 1',episode:1,audio:'Sub',totalBytes:420,status:'Completed',progress:100},
  {id:'astra-02',animeId:'demo:02',release:'Season 1',episode:2,audio:'Sub',totalBytes:460,status:'Downloading',progress:55},
  {id:'astra-03',animeId:'demo:02',release:'Season 1',episode:3,audio:'Sub',totalBytes:440,status:'Queued',progress:0},
  {id:'astra-04',animeId:'demo:02',release:'Season 1',episode:4,audio:'Dub',totalBytes:480,status:'Failed',progress:24},
  {id:'astra-05',animeId:'demo:02',release:'Season 1',episode:5,audio:'Sub',totalBytes:410,status:'Canceled',progress:12},
  {id:'neon-01',animeId:'demo:06',release:'Season 1',episode:1,audio:'Dub',totalBytes:320,status:'Completed',progress:100},
  {id:'neon-02',animeId:'demo:06',release:'Season 1',episode:2,audio:'Dub',totalBytes:390,status:'Completed',progress:100}
 );
 return items;
}
const downloadDemo={entries:makeDemoDownloadEntries(),expanded:new Set(),dismissed:new Set(),fullAt:new Map(),timers:new Map()};
const downloadTerminalStates=new Set(['Completed','Failed','Canceled']);
function visibleDownloadEntries(){return downloadDemo.entries.filter(entry=>!downloadDemo.dismissed.has(entry.id));}
function animeDownloadEntries(id){return visibleDownloadEntries().filter(entry=>entry.animeId===id);}
function allAnimeDownloadEntries(id){return downloadDemo.entries.filter(entry=>entry.animeId===id);}
function downloadProgress(entries){
 const total=entries.reduce((sum,e)=>sum+e.totalBytes,0);
 return total?Math.round(entries.reduce((sum,e)=>sum+e.totalBytes*e.progress/100,0)/total*100):0;
}
function downloadStatusSummary(entries){
 return ['Completed','Downloading','Paused','Queued','Failed','Canceled'].map(status=>{
  const n=entries.filter(entry=>entry.status===status).length;
  return n?`${n} ${status.toLowerCase()}`:'';
 }).filter(Boolean).join(' · ');
}
function downloadGroupStatus(entries){
 if(entries.some(entry=>entry.status==='Downloading'))return ['Downloading','In progress'];
 if(entries.some(entry=>entry.status==='Paused'))return ['Paused','Paused'];
 if(entries.some(entry=>entry.status==='Failed'))return ['Failed','Needs attention'];
 if(entries.some(entry=>entry.status==='Queued'))return ['Queued','Queued'];
 if(entries.every(entry=>entry.status==='Completed'))return ['Completed','Complete'];
 return ['Completed','Finished'];
}
function sfDownloadControlIcon(kind){
 if(kind==='pause')return '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg>';
 return '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="m8 5 11 7-11 7z"/></svg>';
}
/* All Gallery split timelines share one rule: the moving 5px gap is ALWAYS
   present. At 0% it occupies the leading edge; at 100%, the trailing edge.
   The completed and remaining segments divide the rest of the track. */
function galleryTimelineFill(percent){
 const amount=Math.max(0,Math.min(100,Number(percent)||0));
 return `calc((100% - var(--gallery-timeline-gap)) * ${(amount/100).toFixed(6)})`;
}
function downloadProgressTrack(percent,label){
 const amount=Math.max(0,Math.min(100,Number(percent)||0));
 return `<span class="sf-dl-track gallery-split-timeline" role="progressbar" aria-label="${escapeHTML(label)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${amount}"><span class="sf-dl-track-done" style="flex-basis:${galleryTimelineFill(amount)}" aria-hidden="true"></span><span class="sf-dl-track-rest" aria-hidden="true"></span></span>`;
}
function downloadGroupCanDismiss(entries){return entries.length>0&&entries.every(entry=>downloadTerminalStates.has(entry.status));}
function setDownloadGroupExpanded(id,expanded){
 if(expanded)downloadDemo.expanded.add(id);else downloadDemo.expanded.delete(id);
 const group=Array.from(tabPages.downloads.querySelectorAll('[data-download-group]')).find(el=>el.dataset.downloadGroup===id);
 if(!group)return;
 group.classList.toggle('is-expanded',expanded);
 group.querySelector('.download-group-toggle')?.setAttribute('aria-expanded',String(expanded));
 const inner=group.querySelector('.download-group-body-inner');
 if(inner){inner.inert=!expanded;inner.setAttribute('aria-hidden',String(!expanded));}
}
const sfDownloadScrollPositions=new Map();
let sfDownloadUndo=null;
function captureDownloadScroll(){
 tabPages.downloads.querySelectorAll('.sf-dl-viewport[data-scroll-group]').forEach(el=>sfDownloadScrollPositions.set(el.dataset.scrollGroup,el.scrollTop));
}
function restoreDownloadScroll(){
 tabPages.downloads.querySelectorAll('.sf-dl-viewport[data-scroll-group]').forEach(el=>{
  if(sfDownloadScrollPositions.has(el.dataset.scrollGroup))el.scrollTop=sfDownloadScrollPositions.get(el.dataset.scrollGroup);
 });
}
function refreshDownloadDemo(focusAnime=null){
 captureDownloadScroll();
 renderTabPage('downloads');
 restoreDownloadScroll();
 renderDownloadUndoToast();
 if(focusAnime){
  const group=Array.from(tabPages.downloads.querySelectorAll('[data-download-group]')).find(el=>el.dataset.downloadGroup===focusAnime);
  (group?.querySelector('.download-group-toggle')||tabPages.downloads.querySelector('[data-download-filter="All"]'))?.focus({preventScroll:true});
 }
}
function dismissDownloadEpisode(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||!downloadTerminalStates.has(entry.status))return;
 sfDownloadUndo={id,animeId:entry.animeId,wasExpanded:downloadDemo.expanded.has(entry.animeId)};
 downloadDemo.dismissed.add(id);
 if(animeDownloadEntries(entry.animeId).length===0)downloadDemo.expanded.delete(entry.animeId);
 refreshDownloadDemo();
}
function renderDownloadUndoToast(){
 // The tab track is transformed; a fixed toast inside it would appear off-screen.
 // Mount it directly under body so it stays anchored to the actual viewport.
 document.getElementById('sf-dl-undo-global')?.remove();
 if(!sfDownloadUndo||state.view!=='downloads')return;
 const toast=document.createElement('div');
 toast.id='sf-dl-undo-global';toast.className='sf-dl-undo';toast.setAttribute('role','status');
 toast.innerHTML='<span>Episode dismissed from the list. File kept.</span><button type="button">Undo</button>';
 toast.querySelector('button').addEventListener('click',undoDismissDownload);
 document.body.appendChild(toast);
}
function undoDismissDownload(){
 if(!sfDownloadUndo)return;
 const {id,animeId,wasExpanded}=sfDownloadUndo;
 downloadDemo.dismissed.delete(id);
 if(wasExpanded)downloadDemo.expanded.add(animeId);
 sfDownloadUndo=null;
 refreshDownloadDemo(animeId);
}
function dismissDownloadGroup(id){
 const entries=animeDownloadEntries(id);
 if(!downloadGroupCanDismiss(entries))return;
 const anime=demo.find(item=>item.id===id);
 modal('Dismiss download notifications',`<p class="description">Remove <b>${escapeHTML(anime?.name||'this anime')}</b> and its ${entries.length} finished download ${entries.length===1?'entry':'entries'} from this page?</p><p class="tip">This only dismisses notifications. It does not delete, move or change any files.</p>`,
 `<button class="btn" id="dismiss-group-back">Keep notifications</button><button class="btn primary" id="dismiss-group-confirm">Dismiss ${entries.length} ${entries.length===1?'entry':'entries'}</button>`);
 document.getElementById('dismiss-group-back').onclick=closeModal;
 document.getElementById('dismiss-group-confirm').onclick=()=>{
  const latest=animeDownloadEntries(id);
  if(!downloadGroupCanDismiss(latest)){closeModal();return;}
  latest.forEach(entry=>downloadDemo.dismissed.add(entry.id));
  downloadDemo.expanded.delete(id);
  closeModal();refreshDownloadDemo();
 };
}
function cancelDownloadEpisode(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||!['Queued','Downloading','Paused'].includes(entry.status))return;
 modal('Cancel download',`<p class="description">Cancel <b>${escapeHTML(entry.release)} · Episode ${entry.episode}</b>?</p><p class="tip">Cancel stops the transfer. It is different from dismissing a finished notification. This preview does not download anything.</p>`,
 '<button class="btn" id="cancel-download-back">Keep downloading</button><button class="btn primary" id="cancel-download-confirm">Cancel transfer</button>');
 document.getElementById('cancel-download-back').onclick=closeModal;
 document.getElementById('cancel-download-confirm').onclick=()=>{entry.status='Canceled';closeModal();refreshDownloadDemo(entry.animeId);};
}
function toggleDownloadPause(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||!['Downloading','Paused'].includes(entry.status))return;
 entry.status=entry.status==='Downloading'?'Paused':'Downloading';
 captureDownloadScroll();renderTabPage('downloads');restoreDownloadScroll();
 const next=tabPages.downloads.querySelector(`[data-download-pause="${id}"]`);
 next?.focus({preventScroll:true});
}
function retryDownloadEpisode(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||entry.status!=='Failed')return;
 // Demo has no actual partial-file resume support: retry queues from zero.
 entry.status='Queued';entry.progress=0;
 refreshDownloadDemo(entry.animeId);
}
function dismissAllFinishedDownloads(){
 const entries=visibleDownloadEntries().filter(entry=>downloadTerminalStates.has(entry.status));
 if(!entries.length)return;
 modal('Dismiss all finished notifications',`<p class="description">Dismiss <b>${entries.length}</b> completed, failed or canceled download ${entries.length===1?'notification':'notifications'}?</p><p class="tip">Active and queued downloads will remain visible. This clears notifications only; no downloads will be stopped and no files will be changed.</p>`,
 '<button type="button" class="btn" id="dismiss-all-back">Keep notifications</button><button type="button" class="btn primary" id="dismiss-all-confirm">Dismiss finished</button>');
 document.getElementById('dismiss-all-back').onclick=closeModal;
 document.getElementById('dismiss-all-confirm').onclick=()=>{
  sfDownloadUndo=null;
  for(const entry of visibleDownloadEntries())if(downloadTerminalStates.has(entry.status))downloadDemo.dismissed.add(entry.id);
  for(const id of [...downloadDemo.expanded])if(animeDownloadEntries(id).length===0)downloadDemo.expanded.delete(id);
  closeModal();refreshDownloadDemo();
 };
}
function simulateNextDownload(){
 const target=visibleDownloadEntries().find(e=>e.status==='Downloading')||visibleDownloadEntries().find(e=>e.status==='Queued');
 if(!target)return;
 const before=downloadProgress(allAnimeDownloadEntries(target.animeId));
 if(target.status==='Downloading'){
  target.status='Completed';target.progress=100;
 }else{
  target.status='Downloading';target.progress=12;
 }
 const after=downloadProgress(allAnimeDownloadEntries(target.animeId));
 if(before<100&&after===100){
  downloadDemo.fullAt.set(target.animeId,Date.now());
  clearTimeout(downloadDemo.timers.get(target.animeId));
  const timer=setTimeout(()=>{
   const group=Array.from(tabPages.downloads.querySelectorAll('[data-download-group]')).find(el=>el.dataset.downloadGroup===target.animeId);
   group?.querySelector('.download-group-percent')?.classList.add('is-hidden');
  },DEMO_COMPLETION_HOLD_MS);
  downloadDemo.timers.set(target.animeId,timer);
 }
 refreshDownloadDemo();
}
function resetDownloadDemo(){
 for(const timer of downloadDemo.timers.values())clearTimeout(timer);
 downloadDemo.entries=makeDemoDownloadEntries();
 downloadDemo.expanded.clear();downloadDemo.dismissed.clear();downloadDemo.fullAt.clear();downloadDemo.timers.clear();
 state.downloadStatus='All';sfDownloadUndo=null;sfDownloadScrollPositions.clear();refreshDownloadDemo();
}
function downloads(){
 const isSearching=searchOpen&&state.view==='downloads'&&Boolean(state.query.trim());
 const query=isSearching?state.query.trim().toLowerCase():'';
 const all=visibleDownloadEntries();
 const statuses=['All','Downloading','Completed'];
 const filters=`<div class="download-filters" role="group" aria-label="Download status">${statuses.map(status=>`<button class="filterpill ${status===(isSearching?'All':state.downloadStatus)?'active':''}" data-download-filter="${status}" aria-pressed="${status===(isSearching?'All':state.downloadStatus)}">${status} <span class="count">${status==='All'?all.length:all.filter(entry=>entry.status===status).length}</span></button>`).join('')}</div>`;
 const dismissibleCount=all.filter(entry=>downloadTerminalStates.has(entry.status)).length;
 const dismissAllTitle=dismissibleCount?'Dismiss all completed, failed and canceled download notifications; keep files':'No finished notifications to dismiss';
 const actions=`<span class="download-dismiss-all-wrap" title="${dismissAllTitle}"><button type="button" class="download-action-btn download-action-dismiss" id="dismiss-all-downloads" aria-label="${dismissAllTitle}" ${dismissibleCount?'':'disabled'}>${downloadActionIcon('dismiss')}</button></span><button class="btn" id="openfolder">${icon('folder',16)} <span>Open Folder</span></button>`;
 const animeIds=[...new Set(all.map(entry=>entry.animeId))];
 const groups=animeIds.map(id=>{
  const anime=demo.find(item=>item.id===id);
  if(!anime)return '';
  const entries=animeDownloadEntries(id);
  const allEntries=allAnimeDownloadEntries(id);
  const titleMatches=Boolean(query&&anime.name.toLowerCase().includes(query));
  const matched=entries.filter(entry=>{
   if(isSearching)return !query||titleMatches||[entry.release,`episode ${entry.episode}`,String(entry.episode),entry.audio,entry.status].some(value=>value.toLowerCase().includes(query));
   return state.downloadStatus==='All'||entry.status===state.downloadStatus;
  });
  if(!matched.length)return '';
  const progress=downloadProgress(allEntries);
  const expanded=downloadDemo.expanded.has(id);
  const groupStatus=downloadGroupStatus(allEntries);
  const dismissible=downloadGroupCanDismiss(entries);
  const bodyId=`download-group-body-${id.replace(/[^a-z0-9]/gi,'-')}`;
  const episodes=matched.map(entry=>{
   const terminal=downloadTerminalStates.has(entry.status);
   const active=entry.status==='Downloading',paused=entry.status==='Paused',failed=entry.status==='Failed';
   const playPause=active||paused?`<button class="sf-dl-control-button" type="button" data-download-pause="${entry.id}" aria-label="${active?'Pause':'Resume'} ${escapeHTML(anime.name)} · ${escapeHTML(entry.release)} · Episode ${entry.episode}">${sfDownloadControlIcon(active?'pause':'play')}<span>${active?'Pause':'Resume'}</span></button>`:'';
   const retry=failed?`<button class="sf-dl-control-button" type="button" data-download-retry="${entry.id}" aria-label="Retry ${escapeHTML(anime.name)} · Episode ${entry.episode}">${downloadActionIcon('retry')}<span>Retry</span></button>`:'';
   const action=terminal?'dismiss':'cancel';
   const label=terminal?`Dismiss ${anime.name} · Episode ${entry.episode} from Downloads list (keep downloaded file)`:`Cancel ${anime.name} · Episode ${entry.episode} transfer (requires confirmation)`;
   const quick=`<button class="sf-dl-quick-btn" type="button" ${terminal?`data-download-dismiss="${entry.id}"`:`data-download-cancel="${entry.id}"`} aria-label="${escapeHTML(label)}" title="${terminal?'Dismiss list entry; keep file':'Cancel transfer; confirm first'}">${downloadActionIcon('dismiss')}</button>`;
   return `<div class="download-episode sf-dl-episode" data-download-episode="${entry.id}">
     <div class="sf-dl-episode-name">Episode ${String(entry.episode).padStart(2,'0')}<span class="sf-dl-release">${escapeHTML(entry.release)} · ${escapeHTML(entry.audio)}</span></div>
     <div class="sf-dl-episode-status" data-status="${entry.status}"><span class="sf-dl-dot" aria-hidden="true"></span>${escapeHTML(entry.status)}</div>
     <div class="sf-dl-episode-track">${downloadProgressTrack(entry.progress,`${anime.name} · Episode ${entry.episode} progress`)}</div>
     <div class="sf-dl-episode-control">${playPause}${retry||(!playPause?'<span class="sf-dl-control-spacer" aria-hidden="true"></span>':'')}</div>
     <span class="sf-dl-episode-percent">${entry.progress}%</span>
     <div class="sf-dl-episode-quick">${quick}</div>
    </div>`;
  }).join('');
  return `<section class="download-group sf-dl-card ${expanded?'is-expanded':''}" data-download-group="${escapeHTML(id)}" data-download-state="${groupStatus[0]}" aria-label="${escapeHTML(anime.name)} downloads">
    <div class="download-group-top sf-dl-card-top"><button type="button" class="download-group-toggle sf-dl-summary" data-download-toggle="${escapeHTML(id)}" aria-expanded="${expanded}" aria-controls="${bodyId}">
      <span class="sf-dl-cover" style="background:${anime.art}" aria-hidden="true"><span class="sf-dl-cover-ring"></span><span class="sf-dl-cover-label">${escapeHTML(anime.name.split(' ').map(part=>part[0]).slice(0,2).join('').toUpperCase())}</span></span>
      <span class="sf-dl-main"><span class="sf-dl-title">${escapeHTML(anime.name)}</span><span class="sf-dl-summary-line">${escapeHTML(downloadStatusSummary(allEntries))}</span>
        <span class="sf-dl-series-progress">${downloadProgressTrack(progress,`${anime.name} · overall download progress (weighted by file size)`)}<span class="sf-dl-series-percent">${progress}%</span></span>
      </span>
      <span class="sf-dl-right"><span class="sf-dl-status-badge" data-status="${groupStatus[0]}"><span class="sf-dl-dot" aria-hidden="true"></span>${groupStatus[1]}</span><span class="download-group-chevron sf-dl-chevron" aria-hidden="true">${icon('chevron',18)}</span></span>
    </button></div>
    <div class="download-group-body sf-dl-body" id="${bodyId}"><div class="download-group-body-inner sf-dl-body-inner" ${expanded?'':'inert aria-hidden="true"'}>
      ${matched.length===allEntries.length?'':`<p class="download-matched-count">Showing ${matched.length} of ${allEntries.length} notifications</p>`}
      <div class="sf-dl-viewport gallery-episode-scroll" data-scroll-group="${escapeHTML(id)}" role="region" tabindex="0" aria-label="Episodes of ${escapeHTML(anime.name)}">${episodes}</div>
      <p class="sf-dl-action-hint" aria-hidden="true">${downloadActionIcon('dismiss')} Hover over an episode to reveal Dismiss or Cancel. Tab to the action to use it with a keyboard.</p>
    </div></div></section>`;
 }).filter(Boolean).join('');
 const pending=all.some(entry=>entry.status==='Downloading'||entry.status==='Queued');
 return `${pageHeader('Downloads',actions,filters,'downloads')}
  <div class="sf-dl-list-heading">${isSearching?'Search results':'Grouped by series'}<span>${isSearching?'Matching download notifications':'Select a series to view its episodes'}</span></div>
  <section class="downloads-list download-groups sf-dl-list" aria-label="Grouped download notifications">${groups||(isSearching?'<div class="search-empty">No matching download notifications.</div>':'<div class="empty">No download notifications match this filter.</div>')}
   <div class="demo-download-footer"><p class="tip">Demonstration only · Download statuses and file sizes are fictional. Retry requeues failed episodes; dismiss only clears notifications, never files. Pause and Resume control simulated transfers. No files are downloaded or searched.</p><div class="demo-download-actions"><button type="button" class="demo-download-control" id="demo-next-download" ${pending?'':'disabled'}>Simulate next step</button><button type="button" class="demo-download-control" id="demo-reset-downloads">Reset demo</button></div></div>
  </section>`;
}

const seasonStories={
 'demo:01':['A signal after midnight','The distant reply','Orbits and echoes','A quiet visitor','Paper constellations','A light from home','The hidden station','Messages at dawn','Across the signal','A map of stars','The last transmission','First light'],
 'demo:02':['The new constellation','Under the observatory','Through the telescope','Northern horizon','A fragment of light','The second star','Before sunrise']
};
/* Connected records simulate a cached, verified relationship graph.
   Titles and release grouping use genuine naming conventions, but provider episode
   coverage, source matches, tags and progress below are design-only sample data.
   In the real app, IDs are cross-referenced and user corrections are explicit. */
const connectedMetadata={
 'demo:quints':{
   seasons:[
     {id:'quints-s1',label:'Season 1',title:'The Quintessential Quintuplets',seasonNumber:1,total:12,year:'2019',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:4,downloaded:1},
     {id:'quints-s2',label:'Season 2',title:'The Quintessential Quintuplets ∬',seasonNumber:2,total:12,year:'2021',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:0,downloaded:0}
   ],
   related:[
     {id:'quints-movie',title:'The Quintessential Quintuplets Movie',kind:'Movie',year:'2022',note:'The 2022 feature film, shown separately from the numbered TV seasons.',sourceMatched:true,total:1,sub:1,dub:1,status:'Completed',watched:0,downloaded:0},
     {id:'quints-sp-2023',title:'The Quintessential Quintuplets ∽',kind:'Special',year:'2023',note:'2023 special: two episodes, kept separate from the seasons and 2024 special.',sourceMatched:true,total:2,sub:2,dub:2,status:'Completed',watched:0,downloaded:0},
     {id:'quints-sp-2024',title:'The Quintessential Quintuplets ＊',kind:'Special',year:'2024',note:'2024 special: two episodes, kept separate from the 2023 special.',sourceMatched:true,total:2,sub:2,dub:2,status:'Completed',watched:0,downloaded:0}
   ]
 },
 'demo:solo':{
   seasons:[
     {id:'solo-s1',label:'Season 1',title:'Solo Leveling',seasonNumber:1,total:12,year:'2024',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:4,downloaded:1},
     {id:'solo-s2',label:'Season 2',title:'Arise from the Shadow',seasonNumber:2,total:13,year:'2025',status:'Completed',sub:13,dub:9,sourceMatched:true,watched:0,downloaded:0}
   ],related:[]
 },
 'demo:long':{
   seasons:Array.from({length:18},(_,i)=>({id:`long-s${i+1}`,label:`Season ${i+1}`,title:i===0?'The Endless Voyage':i%3===0?`The Endless Voyage: Arc ${i+1}`:`Voyage Arc ${i+1} — ${['Dawn','Eclipse','North Star','Beyond the Horizon'][i%4]}`,seasonNumber:i+1,total:12,year:String(2007+i),status:'Completed',sub:12,dub:i%5===0?0:12,sourceMatched:i!==11,watched:0,downloaded:0})),
   related:[...Array.from({length:5},(_,i)=>({id:`long-m${i+1}`,title:`The Endless Voyage — Feature Film ${i+1}`,kind:'Movie',year:String(2012+i*2),sourceMatched:false,total:1,sub:null,dub:null,status:'Completed',watched:0,downloaded:0})),...Array.from({length:11},(_,i)=>({id:`long-o${i+1}`,title:`Side Story ${i+1}: ${['The First Night','Reunion','Hidden Paths'][i%3]}`,kind:i%2?'OVA':'Special',year:String(2010+i),sourceMatched:false,total:1,sub:null,dub:null,status:'Completed',watched:0,downloaded:0}))]
 },
 'demo:aot':{
   seasons:[
     {id:'aot-s1',label:'Season 1',title:'Attack on Titan',seasonNumber:1,total:25,year:'2013',status:'Completed',sub:25,dub:25,sourceMatched:true,watched:10,downloaded:3},
     {id:'aot-s2',label:'Season 2',title:'Attack on Titan',seasonNumber:2,total:12,year:'2017',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:2,downloaded:0},
{id:'aot-s3',label:'Season 3',title:'Attack on Titan',seasonNumber:3,total:22,year:'2018–2019',status:'Completed',sub:null,dub:null,sourceMatched:false,watched:0,downloaded:0},
     {id:'aot-s4a',label:'Season 4 · Part 1',title:'The Final Season · Part 1',seasonNumber:4,total:16,year:'2020–2021',status:'Completed',sub:16,dub:12,sourceMatched:true,watched:0,downloaded:0},
     {id:'aot-s4b',label:'Season 4 · Part 2',title:'The Final Season · Part 2',seasonNumber:4,total:12,year:'2022',status:'Completed',sub:12,dub:null,sourceMatched:true,watched:0,downloaded:0},
   ],related:[
     {id:'aot-finalchapters',title:'The Final Chapters',kind:'Special',year:'2023',note:'Finale specials · linked, not assigned a new season number',sourceMatched:false,total:2,sub:null,dub:null,watched:0,downloaded:0,status:'Completed'},
     {id:'aot-lastattack',title:'THE LAST ATTACK',kind:'Movie',year:'2024',note:'Film version of the finale · not Season 5',sourceMatched:false,total:1,sub:null,dub:null,watched:0,downloaded:0,status:'Completed'},
     {id:'aot-oad',title:'OAD Archive',kind:'OVA',year:'Various',note:'Original animation releases · separate from numbered seasons',sourceMatched:false,total:8,sub:null,dub:null,watched:0,downloaded:0,status:'Completed'}
   ]
 }
};
function connectedFor(x){return connectedMetadata[x.id]||null;}
function getRelated(x){return connectedFor(x)?.related||[];}
function activeInstallment(x){const related=getRelated(x);return state.detailRelated?related.find(r=>r.id===state.detailRelated):getSeasons(x)[state.detailSeason];}
function seasonTagList(x,season){if(!season?.id)return x.tags;return state.seasonTags[season.id]??(season.id==='solo-s1'?['Watching']:season.id==='solo-s2'?['Plan to Watch']:[]);}
function installmentDisplayName(x,s){return s.title||x.name;}
function installmentSubLabel(s){return s.kind?`${s.kind} · ${s.year}`:s.label;}
function getSeasons(x){
 if(connectedFor(x))return connectedFor(x).seasons;
 if(x.id==='demo:01')return [
  {id:'moon-s1',title:'Moonlit Signals',label:'Season 1',total:12,status:'Completed',sub:12,dub:8,year:'2025',sourceMatched:true,watched:5,downloaded:2},
  {id:'moon-s2',title:'Moonlit Signals',label:'Season 2',total:10,status:'Ongoing',sub:6,dub:2,year:'2026',sourceMatched:true,watched:0,downloaded:0}
 ];
 if(x.id==='demo:04')return [{label:'Season 1',total:13,status:'Completed',sub:13,dub:null,year:'2024'}];
 const supportsSub=x.lang.includes('Sub'),supportsDub=x.lang.includes('Dub');
 const available=x.status==='Ongoing'?Math.max(1,Math.ceil(x.episodes*.63)):x.episodes;
 const dubCount=supportsDub?(x.status==='Ongoing'?Math.max(0,available-2):x.episodes):0;
 return [{label:'Season 1',total:x.episodes,status:x.status,sub:supportsSub?available:0,dub:dubCount,year:x.status==='Ongoing'?'2026':'2025'}];
}
function availabilityText(count,total){return count===null?'Unknown':`${count} / ${total}`;}
function episodeAvailability(season,n){return {sub:season.sub!==null?n<=season.sub:null,dub:season.dub!==null?n<=season.dub:null};}
function audioName(lang){return lang==='dub'?'English (Dub)':'Japanese (Sub)';}
function installmentReleaseYear(item){
 // Use only the year recorded for the installment; undated/"Various" records
 // go after dated releases rather than inventing a release date.
 const match=String(item.year||'').match(/^\d{4}/);
 return match?Number(match[0]):Number.POSITIVE_INFINITY;
}
function installmentRail(x){
 const seasons=getSeasons(x),related=getRelated(x);
 if(seasons.length+related.length<=1)return '';
 // One continuous, chronological strip. Preserve each item's original
 // identity, so a movie or special never becomes a synthetic TV season.
 const releases=[
   ...seasons.map((item,index)=>({...item,_index:index,_kind:'season',_sourceOrder:index})),
   ...related.map((item,index)=>({...item,_kind:'related',_sourceOrder:seasons.length+index}))
 ].sort((a,b)=>installmentReleaseYear(a)-installmentReleaseYear(b)||a._sourceOrder-b._sourceOrder);
 const totals={};
 for(const item of releases)if(item._kind==='related')totals[item.kind]=(totals[item.kind]||0)+1;
 const counters={};
 const cards=releases.map(item=>{
   const current=item._kind==='season'?!state.detailRelated&&item._index===state.detailSeason:state.detailRelated===item.id;
   const title=installmentDisplayName(x,item);
   let label;
   if(item._kind==='season')label=`${item.label}${item.year?' · '+item.year:''}`;
   else {
     const type=item.kind||'Special';
     counters[type]=(counters[type]||0)+1;
     label=`${type}${totals[type]>1?' '+counters[type]:''}${item.year&&item.year!=='Various'?' · '+item.year:''}`;
   }
   return `<button type="button" class="inline-installment-card" data-inline-installment="${escapeHTML(item.id||'')}" data-inline-index="${item._index??''}" data-inline-kind="${item._kind}" aria-current="${current}" aria-label="${escapeHTML(title)}, ${escapeHTML(label)}${current?', selected':''}"><span class="installment-copy"><span class="installment-name">${escapeHTML(title)}</span><span class="installment-number">${escapeHTML(label)}</span></span></button>`;
 }).join('');
 return `<nav class="inline-installments" aria-label="Releases in chronological order"><div class="inline-release-viewport"><div class="inline-installment-rail" id="inline-installment-rail" aria-label="Releases in chronological order" tabindex="0">${cards}</div><div class="inline-release-fade inline-release-fade-left" aria-hidden="false"><button type="button" class="inline-arrow previous" data-inline-scroll="-1" aria-label="Scroll releases one card left" title="Previous release" disabled>${icon('chevron',17)}</button></div><div class="inline-release-fade inline-release-fade-right" aria-hidden="false"><button type="button" class="inline-arrow" data-inline-scroll="1" aria-label="Scroll releases one card right" title="Next release" disabled>${icon('chevron',17)}</button></div></div></nav>`;
}
let activeInstallmentRailObserver=null;
function refreshInstallmentArrows(){
 const rail=screen.querySelector('#inline-installment-rail');
 const viewport=rail?.closest('.inline-release-viewport');
 if(!rail||!viewport)return;
 const maxScroll=Math.max(0,rail.scrollWidth-rail.clientWidth);
 const left=maxScroll>3&&rail.scrollLeft>2;
 const right=maxScroll>3&&rail.scrollLeft<maxScroll-2;
 // A scrolling arrow can vanish under a stationary cursor on the final card.
 // Keep an INVISIBLE full-height hit shield until the pointer leaves the edge.
 const guardLeft=!left&&viewport.dataset.pointerLeft==='true';
 const guardRight=!right&&viewport.dataset.pointerRight==='true';
viewport.classList.toggle('guard-left',guardLeft);
 viewport.classList.toggle('guard-right',guardRight);
 viewport.classList.toggle('can-left',left);
 viewport.classList.toggle('can-right',right);
 const previous=viewport.querySelector('[data-inline-scroll="-1"]');
 const next=viewport.querySelector('[data-inline-scroll="1"]');
 if(previous)previous.disabled=!(left||guardLeft);
 if(next)next.disabled=!(right||guardRight);
}
function setupInstallmentEdgeGuards(viewport){
 if(!viewport)return;
 for(const side of ['left','right']){
   const fade=viewport.querySelector('.inline-release-fade-'+side);
   if(!fade)continue;
   const prop=side==='left'?'pointerLeft':'pointerRight';
   fade.addEventListener('pointerenter',event=>{
     if(event.pointerType==='touch')return;
     viewport.dataset[prop]='true';
     refreshInstallmentArrows();
   });
   fade.addEventListener('pointerleave',()=>{
     viewport.dataset[prop]='false';
     refreshInstallmentArrows();
   });
 }
}
/* Update only release-dependent sections; the rail itself never gets
   destroyed, so its scroll position, pointer target and buttons survive. */
function selectInlineInstallment(card,rail){
 if(card.getAttribute('aria-current')==='true')return;
 const savedScroll=workspace.scrollTop;
 if(card.dataset.inlineKind==='season'){
   state.detailSeason=Number(card.dataset.inlineIndex);
   state.detailRelated=null;
 }else state.detailRelated=card.dataset.inlineInstallment;
 state.detailEpisode=1;
 // Keep All/Playable-only while moving among releases of the same anime.
 // Opening a different anime still starts at All (see showDetail).
 const template=document.createElement('div');
 template.innerHTML=detailPage();
 const newDetail=template.querySelector('.anime-detail');
 if(!newDetail)return;
 // The release rail remains the actual, mounted DOM element.
 for(const selector of ['.detail-overview','.detail-control-panel']){
   const oldPart=screen.querySelector(selector);
   const newPart=newDetail.querySelector(selector);
   if(oldPart&&newPart)oldPart.replaceWith(newPart);
 }
 const section=screen.querySelector('.detail-section');
 const newSection=newDetail.querySelector('.detail-section');
 if(section&&newSection){
   const releaseNav=section.querySelector('.inline-installments');
   section.replaceChildren(releaseNav,...Array.from(newSection.children).filter(node=>!node.classList.contains('inline-installments')));
 }
 for(const release of rail.querySelectorAll('.inline-installment-card')){
   const selected=release===card;
   release.setAttribute('aria-current',String(selected));
   const name=release.getAttribute('aria-label').replace(/, selected$/,'');
   release.setAttribute('aria-label',name+(selected?', selected':''));
 }
 // Controls inside the replaced sections require their own event handlers.
 document.getElementById('manage-detail-tags')?.addEventListener('click',showManageDetailTags);
 document.getElementById('find-source')?.addEventListener('click',showFindSource);
 for(const el of screen.querySelectorAll('[data-detail-audio]'))el.addEventListener('click',()=>{
   if((state.detailAudio||state.defaultPlayback)!==el.dataset.detailAudio)changeDetailAudio(el.dataset.detailAudio);
 });
 bindEpisodeFiltersAndActions();
 for(const el of screen.querySelectorAll('.detail-actions [data-episode-action]'))el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
 workspace.scrollTop=savedScroll;
 requestAnimationFrame(updateTabScrollOverlay);
}

// v27 — Update playback availability in place when changing Sub/Dub.
// A full screen render would destroy the old selected button and its ::before
// before CSS could animate it from opacity 1 to opacity 0.

/* v38 — Keep the count mounted when filtering so the count and its
   divider can fade rather than snapping in with a newly created toolbar. */
function syncEpisodeToolbar(updated){
 const current=screen.querySelector('.episode-toolbar');
 if(!current||!updated)return;
 const oldValues=current.querySelectorAll('.availability-value');
 const newValues=updated.querySelectorAll('.availability-value');
 for(let i=0;i<Math.min(oldValues.length,newValues.length);i++)
   oldValues[i].textContent=newValues[i].textContent;
 const oldCount=current.querySelector('.episode-shown');
 const newCount=updated.querySelector('.episode-shown');
 if(oldCount&&newCount){
   const hidden=newCount.classList.contains('is-hidden');
   if(!hidden)oldCount.textContent=newCount.textContent;
   oldCount.classList.toggle('is-hidden',hidden);
   if(hidden){oldCount.setAttribute('aria-hidden','true');oldCount.removeAttribute('role');}
   else{oldCount.removeAttribute('aria-hidden');oldCount.setAttribute('role','status');}
 }
 // Replace only the filter control (not its surrounding box) so fresh
 // click handlers can be attached without duplicating listeners.
 const oldFilter=current.querySelector('.episode-filter');
 const newFilter=updated.querySelector('.episode-filter');
 if(oldFilter&&newFilter)oldFilter.replaceWith(newFilter);
}
function changeEpisodeFilter(next){
 if(state.detailEpisodeFilter===next)return;
 const y=workspace.scrollTop;
 state.detailEpisodeFilter=next;
 const holder=document.createElement('div');
 holder.innerHTML=detailPage();
 syncEpisodeToolbar(holder.querySelector('.episode-toolbar'));
 const currentList=screen.querySelector('.episode-list');
 const updatedList=holder.querySelector('.episode-list');
 if(currentList&&updatedList)currentList.replaceWith(updatedList);
 bindEpisodeFiltersAndActions();
 workspace.scrollTop=y;
 requestAnimationFrame(updateTabScrollOverlay);
}
function bindEpisodeFiltersAndActions(){
 for(const el of screen.querySelectorAll('[data-episode-filter]')){
   el.addEventListener('click',()=>changeEpisodeFilter(el.dataset.episodeFilter));
 }
 for(const el of screen.querySelectorAll('.episode-list [data-episode-action]')){
   el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
 }
}

function changeDetailAudio(next){
 const toggle=screen.querySelector('.detail-audio-toggle');
 if(!toggle || (state.detailAudio||state.defaultPlayback)===next)return;
 const scroll=workspace.scrollTop;
 state.detailAudio=next;
 // Build the new markup offscreen so other episode controls update immediately,
 // while the original toggle retains its DOM identity and animation state.
 const container=document.createElement('div');
 container.innerHTML=detailPage();
 const updatedToggle=container.querySelector('.detail-audio-toggle');
 for(const lang of ['sub','dub']){
   const current=toggle.querySelector(`[data-detail-audio="${lang}"]`);
   const updated=updatedToggle?.querySelector(`[data-detail-audio="${lang}"]`);
   if(!current||!updated)continue;
   for(const attr of ['aria-label','title'])current.setAttribute(attr,updated.getAttribute(attr));
   current.setAttribute('aria-pressed',String(lang===next));
 }
 toggle.dataset.active=next;
 // The selected button owns its gradient; no shared indicator follows the pointer.
 // These pieces depend on playback language. Replacing them, rather than the
 // whole detail page, also keeps the user's scroll position and hover animation.
 syncEpisodeToolbar(container.querySelector('.episode-toolbar'));
 for(const selector of ['.detail-actions','.episode-list']){
   const current=screen.querySelector(selector);
   const updated=container.querySelector(selector);
   if(current && updated)current.replaceWith(updated);
 }
 document.getElementById('manage-detail-tags')?.addEventListener('click',showManageDetailTags);
 for(const el of screen.querySelectorAll('.detail-actions [data-episode-action]'))
   el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
 bindEpisodeFiltersAndActions();
 workspace.scrollTop=scroll;
 toggle.querySelector(`[data-detail-audio="${next}"]`)?.focus({preventScroll:true});
 requestAnimationFrame(updateTabScrollOverlay);
}

// Informational language availability: labels are not actions.
// Null means unchecked, never "unavailable"; omit that marker until a provider confirms a result.
function episodeAudioIndicator(kind,available){
 if(available===null)return '';
 const isSub=kind==='sub';
 const word=isSub?'Sub':'Dub';
 const typeSvg=isSub
  ? '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M7.5 10h4m-4 4h3m3-4h3m-3 4h3"/>'
  : '<path d="M4 11a8 8 0 0 1 16 0v7a2 2 0 0 1-2 2h-1v-7h3M4 13h3v7H6a2 2 0 0 1-2-2v-7"/>';
 const stateSvg=available
  ? '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>'
  : '<circle cx="12" cy="12" r="9"/><path d="M8 12h8"/>';
 const name=isSub?'Japanese audio / subtitles':'English dub';
 const status=available?'available':'unavailable';
 const svg=path=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${path}</svg>`;
 return `<span class="audio-flag ${available?'available':'unavailable'}" role="img" aria-label="${name} ${status}" title="${name}: ${status}">${svg(typeSvg)}<span>${word}</span><span class="audio-state-icon">${svg(stateSvg)}</span></span>`;
}

function detailPage(){
 const x=demo.find(d=>d.id===state.detailId);if(!x)return '';
 const seasons=getSeasons(x);const si=Math.max(0,Math.min(state.detailSeason,seasons.length-1));
 const s=activeInstallment(x)||seasons[si];const related=Boolean(state.detailRelated);
 const sourceMatched=s.sourceMatched!==false;
 const targetEpisode=Math.max(1,Math.min((Number.isFinite(s.watched)?s.watched:0)+1,s.total)); // Top Watch resumes the next unwatched episode; individual row actions use their own episode.
 const targetAvail=sourceMatched?episodeAvailability(s,targetEpisode):{sub:null,dub:null};
 const audio=state.detailAudio||state.defaultPlayback;
 const canWatch=sourceMatched&&targetAvail[audio]===true;
 const audioOption=(lang,label)=>{
   const available=targetAvail[lang];const status=sourceMatched?(available===true?'available':available===false?'unavailable':'unverified'):'source not matched';
   const info=`${lang==='sub'?'Japanese':'English'} audio · ${status} for ${s.kind||s.label}, episode ${targetEpisode}${state.defaultPlayback===lang?' · your default':''}`;
   return `<button type="button" data-detail-audio="${lang}" aria-pressed="${audio===lang}" aria-label="${escapeHTML(info)}" title="${escapeHTML(info)}">${label}</button>`;
 };
 const audioControl=`<div class="detail-audio-control"><div class="detail-audio-toggle" data-active="${audio}" role="group" aria-label="Audio version for playback">${audioOption('sub','Sub')}${audioOption('dub','Dub')}</div></div>`;
 const playableCount=sourceMatched?Array.from({length:s.total},(_,i)=>episodeAvailability(s,i+1)[audio]===true).filter(Boolean).length:0;
 const playableOnly=state.detailEpisodeFilter==='playable';
 const episodeFilter=sourceMatched?`<div class="episode-filter" role="group" aria-label="Filter episodes by playback availability"><button type="button" data-episode-filter="all" aria-pressed="${!playableOnly}">All</button><button type="button" data-episode-filter="playable" aria-pressed="${playableOnly}" title="Show episodes playable in ${audio==='sub'?'Sub':'Dub'}">Playable only</button></div>`:'';
 const visibleEpisodeNumbers=sourceMatched?Array.from({length:s.total},(_,i)=>i+1).filter(n=>!playableOnly||episodeAvailability(s,n)[audio]===true):[];
 const entries=sourceMatched?(visibleEpisodeNumbers.length?visibleEpisodeNumbers.map(n=>{
 const i=n-1,avail=episodeAvailability(s,n),active=avail.sub===true||avail.dub===true;
 const selectedAudioAvailable=avail[audio]===true;
 const name=(s.id==='moon-s1'?seasonStories[x.id]?.[i]:null)||`Episode ${n}`;
 const stateText=selectedAudioAvailable?'Ready in '+(audio==='sub'?'Sub':'Dub'):
   active?'Not in '+(audio==='sub'?'Sub':'Dub')+' · other audio available':
   (avail.sub===null||avail.dub===null)?'Checking audio availability':'Not available yet';
 return `<div class="episode-item ${!selectedAudioAvailable?'episode-not-playable':''}" role="listitem"><span class="episode-no">${String(n).padStart(2,'0')}</span><div class="episode-copy"><div class="episode-name">${escapeHTML(name)}</div><div class="episode-subtext">${escapeHTML(stateText)}</div></div><div class="episode-tools"><div class="episode-flags" aria-label="Audio availability">${episodeAudioIndicator('sub',avail.sub)}${episodeAudioIndicator('dub',avail.dub)}</div><div class="episode-actions"><button class="iconbtn" type="button" data-episode-action="watch" data-episode="${n}" ${!selectedAudioAvailable?'disabled':''} aria-label="Watch ${escapeHTML(x.name)} ${escapeHTML(s.label||s.kind)} episode ${n}" title="${selectedAudioAvailable?`Watch episode ${n} · ${audioName(audio)}`:`${audioName(audio)} unavailable or unverified for episode ${n}`} ">${icon('play',18)}</button><button class="iconbtn" type="button" data-episode-action="download" data-episode="${n}" ${!active?'disabled':''} aria-label="Download ${escapeHTML(x.name)} ${escapeHTML(s.label||s.kind)} episode ${n}" title="Download episode ${n}">${icon('download',17)}</button></div></div></div>`;
 }).join('<div class="episode-divider" aria-hidden="true"></div>'):'<div class="episode-empty-filter">No episodes are currently confirmed playable in this audio version. Choose <strong>All</strong> to see every episode, or switch the audio option above.</div>'):'<div class="provider-unmatched">'+icon('info',19)+'<div><strong>No streaming source matched</strong><p>This installment is linked through the example relationship graph, but no provider entry is confirmed. The app must not invent episodes or assume a Sub/Dub version is available.</p></div><button class="btn" type="button" id="find-source">Find source</button></div>';
 const seasonInfo=related?`${escapeHTML(s.kind)} · Related release`:`${escapeHTML(s.label)}`;
 const showInstallmentTitle=connectedFor(x)||seasons.length>1;
 const tagList=seasonTagList(x,s);
 const shownCount=visibleEpisodeNumbers.length;
 const reduced=sourceMatched&&playableOnly&&shownCount<s.total;
 const breakdown=sourceMatched?`<div class="availability episode-availability" aria-label="Episode audio availability and filtering"><div class="episode-stats"><span class="availability-label">${icon('headphones',16)} Sub <strong class="availability-value">${availabilityText(s.sub,s.total)}</strong></span><span class="availability-label">Dub <strong class="availability-value">${availabilityText(s.dub,s.total)}</strong></span><span class="episode-shown${reduced?'':' is-hidden'}" ${reduced?'role="status"':'aria-hidden="true"'}>${shownCount} of ${s.total} shown</span></div>${episodeFilter}</div>`:'';
 return `<div class="anime-detail" aria-label="Anime detail: ${escapeHTML(x.name)}">
 <header class="detail-page-header">
  <h1 class="detail-title sf-optical-title">${escapeHTML(x.name)}</h1>
  <button type="button" id="detail-back" class="detail-back">${icon('back',18)} Back to ${state.detailReturnHistory?'Watch History':state.detailReturnView==='library'?'Library':state.detailReturnView==='downloads'?'Downloads':'Discover'}</button>
 </header>
 <section class="detail-hero">
 <div class="detail-cover" style="background:${x.art}"><span class="detail-cover-name">${escapeHTML(x.name)}</span></div>
 <div class="detail-overview"><div class="detail-badges"><span class="detail-badge">${seasons.length} ${seasons.length===1?'season':'seasons'}</span><span class="detail-badge">${escapeHTML(s.year)}</span><span class="detail-badge">${s.kind==='Movie'?'Status':'Airing'}: <strong>${escapeHTML(s.status)}</strong>${related?` · ${escapeHTML(s.kind)}`:''}</span></div>
 <p class="detail-description">${escapeHTML(related?(s.note||x.blurb):x.blurb)}</p>
 <div class="detail-browsing"><span class="detail-browsing-caption">Currently browsing</span><strong>${escapeHTML(installmentSubLabel(s))} <span class="detail-browsing-sep">·</span> ${s.total} ${s.total===1?'episode':'episodes'}</strong>${Number.isInteger(s.watched)?`<span class="detail-browsing-progress">${s.watched} of ${s.total} watched <small>(demo)</small></span>`:''}</div></div>
 <aside class="detail-control-panel" aria-label="Playback and library actions">${audioControl}
 <div class="detail-actions"><button class="btn primary" type="button" aria-label="${s.kind==='Movie'?'Watch movie':`Watch episode ${targetEpisode}`}" data-episode-action="watch" data-episode="${targetEpisode}" ${!canWatch?`disabled title="${sourceMatched?'Audio unavailable or unverified':'No matched provider'}"`:''}>${icon('play',17)} <span class="detail-action-label-long">${s.kind==='Movie'?'Watch movie':`Watch episode ${targetEpisode}`}</span><span class="detail-action-label-short">Watch</span></button><button class="btn" type="button" id="manage-detail-tags" aria-label="${tagList.length?'Manage tags':'Add to Library'}">${icon('bookmark',17)} <span class="detail-action-label-long">${tagList.length?'Manage tags':'Add to Library'}</span><span class="detail-action-label-short">${tagList.length?'Tags':'Add'}</span></button></div></aside>
 </section>
 <section class="detail-section" aria-label="Episodes and availability">${installmentRail(x)}
 <div class="episode-toolbar"><div class="episode-heading"><h2>${s.kind==='Movie'?'Movie':s.kind==='Special'?'Special episodes':'Episodes'}</h2></div>${breakdown}</div>
 <div class="episode-list" role="list">${entries}</div>
 <p class="episode-note">${related?'Related releases remain separate from numbered seasons. ':'Each season has its own identity, tag assignments, and watch/download history. '}Provider availability and progress are fictional for this UI demonstration; unknown coverage is never treated as confirmed.</p>
 </section></div>`;
}
function backFromDetail(){
 transitionGalleryStage(()=>{
  state.playback=null;
  if(state.detailReturnHistory){state.detailReturnHistory=false;whResumeFromDetail();return;}
  state.detailId=null;state.view=state.detailReturnView;
  render();tabPages[state.view].scrollTop=state.detailReturnScroll;
 });
}
function startPlayback(n){
 const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const installment=activeInstallment(x);if(!installment||installment.sourceMatched===false)return;
 const audio=state.detailAudio||state.defaultPlayback;
 const availability=episodeAvailability(installment,n);
 if(availability[audio]!==true)return; // Never fall back to the other version silently.
 transitionGalleryPlayer(()=>{
  state.playbackReturnScroll=workspace.scrollTop;
  state.detailEpisode=n;
  state.playback={episode:n,audio,installmentId:installment.id,subtitles:state.defaultSubtitles};
  closeModal();render();workspace.scrollTop=0;
 });
}
function playbackPage(){
 const x=demo.find(d=>d.id===state.detailId),p=state.playback,s=x&&activeInstallment(x);
 if(!x||!s||!p)return '';
 const label=s.kind==='Movie'?'Movie':`Episode ${p.episode}`;
 const prev=playbackNeighbor(-1),next=playbackNeighbor(1);
 const autoplayNext=playerCanAdvance();
 const centerPrimary=s.kind==='Movie'?installmentDisplayName(x,s):`Episode ${p.episode}`;
 const centerSecondary=s.kind?(s.kind==='Movie'?'Movie':s.kind):s.label;
 const buttonText=(action,side)=>`<span class="nav-label-full">${escapeHTML(action.label)}</span><span class="nav-label-compact">${side==='previous'?'Previous':'Next'}</span>`;
 return `<section class="playback-page" aria-label="Gallery video player">
  <div class="playback-compactbar">
   <div class="playback-title-inline"><strong class="sf-optical-title">${escapeHTML(x.name)}</strong></div>
   <button type="button" class="detail-back" id="back-from-playback">${icon('back',18)} Back to episodes</button>
  </div>
  <div class="player-area" id="player-area" tabindex="0" aria-label="Video and controls">
   <input type="file" id="sf-player-browser-file" accept="video/*" hidden aria-label="Choose a local video to play">
   <video id="local-video" playsinline preload="metadata" aria-label="Local video playback"></video>
   <div class="sf-player-demo-scene" id="sf-player-demo-scene" hidden aria-hidden="true"><div class="sf-player-demo-horizon"></div><div class="sf-player-demo-mark">Gallery<small>Simulated playback · no media loaded</small></div></div>
   <div class="player-no-media" id="player-empty"><div class="player-empty-inner">${icon('film',35)}<strong>No streaming source connected yet</strong><p>The anime entries in this development build are examples. Open a local video file to test our actual player controls.</p><button type="button" class="btn primary" id="open-local-video">${icon('folder',16)} Open local video…</button><button type="button" class="btn sf-player-preview-button" id="sf-player-demo-start">Preview player controls</button></div></div>
   <div class="player-overlay" id="player-overlay">
    <div class="player-bottom"><div class="player-progress-row"><span class="player-time" id="current-time">00:00</span><div class="player-progress" id="timeline"><div class="player-progress-bar gallery-split-timeline"><div class="player-watched" id="watched"></div><div class="player-remaining" id="seek-remaining"></div></div><input type="range" id="seek" min="0" max="1000" value="0" aria-label="Seek within episode" disabled></div><span class="player-time" id="duration-time">00:00</span></div>
    <div class="player-controls"><div class="controls-left"><button type="button" class="player-icon" id="mute" aria-label="Mute" aria-pressed="false" title="Mute"><svg class="player-volume-icon" data-level="4" viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path class="volume-speaker" d="M4 9h4l5 -4v14l-5 -4H4z"/><path class="volume-wave volume-wave-1" d="M15.5 10.5a2.25 2.25 0 0 1 0 3"/><path class="volume-wave volume-wave-2" d="M17 8a5.2 5.2 0 0 1 0 8"/><path class="volume-wave volume-wave-3" d="M18.5 5.5a8.3 8.3 0 0 1 0 13"/><path class="volume-muted-x" d="M17.3 9.5l4.6 5m0 -5l-4.6 5"/></svg></button><input type="range" class="player-volume" id="volume" min="0" max="100" value="${playerSessionVolume}" aria-label="Volume"></div><div class="controls-middle"><button type="button" class="player-icon player-track-control" id="rewind10" aria-label="Rewind 10 seconds" title="Rewind 10 seconds">${icon('rewind10',29)}</button><button type="button" class="player-main-action" id="pause-play" aria-label="Play" title="Play" disabled><svg id="player-play-morph-svg" class="player-play-morph" width="25" height="25" viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true" focusable="false"><g id="player-play-morph-group"><path id="player-play-morph-first" d=""/><path id="player-play-morph-second" d=""/></g></svg></button><button type="button" class="player-icon player-track-control" id="forward10" aria-label="Forward 10 seconds" title="Forward 10 seconds"><svg id="player-morph-icon" class="icon" width="29" height="29" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline id="player-morph-first" points="3,5 3,19 11,12 3,5"></polyline><polyline id="player-morph-second" points="14,5 14,19 22,12 14,5"></polyline></svg></button></div><div class="controls-right"><div class="player-upnext" id="player-upnext" aria-hidden="true"><button type="button" class="player-upnext-cancel" id="player-upnext-cancel" aria-label="Cancel Play Next" title="Cancel Play Next" disabled>${icon('close',17)}</button><div class="player-upnext-text"><strong id="player-upnext-title">Next episode</strong><span id="player-upnext-countdown">Next in 00:20</span></div><span class="player-upnext-divider" aria-hidden="true"></span></div><button type="button" class="player-icon" id="player-settings" aria-label="Player settings">${icon('settings',21)}</button><button type="button" class="player-icon" id="fullscreen" aria-label="Toggle fullscreen">${icon('maximize',21)}</button></div></div></div>
   </div>
  </div>
  <div class="player-episode-nav" aria-label="Episode navigation">
    <div class="player-episode-slot is-previous">${prev?`<button type="button" class="btn small player-episode-previous" id="previous-episode" aria-label="${escapeHTML(prev.label)}">${icon('back',15)}${buttonText(prev,'previous')}</button>`:''}</div>
    <div class="player-episode-label"><strong>${escapeHTML(centerPrimary)}</strong><small>${escapeHTML(centerSecondary||'')}</small></div>
    <div class="player-episode-slot is-next">${next?`<button type="button" class="btn small player-episode-next" id="next-episode" aria-label="${escapeHTML(next.label)}">${buttonText(next,'next')}${icon('chevron',15)}</button>`:''}</div>
  </div>
  <details class="player-dev-tools" data-development-only="true"><summary>Development tools · Local playback / VLC</summary>
   <div class="sf-player-demo-tools"><label class="sf-player-accent-preview"><input type="checkbox" id="sf-player-play-accent" checked> Secondary Play/Pause accent</label><label class="sf-player-accent-preview" for="sf-player-volume-test">Volume thresholds <select id="sf-player-volume-test" aria-label="Preview volume threshold"><option value="">Use slider</option><option value="0">0%</option><option value="1">1%</option><option value="25">25%</option><option value="26">26%</option><option value="50">50%</option><option value="51">51%</option><option value="75">75%</option><option value="76">76%</option><option value="100">100%</option></select></label><button class="btn small" type="button" id="sf-player-demo-toggle">Start simulation</button><button class="btn small" type="button" id="sf-player-demo-jump" disabled>Jump to last 25 s</button><button class="btn small" type="button" id="sf-player-demo-resume" disabled>Resume / Start Over demo</button><label class="sf-player-demo-autoplay" style="display:inline-flex;gap:5px;align-items:center;font-size:11px"><input type="checkbox" id="sf-player-demo-autoplay" checked> Demo autoplay next</label></div>
   <div class="player-file-actions"><button class="btn small" id="preview-play-next" type="button" aria-pressed="false" ${!autoplayNext?'disabled title="Play Next only applies within the current season"':''}>Preview Play Next transition</button><button class="btn small" id="change-local-video">${icon('folder',15)} Open local video…</button><button class="btn small" id="open-external-vlc" disabled>Open in VLC</button><span class="muted" id="local-file-label" style="align-self:center;font-size:12px">No local file selected</span></div>
   <div class="player-notice" id="player-notice">Local-file playback is functional where Electron supports the file's codec. Actual provider streams, bundled MPV rendering, and subtitle imports are not connected yet. Next-episode media is not yet connected, so the Play Next UI is visual/testable but cannot automatically load a following episode.</div>
  </details>
 </section>`;
}
function backFromPlayback(){
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 document.getElementById("local-video")?.pause();resetPlayNextState();isLocalVideoReady=false;
 transitionGalleryPlayer(()=>{
  state.playback=null;render();workspace.scrollTop=state.playbackReturnScroll;
 });
}
function showEpisodeAction(action,n){
 if(action==='watch'){startPlayback(n);return;}
 if(action!=='download')return;
 const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const season=activeInstallment(x);if(!season||season.sourceMatched===false)return;
 const a=episodeAvailability(season,n);
 const choices=[['sub','Japanese · Sub',a.sub],['dub','English · Dub',a.dub]];
 const available=choices.filter(choice=>choice[2]===true);if(!available.length)return;
 const defaultVersion=state.defaultDownload;
 const preferredAvailable=available.some(choice=>choice[0]===defaultVersion);
 const selected=preferredAvailable?defaultVersion:null;
 modal(`Download episode ${n}`,`<p class="description"><b>${escapeHTML(x.name)}</b> · ${escapeHTML(installmentDisplayName(x,season))} · ${escapeHTML(installmentSubLabel(season))} · Episode ${n}</p><div class="field"><span class="label">Audio version for download</span><div class="audio-choose">${choices.map(([id,name,availability])=>`<label><input type="radio" name="episode-audio" value="${id}" ${selected===id?'checked':''} ${availability!==true?'disabled':''}><span>${escapeHTML(name)}${availability===null?' · Unknown':availability===false?' · Unavailable':''}</span></label>`).join('')}</div></div>
 ${preferredAvailable?'':`<div class="preview-warning">The preferred download version (${defaultVersion==='sub'?'Sub':'Dub'}) is unavailable for this episode. Choose another available version explicitly to continue; the app will not switch automatically.</div>`}<div class="preview-warning">Available selectable subtitle tracks will be preserved independently of subtitle visibility. No silent audio-language substitution.</div><p class="tip">Choosing another download version here does not change your saved playback or download preferences.</p>`,`<button class="btn" id="episode-cancel">Cancel</button><button class="btn primary" id="episode-confirm" ${!selected?'disabled':''}>${icon('download',16)} Preview download</button>`);
 document.getElementById('episode-cancel').onclick=closeModal;
 for(const input of modalHost.querySelectorAll('input[name="episode-audio"]'))input.addEventListener('change',()=>{document.getElementById('episode-confirm').disabled=false;});
 document.getElementById('episode-confirm').onclick=()=>{
  const chosen=modalHost.querySelector('input[name="episode-audio"]:checked')?.value;
  if(!chosen||a[chosen]!==true)return;
  modal('Download preview',`<p class="description">${escapeHTML(x.name)} · ${escapeHTML(installmentDisplayName(x,season))} · ${escapeHTML(installmentSubLabel(season))} · Episode ${n}</p><div class="dialog-sample"><b>${chosen==='sub'?'Japanese (Sub)':'English (Dub)'}</b><p class="description">In the finished application, this would queue the selected download version and save accessible selectable subtitles for offline use.</p></div><p class="tip">This is a UI prototype; no downloading occurs.</p>`,`<button class="btn primary" id="episode-ok">Got it</button>`);
  document.getElementById('episode-ok').onclick=closeModal;
 };
}
function showManageDetailTags(){const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const season=activeInstallment(x);if(!season)return;const current=seasonTagList(x,season);
 modal(`Library tags · ${installmentDisplayName(x,season)}`,`<p class="description">Tags are saved for this specific installment (${escapeHTML(installmentSubLabel(season))}), independently of other seasons and their progress. This is temporary demo state only.</p><div class="tag-picker-list">${state.tags.map(tag=>`<label><input type="checkbox" data-detail-tag="${escapeHTML(tag)}" ${current.includes(tag)?'checked':''}><span>${escapeHTML(tag)}</span></label>`).join('')}</div>`,`<button class="btn" id="detail-tags-cancel">Cancel</button><button class="btn primary" id="detail-tags-save">Save tags</button>`);
 document.getElementById('detail-tags-cancel').onclick=closeModal;
 document.getElementById('detail-tags-save').onclick=()=>{const updated=Array.from(modalHost.querySelectorAll('input[data-detail-tag]:checked')).map(el=>el.dataset.detailTag);if(season.id)state.seasonTags[season.id]=updated;else x.tags=updated;closeModal();render();};
}
function showFindSource(){const x=demo.find(d=>d.id===state.detailId),s=x&&activeInstallment(x);if(!s)return;
 modal('Find a streaming source',`<p class="description"><b>${escapeHTML(installmentDisplayName(x,s))}</b> · ${escapeHTML(installmentSubLabel(s))}</p><div class="dialog-sample"><b>Not matched</b><p class="description">The finished application would search installed providers for this exact installment and ask you to confirm ambiguous matches. Nothing is silently linked here.</p></div><p class="tip">A relationship record does not prove that an episode can be streamed or downloaded.</p>`,`<button class="btn primary" id="source-ok">Got it</button>`);
 document.getElementById('source-ok').onclick=closeModal;
}

/* Electron bridge is narrowly scoped; standalone preview still renders. */
let localVideoName='',isLocalVideoReady=false,lastExternalPlayerStatus='not checked';
let savingPreference=false;
async function saveDesktopPreferences(){
 if(!window.galleryDesktop)return;
 try {await window.galleryDesktop.saveSettings({theme:state.theme,font:state.font,defaultPlayback:state.defaultPlayback,defaultDownload:state.defaultDownload,defaultSubtitles:state.defaultSubtitles,playerPreference:state.playerPreference||'built-in'});}catch(err){console.warn('Settings save failed:',err)}
}
async function setupDesktopSettings(){
 if(!window.galleryDesktop)return;
 document.body.classList.add('desktop-build');
 try{
  const prefs=await window.galleryDesktop.getSettings();
  if(SOFT_FUTURISTIC_THEMES.includes(prefs.theme))state.theme=prefs.theme;
  if(supportedGalleryFonts.includes(prefs.font)){state.font=prefs.font;document.body.dataset.font=state.font;try{localStorage.setItem('gallery.font',state.font)}catch{}}
  if(['sub','dub'].includes(prefs.defaultPlayback))state.defaultPlayback=prefs.defaultPlayback;
  if(['sub','dub'].includes(prefs.defaultDownload))state.defaultDownload=prefs.defaultDownload;
  if(typeof prefs.defaultSubtitles==='boolean')state.defaultSubtitles=prefs.defaultSubtitles;
  state.playerPreference=prefs.playerPreference||'built-in';
  document.body.dataset.theme=state.theme;
  render();
 }catch(err){console.warn('Could not load local settings:',err)}
}
/* v99 — The player menu selects subtitle tracks; audio language is chosen before playback.
   Remember the last track when Off is selected so the user can restore it easily. */
const playerSubtitleState={enabled:true,lastIndex:null,lastLanguage:'en'};
function playerSubtitleTracks(video){
 return Array.from(video?.textTracks||[]).map((track,index)=>({track,index})).filter(({track})=>track.kind==='subtitles'||track.kind==='captions');
}
function preferredPlayerSubtitleTrack(entries){
 return entries.find(({index})=>index===playerSubtitleState.lastIndex)
  ||entries.find(({track})=>track.language?.toLowerCase()===playerSubtitleState.lastLanguage)
  ||entries.find(({track})=>track.language?.toLowerCase().startsWith('en'))
  ||entries[0]||null;
}
function applyPlayerSubtitleState(video){
 const entries=playerSubtitleTracks(video),selected=preferredPlayerSubtitleTrack(entries);
 Array.from(video?.textTracks||[]).forEach(track=>{
  if(track.kind==='subtitles'||track.kind==='captions')track.mode=playerSubtitleState.enabled&&selected?.track===track?'showing':'disabled';
 });
 if(playerSubtitleState.enabled&&selected){
  playerSubtitleState.lastIndex=selected.index;
  if(selected.track.language)playerSubtitleState.lastLanguage=selected.track.language.toLowerCase();
 }
}
function openPlayerSettings(video){
 const entries=playerSubtitleTracks(video);
 const selected=preferredPlayerSubtitleTrack(entries);
 const selectedValue=playerSubtitleState.enabled&&selected?`track-${selected.index}`:'off';
 const choices=entries.map(({track,index})=>{
  const lang=track.language||'';
  const languageNames={en:'English',da:'Danish',ja:'Japanese',de:'German',fr:'French',es:'Spanish',pt:'Portuguese',it:'Italian',ko:'Korean',zh:'Chinese'};
  const displayName=track.label||languageNames[lang.toLowerCase().split('-')[0]]||lang||`Subtitle track ${index+1}`;
  return `<option value="track-${index}" ${selectedValue===`track-${index}`?'selected':''}>${escapeHTML(displayName)}</option>`;
 }).join('');
 const trackInfo=entries.length
  ?'<p class="tip">Choose a subtitle track or turn subtitles Off. Changing subtitles does not change the audio language.</p>'
  :'<p class="tip">No selectable subtitle tracks are available in this video. External subtitle imports are not connected in this HTML build.</p>';
 modal('Player settings',`<div class="field"><label for="video-rate">Playback speed</label><select id="video-rate">${[0.5,0.75,1,1.25,1.5,2].map(r=>`<option value="${r}" ${video.playbackRate===r?'selected':''}>${r}×</option>`).join('')}</select></div><div class="field"><label for="player-subtitle-track">Subtitles</label><select id="player-subtitle-track"><option value="off" ${selectedValue==='off'?'selected':''}>Off</option>${choices}</select>${trackInfo}</div>`,`<button class="btn primary" id="save-player-settings">Apply</button>`);
 document.getElementById('save-player-settings').onclick=()=>{
  video.playbackRate=Number(document.getElementById('video-rate').value);
  const value=document.getElementById('player-subtitle-track').value;
  if(value==='off')playerSubtitleState.enabled=false;
  else{
   const index=Number(value.slice('track-'.length));
   const item=entries.find(entry=>entry.index===index);
   if(item){
    playerSubtitleState.enabled=true;
    playerSubtitleState.lastIndex=index;
    if(item.track.language)playerSubtitleState.lastLanguage=item.track.language.toLowerCase();
   }
  }
  if(state.playback)state.playback.subtitles=playerSubtitleState.enabled;
  applyPlayerSubtitleState(video);
  closeModal();
 };
}
function fmtTime(sec){if(!Number.isFinite(sec)||sec<0)return '00:00';const x=Math.floor(sec);return `${String(Math.floor(x/3600)).padStart(x>=3600?1:2,'0')}:${String(Math.floor(x%3600/60)).padStart(2,'0')}:${String(x%60).padStart(2,'0')}`.replace(/^00:/,'');}


/* The approved Player Morph Refinement 02, now linked to real HTML5 and simulated
   playback states. No dependency or external assets; button markup is persistent. */
const SF_PLAY_MORPH_DURATION=260;
const SF_PLAY_FROM=[[[5.7,4],[13.4,8.1],[13.4,15.9],[5.7,20]],[[13.4,8.1],[20.4,11.35],[20.4,12.65],[13.4,15.9]]];
const SF_PLAY_TO=[[[5.6,4],[10.5,4],[10.5,20],[5.6,20]],[[13.5,4],[18.4,4],[18.4,20],[13.5,20]]];
let sfPlayMorph={amount:0,target:0,frame:0};
function sfPlayMorphPath(quad,radius){
 const corners=[];
 for(let i=0;i<4;i++){
  const prev=quad[(i+3)%4],now=quad[i],next=quad[(i+1)%4];
  const back=Math.hypot(prev[0]-now[0],prev[1]-now[1])||1;
  const ahead=Math.hypot(next[0]-now[0],next[1]-now[1])||1;
  const before=[now[0]+(prev[0]-now[0])*radius/back,now[1]+(prev[1]-now[1])*radius/back];
  const after=[now[0]+(next[0]-now[0])*radius/ahead,now[1]+(next[1]-now[1])*radius/ahead];
  corners.push({before,after,now});
 }
 const fmt=x=>Number(x).toFixed(3);
 let d=`M${fmt(corners[0].before[0])} ${fmt(corners[0].before[1])}`;
 for(let i=0;i<4;i++){
  const c=corners[i],n=corners[(i+1)%4];
  d+=` Q${fmt(c.now[0])} ${fmt(c.now[1])} ${fmt(c.after[0])} ${fmt(c.after[1])}`;
  d+=` L${fmt(n.before[0])} ${fmt(n.before[1])}`;
 }
 return d+' Z';
}
function sfDrawPlayMorph(){
 const first=document.getElementById('player-play-morph-first');
 const second=document.getElementById('player-play-morph-second');
 if(!first||!second)return;
 const t=Math.min(1,Math.max(0,sfPlayMorph.amount));
 for(let i=0;i<2;i++){
  const quad=SF_PLAY_FROM[i].map((point,j)=>point.map((value,k)=>value+(SF_PLAY_TO[i][j][k]-value)*t));
  // Both halves of the play triangle formerly touched at an antialiased seam.
  // Overlap their shared inner edge while in Play, fading that overlap away
  // as the halves morph into independent Pause bars. Outer contours stay put.
  const sharedOverlap=.85*(1-t);
  if(i===0){quad[1][0]+=sharedOverlap;quad[2][0]+=sharedOverlap;}
  else{quad[0][0]-=sharedOverlap;quad[3][0]-=sharedOverlap;}
  (i===0?first:second).setAttribute('d',sfPlayMorphPath(quad,.4+(.75*t)));
 }
 // The play triangle's mass sits left of its bounding box. Nudge it optically
 // toward the center; the pause bars stay precisely centered at t=1.
 const group=document.getElementById('player-play-morph-group');
 if(group)group.setAttribute('transform',`translate(${(1.05*(1-t)).toFixed(3)} 0)`);
}
function sfSetPlayMorph(playing,{instant=false}={}){
 const to=playing?1:0;
 const button=document.getElementById('pause-play');
 if(button){button.setAttribute('aria-label',playing?'Pause':'Play');button.title=playing?'Pause':'Play';}
 if(!instant && sfPlayMorph.target===to)return;
 cancelAnimationFrame(sfPlayMorph.frame);sfPlayMorph.frame=0;
 sfPlayMorph.target=to;
 const from=sfPlayMorph.amount;
 if(instant||window.matchMedia('(prefers-reduced-motion: reduce)').matches||Math.abs(from-to)<.001){
  sfPlayMorph.amount=to;sfDrawPlayMorph();return;
 }
 const duration=SF_PLAY_MORPH_DURATION*Math.abs(to-from);
 const start=performance.now();
 function tick(now){
  const p=Math.min(1,Math.max(0,(now-start)/duration));
  const eased=p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
  sfPlayMorph.amount=from+(to-from)*eased;
  sfDrawPlayMorph();
  if(p<1)sfPlayMorph.frame=requestAnimationFrame(tick);else sfPlayMorph.frame=0;
 }
 sfPlayMorph.frame=requestAnimationFrame(tick);
}
function sfResetPlayMorph(){
 cancelAnimationFrame(sfPlayMorph.frame);
 sfPlayMorph={amount:0,target:0,frame:0};
 sfDrawPlayMorph();
}

/* v98 — The user-approved, interruptible SVG morph: Tabler Player Track Next
   becomes Player Skip Forward, with an independent, reversible Up Next fade.
   This player currently handles local test media; provider episode URLs are not
   connected, so we never pretend an actual next-episode stream can start. */
const PLAYER_MORPH_MS=280;
const PLAYER_MORPH_FIRST_FROM=[[3,5],[3,19],[11,12],[3,5]];
const PLAYER_MORPH_FIRST_TO=[[4,5],[4,19],[16,12],[4,5]];
const PLAYER_MORPH_SECOND_FROM=[[14,5],[14,19],[22,12],[14,5]];
const PLAYER_MORPH_SECOND_TO=[[20,5],[20,19],[20,19],[20,5]];
let playNextMorph={amount:0,frame:0};
let playNextShown=false,playNextCanceled=false,playNextPreview=false;

/* Previous/Next may change episode, season or explicitly linked movie/special.
   Available audio must be verified for the destination. `watchNextId` and
   `watchPreviousId` are optional, provider-confirmed watch-order link IDs;
   never infer a movie's narrative position from release dates alone. */
function playbackNeighbor(step,{sameInstallmentOnly=false}={}){
 if(step!==1&&step!==-1)return null;
 const p=state.playback,x=demo.find(item=>item.id===state.detailId);
 const current=x&&activeInstallment(x);
 if(!p||!current)return null;
 const episode=p.episode+step;
 if(episode>=1&&episode<=current.total){
  if(episodeAvailability(current,episode)[p.audio]!==true)return null;
  return {episode,installment:current,seasonIndex:state.detailSeason,
   relatedId:state.detailRelated||null,kind:'episode',label:step>0?'Next episode':'Previous episode'};
 }
 if(sameInstallmentOnly)return null;
 const seasons=getSeasons(x),related=getRelated(x),all=[...seasons,...related];
 let target=null;
 const explicitId=step>0?current.watchNextId:current.watchPreviousId;
 if(explicitId){
  target=all.find(entry=>entry.id===explicitId)||null;
 }else{
  const reverseKey=step>0?'watchPreviousId':'watchNextId';
  const reverse=all.filter(entry=>entry.id!==current.id&&entry[reverseKey]===current.id);
  if(reverse.length===1)target=reverse[0];
  else if(reverse.length>1)return null; // Conflicting watch-order links.
  else if(!state.detailRelated){
   const index=state.detailSeason+step;
   target=seasons[index]||null;
  }
 }
 if(!target||target.sourceMatched===false)return null;
 const targetEpisode=step>0?1:target.total;
 if(!Number.isInteger(targetEpisode)||targetEpisode<1||episodeAvailability(target,targetEpisode)[p.audio]!==true)return null;
 const seasonIndex=seasons.findIndex(item=>item===target||(item.id&&item.id===target.id));
 const relatedId=seasonIndex<0?target.id:null;
 if(seasonIndex<0&&!relatedId)return null;
 const kind=seasonIndex>=0?'season':target.kind==='Movie'?'movie':
  target.kind==='OVA'?'OVA':(target.kind||'special').toLowerCase();
 const label=`${step>0?'Next':'Previous'} ${kind}`;
 return {episode:targetEpisode,installment:target,seasonIndex:seasonIndex>=0?seasonIndex:state.detailSeason,
  relatedId,kind,label};
}
function playerCanAdvance(){
 return Boolean(playbackNeighbor(1,{sameInstallmentOnly:true}));
}
function setPlayerMorphGeometry(amount){
 const first=document.getElementById('player-morph-first'),second=document.getElementById('player-morph-second');
 if(!first||!second)return;
 function points(a,b){return a.map((point,i)=>point.map((val,j)=>(val+(b[i][j]-val)*amount).toFixed(3)).join(',')).join(' ');}
 first.setAttribute('points',points(PLAYER_MORPH_FIRST_FROM,PLAYER_MORPH_FIRST_TO));
 second.setAttribute('points',points(PLAYER_MORPH_SECOND_FROM,PLAYER_MORPH_SECOND_TO));
}
function morphPlayerTo(target){
 cancelAnimationFrame(playNextMorph.frame);playNextMorph.frame=0;
 const button=document.getElementById('forward10');
 if(button){button.setAttribute('aria-label',target?'Next episode':'Forward 10 seconds');button.title=target?'Next episode':'Forward 10 seconds';}
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
  playNextMorph.amount=target?1:0;setPlayerMorphGeometry(playNextMorph.amount);return;
 }
 const from=playNextMorph.amount,to=target?1:0;
 if(Math.abs(from-to)<.0001){playNextMorph.amount=to;setPlayerMorphGeometry(to);return;}
 const duration=PLAYER_MORPH_MS*Math.abs(to-from);
 const beginning=performance.now();
 const frame=time=>{
  const progress=Math.min(1,Math.max(0,(time-beginning)/duration));
  const eased=progress<.5?4*progress*progress*progress:1-Math.pow(-2*progress+2,3)/2;
  playNextMorph.amount=from+(to-from)*eased;
  setPlayerMorphGeometry(playNextMorph.amount);
  if(progress<1)playNextMorph.frame=requestAnimationFrame(frame);else playNextMorph.frame=0;
 };
 playNextMorph.frame=requestAnimationFrame(frame);
}
function setPlayNextVisible(show){
 if(show===playNextShown)return;
 playNextShown=show;
 const area=document.getElementById('player-area'),upnext=document.getElementById('player-upnext');
 if(!area||!upnext)return;
 area.classList.toggle('play-next-active',show);
 upnext.setAttribute('aria-hidden',String(!show));
 const cancel=document.getElementById('player-upnext-cancel');if(cancel)cancel.disabled=!show;
 morphPlayerTo(show);
 if(show){area.classList.remove('controls-hidden');clearTimeout(playerControlsTimer);playerControlsTimer=null;}
 else playerControlsScheduleHide();
}

/* Standalone browser-review aid. Real provider streams are not simulated here.
   The existing v103 HTML5 video handlers remain responsible for actual playback. */
const SF_PLAYER_DEMO_DURATION=1470;
let sfPlayerDemo={active:false,playing:false,time:462,frame:0,lastStamp:0,autoplay:true};
let sfPlayerLocalObjectURL=null;
function sfPlayerDemoStop(){
 cancelAnimationFrame(sfPlayerDemo.frame);
 sfPlayerDemo={active:false,playing:false,time:462,frame:0,lastStamp:0,autoplay:true};
 document.getElementById('sf-player-demo-scene')?.setAttribute('hidden','');
 const btn=document.getElementById('sf-player-demo-toggle');if(btn)btn.textContent='Start simulation';
 for(const id of ['sf-player-demo-jump','sf-player-demo-resume']){
  const el=document.getElementById(id);if(el)el.disabled=true;
 }
}
function sfPlayerDemoStart(){
 const video=document.getElementById('local-video');if(!video)return;
 video.pause();
 sfPlayerDemoStop();
 sfPlayerDemo.active=true;
 sfPlayerDemo.autoplay=document.getElementById('sf-player-demo-autoplay')?.checked??true;
 sfPlayerDemo.lastStamp=0;
 document.getElementById('player-empty').hidden=true;
 document.getElementById('sf-player-demo-scene').hidden=false;
 const btn=document.getElementById('sf-player-demo-toggle');if(btn)btn.textContent='Stop simulation';
 for(const id of ['sf-player-demo-jump','sf-player-demo-resume']){
  const el=document.getElementById(id);if(el)el.disabled=false;
 }
 showPlayerNotice('SIMULATION ONLY: no video stream or episode is playing. Use the controls to examine Gallery’s player animations.');
 updatePlaybackUI();
 sfPlayerDemo.frame=requestAnimationFrame(sfPlayerDemoTick);
}
function sfPlayerDemoTick(stamp){
 if(!sfPlayerDemo.active)return;
 if(sfPlayerDemo.playing){
  if(sfPlayerDemo.lastStamp)sfPlayerDemo.time=Math.min(SF_PLAYER_DEMO_DURATION,sfPlayerDemo.time+Math.min((stamp-sfPlayerDemo.lastStamp)/1000,.10));
  if(sfPlayerDemo.time>=SF_PLAYER_DEMO_DURATION){
   sfPlayerDemo.playing=false;
   showPlayerNotice('Simulation reached the end. A real next episode cannot be loaded without a connected source.');
  }
  updatePlaybackUI();
 }
 sfPlayerDemo.lastStamp=stamp;
 sfPlayerDemo.frame=requestAnimationFrame(sfPlayerDemoTick);
}
function sfPlayerDemoSeek(t){
 sfPlayerDemo.time=Math.max(0,Math.min(SF_PLAYER_DEMO_DURATION,t));
 if(sfPlayerDemo.time<SF_PLAYER_DEMO_DURATION-20)playNextCanceled=false;
 updatePlaybackUI();playerControlsWake();
}
function sfPlayerDemoPlayPause(){
 if(sfPlayerDemo.time>=SF_PLAYER_DEMO_DURATION)sfPlayerDemoSeek(0);
 sfPlayerDemo.playing=!sfPlayerDemo.playing;
 sfPlayerDemo.lastStamp=0;
 updatePlaybackUI();playerControlsWake();
}
function sfPlayerReleaseBrowserVideo(){
 if(sfPlayerLocalObjectURL){URL.revokeObjectURL(sfPlayerLocalObjectURL);sfPlayerLocalObjectURL=null;}
}
function sfPlayerPickBrowserVideo(file){
 if(!file)return;
 const video=document.getElementById('local-video');if(!video)return;
 sfPlayerDemoStop();video.pause();sfPlayerReleaseBrowserVideo();
 sfPlayerLocalObjectURL=URL.createObjectURL(file);
 video.src=sfPlayerLocalObjectURL;video.load();
 document.getElementById('player-empty').hidden=true;
 document.getElementById('local-file-label').textContent=file.name;
 showPlayerNotice('Local video loaded in this browser preview. Playback depends on browser codec support; no file has been uploaded.');
}

function updatePlayNext(){
 const video=document.getElementById('local-video');if(!video)return;
 const title=document.getElementById('player-upnext-title'),countdown=document.getElementById('player-upnext-countdown');
 const remaining=sfPlayerDemo.active?Math.max(0,SF_PLAYER_DEMO_DURATION-sfPlayerDemo.time):Number.isFinite(video.duration)?Math.max(0,video.duration-video.currentTime):Infinity;
 const triggered=playerCanAdvance()&&(playNextPreview||(
  (sfPlayerDemo.active?sfPlayerDemo.autoplay:state.autoplayNextEpisode) && !playNextCanceled &&
  (sfPlayerDemo.active||isLocalVideoReady) && !(sfPlayerDemo.active?sfPlayerDemo.time>=SF_PLAYER_DEMO_DURATION:video.ended) && Number.isFinite(remaining) && remaining<=20 && (sfPlayerDemo.active?sfPlayerDemo.time:video.currentTime)>0
 ));
 if(title){const p=state.playback;title.textContent=p?`Episode ${p.episode+1}`:'Next episode';}
 if(countdown)countdown.textContent=playNextPreview?'Next in 00:12':`Next in ${fmtTime(Math.ceil(remaining))}`;
 setPlayNextVisible(triggered);
}
function cancelPlayNext(){
 playNextCanceled=true;playNextPreview=false;
 const demoButton=document.getElementById('preview-play-next');
 if(demoButton){demoButton.setAttribute('aria-pressed','false');demoButton.textContent='Preview Play Next transition';}
 setPlayNextVisible(false);
 const area=document.getElementById('player-area');if(area&&area.contains(document.activeElement))area.focus({preventScroll:true});
}
function resetPlayNextState(){
 cancelAnimationFrame(playNextMorph.frame);
 playNextMorph={amount:0,frame:0};playNextShown=false;playNextCanceled=false;playNextPreview=false;
}

/* Volume indicator is state-derived; keep the DOM stable so its waves can fade. */
let playerLastAudibleVolume=(playerSessionVolume>0?playerSessionVolume:GALLERY_INITIAL_VOLUME)/100;
function playerVolumeLevel(video){
 if(!video||video.muted||video.volume<=0)return 0;
 const pct=Math.round(video.volume*100);
 if(pct<=25)return 1;
 if(pct<=50)return 2;
 if(pct<=75)return 3;
 return 4;
}
function updatePlayerVolumeIcon(video){
 if(!video)return;
 const button=document.getElementById('mute');
 const svg=button?.querySelector('.player-volume-icon');
 if(!button||!svg)return;
 const level=playerVolumeLevel(video);
 svg.dataset.level=String(level);
 const muted=level===0;
 button.setAttribute('aria-label',muted?'Unmute':'Mute');
 button.setAttribute('aria-pressed',String(muted));
 button.title=muted?'Unmute':'Mute';
 const slider=document.getElementById('volume');
 if(slider){
  slider.value=String(Math.round(video.volume*100));
  slider.setAttribute('aria-valuetext',`${Math.round(video.volume*100)} percent${video.muted?' (muted)':''}`);
 }
 if(!video.muted&&video.volume>0)playerLastAudibleVolume=video.volume;
}

function updatePlaybackUI(){
 const video=document.getElementById('local-video');if(!video)return;
 const duration=sfPlayerDemo.active?SF_PLAYER_DEMO_DURATION:Number.isFinite(video.duration)?video.duration:0;
 const currentTime=sfPlayerDemo.active?sfPlayerDemo.time:video.currentTime;
 const paused=sfPlayerDemo.active?!sfPlayerDemo.playing:video.paused;
 const portion=duration?Math.min(1,Math.max(0,currentTime/duration)):0;
 const watched=document.getElementById('watched'),seek=document.getElementById('seek');
 if(watched)watched.style.flexBasis=galleryTimelineFill(portion*100);
 if(seek){seek.value=String(Math.round(portion*1000));seek.disabled=!duration;}
 document.getElementById('current-time').textContent=fmtTime(currentTime);
 document.getElementById('duration-time').textContent=fmtTime(duration);
 const play=document.getElementById('pause-play');if(play)play.disabled=!(isLocalVideoReady||sfPlayerDemo.active);sfSetPlayMorph(!paused);
 updatePlayerVolumeIcon(video);
 updatePlayNext();
}
function showPlayerNotice(text){const n=document.getElementById('player-notice');if(n)n.textContent=text;}
async function openLocalForPlayer(){
 if(!window.galleryDesktop){document.getElementById('sf-player-browser-file')?.click();return;}
 let chosen;
 try{chosen=await window.galleryDesktop.openVideo();}
 catch(error){showPlayerNotice(`Unable to open file: ${error.message}`);return;}
 if(!chosen)return;
 const video=document.getElementById('local-video');if(!video)return;
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 video.pause();isLocalVideoReady=false;localVideoName=chosen.name;
 video.src=chosen.fileURL;video.load();
 document.getElementById('player-empty').hidden=true;
 document.getElementById('local-file-label').textContent=chosen.name;
 document.getElementById('open-external-vlc').disabled=false;
 showPlayerNotice(`Selected local file: ${chosen.name}. The codec must be supported by Electron for in-app playback. Subtitles and streaming providers are not wired in this milestone.`);
 if(state.playerPreference==='vlc'){
  const result=await window.galleryDesktop.openInVLC();
  if(result.ok){
   video.pause();showPlayerNotice(`Opened ${chosen.name} in VLC as requested. Gallery cannot reliably track external playback progress; player compatibility is not guaranteed.`);
  }else{
   video.pause();showPlayerNotice(`VLC is your selected player, but it could not open the file: ${result.message}. You can press Play to use the built-in player for this file, or locate VLC in Settings.`);
  }
 }
 // User action picked a file; no automatic next-episode transition.
}
function advanceEpisode(step,{sameInstallmentOnly=false}={}){
 const destination=playbackNeighbor(step,{sameInstallmentOnly});
 if(!destination)return;
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 resetPlayNextState();
 const p=state.playback;
 state.detailSeason=destination.seasonIndex;
 state.detailRelated=destination.relatedId;
 state.detailEpisode=destination.episode;
 state.playback={...p,episode:destination.episode,installmentId:destination.installment.id};
 isLocalVideoReady=false;localVideoName='';render();workspace.scrollTop=0;
}
// The controls fade out during playback and stay visible for keyboard users.
let playerControlsTimer=null;
let playerEventController=null;
let playerKeyboardFocus=false;
const PLAYER_CONTROLS_IDLE_MS=2600;
function playerControlsWake(){
 const area=document.getElementById('player-area');if(!area)return;
 area.classList.remove('controls-hidden');
 playerControlsScheduleHide();
}
function playerControlsScheduleHide(){
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 const area=document.getElementById('player-area'),video=document.getElementById('local-video');
 if(!area||!video)return;
 const playingNow=sfPlayerDemo.active?sfPlayerDemo.playing:(!video.paused&&!video.ended);
 if((!isLocalVideoReady&&!sfPlayerDemo.active)||!playingNow||playNextShown){area.classList.remove('controls-hidden');return;}
 const focused=document.activeElement;
 if(playerKeyboardFocus&&focused&&area.contains(focused)&&focused!==area)return;
 if(document.getElementById('modal-host')?.firstElementChild)return;
 playerControlsTimer=setTimeout(()=>{
  const currentVideo=document.getElementById('local-video'),currentArea=document.getElementById('player-area');
  if(!currentArea||!currentVideo||currentVideo!==video||!(sfPlayerDemo.active?sfPlayerDemo.playing:(!currentVideo.paused&&!currentVideo.ended))||playNextShown)return;
  const active=document.activeElement;
  if(playerKeyboardFocus&&active&&currentArea.contains(active)&&active!==currentArea)return;
  if(document.getElementById('modal-host')?.firstElementChild)return;
  currentArea.classList.add('controls-hidden');
 },PLAYER_CONTROLS_IDLE_MS);
}
function initializePlayer(){
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 const v=document.getElementById('local-video');if(!v)return;
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 playerEventController?.abort();playerEventController=new AbortController();
 isLocalVideoReady=false;localVideoName='';
 resetPlayNextState();
 sfResetPlayMorph();
 playerSubtitleState.enabled=state.playback?.subtitles!==false;
 playerSubtitleState.lastIndex=null;
 playerSubtitleState.lastLanguage='en';
 v.volume=playerSessionVolume/100;v.muted=playerSessionMuted;v.autoplay=false;v.loop=false;
 whInitPlayerSession();
 v.addEventListener('timeupdate',()=>whOnVideoTick(v));
 v.addEventListener('seeked',()=>whOnVideoSeek(v));
 v.addEventListener('loadedmetadata',()=>{whInitPlayerSession();isLocalVideoReady=true;document.getElementById('player-empty').hidden=true;applyPlayerSubtitleState(v);updatePlaybackUI();});
 v.textTracks?.addEventListener?.('addtrack',()=>applyPlayerSubtitleState(v));
 v.addEventListener('error',()=>{isLocalVideoReady=false;document.getElementById('player-empty').hidden=false;showPlayerNotice('The selected file cannot be decoded in the integrated Chromium player. You may try VLC, if installed, or another compatible file.');updatePlaybackUI();});
 for(const name of ['timeupdate','seeked','durationchange','play','pause','ended','ratechange'])v.addEventListener(name,updatePlaybackUI);
 v.addEventListener('volumechange',()=>{rememberGalleryPlayerVolume(v);updatePlaybackUI();});
 v.addEventListener('play',playerControlsWake);
  v.addEventListener('ended',()=>{if(state.autoplayNextEpisode&&!playNextCanceled&&playerCanAdvance()&&!playNextPreview)showPlayerNotice('This local-file test ended. Play Next cannot load the following episode until a real episode source is connected.');});
 for(const name of ['pause','ended','emptied'])v.addEventListener(name,()=>{clearTimeout(playerControlsTimer);document.getElementById('player-area')?.classList.remove('controls-hidden');});
 const playerArea=document.getElementById('player-area');
 playerArea.addEventListener('pointermove',()=>{playerKeyboardFocus=false;playerControlsWake();});
 playerArea.addEventListener('pointerdown',()=>{playerKeyboardFocus=false;playerControlsWake();});
 playerArea.addEventListener('keydown',()=>{playerKeyboardFocus=true;playerControlsWake();});
 document.addEventListener('keydown',e=>{if(e.key==='Tab')playerKeyboardFocus=true;},{signal:playerEventController.signal});
 playerArea.addEventListener('focusin',playerControlsWake);
 playerArea.addEventListener('focusout',()=>setTimeout(playerControlsScheduleHide,0));
 document.addEventListener('fullscreenchange',playerControlsWake,{signal:playerEventController.signal});
 document.getElementById('open-local-video').onclick=openLocalForPlayer;
 document.getElementById('sf-player-browser-file').onchange=e=>{sfPlayerPickBrowserVideo(e.target.files?.[0]);e.target.value='';};
 document.body.dataset.sfPlayAccent='secondary';
 document.getElementById('sf-player-play-accent').onchange=e=>{document.body.dataset.sfPlayAccent=e.target.checked?'secondary':'original';};
 document.getElementById('sf-player-demo-start').onclick=sfPlayerDemoStart;
 document.getElementById('sf-player-demo-toggle').onclick=()=>{
  if(sfPlayerDemo.active){sfPlayerDemoStop();document.getElementById('player-empty').hidden=!!isLocalVideoReady;updatePlaybackUI();}
  else sfPlayerDemoStart();
 };
 document.getElementById('sf-player-demo-jump').onclick=()=>{playNextCanceled=false;sfPlayerDemoSeek(SF_PLAYER_DEMO_DURATION-25);};
 document.getElementById('sf-player-demo-autoplay').onchange=e=>{sfPlayerDemo.autoplay=e.target.checked;updatePlaybackUI();};
 document.getElementById('sf-player-demo-resume').onclick=()=>{
  sfPlayerDemo.playing=false;updatePlaybackUI();
  modal('Resume or start over · simulation',`<p class="description">This is a simulated watch-history prompt. The saved position is 12:18. Resume starts eight seconds earlier; no real watch history is changed.</p>`,
  '<button class="btn" id="sf-resume-cancel">Cancel</button><button class="btn" id="sf-start-over">Start over</button><button class="btn primary" id="sf-resume-now">Resume</button>');
  document.getElementById('sf-resume-cancel').onclick=closeModal;
  document.getElementById('sf-start-over').onclick=()=>{sfPlayerDemoSeek(0);closeModal();};
  document.getElementById('sf-resume-now').onclick=()=>{sfPlayerDemoSeek(730);closeModal();};
 };

 document.getElementById('change-local-video').onclick=openLocalForPlayer;
 document.getElementById('pause-play').onclick=()=>{if(sfPlayerDemo.active){sfPlayerDemoPlayPause();return;}if(!isLocalVideoReady)return;if(v.paused)v.play().catch(e=>showPlayerNotice('Unable to play file: '+e.message));else v.pause();};
 document.getElementById('rewind10').onclick=()=>{if(sfPlayerDemo.active){sfPlayerDemoSeek(sfPlayerDemo.time-10);return;}if(Number.isFinite(v.duration))v.currentTime=Math.max(0,v.currentTime-10);};
 document.getElementById('forward10').onclick=()=>{if(playNextShown){if(sfPlayerDemo.active){showPlayerNotice('Simulation: Next episode is not connected.');sfPlayerDemo.playing=false;updatePlaybackUI();return;}advanceEpisode(1,{sameInstallmentOnly:true});return;}if(sfPlayerDemo.active){sfPlayerDemoSeek(sfPlayerDemo.time+10);return;}if(Number.isFinite(v.duration))v.currentTime=Math.min(v.duration,v.currentTime+10);};
  document.getElementById('player-upnext-cancel').onclick=cancelPlayNext;
  document.getElementById('preview-play-next').onclick=e=>{playNextPreview=!playNextPreview;playNextCanceled=false;e.currentTarget.setAttribute('aria-pressed',String(playNextPreview));e.currentTarget.textContent=playNextPreview?'Stop Play Next preview':'Preview Play Next transition';updatePlayNext();};
 document.getElementById('seek').oninput=e=>{if(sfPlayerDemo.active){sfPlayerDemoSeek(SF_PLAYER_DEMO_DURATION*Number(e.target.value)/1000);return;}if(Number.isFinite(v.duration))v.currentTime=v.duration*Number(e.target.value)/1000;};
 const thresholdPreview=document.getElementById('sf-player-volume-test');
 if(thresholdPreview)thresholdPreview.onchange=()=>{
  if(thresholdPreview.value==='')return;
  const percentage=Number(thresholdPreview.value);
  v.volume=percentage/100;
  v.muted=percentage===0;
  rememberGalleryPlayerVolume(v);
  updatePlayerVolumeIcon(v);
 };
 const volume=document.getElementById('volume');volume.oninput=()=>{
  if(thresholdPreview)thresholdPreview.value='';
  v.volume=Number(volume.value)/100;
  v.muted=v.volume===0;
  rememberGalleryPlayerVolume(v);
  updatePlayerVolumeIcon(v);
 };
 document.getElementById('mute').onclick=()=>{
  if(v.muted||v.volume===0){
   if(v.volume===0)v.volume=playerLastAudibleVolume>0?playerLastAudibleVolume:GALLERY_INITIAL_VOLUME/100;
   v.muted=false;
  }else{
   playerLastAudibleVolume=v.volume;
   v.muted=true;
  }
  rememberGalleryPlayerVolume(v);
  updatePlayerVolumeIcon(v);
 };
 document.getElementById('player-settings').onclick=()=>openPlayerSettings(v);
 const fullscreen=()=>{const area=document.getElementById('player-area');if(!document.fullscreenElement)area.requestFullscreen?.().catch(()=>showPlayerNotice('Fullscreen is not available in this environment.'));else document.exitFullscreen?.();};
 document.getElementById('fullscreen').onclick=fullscreen;
 document.getElementById('previous-episode')?.addEventListener('click',()=>advanceEpisode(-1));
 document.getElementById('next-episode')?.addEventListener('click',()=>advanceEpisode(1));
 document.getElementById('open-external-vlc').onclick=async()=>{
  if(!window.galleryDesktop)return;
  const result=await window.galleryDesktop.openInVLC();
  if(!result.ok)showPlayerNotice(`${result.message} Use Settings to locate VLC manually if automatic detection fails. External-player compatibility and progress tracking are not guaranteed.`);
  else showPlayerNotice('The selected local file was handed to VLC. Watch progress in Gallery is not tracked for external playback.');
 };
 updatePlaybackUI();
}

function render(){
 if(!state.playback){clearTimeout(playerControlsTimer);playerControlsTimer=null;playerEventController?.abort();playerEventController=null;resetPlayNextState();}
 document.body.classList.toggle('player-view',Boolean(state.playback));
 // Both the Anime detail and Watch History are secondary pages: hide main
 // navigation, but retain the standard Gallery brand header and back buttons.
 document.body.classList.toggle('detail-view',Boolean(state.detailId&&!state.playback&&!whOpen));
 if(whOpen){
  freezeTabTrack();hideTabScrollOverlay();workspace.classList.remove('tab-pages-visible','library-view');tabPagesViewport.hidden=true;screen.hidden=false;screen.dataset.surfaceKey='watch-history';whRender({keepScroll:false});return;
 }
 if(!state.playback&&!state.detailId){showTabPages();return;}
 // Detail and player screens retain their existing layout and event handling.
 freezeTabTrack();
 hideTabScrollOverlay();
 workspace.classList.remove('tab-pages-visible');
 tabPagesViewport.hidden=true;
 screen.hidden=false;
 const oldTagScroll=screen.querySelector('.tagbar')?.scrollLeft||0;
 const priorRailScroll=screen.querySelector('#inline-installment-rail')?.scrollLeft||0;
 workspace.classList.toggle('library-view',state.view==='library'&&!state.detailId);
 // Animate actual screen navigation, not routine player updates or episode selections.
 const surfaceKey=state.playback?'playback':state.detailId?'detail:'+state.detailId:state.view==='discover'?'discover:'+state.filterStatus+':'+state.filterAudio:state.view==='library'?'library:'+state.tag:'downloads:'+state.downloadStatus;
 const surfaceChanged=screen.dataset.surfaceKey!==surfaceKey;
 screen.dataset.surfaceKey=surfaceKey;
 screen.innerHTML=state.playback?playbackPage():state.detailId?detailPage():state.view==='discover'?discover():state.view==='library'?library():downloads();
 if(surfaceChanged){
  clearGallerySurfaceEntrance();
  if(!galleryStageMutating&&!galleryReducedMotion.matches){
   void screen.offsetWidth;
   screen.classList.add('surface-enter');
  }
 }
 if(state.playback){
   document.getElementById('back-from-playback')?.addEventListener('click',backFromPlayback);
   initializePlayer();requestAnimationFrame(updateTabScrollOverlay);return;
 }
 if(state.detailId){
   document.getElementById('detail-back')?.addEventListener('click',backFromDetail);
   activeInstallmentRailObserver?.disconnect();
   activeInstallmentRailObserver=null;
   const rail=document.getElementById('inline-installment-rail');
   if(rail){
     rail.addEventListener('scroll',refreshInstallmentArrows,{passive:true});
     setupInstallmentEdgeGuards(rail.closest('.inline-release-viewport'));
     activeInstallmentRailObserver=new ResizeObserver(refreshInstallmentArrows);
     activeInstallmentRailObserver.observe(rail);
     for(const card of rail.children)activeInstallmentRailObserver.observe(card);
     requestAnimationFrame(refreshInstallmentArrows);
     rail.scrollLeft=priorRailScroll;
     for(const arrow of screen.querySelectorAll('[data-inline-scroll]'))arrow.addEventListener('click',()=>{
// One arrow click advances by exactly one discrete release, not a viewport fraction.
       const direction=Number(arrow.dataset.inlineScroll);
       // Even at the end, this click is consumed by the invisible guard.
       if(arrow.closest('.inline-release-viewport').classList.contains(direction>0?'guard-right':'guard-left'))return;
       const cards=Array.from(rail.querySelectorAll('.inline-installment-card'));
       const railX=rail.getBoundingClientRect().left;
       const offsets=cards.map(card=>card.getBoundingClientRect().left-railX+rail.scrollLeft);
       const position=rail.scrollLeft;
       const target=direction>0
         ? offsets.find(offset=>offset>position+4)
         : [...offsets].reverse().find(offset=>offset<position-4);
       const limit=Math.max(0,rail.scrollWidth-rail.clientWidth);
       if(target===undefined)return;
       rail.scrollTo({left:Math.max(0,Math.min(target,limit)),behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
     });
     for(const card of rail.querySelectorAll('[data-inline-installment]'))
       card.addEventListener('click',()=>selectInlineInstallment(card,rail));
   }
   document.getElementById('find-source')?.addEventListener('click',showFindSource);
   bindEpisodeFiltersAndActions();
     for(const el of screen.querySelectorAll('[data-detail-audio]'))el.addEventListener('click',()=>{
     const next=el.dataset.detailAudio;
     if((state.detailAudio||state.defaultPlayback)===next)return;
     changeDetailAudio(next);
   });
   document.getElementById('manage-detail-tags')?.addEventListener('click',showManageDetailTags);
   for(const el of screen.querySelectorAll('.detail-actions [data-episode-action]'))el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
   requestAnimationFrame(updateTabScrollOverlay);
   return;
 }
 if(state.view==='library'&&screen.querySelector('.tagbar'))screen.querySelector('.tagbar').scrollLeft=oldTagScroll;
 for(const el of screen.querySelectorAll('[data-detail]'))el.addEventListener('click',()=>showDetail(el.dataset.detail));
 for(const el of screen.querySelectorAll('[data-tag]'))el.addEventListener('click',()=>{state.tag=el.dataset.tag;render();});
 const on=(id,fn)=>{const el=document.getElementById(id);if(el)el.addEventListener('click',fn)};
 on('filters',showFilters);on('resume',()=>showDetail('demo:02'));on('discover-browse-sources',openSourceManagerFromDiscover);on('import',showImport);on('newtag',showNewTag);on('sharetag',showShare);on('renametag',showRenameTag);on('openfolder',showFolderInfo);
 for(const el of screen.querySelectorAll('[data-download-filter]'))el.addEventListener('click',()=>{state.downloadStatus=el.dataset.downloadFilter;render();});
}
/* v39: Modal lifecycle and keyboard focus stay stable across every Gallery dialog.
   Preserve the original opener even when a dialog replaces another (e.g. import preview). */
const galleryApp=document.querySelector('.app');
let modalReturnFocus=null;
const modalFocusable='button:not([disabled]),[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';
function visibleModalControls(){
 const dialog=modalHost.querySelector('.dialog');
 return dialog?Array.from(dialog.querySelectorAll(modalFocusable)).filter(el=>!el.closest('[hidden]')&&el.getClientRects().length>0&&!el.inert):[];
}
function modal(title,inner,actions=''){
 const previouslyOpen=!!modalHost.querySelector('.overlay');
 if(!previouslyOpen){
  const opener=document.activeElement;
  modalReturnFocus=opener instanceof HTMLElement&&opener!==document.body&&!modalHost.contains(opener)?opener:null;
 }
 clearTimeout(modalExitTimer);modalExitTimer=null;
 modalHost.innerHTML=`<div class="overlay" role="presentation"><div class="dialog" role="dialog" aria-modal="true" aria-label="${escapeHTML(title)}" tabindex="-1"><div class="dialog-scroll"><div class="dialog-head"><h2>${escapeHTML(title)}</h2><button class="iconbtn" aria-label="Close dialog" id="close-dialog">${icon('close',20)}</button></div>${inner}${actions?`<div class="dialog-actions">${actions}</div>`:''}</div></div></div>`;
 galleryApp.inert=true;
 modalHost.querySelector('.overlay').addEventListener('click',e=>{if(e.target.classList.contains('overlay'))closeModal()});
 document.getElementById('close-dialog').addEventListener('click',closeModal);
 (modalHost.querySelector('button:not(#close-dialog),input,select')||document.getElementById('close-dialog')).focus({preventScroll:true});
}
function finishModalClose(overlay){
 if(modalHost.firstElementChild!==overlay)return;
 const expandedStage=overlay.querySelector('#subtitle-expanded-stage');
 if(expandedStage)subtitleResizeObserver?.unobserve(expandedStage);
 modalHost.innerHTML='';
 galleryApp.inert=false;
 const target=modalReturnFocus;
 modalReturnFocus=null;
 if(target?.isConnected&&!target.disabled)target.focus({preventScroll:true});
 else document.getElementById('settings')?.focus({preventScroll:true});
}
function closeModal(){
 const overlay=modalHost.querySelector('.overlay');
 if(!overlay||overlay.classList.contains('is-closing'))return;
clearTimeout(modalExitTimer);
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){finishModalClose(overlay);return;}
 overlay.classList.add('is-closing');
 modalExitTimer=setTimeout(()=>{
  finishModalClose(overlay);
  modalExitTimer=null;
 },150);
}
/* v41: All Tab / Shift+Tab focus changes in dialogs are managed here.
   Prevent Chrome's instant implicit focus scroll, then reveal the newly
   focused control through the same smooth scroll path as wraparound.
   Keep focus itself immediate, the dialog stationary and Reduce Motion intact. */
let modalScrollFrame=null;
let modalScrollGoal=null;
let modalScrollContainer=null;
function cancelModalKeyboardScroll(){
 if(modalScrollFrame!==null)cancelAnimationFrame(modalScrollFrame);
 modalScrollFrame=null;modalScrollGoal=null;modalScrollContainer=null;
}
function revealModalControl(control,edge='nearest'){
 const scroller=modalHost.querySelector('.dialog-scroll');
 if(!scroller||!control||!scroller.contains(control))return;
 // Compute visibility relative to the *intended* destination of any in-flight
 // keyboard scroll, not an intermediate animation frame. Repeated Tab presses
 // can therefore redirect the scroll without piling up contradictory requests.
 const base=(scroller===modalScrollContainer&&modalScrollGoal!==null)
  ?modalScrollGoal:scroller.scrollTop;
 const max=Math.max(0,scroller.scrollHeight-scroller.clientHeight);
 let target=base;
 if(edge==='start')target=0;
 else if(edge==='end')target=max;
 else{
  const view=scroller.getBoundingClientRect();
  const item=control.getBoundingClientRect();
  const itemTop=item.top-view.top+scroller.scrollTop;
  const itemBottom=item.bottom-view.top+scroller.scrollTop;
  const breathingRoom=10;
  if(itemTop<base+breathingRoom)target=itemTop-breathingRoom;
  else if(itemBottom>base+scroller.clientHeight-breathingRoom)
   target=itemBottom-scroller.clientHeight+breathingRoom;
 }
 target=Math.max(0,Math.min(target,max));
 cancelModalKeyboardScroll();
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
  scroller.scrollTop=target;return;
 }
 const start=scroller.scrollTop;
 if(Math.abs(target-start)<1)return;
 modalScrollContainer=scroller;modalScrollGoal=target;
 const distance=Math.abs(target-start);
 const duration=Math.min(410,Math.max(220,180+Math.sqrt(distance)*7));
 let started=null;
 function step(time){
  if(modalScrollContainer!==scroller)return;
  if(started===null)started=time;
  const fraction=Math.min(1,(time-started)/duration);
  const eased=1-Math.pow(1-fraction,3);
  scroller.scrollTop=start+(target-start)*eased;
  if(fraction<1)modalScrollFrame=requestAnimationFrame(step);
  else{modalScrollFrame=null;modalScrollGoal=null;modalScrollContainer=null;}
 }
 modalScrollFrame=requestAnimationFrame(step);
}
// Pointer/wheel scrolling always takes precedence over keyboard-initiated motion.
modalHost.addEventListener('wheel',cancelModalKeyboardScroll,{passive:true,capture:true});
modalHost.addEventListener('touchstart',cancelModalKeyboardScroll,{passive:true,capture:true});
/* Set before focus() and cleared synchronously by focusin. This prevents
   the focusin fallback from issuing a second, conflicting scroll request. */
let modalKeyboardFocusTarget=null;
document.addEventListener('keydown',event=>{
 const overlay=modalHost.querySelector('.overlay');
 if(!overlay)return;
 if(event.key==='Escape'){
  event.preventDefault();event.stopImmediatePropagation();closeModal();return;
 }
 if(event.key!=='Tab'||overlay.classList.contains('is-closing')||event.altKey||event.ctrlKey||event.metaKey)return;
 const controls=visibleModalControls();
 const active=document.activeElement;
 const backward=event.shiftKey;
 // Only Settings requires manual Tab navigation. Other dialogs retain native
 // Tab behavior (important for radio groups) and the original focus trap.
 if(!overlay.querySelector('#apply-preferences')){
  const first=controls[0],last=controls[controls.length-1];
  if(!first){event.preventDefault();overlay.querySelector('.dialog')?.focus({preventScroll:true});return;}
  if(!overlay.contains(active)||(backward&&active===first)||(!backward&&active===last)){
   event.preventDefault();
   const next=backward?last:first;
   modalKeyboardFocusTarget=next;
   next.focus({preventScroll:true});
   if(modalKeyboardFocusTarget===next)modalKeyboardFocusTarget=null;
   revealModalControl(next,backward?'end':'start');
  }
  return;
 }
 event.preventDefault(); // Never let Chrome jump to an off-screen Settings control.
 if(!controls.length){overlay.querySelector('.dialog')?.focus({preventScroll:true});return;}
 const index=controls.indexOf(active);
 const nextIndex=index<0?(backward?controls.length-1:0):(index+(backward?-1:1)+controls.length)%controls.length;
 const next=controls[nextIndex];
 const wrap=index>=0&&((backward&&index===0)||(!backward&&index===controls.length-1));
 modalKeyboardFocusTarget=next;
 next.focus({preventScroll:true});
 // A click or programmatic focus may already have focused next.
 if(modalKeyboardFocusTarget===next)modalKeyboardFocusTarget=null;
 revealModalControl(next,wrap?(backward?'end':'start'):'nearest');
},true);
document.addEventListener('focusin',event=>{
 const overlay=modalHost.querySelector('.overlay');
 if(!overlay||overlay.classList.contains('is-closing'))return;
 if(overlay.contains(event.target)){
  const focused=event.target;
  if(focused===modalKeyboardFocusTarget){modalKeyboardFocusTarget=null;return;}
  // Mouse/programmatic focus outside Tab should still reveal hidden controls.
  requestAnimationFrame(()=>{
   if(document.activeElement===focused)revealModalControl(focused);
  });
  return;
 }
 const first=visibleModalControls()[0]||overlay.querySelector('.dialog');
 first?.focus({preventScroll:true});
 revealModalControl(first);
},true);
function showDetail(id,fromHistory=false,installmentId=null){
 const x=demo.find(t=>t.id===id);if(!x)return;
 transitionGalleryStage(()=>{
  state.playback=null;state.detailReturnHistory=fromHistory;
  state.detailReturnView=state.view;state.detailReturnScroll=selectedTabScroll();
  state.detailId=id;state.detailSeason=0;state.detailRelated=null;
  if(installmentId){const index=getSeasons(x).findIndex(season=>season.id===installmentId);if(index>=0)state.detailSeason=index;}
  state.detailEpisodeFilter='all';state.detailEpisode=1;state.detailAudio=null;
  closeModal();render();workspace.scrollTop=0;
 });
}
function showFolderInfo(){modal('Downloads folder',`<p class="description">In the finished macOS application, this button will open your configured download folder in Finder.</p><div class="dialog-sample"><b>Design prototype</b><p class="description">This standalone HTML demo has no access to a real application's downloaded files or chosen folder.</p></div>`,`<button class="btn primary" id="folder-okay">Got it</button>`);document.getElementById('folder-okay').onclick=closeModal;}
/* v57 — Settings is a full page. Original tabs and detail DOM stay mounted,
   not rerendered, so returning preserves the active view, filters, and scroll. */
let settingsReturnScroll=0;
let settingsLastSection='appearance';
let appearanceTab='theme';
let playbackTab='general';
let settingsClosing=false;
let settingsCloseFallback=null;
let settingsReturnAnimationTimer=null;
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

/* v62 Sources preview — Sample data is intentionally separate from rendering.
   Later, a source service can provide this shape without changing the UI. */
const SOURCES_PREVIEW_CATALOG=Object.freeze([
 {id:'anikoto',name:'anikoto',publisher:'TheYogMehta',repository:'official',latest:'7.0.0',minApp:'11.1.0',initialVersion:'6.0.1',initialHealth:'healthy'},
 {id:'pahe',name:'pahe',publisher:'TheYogMehta',repository:'official',latest:'7.0.1',minApp:'11.1.0',initialVersion:'6.0.1',initialHealth:'incompatible'}
]);
const SOURCES_PREVIEW_REPO=Object.freeze({id:'official',name:'Official StrawVerse extensions',publisher:'TheYogMehta',url:'https://github.com/TheYogMehta/extensions'});
// On entering Sources, show installed extensions if there are any;
// otherwise lead with the Marketplace. Keep the tab order stable.
function preferredSourcesTab(){
 return SOURCES_PREVIEW_CATALOG.some(p=>!!sourceDemoState[p.id]?.installed)?'installed':'marketplace';
}
let sourcesTab='installed';
let sourcesExpanded=new Set();
let sourcesFeedback='';
let sourceDemoState={};
let sourceDemoRepos=[];
let sourceDemoBusy=null;
let sourceDemoBusyAction=null;
let sourceDemoPhase=-1;
let sourceDemoOpToken=0;
function resetSourcesPreview(){
 sourceDemoOpToken++;
 sourceDemoState=Object.fromEntries(SOURCES_PREVIEW_CATALOG.map(p=>[p.id,{installed:p.initialVersion,health:p.initialHealth,nextOutcome:'working',notice:null,backup:null}]));
 sourceDemoRepos=[];sourceDemoBusy=null;sourceDemoBusyAction=null;sourceDemoPhase=-1;sourcesExpanded.clear();
 sourcesFeedback='Demo restored: sample source versions and states reset.';
 sourcesTab=preferredSourcesTab();
 renderSourcesPreview();
 refreshDiscoverFromSourcePreview();
}
// Initialise only the demonstration model, never touch source files or network.
sourceDemoState=Object.fromEntries(SOURCES_PREVIEW_CATALOG.map(p=>[p.id,{installed:p.initialVersion,health:p.initialHealth,nextOutcome:'working',notice:null,backup:null}]));

/* v68 · Independent mock provider listings reconciled by Gallery's canonical anime IDs.
   These are local demonstration fixtures; this is not an actual anime index,
   title-matching algorithm, provider API, or downloaded content. */
const SOURCE_PREVIEW_LISTINGS=Object.freeze({
 anikoto:Object.freeze(['demo:quints','demo:solo','demo:long','demo:aot','demo:01','demo:02','demo:03','demo:04','demo:05','demo:06','demo:08']),
 pahe:Object.freeze(['demo:quints','demo:solo','demo:aot','demo:02','demo:06','demo:07','demo:08','demo:09','demo:10'])
});
function getSourceCataloguePreview(){
 const installed=SOURCES_PREVIEW_CATALOG.filter(p=>!!sourceDemoState[p.id]?.installed);
 // A temporarily offline provider keeps previously known catalogue entries visible.
 // A broken/incompatible extension cannot supply a current listing in this demo.
 const catalogSources=installed.filter(p=>!['incompatible','broken'].includes(sourceDemoState[p.id].health));
 const listings=new Map();
 for(const provider of catalogSources){
  for(const id of SOURCE_PREVIEW_LISTINGS[provider.id]||[]){
   if(!listings.has(id))listings.set(id,new Set());
   listings.get(id).add(provider.id);
  }
 }
 return {
  installed, catalogSources, listings,
  titles:demo.filter(item=>listings.has(item.id)),
  duplicates:[...listings.values()].filter(providers=>providers.size>1).length,
  cached:catalogSources.some(p=>sourceDemoState[p.id].health==='offline')
 };
}
function sourceCatalogueEmptyMarkup(model){
 const hasSources=model.installed.length>0;
 const title=hasSources?'Your sources need attention':'Discover starts with a source';
 const desc=hasSources
  ?'Your installed sources cannot currently provide a catalogue. Open Sources to inspect their status or install another provider. Your Library and Downloads are still available.'
  :'Install an anime source to start exploring titles. The official StrawVerse repository is already configured.';
 return `<section class="discover-source-empty" aria-label="${hasSources?'Sources need attention':'No sources installed'}"><div class="discover-source-empty-icon">${icon(hasSources?'info':'compass',26)}</div><h2>${title}</h2><p>${desc}</p><button type="button" class="btn primary" id="discover-browse-sources">${icon('globe',16)} ${hasSources?'Manage Sources':'Browse Sources'}</button><p class="discover-source-note">Local interface simulation · no real extensions or websites are accessed.</p></section>`;
}
function discoverSourceCount(model,items){
 const count=items.length;
 return `${count} ${count===1?'sample title':'sample titles'}${model.catalogSources.length?` · ${model.catalogSources.length} ${model.catalogSources.length===1?'source':'sources'}`:''}`;
}
function openSourceManagerFromDiscover(){
 showSettings(()=>{
  // The Settings page is independent of the main navigation; use its native
  // section switch and its built-in installed-first/marketplace-first rule.
  setSettingsSection('sources');
  if(preferredSourcesTab()==='marketplace')setSourcesTab('marketplace',false);
 });
}
function refreshDiscoverFromSourcePreview(){
 if(tabPagesReady){
  const panel=tabPages.discover;
  const originalScroll=panel.scrollTop;
  renderTabPage('discover');
  panel.scrollTop=originalScroll;
 }
}
function sourcesCatalogueScenarioMarkup(){
 const preview=getSourceCataloguePreview();
 return `<details class="sources-scenario sources-catalogue-preview"><summary>Preview Discover with different installed sources</summary><p>Try zero, one, or two installed sources. These shortcuts only update sample source availability; your Library entries, viewing history, and Downloads are not changed.</p><div class="sources-catalogue-actions"><button type="button" class="btn small" data-source-action="catalogue-none">No sources</button><button type="button" class="btn small" data-source-action="catalogue-one">Anikoto only</button><button type="button" class="btn small" data-source-action="catalogue-both">Both sources</button></div><p class="sources-catalogue-current">Currently: ${preview.installed.length} installed · ${preview.titles.length} distinct Discover titles${preview.duplicates?` · ${preview.duplicates} shared titles merged`:''}. Visit Discover to see the result.</p></details>`;
}
function applySourceCatalogueScenario(mode){
 // Cancel simulated asynchronous updates before switching preview presets.
 sourceDemoOpToken++;
 sourceOperationEnd();
 for(const p of SOURCES_PREVIEW_CATALOG){
  const enabled=mode==='catalogue-both'||(mode==='catalogue-one'&&p.id==='anikoto');
  sourceDemoState[p.id]={installed:enabled?p.latest:null,health:'healthy',nextOutcome:'working',notice:null,backup:null};
 }
 sourcesExpanded.clear();
 sourcesTab=preferredSourcesTab();
 const model=getSourceCataloguePreview();
 sourcesFeedback=`Demo: ${model.installed.length} installed ${model.installed.length===1?'source':'sources'}; ${model.titles.length} distinct titles in Discover. Your Library and Downloads were preserved.`;
 renderSourcesPreview();
 refreshDiscoverFromSourcePreview();
}

function sourceVersionNewer(current,latest){if(!current)return false;const x=current.split('.').map(Number),y=latest.split('.').map(Number);for(let i=0;i<Math.max(x.length,y.length);i++){if((x[i]||0)!==(y[i]||0))return (x[i]||0)<(y[i]||0);}return false;}
// The prototype distinguishes installed files, extension validation, and provider health.
// Update outcomes are chosen by the tester, not inferred from real network activity.
const SOURCE_UPDATE_PHASES=['Preparing update','Downloading update','Validating extension','Activating version','Checking provider'];
function sourcesStatus(p){
 const d=sourceDemoState[p.id];
 if(sourceDemoBusy===p.id)return {label:sourceDemoBusyAction==='retry'?'Checking…':sourceDemoBusyAction==='update'?'Updating…':'Installing…',kind:'',description:'The demonstration is progressing through validation and activation.'};
 if(!d.installed)return {label:'Not installed',kind:'',description:'This provider has not been installed.'};
 if(d.notice?.kind==='error')return {label:'Update failed',kind:'needs-attention',description:d.notice.text};
 if(d.health==='incompatible')return {label:'Update required',kind:'needs-attention',description:`The v${d.installed} file remains installed but cannot load. Updating may repair it; the previous version is not assumed to work.`};
 if(d.health==='broken')return {label:'Source broken',kind:'needs-attention',description:`The v${d.installed} extension is known not to work in this simulated scenario. An update may repair it.`};
 if(d.health==='offline')return {label:'Source unavailable',kind:'offline',description:`The installed v${d.installed} extension is intact, but its provider cannot currently be reached. This is not proof of broken code or missing episodes.`};
 if(sourceVersionNewer(d.installed,p.latest))return {label:'Update available',kind:'needs-attention',description:`A newer version is available. Gallery validates it before activation and retains a recovery copy of a previously working version.`};
 return {label:'Installed',kind:'',description:'The extension is installed and loaded successfully in this sample.'};
}
function sourceUpdateStageMarkup(){
 const retry=sourceDemoBusyAction==='retry';
 const i=Math.max(0,sourceDemoPhase);
 const stage=retry?'Checking provider':SOURCE_UPDATE_PHASES[i];
 const step=retry?'':' · '+(i+1)+' of '+SOURCE_UPDATE_PHASES.length;
 const progress=retry?60:((i+1)*100/SOURCE_UPDATE_PHASES.length);
 return {
  inline:`<span class="sources-inline-progress" title="${escapeHTML(stage+step)}">${icon('refresh',13)}<span>${escapeHTML(stage+step)}</span></span>`,
  track:`<div class="sources-update-track" role="progressbar" aria-label="${escapeHTML(stage)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${progress}"><span class="sources-update-track-fill" style="width:${progress}%"></span></div>`
 };
}
function sourceResultSummary(p,d){
 if(!d.notice)return `v${escapeHTML(p.latest)} available${d.installed?` · <b>v${escapeHTML(d.installed)} installed</b>`:''}`;
 let summary;
 if(d.notice.kind==='error')summary=`Update failed · ${d.installed?'v'+d.installed+' preserved':'Nothing installed'}`;
 else if(d.notice.kind==='warning')summary=`v${d.installed} installed · Provider unavailable`;
 else summary=`v${d.installed} installed · Provider verified`;
 return `<span class="sources-inline-result is-${d.notice.kind}" title="${escapeHTML(d.notice.text)}">${icon(d.notice.kind==='success'?'check':'info',13)}<span>${escapeHTML(summary)}</span></span>`;
}
function sourcesProviderMarkup(p){
 const d=sourceDemoState[p.id],st=sourcesStatus(p),isInstalled=!!d.installed,busy=!!sourceDemoBusy,active=sourceDemoBusy===p.id,expanded=sourcesExpanded.has(p.id);
 const action=isInstalled?(sourceVersionNewer(d.installed,p.latest)?'Update':null):'Install';
 const primary=action?`<button type="button" class="btn small primary" data-source-action="${action.toLowerCase()}" data-source-id="${p.id}" ${busy?'disabled':''}>${action}</button>`:'';
 const backup=d.backup;
 const recovery=backup?`<p class="sources-recovery-note">Recovery copy: <b>v${escapeHTML(backup.version)}</b> · ${backup.usable?'last known working version':'not confirmed working'}. ${backup.usable?'You may choose to restore it.':'Gallery will not suggest restoring a known-broken or unverified version.'}</p>${backup.usable?`<div class="sources-recovery-actions"><button type="button" class="btn small" data-source-action="restore" data-source-id="${p.id}" ${busy?'disabled':''}>Restore v${escapeHTML(backup.version)}…</button></div>`:''}`:'';
 const needsAlternative=isInstalled&&(d.health==='offline'||d.health==='broken'||d.health==='incompatible');
 const alternatives=needsAlternative?`<div class="sources-recovery-actions"><button type="button" class="btn small" data-source-action="retry" data-source-id="${p.id}" ${busy?'disabled':''}>Retry source check</button><button type="button" class="btn small" data-source-action="other-sources" data-source-id="${p.id}">Other Sources</button></div>`:'';
 const progress=active?sourceUpdateStageMarkup():null;
 const subline=progress?progress.inline:sourceResultSummary(p,d);
 const content=`<div class="sources-provider-main"><div class="sources-provider-icon" aria-hidden="true">${p.name[0].toUpperCase()}</div><div class="sources-provider-copy"><div class="sources-provider-name"><strong>${escapeHTML(p.name)}</strong><span class="sources-publisher">@${escapeHTML(p.publisher)}</span></div><div class="sources-version" ${active?'role="status" aria-live="polite"':''}>${subline}</div></div><div class="sources-provider-controls"><span class="sources-status ${st.kind}">${escapeHTML(st.label)}</span><span class="sources-action-slot">${primary}</span><button type="button" class="sources-detail-toggle" data-source-action="details" data-source-id="${p.id}" aria-expanded="${expanded}">${expanded?'Less':'Details'} ${icon('chevron',13)}</button></div></div>`;
 const details=expanded?`<div class="sources-provider-detail"><p>${escapeHTML(st.description)}</p><div class="sources-detail-meta"><span><strong>Publisher</strong> @${escapeHTML(p.publisher)}</span><span><strong>Requires</strong> StrawVerse ${escapeHTML(p.minApp)}+</span><span><strong>Repository</strong> Official</span></div>${recovery}${alternatives}<div class="sources-detail-actions"><a class="sources-link" href="${SOURCES_PREVIEW_REPO.url}" target="_blank" rel="noopener noreferrer">View repository ↗</a>${isInstalled?`<button type="button" class="sources-danger" data-source-action="remove" data-source-id="${p.id}" ${busy?'disabled':''}>Remove extension…</button>`:''}</div></div>`:'';
 return `<article class="sources-provider" data-source-entry="${p.id}">${content}${progress?progress.track:''}${details}</article>`;
}
function sourcesScenarioMarkup(){
 return `<details class="sources-scenario"><summary>Preview other source and update states</summary><p>Pick a source condition and the outcome of its next update. No files or provider websites are accessed.</p><div class="field"><label for="sources-scenario-provider">Provider</label><select id="sources-scenario-provider">${SOURCES_PREVIEW_CATALOG.map(p=>`<option value="${p.id}">${escapeHTML(p.name)}</option>`).join('')}</select></div><div class="field"><label for="sources-scenario-state">Current extension condition</label><select id="sources-scenario-state"><option value="healthy">Working</option><option value="offline">Provider temporarily unavailable</option><option value="broken">Old source no longer works</option><option value="incompatible">Extension cannot load</option></select></div><div class="field"><label for="sources-scenario-outcome">Next update result</label><select id="sources-scenario-outcome"><option value="working">New source works</option><option value="rejected">New extension fails validation</option><option value="unreachable">New extension loads, but provider is unavailable</option></select></div><button type="button" class="btn small" data-source-action="simulate" style="margin-top:12px">Apply scenario</button><p class="sources-scenario-footnote">A provider outage alone does not prove an old extension is broken. Only a previously working version is offered as a recovery option.</p></details>`;
}
function sourcesRepoMarkup(r,official){
 const hint=official?'Official repository · always configured':`${r.kind==='github'?'GitHub repository':'Direct marketplace manifest'} · Format checked only`;
 return `<div class="sources-repo" ${official?'id="settings-official-repository" tabindex="-1"':''} title="${escapeHTML(hint)}"><div class="sources-repo-icon" aria-hidden="true">${icon(official?'check':'globe',18)}</div><div class="sources-repo-copy"><strong title="${escapeHTML(r.name)}">${escapeHTML(r.name)}</strong><small title="${escapeHTML(r.url)}">${escapeHTML(r.url)}</small></div><div class="sources-repo-actions"><span class="sources-repo-status">${official?'Built in':'Not verified'}</span>${official?'':`<button type="button" class="sources-danger" data-source-action="remove-repo" data-repo-id="${escapeHTML(r.id)}" aria-label="Remove ${escapeHTML(r.name)} repository">Remove</button>`}</div></div>`;
}
function renderSourcesPreview(){
 const shell=settingsPage.querySelector('#sources-shell');if(!shell)return;
 for(const el of shell.querySelectorAll('[data-source-tab]')){
  const current=el.dataset.sourceTab===sourcesTab;
  el.setAttribute('aria-selected',String(current));el.tabIndex=current?0:-1;
 }
 const count=SOURCES_PREVIEW_CATALOG.filter(p=>!!sourceDemoState[p.id].installed).length;
 const number=shell.querySelector('#sources-installed-count');if(number)number.textContent=count;
 const region=shell.querySelector('#sources-dynamic-content');
 const feedback=shell.querySelector('#sources-status-message');if(feedback)feedback.textContent=sourcesFeedback;
 if(!region)return;
 if(sourcesTab==='marketplace'||sourcesTab==='installed'){
  const available=sourcesTab==='marketplace'?SOURCES_PREVIEW_CATALOG:SOURCES_PREVIEW_CATALOG.filter(p=>!!sourceDemoState[p.id].installed);
  region.innerHTML=`<div id="sources-${sourcesTab}-region" tabindex="-1"><div class="sources-section-top"><div><h3>${sourcesTab==='marketplace'?'Marketplace':'Installed sources'}</h3><p>${sourcesTab==='marketplace'?'Browse sources from the built-in StrawVerse repository.':'Extensions remain listed here even if they are unable to load.'}</p></div><button class="sources-preview-reset" type="button" data-source-action="reset">Reset demo</button></div>${available.length?`<div class="sources-provider-list">${available.map(sourcesProviderMarkup).join('')}</div>`:'<div class="sources-empty">No sources installed in this demonstration.<br><button type="button" class="btn small" data-source-action="browse-marketplace" style="margin-top:14px">Browse Marketplace</button></div>'}${sourcesCatalogueScenarioMarkup()}${sourcesTab==='installed'?sourcesScenarioMarkup():''}</div>`;
 }else{
  region.innerHTML=`<div id="settings-repositories-card" tabindex="-1"><div class="sources-section-top"><div><h3>Repositories</h3><p>The official repository is always configured. You can add or remove community repository entries.</p></div><button class="sources-preview-reset" type="button" data-source-action="reset">Reset demo</button></div><div class="sources-repo-list">${sourcesRepoMarkup(SOURCES_PREVIEW_REPO,true)}${sourceDemoRepos.map(r=>sourcesRepoMarkup(r,false)).join('')}</div><div class="sources-repo-add"><button type="button" class="btn small" data-source-action="add-repo">${icon('plus',16)} Add repository…</button></div><p class="settings-card-note">Links are checked for format and duplicates locally. This prototype does not fetch manifests or install sources. The desktop application will verify repository contents before listing extensions.</p></div>`;
 }
}
function setSourcesTab(next,resetScroll=true){
 if(!['marketplace','installed','repositories'].includes(next))return;
 sourcesTab=next;renderSourcesPreview();
 if(resetScroll)requestAnimationFrame(()=>{
  const el=settingsPage.querySelector('.sources-subnav');if(el)revealSettingsControl(el);
 });
}
function sourceOperationEnd(){sourceDemoBusy=null;sourceDemoBusyAction=null;sourceDemoPhase=-1;}
function beginPreviewUpdate(p,entry,action){
 const id=p.id;
 const previous={version:entry.installed,health:entry.health,working:entry.health==='healthy'};
 const result=entry.nextOutcome||'working';
 sourceDemoBusy=id;sourceDemoBusyAction=action;sourceDemoPhase=0;entry.notice=null;
 const token=++sourceDemoOpToken;
 sourcesFeedback=`Preview: ${action==='install'?'installing':'updating'} ${p.name}. No real files are touched.`;
 renderSourcesPreview();
 function advance(phase){
  if(token!==sourceDemoOpToken||sourceDemoBusy!==id)return;
  sourceDemoPhase=phase;
  sourcesFeedback=`${p.name}: ${SOURCE_UPDATE_PHASES[phase].toLowerCase()} (simulation).`;
  renderSourcesPreview();
  if(result==='rejected'&&phase===SOURCE_UPDATE_PHASES.indexOf('Validating extension')){
   setTimeout(()=>{
    if(token!==sourceDemoOpToken)return;
    sourceOperationEnd();
    entry.notice={kind:'error',text:`Update validation failed. ${previous.version?`v${previous.version} remains installed ${previous.working?'and working':'but was already unavailable'}.`:'No version was installed.'} Nothing was replaced.`};
    sourcesFeedback=`Preview: ${p.name} update rejected. Existing installation preserved.`;
    renderSourcesPreview();
   },850);return;
  }
  if(phase<SOURCE_UPDATE_PHASES.length-1){setTimeout(()=>advance(phase+1),850);return;}
  setTimeout(()=>{
   if(token!==sourceDemoOpToken)return;
   // Extension passed validation/activation. Provider reachability is a separate test.
   entry.installed=p.latest;
   if(previous.version&&previous.version!==p.latest){entry.backup={version:previous.version,usable:previous.working,health:previous.health};}
   if(result==='unreachable'){
    entry.health='offline';
    entry.notice={kind:'warning',text:`v${p.latest} activated, but the provider could not be reached. The new version stays installed; no automatic rollback was made.`};
    sourcesFeedback=`Preview: ${p.name} updated, but its provider is unavailable. Retry or select another source.`;
   }else{
    entry.health='healthy';
    entry.notice={kind:'success',text:`v${p.latest} activated and the provider check passed. ${entry.backup?.usable?'The previous working version is retained as a recovery copy.':''}`};
    sourcesFeedback=`Preview: ${p.name} v${p.latest} installed successfully. No files were downloaded.`;
   }
   sourceOperationEnd();renderSourcesPreview();refreshDiscoverFromSourcePreview();
  },900);
 }
 setTimeout(()=>advance(1),700);
}
function previewSourceAction(action,id){
 const p=SOURCES_PREVIEW_CATALOG.find(x=>x.id===id);if(!p)return;
 const entry=sourceDemoState[id];
 if(action==='details'){
  if(sourcesExpanded.has(id))sourcesExpanded.delete(id);else sourcesExpanded.add(id);
  renderSourcesPreview();
  settingsPage.querySelector(`[data-source-action="details"][data-source-id="${id}"]`)?.focus({preventScroll:true});
  return;
 }
 if(action==='other-sources'){
  sourcesFeedback=`Select another provider for the episode if needed. ${p.name} remains the preferred source until you change it.`;
  setSourcesTab('marketplace');return;
 }
 if(sourceDemoBusy)return;
 if(action==='remove'){
  modal('Remove source?',`<p class="description"><strong>${escapeHTML(p.name)}</strong> will be marked as removed in this interface preview. In the real app, removing a source will not delete your Library, watch history, or downloaded files.</p><p class="tip">No files on your Mac are changed here.</p>`,`<button class="btn" id="source-remove-cancel">Cancel</button><button class="btn primary" id="source-remove-confirm">Remove in preview</button>`);
  document.getElementById('source-remove-cancel').onclick=closeModal;
  document.getElementById('source-remove-confirm').onclick=()=>{
   entry.installed=null;entry.health='healthy';entry.backup=null;entry.notice=null;sourcesFeedback=`Preview: ${p.name} removed. Your anime library remains untouched.`;closeModal();
   if(sourcesTab==='installed'&&preferredSourcesTab()==='marketplace')sourcesTab='marketplace';
   renderSourcesPreview();refreshDiscoverFromSourcePreview();
  };
  return;
 }
 if(action==='restore'){
  const backup=entry.backup;
  if(!backup||!backup.usable)return;
  modal('Restore previous extension?',`<p class="description">Restore the last known working version of <b>${escapeHTML(p.name)}</b> (v${escapeHTML(backup.version)})? Gallery would check the recovery copy before activating it. It will not automatically replace the current version.</p><p class="tip">This is a simulated restoration.</p>`,`<button class="btn" id="source-restore-cancel">Cancel</button><button class="btn primary" id="source-restore-confirm">Restore in preview</button>`);
  document.getElementById('source-restore-cancel').onclick=closeModal;
  document.getElementById('source-restore-confirm').onclick=()=>{
   entry.installed=backup.version;entry.health=backup.health;entry.backup=null;
   entry.notice={kind:'success',text:`v${entry.installed} was restored in the preview. A real app would verify the recovery copy and recheck provider health.`};
   sourcesFeedback=`Preview: ${p.name} restored to v${entry.installed}.`;
   closeModal();renderSourcesPreview();refreshDiscoverFromSourcePreview();
  };
  return;
 }
 if(action==='retry'){
  if(!entry.installed)return;
  sourceDemoBusy=id;sourceDemoBusyAction='retry';sourceDemoPhase=SOURCE_UPDATE_PHASES.length-1;const token=++sourceDemoOpToken;
  entry.notice=null;sourcesFeedback=`Preview: checking ${p.name}'s provider again…`;renderSourcesPreview();
  setTimeout(()=>{
   if(token!==sourceDemoOpToken)return;
   sourceOperationEnd();
   if(entry.nextOutcome==='working'){
    entry.health='healthy';entry.notice={kind:'success',text:'The simulated provider recheck succeeded. The selected source was not changed.'};
    sourcesFeedback=`Preview: ${p.name} provider is available again.`;
   }else{
    entry.health='offline';entry.notice={kind:'warning',text:'The simulated provider recheck still failed. Keep the installed version and choose Retry or Other Sources.'};
    sourcesFeedback=`Preview: ${p.name} provider is still unavailable.`;
   }
   renderSourcesPreview();refreshDiscoverFromSourcePreview();
  },950);
  return;
 }
 if(!['install','update'].includes(action))return;
 beginPreviewUpdate(p,entry,action);
}
// Local-only URL shape checks; these do NOT establish that a remote repository exists
// or that an extension is trusted, compatible, or safe to install.
function parsePreviewRepoUrl(text){
 let url;
 try{url=new URL(text.trim());}catch(_){return {error:'Enter a complete HTTPS repository URL.'};}
 if(url.protocol!=='https:'||url.username||url.password){return {error:'Use an HTTPS URL without a username or password.'};}
 if(url.search||url.hash){return {error:'Remove query parameters and fragments from the URL.'};}
 const host=url.hostname.toLowerCase();
 if(!host||host==='localhost'||host.endsWith('.localhost')||host==='127.0.0.1'||host==='[::1]')return {error:'Use a public repository URL.'};
 const pieces=url.pathname.split('/').filter(Boolean);
 if(host==='github.com'){
  if(pieces.length!==2||!pieces.every(x=>/^[a-z0-9_.-]+$/i.test(x))){return {error:'Use a GitHub URL like https://github.com/owner/repository.'};}
  const owner=pieces[0],repo=pieces[1].replace(/\.git$/i,'');
  if(!repo)return {error:'Include the repository name in the GitHub URL.'};
  return {url:`https://github.com/${owner}/${repo}`,key:`github:${owner.toLowerCase()}/${repo.toLowerCase()}`,name:`${owner}/${repo}`,kind:'github'};
 }
 if(host==='raw.githubusercontent.com'){
  let path=pieces;
  if(path[2]==='refs'&&path[3]==='heads')path=[path[0],path[1],...path.slice(4)];
  if(path.length<4||path.at(-1).toLowerCase()!=='marketplace.json'||!path.slice(0,2).every(x=>/^[a-z0-9_.-]+$/i.test(x))){return {error:'Use a raw GitHub marketplace.json URL, including its branch.'};}
  const [owner,repo]=path;
  return {url:`https://raw.githubusercontent.com/${pieces.join('/')}`,key:`github:${owner.toLowerCase()}/${repo.toLowerCase()}`,name:`${owner}/${repo}`,kind:'manifest'};
 }
 if(pieces.at(-1)?.toLowerCase()!=='marketplace.json')return {error:'Use a GitHub repository URL or a direct marketplace.json URL.'};
 if(!host.includes('.'))return {error:'Enter a valid repository hostname.'};
 return {url:url.origin+url.pathname.replace(/\/$/,''),key:`manifest:${host}${url.pathname.replace(/\/$/,'')}`,name:`${host} / marketplace.json`,kind:'manifest'};
}
function sourceRepoIsDuplicate(parsed){
 const official=parsePreviewRepoUrl(SOURCES_PREVIEW_REPO.url);
 return parsed.key===official.key||sourceDemoRepos.some(r=>r.key===parsed.key);
}
function previewRepoInput(){
 modal('Add repository',`<p class="description">Add a StrawVerse-compatible repository to the <b>local preview</b>. No internet connection or extension download occurs.</p><div class="field"><label for="source-repo-url">GitHub repository or direct marketplace.json URL</label><input type="url" id="source-repo-url" placeholder="https://github.com/owner/extensions" autocomplete="off" spellcheck="false" aria-describedby="source-repo-validation"></div><p class="sources-repo-validation" id="source-repo-validation" aria-live="polite">Paste a repository link to check its URL format.</p>`,`<button class="btn" id="source-repo-cancel">Cancel</button><button class="btn primary" id="source-repo-add-preview" disabled>Add preview entry</button>`);
 const input=document.getElementById('source-repo-url');
 const hint=document.getElementById('source-repo-validation');
 const add=document.getElementById('source-repo-add-preview');
 document.getElementById('source-repo-cancel').onclick=closeModal;
 let candidate=null;
 function validate(){
  const value=input.value.trim();
  candidate=value?parsePreviewRepoUrl(value):null;
  if(candidate&&!candidate.error&&sourceRepoIsDuplicate(candidate))candidate={error:'This repository is already configured, possibly through a different URL format.'};
  const error=candidate?.error;
  const valid=!!candidate&&!error;
  add.disabled=!valid;
  input.setAttribute('aria-invalid',error?'true':'false');
  hint.className='sources-repo-validation'+(error?' is-error':valid?' is-valid':'');
  hint.textContent=error|| (valid?'URL format accepted. Repository contents are NOT verified.':'Paste a repository link to check its URL format.');
 }
 input.addEventListener('input',validate);
 input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!add.disabled){e.preventDefault();add.click();}});
 add.onclick=()=>{
  validate();if(!candidate||candidate.error)return;
  const id='preview-'+(sourceDemoRepos.length+1)+'-'+Date.now();
  sourceDemoRepos.push({id,...candidate});
  sourcesFeedback=`Added ${candidate.name} to the local preview. Its contents have not been fetched or verified.`;
  closeModal();renderSourcesPreview();
 };
 input.focus({preventScroll:true});
}
function previewRemoveRepo(id){
 const r=sourceDemoRepos.find(r=>r.id===id);if(!r)return;
 modal('Remove repository?',`<p class="description">Remove <strong>${escapeHTML(r.name)}</strong> from the Marketplace preview?</p><p class="tip">Installed extensions from this repository would remain on your Mac. They would stop receiving updates through this repository until it is added again. This prototype changes no files.</p>`,`<button class="btn" id="source-repo-keep">Keep repository</button><button class="btn" id="source-repo-remove">Remove repository</button>`);
 document.getElementById('source-repo-keep').onclick=closeModal;
 document.getElementById('source-repo-remove').onclick=()=>{
  sourceDemoRepos=sourceDemoRepos.filter(x=>x.id!==id);
  sourcesFeedback=`Removed ${r.name} from preview. Installed extension state is unchanged.`;
  closeModal();renderSourcesPreview();
 };
}
function attachSourcesPreview(){
 const shell=settingsPage.querySelector('#sources-shell');if(!shell)return;
 renderSourcesPreview();
 shell.addEventListener('click',event=>{
  const tab=event.target.closest('[data-source-tab]');if(tab){setSourcesTab(tab.dataset.sourceTab);return;}
  const action=event.target.closest('[data-source-action]');if(!action)return;
  const mode=action.dataset.sourceAction;
  if(mode==='reset'){resetSourcesPreview();return;}
  if(mode==='browse-marketplace'){setSourcesTab('marketplace');return;}
  if(mode==='simulate'){
   const id=shell.querySelector('#sources-scenario-provider').value;
   const health=shell.querySelector('#sources-scenario-state').value;
   const outcome=shell.querySelector('#sources-scenario-outcome').value;
   if(sourceDemoState[id]){
    sourceDemoState[id].health=health;sourceDemoState[id].nextOutcome=outcome;sourceDemoState[id].notice=null;
    sourcesFeedback=`Preview: ${id} is ${health}; next update will ${outcome==='working'?'succeed':outcome==='rejected'?'fail validation':'leave the provider unreachable'}.`;
    renderSourcesPreview();refreshDiscoverFromSourcePreview();
   }
   return;
  }
  if(['catalogue-none','catalogue-one','catalogue-both'].includes(mode)){applySourceCatalogueScenario(mode);return;}
  if(mode==='add-repo'){previewRepoInput();return;}
  if(mode==='remove-repo'){previewRemoveRepo(action.dataset.repoId);return;}
  previewSourceAction(mode,action.dataset.sourceId);
 });
 shell.addEventListener('keydown',event=>{
  const current=event.target.closest('[data-source-tab]');if(!current||!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();
  const keys=['installed','marketplace','repositories'];const i=keys.indexOf(current.dataset.sourceTab);
  const index=event.key==='Home'?0:event.key==='End'?2:(i+(event.key==='ArrowLeft'?-1:1)+3)%3;
  setSourcesTab(keys[index]);shell.querySelector(`[data-source-tab="${keys[index]}"]`)?.focus({preventScroll:true});
 });
}

/* v75 · About & Legal — quiet hierarchy, with Gallery v74 Settings visual language. */
function galleryBuildDisplay(){
 const brandVersion=(document.querySelector('.brand .subtitle')?.textContent||'').match(/v\d+(?:\.\d+)*/)?.[0]||'prototype';
 const revision=(document.title.match(/–\s*v(\d+)\s*·/)||[])[1]||'?';
 return {brandVersion,revision};
}
function aboutMarkup(){
 const build=galleryBuildDisplay();
 const link=(href,label)=>`<a href="${href}" target="_blank" rel="noopener noreferrer">${label}</a>`;
 const row=(id,ico,title,detail,context='')=>`<button class="about-menu-item" type="button" data-about-open="${id}">${icon(ico,19)}<span class="about-menu-copy"><strong>${title}</strong><small>${detail}</small></span>${context?`<span class="about-menu-context">${context}</span>`:''}${icon('chevron',17)}</button>`;
 const page=(id,title,description,html)=>`<section class="about-detail" data-about-view="${id}" aria-label="${title}" hidden><h3 class="about-detail-title" id="settings-about-${id}" tabindex="-1">${title}</h3><p class="about-detail-description">${description}</p>${html}</section>`;
 const miniNote='<p class="about-legal-note">Draft content for the proposed native Gallery application. These statements are design commitments, not a verified description of this HTML prototype or a final legal policy.</p>';
 return `<div class="about-shell" id="settings-about-root">
  <section class="about-overview" data-about-view="overview" aria-label="About Gallery">
   <div class="about-identity" id="settings-about-card" tabindex="-1">
    <div class="about-identity-primary">
     <span class="about-identity-logo" aria-hidden="true">${icon('clapper',34)}</span>
     <div class="about-identity-copy"><h3>Gallery</h3><p class="about-identity-description">Your anime library and player for macOS.</p><p class="about-identity-version">Interface prototype ${escapeHTML(build.revision)}</p></div>
    </div>
    <dl class="about-identity-facts" aria-label="Application details">
     <div class="about-identity-fact"><dt>Version</dt><dd>${escapeHTML(build.brandVersion)}</dd></div>
     <div class="about-identity-fact"><dt>Platform</dt><dd>macOS · Apple Silicon</dd></div>
     <div class="about-identity-fact"><dt>Based on</dt><dd>StrawVerse</dd></div>
    </dl>
   </div>
   <p class="about-group-label">PROJECT</p>
   <div class="about-menu" aria-label="Project details">
    ${row('credits','heart','Acknowledgements','Projects and contributors','StrawVerse · TheYogMehta')}
    ${row('licenses','info','Open Source Licenses','Software licenses and notices','GPL-3.0')}
   </div>
   <p class="about-group-label about-group-gap">LEGAL</p>
   <div class="about-menu" aria-label="Legal information">
    ${row('legal','globe','Legal &amp; Privacy','Terms, privacy and copyright information','Privacy-conscious by design')}
   </div>
   <p class="about-footnote">Gallery is an independent project based on ${link('https://github.com/TheYogMehta/StrawVerse','StrawVerse')} by TheYogMehta. Not an official StrawVerse release.</p>
  </section>
  ${page('credits','Acknowledgements','The people and open-source projects behind Gallery.',`
   <div class="about-detail-card">
    <h4>Built on StrawVerse</h4>
    <p>Gallery is being developed as an independent macOS application based on <strong>StrawVerse</strong>, created by <strong>TheYogMehta</strong>. Gallery is not an official StrawVerse release.</p>
    <div class="about-detail-links">${link('https://github.com/TheYogMehta/StrawVerse','StrawVerse on GitHub ↗')}${link('https://github.com/TheYogMehta/extensions','Official extensions ↗')}</div>
   </div>
   <div class="about-menu about-nested-menu" aria-label="Additional acknowledgements">
    ${row('components','play','Third-Party Components','Playback tools, extensions and dependencies')}
   </div>
   <p class="about-detail-footnote">Credits and licenses for dependencies actually bundled with the future native release will be generated from its build inventory and reviewed.</p>
  `)}
  ${page('licenses','Open Source Licenses','Software licenses and attribution notices.',`
   <div class="about-detail-card">
    <div class="about-detail-line"><span><strong>StrawVerse</strong><small>GNU General Public License, version 3 (GPL-3.0-only)</small></span>${link('https://github.com/TheYogMehta/StrawVerse/blob/main/LICENSE','Read GPL-3.0 ↗')}</div>
    <div class="about-detail-line"><span><strong>Gallery's future native release</strong><small>Applicable source, copyright notices and full license texts will accompany the distributed app, as required.</small></span></div>
    <div class="about-detail-line"><span><strong>Third-party dependencies</strong><small>License inventory will reflect the libraries and binaries actually shipped, not an assumed dependency list.</small></span></div>
   </div>
   <p class="about-detail-footnote">This standalone HTML prototype is not the finished macOS distribution. No generated native license inventory exists yet.</p>
  `)}
  ${page('components','Third-Party Components','Media and extension technologies under consideration.',`
   <div class="about-detail-card">
    <div class="about-detail-line"><span><strong>mpv</strong><small>Planned native video playback integration</small></span>${link('https://github.com/mpv-player/mpv','Project ↗')}</div>
    <div class="about-detail-line"><span><strong>FFmpeg</strong><small>Possible media processing dependency; shipped configuration and license must be verified</small></span>${link('https://ffmpeg.org/','Project ↗')}</div>
    <div class="about-detail-line"><span><strong>StrawVerse-compatible sources</strong><small>Individual extensions are provided by their respective maintainers.</small></span></div>
   </div>
   <p class="about-detail-footnote">These are plans, not a claim that any native media binary is included in this HTML prototype.</p>
  `)}
  ${page('legal','Legal &amp; Privacy','How Gallery is intended to work and what third parties can see.',`
   <div class="about-privacy-summary"><span class="about-privacy-symbol">${icon('info',21)}</span><div><h4>Privacy-conscious by design</h4><p>No developer analytics, telemetry or tracking is planned. External providers can still receive network requests and may collect information independently.</p></div></div>
   <div class="about-menu" aria-label="Legal documents">
    ${row('terms','info','Terms of Service','Use of Gallery, sources and responsibilities')}
    ${row('privacy','globe','Privacy Policy','Local data and third-party network requests')}
    ${row('copyright','film','Copyright &amp; Disclaimer','External content and copyright enquiries')}
   </div>
   <p class="about-detail-footnote">These are working drafts based on Gallery's intended behavior, not copied StrawVerse legal terms. They must be checked against the finished native implementation before release.</p>
  `)}
  ${page('terms','Terms of Service','Proposed terms for the future Gallery macOS application.',`
   ${miniNote}
   <article class="about-legal-document">
    <h4>1. Open-source software</h4><p>Gallery is being developed from the GPL-licensed StrawVerse project. Rights to copy, modify and distribute covered software are governed by the applicable open-source licenses, including GNU GPL v3.0; these terms do not replace those rights.</p>
    <h4>2. Application and external services</h4><p>Gallery is intended as a macOS client that retrieves information and content through user-selected third-party sources. Availability and operation of those external services are outside Gallery's control. Local downloads and application data may be stored on the user's Mac.</p>
    <h4>3. User responsibility</h4><p>Users are responsible for their choices of sources and for complying with applicable laws and the terms of external services.</p>
    <h4>4. Warranty</h4><p>GPL-covered software is provided subject to the disclaimer of warranty in its license, to the extent permitted by applicable law. Any additional terms for Gallery must be reviewed before public distribution.</p>
    <h4>5. Support</h4><p>Support and issue-reporting contact details for Gallery will be provided when the project is released. The StrawVerse community is independent from Gallery.</p>
   </article>
  `)}
  ${page('privacy','Privacy Policy','Proposed privacy commitments for the future Gallery app.',`
   ${miniNote}
   <div class="about-privacy-summary about-privacy-summary-compact"><span class="about-privacy-symbol">${icon('info',20)}</span><div><h4>No developer data collection</h4><p>Our goal is zero analytics, developer telemetry, tracking identifiers or automatic crash-report uploads.</p></div></div>
   <article class="about-legal-document">
    <h4>1. Data stored on your device</h4><p>Gallery is intended to store your library, watch progress, downloads and preferences on your Mac, rather than sending those records to Gallery's developers. Locally stored information remains under your control.</p>
    <h4>2. No developer analytics</h4><p>Gallery will not deliberately include developer usage analytics, advertising trackers or automatic diagnostic uploads. This commitment must be verified in the native release and its included dependencies.</p>
    <h4>3. Third-party connections</h4><p>To search for anime, retrieve metadata, play video, use source extensions or check for updates, Gallery may contact external websites and services directly. Those services can receive your IP address and information about requested content, and may independently log or analyze requests under their own policies.</p>
    <h4>4. Optional integrations</h4><p>If external accounts or synchronization are introduced later, they should be optional and clearly explain what data will be shared. Gallery does not require a developer-operated account by design.</p>
    <h4>5. Your choices</h4><p>Users will be able to manage local app data and their installed sources. Detailed storage, export and deletion instructions will be confirmed for the native release.</p>
   </article>
  `)}
  ${page('copyright','Copyright &amp; Disclaimer','Proposed statement about content and third-party providers.',`
   ${miniNote}
   <article class="about-legal-document">
    <h4>1. Independent client</h4><p>Gallery is intended as an independent macOS application that interacts with external content providers. It is not an official StrawVerse release and does not operate a developer-hosted library of third-party media.</p>
    <h4>2. Local retrieval and downloads</h4><p>Metadata requests, playback and user-initiated downloads may involve external sources and files stored on the user's device. Gallery therefore should not claim that no content is ever indexed, cached or downloaded.</p>
    <h4>3. Third-party rights</h4><p>Content and services accessible through sources belong to their respective owners and providers. Users should respect applicable copyright law and provider terms.</p>
    <h4>4. Copyright enquiries</h4><p>Requests relating to content hosted by third parties should normally be directed to the appropriate host or provider. Gallery-specific contact information and an appropriate handling process must be established before distribution; this disclaimer does not remove any applicable legal obligations.</p>
   </article>
  `)}
 </div>`;
}
let currentAboutView='overview';
const aboutViewParents={overview:null,credits:'overview',licenses:'overview',components:'credits',legal:'overview',terms:'legal',privacy:'legal',copyright:'legal'};
function updateSettingsBackButton(){
 const back=settingsPage.querySelector('#settings-back');
 if(!back)return;
 const inDetail=settingsLastSection==='about'&&currentAboutView!=='overview';
 const parent=inDetail?aboutViewParents[currentAboutView]:null;
 const dest=parent==='overview'?'About':parent==='legal'?'Legal & Privacy':parent==='credits'?'Acknowledgements':'Gallery';
 back.setAttribute('aria-label',inDetail?'Back to '+dest:'Back to Gallery');
 back.setAttribute('title',inDetail?'Back to '+dest:'Back to Gallery');
 const label=back.querySelector('span');
 if(label)label.textContent=inDetail?dest:'Back';
}
function settingsBackAction(){
 if(settingsLastSection==='about'&&currentAboutView!=='overview')setAboutView(aboutViewParents[currentAboutView]||'overview');
 else closeSettings();
}
function setAboutView(view,focusHeading=true){
 const root=settingsPage.querySelector('#settings-about-root');
 if(!root)return;
 const active=Object.hasOwn(aboutViewParents,view)?view:'overview';
 if(active===currentAboutView){updateSettingsBackButton();return;}
  const returning=aboutViewParents[currentAboutView]===active;
  root.dataset.aboutDirection=returning?'back':'forward';
  currentAboutView=active;
  updateSettingsBackButton();
  for(const section of root.querySelectorAll('[data-about-view]'))section.hidden=section.dataset.aboutView!==active;
 if(active==='overview'){
  if(focusHeading)root.querySelector('#settings-about-card')?.focus({preventScroll:true});
 }else if(focusHeading){
  root.querySelector(`[data-about-view="${active}"] .about-detail-title`)?.focus({preventScroll:true});
 }
 workspace.scrollTop=0;
 requestAnimationFrame(updateTabScrollOverlay);
}

function subtitleAppearanceMarkup(){
 const fontOptions=[['system','System (San Francisco)'],['atkinson','Atkinson Hyperlegible Next'],['inter','Inter']];
 const choices=(items,value)=>items.map(([id,title])=>`<option value="${id}" ${value===id?'selected':''}>${title}</option>`).join('');
 const styles=[['outline','Outline'],['shadow','Drop Shadow'],['box','Background Box'],['none','None']];
 const activePreset=({outline:'outlinePreset',shadow:'shadowPreset',box:'boxPreset'})[subtitlePrefs.effect];
 return `<section class="sf-subtitle-workbench" aria-label="Subtitle appearance and live preview">
   <div class="sf-subtitle-heading" id="settings-subtitle-appearance" tabindex="-1">
    <div class="sf-subtitle-preview-heading"><div><h3><span class="sf-subtitle-full-title">Subtitle preview</span><span class="sf-subtitle-compact-title">Subtitle appearance</span></h3>
     <p class="sf-subtitle-compact-description">Fine-tune your subtitles, then open the preview to inspect the results.</p>
    </div>${subtitleSceneToggle()}</div>
    <button type="button" class="sf-subtitle-reset" id="subtitle-reset">Reset to defaults</button>
   </div>
   <div class="sf-subtitle-compact-preview"><button type="button" class="sf-subtitle-compact-button" id="subtitle-compact-preview" aria-label="Preview subtitles">${icon('maximize',16)}Preview subtitles</button></div>
   <div class="sf-subtitle-main">
    <div class="sf-subtitle-video">
     <div class="sf-subtitle-stage subtitle-stage" id="subtitle-preview-stage" data-position="bottom" aria-label="Subtitle preview">
      <button type="button" class="sf-subtitle-expand" id="subtitle-expand-preview" aria-label="Expand subtitle preview" title="Expand preview">${icon('maximize',17)}</button>
      <img class="sf-day subtitle-stage-image subtitle-stage-day" alt="" draggable="false"><img class="sf-night subtitle-stage-image subtitle-stage-night" alt="" draggable="false">
      <div class="sf-subtitle-shade subtitle-stage-shade" aria-hidden="true"></div><div class="sf-subtitle-caption subtitle-preview-caption" id="subtitle-live-caption" aria-live="off"></div>
     </div>
    </div>
    <div class="sf-subtitle-controls" aria-label="Subtitle appearance controls">
     <div class="sf-subtitle-group" data-subtitle-group="font"><label class="sf-subtitle-label" for="subtitle-font">Font</label><select class="sf-subtitle-font" id="subtitle-font">${choices(fontOptions,subtitlePrefs.font)}</select></div>
     <div class="sf-subtitle-group" data-subtitle-group="size"><div class="sf-subtitle-size-heading"><span class="sf-subtitle-label" id="subtitle-size-label">Text size</span><span class="sf-subtitle-current" id="subtitle-size-current">${(SUBTITLE_SIZES.find(p=>p.id===subtitlePrefs.size)||SUBTITLE_SIZES[2]).label}</span></div>
      <div class="sf-subtitle-five" role="group" aria-labelledby="subtitle-size-label">${SUBTITLE_SIZES.map((preset,i)=>`<button type="button" class="sf-subtitle-choice" data-subtitle-size="${preset.id}" aria-label="${preset.label}" title="${preset.label}" aria-pressed="${subtitlePrefs.size===preset.id}">${['XS','S','N','L','XL'][i]}</button>`).join('')}</div></div>
     <div class="sf-subtitle-group" data-subtitle-group="text"><span class="sf-subtitle-label" id="subtitle-text-color-label">Text color</span>
      <div class="sf-subtitle-colors" role="group" aria-labelledby="subtitle-text-color-label">
       <button type="button" class="sf-subtitle-choice" data-subtitle-text-color="white" aria-label="Soft White" title="Soft White" aria-pressed="${subtitlePrefs.colorMode==='white'}"><span class="sf-subtitle-swatch subtitle-choice-swatch" style="background:#F8F8F8" aria-hidden="true"></span>White</button>
       <button type="button" class="sf-subtitle-choice" data-subtitle-text-color="yellow" aria-label="Yellow" title="Yellow" aria-pressed="${subtitlePrefs.colorMode==='yellow'}"><span class="sf-subtitle-swatch subtitle-choice-swatch" style="background:#FFE066" aria-hidden="true"></span>Yellow</button>
       <button type="button" class="sf-subtitle-choice" data-subtitle-text-color="custom" aria-label="Custom text color" aria-pressed="${subtitlePrefs.colorMode==='custom'}"><span class="sf-subtitle-custom-indicator" aria-hidden="true"><span id="subtitle-custom-palette" ${subtitlePrefs.customColorSet?'hidden':''}>${icon('palette',14)}</span><span class="sf-subtitle-swatch subtitle-choice-swatch" id="subtitle-custom-swatch" style="background:${subtitlePrefs.customColor}" ${subtitlePrefs.customColorSet?'':'hidden'}></span></span>Custom</button>
      </div></div>
     <div class="sf-subtitle-group" data-subtitle-group="style"><span class="sf-subtitle-label" id="subtitle-effect-label">Subtitle style</span>
      <div class="sf-subtitle-styles" role="group" aria-labelledby="subtitle-effect-label">${styles.map(([id,label])=>`<button type="button" class="sf-subtitle-choice" data-subtitle-effect="${id}" aria-pressed="${subtitlePrefs.effect===id}">${label}</button>`).join('')}</div></div>
     <div class="sf-subtitle-effects" id="subtitle-tuning-grid" data-subtitle-style="${subtitlePrefs.effect}">
      <div id="subtitle-strength-field"><div class="sf-subtitle-effect-heading"><span class="sf-subtitle-label" id="subtitle-effect-amount-label">Effect intensity</span>
       <span id="subtitle-effect-color-field"><button type="button" class="sf-subtitle-effect-color" id="subtitle-effect-color" aria-label="Edit outline color" title="Edit outline color" aria-haspopup="dialog"><span class="sf-subtitle-swatch subtitle-choice-swatch" id="subtitle-effect-color-swatch" style="background:${subtitlePrefs.outlineColor}" aria-hidden="true"></span>Color</button><output class="only-sr" id="subtitle-effect-color-value">${subtitlePrefs.outlineColor.toUpperCase()}</output></span></div>
       <div class="sf-subtitle-three" role="group" aria-labelledby="subtitle-effect-amount-label">${['light','normal','strong'].map((value,i)=>`<button type="button" class="sf-subtitle-choice" data-effect-strength="${value}" aria-pressed="${activePreset?subtitlePrefs[activePreset]===value:false}">${SUBTITLE_EFFECT_LABELS[i]}</button>`).join('')}</div>
      </div>
     </div>
    </div>
   </div>
   <span class="only-sr" id="subtitle-saved-status" role="status" aria-live="polite"></span>
  </section>`;
}
function setPlaybackTab(tab,resetScroll=true){
 cancelGalleryTextColorPopover(false);
 if(!['general','subtitles'].includes(tab))return;
 playbackTab=tab;
 for(const pane of settingsPage.querySelectorAll('[data-playback-pane]'))pane.hidden=pane.dataset.playbackPane!==tab;
 for(const button of settingsPage.querySelectorAll('[data-playback-tab]')){
  const current=button.dataset.playbackTab===tab;
  button.setAttribute('aria-selected',String(current));button.tabIndex=current?0:-1;
 }
 if(resetScroll){workspace.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});hideTabScrollOverlay();}
 if(tab==='subtitles')requestAnimationFrame(renderSubtitlePreview);
}
let subtitleResizeObserver=null;
function renderSubtitleStage(stage){
 const caption=stage?.querySelector('.subtitle-preview-caption');
 if(!stage||!caption)return;
 // Size relative to the displayed video area in logical CSS pixels.
 const displayedHeight=stage.getBoundingClientRect().height||720;
 const scale=displayedHeight/1080;
 caption.textContent=SUBTITLE_PREVIEW_TEXT;
 caption.style.fontFamily=SUBTITLE_FONTS[subtitlePrefs.font];
 caption.style.fontSize=(subtitleReferenceSize(subtitlePrefs.size)*scale).toFixed(2)+'px';
 caption.style.webkitTextStroke='0px transparent';
 caption.style.textShadow='none';
 caption.style.backgroundColor='transparent';
 caption.style.padding='0';
 caption.style.borderRadius='0';
 const style=subtitlePrefs.effect;
 if(style==='outline'){
  caption.style.webkitTextStroke=(subtitlePrefs.outline*scale).toFixed(2)+'px '+subtitlePrefs.outlineColor;
 }else if(style==='shadow'){
  const strength=subtitlePrefs.shadow*scale;
  caption.style.textShadow=strength>0?`${(strength*.48).toFixed(2)}px ${(strength*.68).toFixed(2)}px ${(strength*1.65).toFixed(2)}px ${subtitlePrefs.shadowColor}`:'none';
 }else if(style==='box'){
  const h=subtitlePrefs.boxColor.replace('#','');
  const r=parseInt(h.slice(0,2),16),g=parseInt(h.slice(2,4),16),b=parseInt(h.slice(4,6),16);
  caption.style.backgroundColor=`rgba(${r},${g},${b},${subtitlePrefs.boxOpacity/100})`;
  caption.style.padding='0.24em .55em';
  caption.style.borderRadius='0.25em';
 }
 caption.style.paintOrder='stroke fill';
 caption.style.color=subtitlePrefs.color;
}
// One manually selected scene is shared by both preview surfaces.
let subtitlePreviewScene='day';
function subtitleSceneToggle(){
 const option=(scene,label,symbol)=>`<button type="button" class="scene-${scene}" data-subtitle-scene="${scene}" aria-pressed="${subtitlePreviewScene===scene}">${icon(symbol,14)}${label}</button>`;
 return `<div class="sf-subtitle-scene-toggle" role="group" aria-label="Subtitle preview scene" data-active="${subtitlePreviewScene}">${option('day','Day','sun')}${option('night','Night','moon')}</div>`;
}
function subtitleStages(){
 return [settingsPage.querySelector('#subtitle-preview-stage'),modalHost.querySelector('#subtitle-expanded-stage')].filter(Boolean);
}
function applySubtitlePreviewScene(){
 const night=subtitlePreviewScene==='night';
 for(const stage of subtitleStages()){
  const layer=stage.querySelector('.subtitle-stage-night');
  if(layer)layer.style.opacity=night?'1':'0';
 }
 for(const root of [settingsPage,modalHost]){
  for(const toggle of root.querySelectorAll('.sf-subtitle-scene-toggle')){
   toggle.dataset.active=subtitlePreviewScene;
   for(const button of toggle.querySelectorAll('[data-subtitle-scene]'))
    button.setAttribute('aria-pressed',String(button.dataset.subtitleScene===subtitlePreviewScene));
  }
 }
}
function bindSubtitleSceneToggle(root){
 for(const button of root.querySelectorAll('[data-subtitle-scene]'))button.addEventListener('click',()=>{
  const next=button.dataset.subtitleScene;
  if(next===subtitlePreviewScene)return;
  subtitlePreviewScene=next;
  applySubtitlePreviewScene();
  button.focus({preventScroll:true});
 });
}
function updateSubtitlePreviewScaleControl(){
 const stage=modalHost.querySelector('#subtitle-expanded-stage');
 const viewport=modalHost.querySelector('#subtitle-expanded-viewport');
 const actual=modalHost.querySelector('#subtitle-actual-size');
 if(!stage||!viewport||!actual)return;
 const manual=viewport.classList.contains('is-actual-size');
 // Use layout dimensions, not transformed bounds during the dialog entrance.
 // 100% is the established 1280 × 720 logical CSS-pixel stage, independent of DPR.
 const alreadyFull=stage.offsetWidth===1280&&stage.offsetHeight===720;
 const hide=!manual&&alreadyFull;
 if(hide&&document.activeElement===actual)
  modalHost.querySelector('.sf-subtitle-scene-toggle [aria-pressed="true"]')?.focus({preventScroll:true});
 actual.hidden=hide;
 actual.setAttribute('aria-pressed',String(manual));
 actual.textContent=manual?'Fit':'100%';
 actual.setAttribute('aria-label',manual?'Fit to window':'View at 100%');
 actual.title=manual?'Fit the preview to the window':'View at 100% (1280 × 720 CSS pixels; scroll to inspect)';
}
function renderSubtitlePreview(){
 renderSubtitleStage(settingsPage.querySelector('#subtitle-preview-stage'));
 renderSubtitleStage(modalHost.querySelector('#subtitle-expanded-stage'));
 applySubtitlePreviewScene();
 updateSubtitlePreviewScaleControl();
}
function showExpandedSubtitlePreview(){
 // Reuse Gallery's established dialog lifecycle, focus trapping and Escape key.
 modal('Expanded subtitle preview',`<div class="subtitle-expanded-header-controls"><button type="button" class="btn small" id="subtitle-actual-size" aria-pressed="false" aria-label="View at 100%" title="View at 100% (1280 × 720 CSS pixels; scroll to inspect)">100%</button>${subtitleSceneToggle()}</div>
  <div class="subtitle-expanded-viewport" id="subtitle-expanded-viewport">
   <div class="subtitle-stage" id="subtitle-expanded-stage" data-position="bottom" aria-label="Expanded subtitle preview">
    <img class="subtitle-stage-image subtitle-stage-day" alt="" draggable="false"><img class="subtitle-stage-image subtitle-stage-night" alt="" draggable="false"><div class="subtitle-stage-shade" aria-hidden="true"></div><div class="subtitle-preview-caption" aria-live="off"></div>
   </div>
  </div>`);
 const dialog=modalHost.querySelector('.dialog');
 dialog.classList.add('subtitle-preview-dialog');
 const headerControls=dialog.querySelector('.subtitle-expanded-header-controls');
 dialog.querySelector('.dialog-head').insertBefore(headerControls,dialog.querySelector('#close-dialog'));
 bindSubtitleSceneToggle(dialog);
 const stage=dialog.querySelector('#subtitle-expanded-stage');
 stage.querySelector('.subtitle-stage-day').src=SHRINE_DAY_IMAGE;
 stage.querySelector('.subtitle-stage-night').src=SHRINE_NIGHT_IMAGE;
 const viewport=dialog.querySelector('#subtitle-expanded-viewport');
 const actual=dialog.querySelector('#subtitle-actual-size');
 actual.addEventListener('click',()=>{
  const enabled=viewport.classList.toggle('is-actual-size');
  viewport.scrollLeft=enabled?(viewport.scrollWidth-viewport.clientWidth)/2:0;
  if(!enabled)viewport.scrollTop=0;
  renderSubtitlePreview();
 });
 subtitleResizeObserver?.observe(stage);
 renderSubtitlePreview();
 (actual.hidden?dialog.querySelector('.sf-subtitle-scene-toggle [aria-pressed="true"]'):actual)?.focus({preventScroll:true});
 requestAnimationFrame(renderSubtitlePreview);
}
/* A12: Small, theme-aware color editor with live preview, explicit commit and
   cancel, pointer and keyboard access. Kept outside Gallery's clipped .app. */
let cancelGalleryTextColorPopover=()=>{};
function galleryHexToHSV(hex){
 const x=hex.replace('#','');const r=parseInt(x.slice(0,2),16)/255,g=parseInt(x.slice(2,4),16)/255,b=parseInt(x.slice(4,6),16)/255;
 const max=Math.max(r,g,b),min=Math.min(r,g,b),delta=max-min;
 let hue=0;
 if(delta){
  if(max===r)hue=((g-b)/delta)%6;
  else if(max===g)hue=(b-r)/delta+2;
  else hue=(r-g)/delta+4;
  hue=(hue*60+360)%360;
 }
 return {h:hue,s:max===0?0:delta/max*100,v:max*100};
}
function galleryHSVToHex(h,s,v){
 const sat=s/100,val=v/100,chroma=val*sat,x=chroma*(1-Math.abs(((h/60)%2)-1)),m=val-chroma;
 let rgb;
 if(h<60)rgb=[chroma,x,0];else if(h<120)rgb=[x,chroma,0];else if(h<180)rgb=[0,chroma,x];
 else if(h<240)rgb=[0,x,chroma];else if(h<300)rgb=[x,0,chroma];else rgb=[chroma,0,x];
 return '#'+rgb.map(n=>Math.round((n+m)*255).toString(16).padStart(2,'0')).join('');
}
function openGalleryColorPopover(trigger,mode='text'){
 // First close a stale editor, if any. The local snapshot below is authoritative.
 cancelGalleryTextColorPopover(false);
  const effectKey=mode==='effect'?({outline:'outlineColor',shadow:'shadowColor',box:'boxColor'}[subtitlePrefs.effect]):null;
  if(mode==='effect'&&!effectKey)return;
  const prior=mode==='text'?{colorMode:subtitlePrefs.colorMode,color:subtitlePrefs.color,
   customColor:subtitlePrefs.customColor,customColorSet:subtitlePrefs.customColorSet}
   :{[effectKey]:subtitlePrefs[effectKey]};
  let value=(mode==='effect'?subtitlePrefs[effectKey]:subtitlePrefs.customColor).toLowerCase();
 let hsv=galleryHexToHSV(value);
 if(hsv.s<0.01)hsv.h=278; // Purple starting hue for a previously white swatch.
 const popup=document.createElement('div');
 popup.className='gallery-color-popover';
  const heading=mode==='effect'?'Effect color':'Custom text color';
  popup.setAttribute('role','dialog');popup.setAttribute('aria-label',heading);
  popup.innerHTML=`<div class="gallery-color-heading"><span class="gallery-color-title">${heading}</span><button type="button" class="gallery-color-close" aria-label="Cancel color change" title="Cancel">×</button></div>
 <div class="gallery-color-area" tabindex="0" role="slider" aria-label="Color saturation and brightness" aria-valuemin="0" aria-valuemax="100" aria-valuenow="100" aria-valuetext="Color saturation and brightness"><span class="gallery-color-target" aria-hidden="true"></span></div>
 <input type="range" class="gallery-color-hue" min="0" max="359" step="1" aria-label="Hue" value="${hsv.h}">
 <div class="gallery-color-bottom"><div class="gallery-color-sample" aria-hidden="true"></div><input type="text" class="gallery-color-hex" aria-label="Hex color" spellcheck="false" autocapitalize="characters" autocomplete="off" maxlength="7" value="${value.toUpperCase()}"><button type="button" class="gallery-color-done">Done</button></div>`;
 document.body.appendChild(popup);
 // Only needed when a short window cannot accommodate the anchored editor.
 let backdrop=null;
 const area=popup.querySelector('.gallery-color-area'), hue=popup.querySelector('.gallery-color-hue'),hex=popup.querySelector('.gallery-color-hex');
 const done=popup.querySelector('.gallery-color-done'),sample=popup.querySelector('.gallery-color-sample');
 let closed=false;
const position=()=>{
  if(closed)return;
  if(!trigger.isConnected||!document.body.classList.contains('settings-view')){close(false,false);return;}
  const app=document.querySelector('.app');
  const workspace=document.getElementById('workspace');
  const panel=trigger.closest('.sf-subtitle-controls');
  const anchor=mode==='text'?panel?.querySelector('.sf-subtitle-colors'):trigger;
  if(!app||!workspace||!panel||!anchor){close(false,false);return;}
  const a=app.getBoundingClientRect(),p=panel.getBoundingClientRect(),c=anchor.getBoundingClientRect();
  const v=workspace.getBoundingClientRect();
  const margin=12,gap=2,panelInset=2;
  const visibleTop=Math.max(v.top+8,a.top+8,0);
  const visibleBottom=Math.min(v.bottom-8,a.bottom-8,innerHeight-8);
  const usableHeight=Math.max(0,visibleBottom-visibleTop);
  const compact=usableHeight<385;
  popup.classList.toggle('is-short-window',compact);
  popup.style.maxHeight='';popup.style.overflowY='';
  area.style.height='110px';
  if(compact){
   if(!backdrop){
    backdrop=document.createElement('div');backdrop.className='gallery-color-backdrop';
    backdrop.setAttribute('aria-hidden','true');document.body.appendChild(backdrop);
   }
   backdrop.style.left=Math.max(0,v.left)+'px';
   backdrop.style.top=Math.max(0,v.top)+'px';
   backdrop.style.width=Math.max(0,Math.min(innerWidth,v.right)-Math.max(0,v.left))+'px';
   backdrop.style.height=Math.max(0,Math.min(innerHeight,v.bottom)-Math.max(0,v.top))+'px';
   const settingsContent=document.querySelector('.settings-content');
   const r=settingsContent?.getBoundingClientRect()||v;
   const horizontalLeft=Math.max(8,v.left+12,r.left+8);
   const horizontalRight=Math.min(innerWidth-8,v.right-12,r.right-8);
   const width=Math.max(160,Math.min(258,horizontalRight-horizontalLeft));
   popup.style.width=width+'px';
   // Preserve a useful color area; the popup scrolls internally only when
   // there truly is not enough vertical space for all of its controls.
   area.style.height=Math.max(48,Math.min(110,usableHeight-153))+'px';
   popup.style.maxHeight=Math.max(90,usableHeight-10)+'px';
   popup.style.overflowY='auto';
   const height=Math.min(popup.offsetHeight,usableHeight-10);
   const center=(horizontalLeft+horizontalRight)/2;
   const left=Math.max(horizontalLeft,Math.min(center-width/2,horizontalRight-width));
   const top=visibleTop+Math.max(0,(usableHeight-height)/2);
   popup.style.left=Math.round(left)+'px';popup.style.top=Math.round(top)+'px';
   return;
  }
  if(backdrop){backdrop.remove();backdrop=null;}
  // Normal sizes retain A25's right-column anchored positioning; the header
  // is now a hard top boundary even if the settings page has been scrolled.
  const leftBound=Math.max(a.left+margin,p.left+10,v.left+8,0);
  const rightBound=Math.min(a.right-margin,p.right-10,v.right-8,innerWidth);
  const available=Math.max(0,rightBound-leftBound);
  popup.style.width=Math.max(0,Math.min(258,available))+'px';
  const w=popup.offsetWidth;
  const left=Math.max(leftBound,Math.min(c.right-w,rightBound-w));
  const viewTop=Math.max(visibleTop,p.top+panelInset);
  const viewBottom=Math.min(visibleBottom,p.bottom-panelInset);
  const fullHeight=popup.offsetHeight;
  let top;
  if(mode==='text'){
   const idealTop=c.bottom+gap;
   const availableBelowChoices=viewBottom-idealTop;
   if(availableBelowChoices<fullHeight){
    area.style.height=Math.max(70,110-(fullHeight-availableBelowChoices))+'px';
   }
   top=Math.max(viewTop,Math.min(idealTop,viewBottom-popup.offsetHeight));
  }else{
   const availableAbove=c.top-gap-viewTop;
   if(availableAbove<fullHeight){
    area.style.height=Math.max(70,110-(fullHeight-availableAbove))+'px';
   }
   top=Math.max(viewTop,Math.min(c.top-gap-popup.offsetHeight,viewBottom-popup.offsetHeight));
  }
  popup.style.left=Math.round(left)+'px';popup.style.top=Math.round(top)+'px';
 };
 const draw=(preview=true)=>{
  value=galleryHSVToHex(hsv.h,hsv.s,hsv.v);
  popup.style.setProperty('--gallery-hue',String(hsv.h));
  popup.style.setProperty('--gallery-sat',String(hsv.s));
  popup.style.setProperty('--gallery-val',String(hsv.v));
  const marker=popup.querySelector('.gallery-color-target');
  marker.style.left=hsv.s+'%';marker.style.top=(100-hsv.v)+'%';
  area.setAttribute('aria-valuenow',String(Math.round(hsv.s)));
  area.setAttribute('aria-valuetext',`${Math.round(hsv.s)} percent saturation, ${Math.round(hsv.v)} percent brightness`);
  if(document.activeElement!==hex)hex.value=value.toUpperCase();
  hue.value=String(hsv.h);sample.style.backgroundColor=value;
  hex.setAttribute('aria-invalid','false');done.disabled=false;
   if(preview){
    if(mode==='effect')subtitlePrefs[effectKey]=value;
    else {subtitlePrefs.colorMode='custom';subtitlePrefs.customColor=value;subtitlePrefs.color=value;}
    updateSubtitleControls();renderSubtitlePreview();
   }
 };
 function close(accept=false,restoreFocus=true){
  if(closed)return;closed=true;
   if(accept){
    if(mode==='effect')subtitlePrefs[effectKey]=value;
    else {subtitlePrefs.colorMode='custom';subtitlePrefs.customColor=value;
     subtitlePrefs.color=value;subtitlePrefs.customColorSet=true;}
    persistSubtitlePrefs();
   }else{Object.assign(subtitlePrefs,prior);}
  updateSubtitleControls();renderSubtitlePreview();
  document.removeEventListener('pointerdown',outside,true);
  document.removeEventListener('keydown',onKey,true);
  window.removeEventListener('resize',position);
  document.removeEventListener('scroll',position,true);
  popup.remove();if(backdrop){backdrop.remove();backdrop=null;}cancelGalleryTextColorPopover=()=>{};
  if(restoreFocus&&trigger.isConnected)trigger.focus({preventScroll:true});
 }
 cancelGalleryTextColorPopover=(focus=true)=>close(false,focus);
 const outside=e=>{if(!popup.contains(e.target)&&e.target!==trigger&&!trigger.contains(e.target))close(false,false);};
 const onKey=e=>{
  if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();close(false);return;}
  if(e.key==='Tab'){
   const nodes=[popup.querySelector('.gallery-color-close'),area,hue,hex,done];
   const index=nodes.indexOf(document.activeElement);
   if(e.shiftKey&&(index<=0)){e.preventDefault();nodes[nodes.length-1].focus();}
   else if(!e.shiftKey&&index===nodes.length-1){e.preventDefault();nodes[0].focus();}
  }
 };
 const setFromPointer=e=>{
  const r=area.getBoundingClientRect();
  hsv.s=Math.max(0,Math.min(100,(e.clientX-r.left)/r.width*100));
  hsv.v=100-Math.max(0,Math.min(100,(e.clientY-r.top)/r.height*100));
  draw();
 };
 area.addEventListener('pointerdown',e=>{if(e.button!==0)return;area.focus({preventScroll:true});area.setPointerCapture(e.pointerId);setFromPointer(e);});
 area.addEventListener('pointermove',e=>{if(e.buttons===1&&area.hasPointerCapture(e.pointerId))setFromPointer(e);});
 area.addEventListener('keydown',e=>{
  const step=e.shiftKey?10:2;
  if(e.key==='ArrowLeft')hsv.s=Math.max(0,hsv.s-step);
  else if(e.key==='ArrowRight')hsv.s=Math.min(100,hsv.s+step);
  else if(e.key==='ArrowUp')hsv.v=Math.min(100,hsv.v+step);
  else if(e.key==='ArrowDown')hsv.v=Math.max(0,hsv.v-step);
  else return;
  e.preventDefault();draw();
 });
 hue.addEventListener('input',()=>{hsv.h=Number(hue.value);draw();});
 hex.addEventListener('input',()=>{
  const candidate=hex.value.trim();const valid=/^#[0-9a-fA-F]{6}$/.test(candidate);
  hex.setAttribute('aria-invalid',String(!valid));done.disabled=!valid;
  if(valid){hsv=galleryHexToHSV(candidate);value=candidate.toLowerCase();
   // A grayscale hex color does not need to reset the previously chosen hue.
   if(hsv.s===0)hsv.h=Number(hue.value);
   draw();}
 });
 hex.addEventListener('blur',()=>{if(hex.getAttribute('aria-invalid')==='true'){hex.value=value.toUpperCase();hex.setAttribute('aria-invalid','false');done.disabled=false;}});
 hex.addEventListener('keydown',e=>{if(e.key==='Enter'&&!done.disabled){e.preventDefault();close(true);}});
 done.addEventListener('click',()=>close(true));
 popup.querySelector('.gallery-color-close').addEventListener('click',()=>close(false));
 document.addEventListener('pointerdown',outside,true);
 document.addEventListener('keydown',onKey,true);
 window.addEventListener('resize',position);
 document.addEventListener('scroll',position,true);
 draw(true);position();area.focus({preventScroll:true});
}

function setupSubtitlePreview(){
 const stage=settingsPage.querySelector('#subtitle-preview-stage');if(!stage)return;
 bindSubtitleSceneToggle(settingsPage);
 settingsPage.querySelector('#subtitle-expand-preview')?.addEventListener('click',showExpandedSubtitlePreview);
 settingsPage.querySelector('#subtitle-compact-preview')?.addEventListener('click',showExpandedSubtitlePreview);
 const d=stage.querySelector('.subtitle-stage-day'); const n=stage.querySelector('.subtitle-stage-night');
 d.src=SHRINE_DAY_IMAGE;n.src=SHRINE_NIGHT_IMAGE;
 const controls={font:'subtitle-font'};
 const bind=(key,id)=>{const el=settingsPage.querySelector('#'+id);el.addEventListener('input',()=>{
  subtitlePrefs[key]=el.value;
  persistSubtitlePrefs();updateSubtitleControls();renderSubtitlePreview();
 });};
  for(const [key,id] of Object.entries(controls))bind(key,id);
  for(const button of settingsPage.querySelectorAll('[data-subtitle-text-color]'))button.addEventListener('click',()=>{
   const mode=button.dataset.subtitleTextColor;
   if(!['white','yellow','custom'].includes(mode))return;
   if(mode==='custom'){
    // Unsaved or already selected = edit; saved and inactive = recall once.
    if(!subtitlePrefs.customColorSet||subtitlePrefs.colorMode==='custom'){
openGalleryColorPopover(button,'text');return;
    }
   }
   subtitlePrefs.colorMode=mode;
   subtitlePrefs.color=mode==='custom'?subtitlePrefs.customColor:SUBTITLE_TEXT_COLOR_PRESETS[mode];
   persistSubtitlePrefs();updateSubtitleControls();renderSubtitlePreview();
  });
 for(const button of settingsPage.querySelectorAll('[data-subtitle-size]'))button.addEventListener('click',()=>{
  subtitlePrefs.size=normalizeSubtitleSize(button.dataset.subtitleSize);
  subtitlePrefs.outline=subtitlePresetValue('outline',subtitlePrefs.outlinePreset,subtitlePrefs.size);
  persistSubtitlePrefs();updateSubtitleControls();renderSubtitlePreview();
 });
 for(const button of settingsPage.querySelectorAll('[data-subtitle-effect]'))button.addEventListener('click',()=>{
  subtitlePrefs.effect=button.dataset.subtitleEffect;
  persistSubtitlePrefs();updateSubtitleControls();renderSubtitlePreview();
 });
 for(const button of settingsPage.querySelectorAll('[data-effect-strength]'))button.addEventListener('click',()=>{
  const effect=subtitlePrefs.effect;
  const key={outline:'outline',shadow:'shadow',box:'boxOpacity'}[effect];
  const presetKey={outline:'outlinePreset',shadow:'shadowPreset',box:'boxPreset'}[effect];
  if(!key||!presetKey)return;
  subtitlePrefs[presetKey]=button.dataset.effectStrength;
  subtitlePrefs[key]=subtitlePresetValue(effect,subtitlePrefs[presetKey],subtitlePrefs.size);
  persistSubtitlePrefs();updateSubtitleControls();renderSubtitlePreview();
 });
 settingsPage.querySelector('#subtitle-effect-color').addEventListener('click',e=>{
  if(subtitlePrefs.effect==='none')return;
  openGalleryColorPopover(e.currentTarget,'effect');
 });
 settingsPage.querySelector('#subtitle-reset').addEventListener('click',()=>{
  subtitlePrefs={...SUBTITLE_DEFAULTS};persistSubtitlePrefs();updateSubtitleControls();renderSubtitlePreview();
  settingsPage.querySelector('#subtitle-saved-status').textContent='Subtitle preview settings reset to defaults.';
 });
 subtitleResizeObserver?.disconnect();
 if('ResizeObserver' in window){subtitleResizeObserver=new ResizeObserver(()=>renderSubtitlePreview());subtitleResizeObserver.observe(stage);}
 updateSubtitleControls();requestAnimationFrame(renderSubtitlePreview);
}
function updateSubtitleControls(){
 const fields={font:'subtitle-font'};
 for(const [key,id] of Object.entries(fields)){
  const el=settingsPage.querySelector('#'+id);
  if(el && el.value!==String(subtitlePrefs[key]))el.value=subtitlePrefs[key];
 }
 for(const button of settingsPage.querySelectorAll('[data-subtitle-size]'))
  button.setAttribute('aria-pressed',String(button.dataset.subtitleSize===subtitlePrefs.size));
 const currentSizeLabel=settingsPage.querySelector('#subtitle-size-current');
 if(currentSizeLabel)currentSizeLabel.textContent=(SUBTITLE_SIZES.find(p=>p.id===subtitlePrefs.size)||SUBTITLE_SIZES[2]).label;
 const selected=subtitlePrefs.effect;
 for(const button of settingsPage.querySelectorAll('[data-subtitle-effect]'))
  button.setAttribute('aria-pressed',String(button.dataset.subtitleEffect===selected));
 const noEffect=selected==='none';
 if(!noEffect)subtitleLastStyledEffect=selected;
 const effectForControls=noEffect?subtitleLastStyledEffect:selected;
 const grid=settingsPage.querySelector('#subtitle-tuning-grid');
 if(grid){
  grid.dataset.subtitleStyle=selected;
  grid.hidden=false;
  grid.classList.toggle('is-disabled',noEffect);
  grid.setAttribute('aria-disabled',String(noEffect));
 }
 const strengthField=settingsPage.querySelector('#subtitle-strength-field');
 const effectColorField=settingsPage.querySelector('#subtitle-effect-color-field');
 if(strengthField)strengthField.hidden=false;
 if(effectColorField)effectColorField.hidden=false;
 const sliderLabel=settingsPage.querySelector('#subtitle-effect-amount-label');
 const strengthKey={outline:'outlinePreset',shadow:'shadowPreset',box:'boxPreset'}[effectForControls];
 const strengthLabels=SUBTITLE_EFFECT_LABELS;
 if(sliderLabel)sliderLabel.textContent='Effect intensity';
 for(const [i,button] of Array.from(settingsPage.querySelectorAll('[data-effect-strength]')).entries()){
  const id=button.dataset.effectStrength;
  button.textContent=strengthLabels[i]||id;
  button.setAttribute('aria-pressed',String(Boolean(strengthKey)&&subtitlePrefs[strengthKey]===id));
  button.disabled=noEffect;
  button.title=noEffect?'Choose a subtitle style to adjust effect intensity':'Effect intensity · '+(strengthLabels[i]||id);
 }
  const colorButton=settingsPage.querySelector('#subtitle-effect-color');
 const colorOutput=settingsPage.querySelector('#subtitle-effect-color-value');
  const colorSwatch=settingsPage.querySelector('#subtitle-effect-color-swatch');
 const colorKey={outline:'outlineColor',shadow:'shadowColor',box:'boxColor'}[effectForControls];
 const colorName={outline:'Outline color',shadow:'Shadow color',box:'Background box color'}[effectForControls];
  if(colorButton && colorKey){
   colorButton.disabled=noEffect;
   colorButton.setAttribute('aria-label',noEffect?'Effect color unavailable when subtitle style is None':'Edit '+colorName.toLowerCase());
   colorButton.title=noEffect?'Choose a subtitle style to edit effect color':'Edit '+colorName.toLowerCase()+' · '+subtitlePrefs[colorKey].toUpperCase();
  }
  if(colorSwatch && colorKey)colorSwatch.style.backgroundColor=subtitlePrefs[colorKey];
 if(colorOutput && colorKey)colorOutput.textContent=subtitlePrefs[colorKey].toUpperCase();
  for(const button of settingsPage.querySelectorAll('[data-subtitle-text-color]'))
   button.setAttribute('aria-pressed',String(button.dataset.subtitleTextColor===subtitlePrefs.colorMode));
  const customButton=settingsPage.querySelector('[data-subtitle-text-color="custom"]');
  if(customButton){
   const action=!subtitlePrefs.customColorSet?'Choose a custom subtitle text color'
    :subtitlePrefs.colorMode==='custom'?'Edit custom subtitle text color'
    :'Use saved custom subtitle text color';
   customButton.setAttribute('aria-label',action);
   customButton.title=action+(subtitlePrefs.customColorSet?' · '+subtitlePrefs.customColor.toUpperCase():'');
  }
  const customInput=settingsPage.querySelector('#subtitle-custom-color');
  if(customInput && customInput.value!==subtitlePrefs.customColor)customInput.value=subtitlePrefs.customColor;
  const customOutput=settingsPage.querySelector('#subtitle-custom-color-value');
  if(customOutput)customOutput.textContent=subtitlePrefs.customColor.toUpperCase();
  const customSwatch=settingsPage.querySelector('#subtitle-custom-swatch');
  if(customSwatch){customSwatch.style.backgroundColor=subtitlePrefs.customColor;customSwatch.hidden=!subtitlePrefs.customColorSet;}
   const customPalette=settingsPage.querySelector('#subtitle-custom-palette');
   if(customPalette)customPalette.hidden=subtitlePrefs.customColorSet;
}

function settingsMarkup(){
 const fontTile=(id,label,name,desc)=>`<button type="button" class="settings-font-tile" data-font-choice="${id}" aria-pressed="${state.font===id}" aria-label="Use ${label} font"><span class="settings-font-top"><span><span class="settings-font-name">${label}</span><span class="settings-font-sub">${desc}</span></span><span class="settings-font-check">${icon('check',18)}</span></span><span class="settings-font-example">${fontPreviewMarkupTile()}</span></button>`;
 const themeTile=(id,title,bg,bg2,accent)=>`<button type="button" class="theme-tile settings-theme-tile sf-theme-tile" data-theme-button="${id}" aria-pressed="${state.theme===id}" aria-label="Use ${title} theme"><span class="sf-theme-art" aria-hidden="true" style="--tile-bg:${bg};--tile-bg2:${bg2};--tile-accent:${accent}"></span><span class="sf-theme-row"><b>${title}</b><span class="sf-theme-check" aria-hidden="true">${icon('check',16)}</span></span></button>`;
 const audio=(id,value,label)=>`<div class="field"><label for="${id}">${label}</label><select id="${id}"><option value="sub" ${value==='sub'?'selected':''}>Japanese (Sub)</option><option value="dub" ${value==='dub'?'selected':''}>English (Dub)</option></select></div>`;
 const panel=(key,title,description,body)=>`<section class="settings-panel" data-settings-panel="${key}" aria-label="${title}" ${key===settingsLastSection?'':'hidden'}><header class="settings-panel-head"><h2>${title}</h2><p class="description">${description}</p></header>${body}</section>`;
 return `<header class="settings-page-head"><h1 class="sf-optical-title">Settings</h1><button type="button" class="settings-back" id="settings-back" aria-label="Back to Gallery">${icon('back',18)}<span>Back</span></button></header>
 <div class="settings-layout"><nav class="settings-side" aria-label="Settings sections">${settingsSections.map(([key,label,ico])=>`<button type="button" class="settings-section-button ${settingsLastSection===key?'is-active':''}" data-settings-section="${key}" aria-current="${settingsLastSection===key?'page':'false'}">${icon(ico,19)}<span>${label}</span></button>`).join('')}</nav>
 <div class="settings-content"><section class="settings-search-results" id="settings-search-results" role="region" aria-label="Settings search results" hidden></section>${panel('appearance','Appearance','Choose how Gallery looks and feels.',`<div class="appearance-subnav" role="tablist" aria-label="Appearance categories"><button type="button" role="tab" id="appearance-theme-tab" aria-controls="appearance-theme-pane" data-appearance-tab="theme" aria-selected="${appearanceTab==='theme'}" tabindex="${appearanceTab==='theme'?'0':'-1'}">Theme</button><button type="button" role="tab" id="appearance-typography-tab" aria-controls="appearance-typography-pane" data-appearance-tab="typography" aria-selected="${appearanceTab==='typography'}" tabindex="${appearanceTab==='typography'?'0':'-1'}">Typography</button></div><div class="appearance-pane" id="appearance-theme-pane" data-appearance-pane="theme" role="tabpanel" aria-labelledby="appearance-theme-tab" ${appearanceTab==='theme'?'':'hidden'}><div class="settings-card" id="settings-theme-card" tabindex="-1"><div class="settings-card-title">Choose your theme</div><p class="settings-card-note">Six different personalities, one shared interface. Select any theme to apply it instantly.</p><div class="theme-list settings-theme-list sf-theme-grid">${themeTile('ocean','Ocean','#244a52','#152d39','#a0f1d6')}${themeTile('twilight','Twilight','#38345e','#20213b','#c8bcff')}${themeTile('ember','Ember','#573238','#341e26','#f0c0ab')}${themeTile('slate','Slate','#43505a','#29333b','#c7d2da')}${themeTile('glacier','Glacier','#5c7489','#222f3d','#f4fbff')}${themeTile('verdant','Verdant','#335542','#1d3127','#c3efd0')}</div></div></div>
 <div class="appearance-pane" id="appearance-typography-pane" data-appearance-pane="typography" role="tabpanel" aria-labelledby="appearance-typography-tab" ${appearanceTab==='typography'?'':'hidden'}><div class="settings-card" id="settings-font-card" tabindex="-1"><div class="settings-card-title">Typography</div><p class="settings-card-note">Choose the font you find most comfortable to read. The selection applies throughout Gallery. Choose what feels best to you.</p>
 <div class="settings-font-list" role="group" aria-label="Application font">
 ${fontTile('system','System','San Francisco','The familiar macOS default')}
 ${fontTile('atkinson','Atkinson Hyperlegible Next','Atkinson Hyperlegible Next','Distinctive letterforms')}
 ${fontTile('inter','Inter','Inter','Clean, modern typography')}
 </div>
 <p class="settings-font-missing" id="settings-font-missing" role="status" aria-live="polite" hidden></p>
 <p class="settings-font-notice">This standalone HTML uses locally installed fonts and makes no font-service requests. If a font is not installed, the system font is shown instead. A future native build can bundle the custom fonts locally, subject to their license notices. <a href="https://www.brailleinstitute.org/freefont/" target="_blank" rel="noopener noreferrer">Atkinson Hyperlegible Next</a> · <a href="https://rsms.me/inter/" target="_blank" rel="noopener noreferrer">Inter</a></p>
 </div></div>`)}
 ${panel('playback','Playback','Set playback preferences and customize subtitles.',`<div class="appearance-subnav playback-subnav" role="tablist" aria-label="Playback categories"><button type="button" role="tab" id="playback-general-tab" aria-controls="playback-general-pane" data-playback-tab="general" aria-selected="${playbackTab==='general'}" tabindex="${playbackTab==='general'?'0':'-1'}">General</button><button type="button" role="tab" id="playback-subtitles-tab" aria-controls="playback-subtitles-pane" data-playback-tab="subtitles" aria-selected="${playbackTab==='subtitles'}" tabindex="${playbackTab==='subtitles'?'0':'-1'}">Subtitles</button></div>
 <div class="playback-pane" id="playback-general-pane" data-playback-pane="general" role="tabpanel" aria-labelledby="playback-general-tab" ${playbackTab==='general'?'':'hidden'}><div class="settings-card"><div class="settings-card-title">Playback preferences</div>${audio('pref-playback',state.defaultPlayback,'Default playback audio')}<div class="field"><label for="pref-subs">Subtitles when playback starts</label><select id="pref-subs"><option value="on" ${state.defaultSubtitles?'selected':''}>On</option><option value="off" ${!state.defaultSubtitles?'selected':''}>Off</option></select></div><div class="field"><label for="pref-autoplay">Autoplay next episode</label><select id="pref-autoplay"><option value="on" ${state.autoplayNextEpisode?'selected':''}>On</option><option value="off" ${!state.autoplayNextEpisode?'selected':''}>Off</option></select></div><p class="settings-card-note">Autoplay can continue to the next episode within the same season, but never starts a new season or movie. Connected playback sources are still required to load another episode automatically.</p></div><div class="settings-card"><div class="settings-card-title">Player integration</div><div class="field"><label for="player-pref">Preferred player for local files</label><select id="player-pref"><option value="built-in" ${(state.playerPreference||'built-in')==='built-in'?'selected':''}>Built-in (recommended)</option><option value="vlc" ${state.playerPreference==='vlc'?'selected':''}>VLC (optional · external)</option></select></div><div class="player-volume-preferences" id="settings-starting-volume-card" tabindex="-1" ${state.playerPreference==='vlc'?'hidden':''}><div class="player-volume-preferences-title">Starting volume</div><p class="settings-card-note">Controls the built-in player’s starting volume. Switching episodes keeps your current level.</p>
 <div class="starting-volume-choices" role="radiogroup" aria-label="Starting volume preference">
 <label class="starting-volume-choice"><input type="radio" name="starting-volume-mode" value="gallery" ${galleryVolumePreferences.mode==='gallery'?'checked':''}><span class="starting-volume-choice-copy"><strong>Gallery default · 70%</strong><small>Start each new Gallery session at 70%.</small></span></label>
 <label class="starting-volume-choice"><input type="radio" name="starting-volume-mode" value="user" ${galleryVolumePreferences.mode==='user'?'checked':''}><span class="starting-volume-choice-copy"><strong>User default</strong><small>Choose your preferred volume and slider precision.</small></span></label>
 </div>
 <div class="starting-volume-fixed" id="starting-volume-fixed" ${galleryVolumePreferences.mode==='user'?'':'hidden'}>
  <div class="starting-volume-value-row"><label for="starting-volume-slider">Preferred volume</label><output id="starting-volume-output" for="starting-volume-slider">${galleryVolumePreferences.preferred}%</output></div>
  <div class="starting-volume-slider-wrap player-progress" id="starting-volume-slider-wrap" style="--volume-pct:${galleryTimelineFill(galleryVolumePreferences.preferred)}">
   <div class="player-progress-bar gallery-split-timeline" aria-hidden="true"><div class="player-watched"></div><div class="player-remaining"></div></div>
   <input type="range" id="starting-volume-slider" min="0" max="100" step="1" value="${galleryVolumePreferences.preferred}" aria-label="Preferred starting volume" aria-valuetext="${galleryVolumePreferences.preferred} percent" aria-describedby="starting-volume-instructions">
  </div>
  <div class="starting-volume-ticks" aria-hidden="true">${Array.from({length:21},(_,i)=>`<span class="starting-volume-tick ${i%5===0?'major':''}"></span>`).join('')}</div>
  <div class="starting-volume-tick-labels" aria-hidden="true"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>
  <div class="starting-volume-precision-row"><span id="starting-volume-instructions">Adjustment precision</span><div class="starting-volume-precision" role="group" aria-label="Slider precision"><button type="button" data-volume-precision="steps" aria-pressed="${galleryVolumePreferences.precision==='steps'}">5% steps</button><button type="button" data-volume-precision="fine" aria-pressed="${galleryVolumePreferences.precision==='fine'}">Fine (1%)</button></div></div>
 </div>
 <p class="settings-card-note">Starting volume applies when Gallery opens. Changes during playback carry between episodes, while muting never changes this preference.</p>
 </div><p class="settings-card-note player-vlc-volume-note" id="player-vlc-volume-note" ${state.playerPreference==='vlc'?'':'hidden'}>Volume is controlled in VLC, not Gallery.</p><p class="settings-card-note">External player subtitles, compatibility, and watch progress cannot be guaranteed. Gallery recommends the built-in player.</p><button type="button" class="btn small" id="locate-vlc">Locate VLC manually…</button><div class="tip" id="vlc-detection" aria-live="polite">VLC detection uses standard application locations and macOS Spotlight metadata — no full disk scan.</div></div></div>
 <div class="playback-pane" id="playback-subtitles-pane" data-playback-pane="subtitles" role="tabpanel" aria-labelledby="playback-subtitles-tab" ${playbackTab==='subtitles'?'':'hidden'}>${subtitleAppearanceMarkup()}</div>`)}
 ${panel('downloads','Downloads','Set preferences for new downloads.',`<div class="settings-card"><div class="settings-card-title">Download preferences</div>${audio('pref-download',state.defaultDownload,'Default download language')}<p class="settings-card-note">A title's available languages may differ from your preference.</p></div><div class="settings-card download-location-settings" id="settings-download-location" tabindex="-1"><div class="settings-card-title">Destination folder</div><p class="settings-card-note">Previously saved files keep their original recorded location.</p><label class="download-folder-choice"><input type="radio" name="download-destination" value="default" ${(state.downloadDestination||'default')==='default'?'checked':''}><span><b>Standard Downloads folder</b><small>Use your Mac's Downloads folder</small></span></label><label class="download-folder-choice"><input type="radio" name="download-destination" value="custom" ${state.downloadDestination==='custom'?'checked':''}><span><b>Custom destination</b><small>Folder picker will be available in the macOS implementation</small></span></label><div class="download-folder-placeholder" id="download-folder-placeholder" ${state.downloadDestination==='custom'?'':'hidden'}>${icon('folder',16)} Folder selection is not available in this HTML prototype.</div><p class="tip">This browser prototype does not access files or folders. Download destination selection is a design preview, not a saved system location.</p></div>`)}
 ${panel('sources','Sources','Browse and manage StrawVerse-compatible extensions.',`<div class="sources-shell" id="sources-shell" tabindex="-1"><div class="sources-demo-banner">${icon('info',17)}<span><b>Interactive interface preview.</b> Providers, versions, installation states, and repositories below are sample data. Install, update, and repository controls are simulated; they do not change your Mac or fetch extensions.</span></div><div class="sources-subnav" role="tablist" aria-label="Source management"><button type="button" role="tab" data-source-tab="installed" aria-selected="true">Installed <span class="sources-count" id="sources-installed-count">2</span></button><button type="button" role="tab" data-source-tab="marketplace" aria-selected="false">Marketplace</button><button type="button" role="tab" data-source-tab="repositories" aria-selected="false">Repositories</button></div><div id="sources-status-message" class="sources-feedback" role="status" aria-live="polite"></div><div id="sources-dynamic-content"></div></div>`)}
 ${panel('about','About','Application information, acknowledgements and legal details.', aboutMarkup())}
 </div></div>`;
}
/* v59 — Search settings across sections without changing their preferences.
   This index mirrors real v59 controls. Unimplemented Sources features remain previews. */
const settingsSearchIndex=[
 {key:'theme',section:'appearance',title:'Theme',path:'Appearance → Theme',target:'settings-theme-card',terms:'appearance color colour style light dark display theme look interface personalize customise neon reel midnight cinema paper lantern'},
 {key:'font',section:'appearance',title:'Typography',path:'Appearance → Typography',target:'settings-font-card',terms:'font fonts typeface typography atkinson hyperlegible next braille institute dyslexia reading readability low vision accessible accessibility inter san francisco system text characters letters alphabet language locale numbers special symbols preview'},
 {key:'subtitle-appearance',section:'playback',playbackTab:'subtitles',title:'Subtitle appearance',path:'Playback → Subtitles',target:'settings-subtitle-appearance',terms:'subtitles captions outline thickness drop shadow shadow strength font size effects customize appearance preview live position border text colour color white soft white yellow custom background box opacity none night day shrine video accessibility'},
 {key:'audio',section:'playback',title:'Default playback audio',path:'Playback → Playback preferences',target:'pref-playback',terms:'language sound voice dialogue dub sub japanese english audio playback preferred'},
 {key:'subtitles',section:'playback',title:'Subtitles when playback starts',path:'Playback → Playback preferences',target:'pref-subs',terms:'subtitle subtitles captions cc closed caption language text on off playback accessibility'},
  {key:'starting-volume',section:'playback',playbackTab:'general',title:'Starting volume',path:'Playback → General → Player integration',target:'settings-starting-volume-card',terms:'volume audio sound loudness starting user gallery preferred default fine slider percent steps playback mute level'},
 {key:'player',section:'playback',title:'Preferred player for local files',path:'Playback → Player integration',target:'player-pref',terms:'vlc mpv built-in player playback video external default local files'},
 {key:'vlc',section:'playback',title:'Locate VLC manually',path:'Playback → Player integration',target:'locate-vlc',terms:'vlc external media player find locate choose app macos'},
 {key:'download-language',section:'downloads',title:'Default download language',path:'Downloads → Download preferences',target:'pref-download',terms:'download language audio dub sub english japanese preferred'},
 {key:'destination',section:'downloads',title:'Destination folder',path:'Downloads → Destination folder',target:'settings-download-location',terms:'download location path save files folder directory standard downloads custom storage drive disk destination'},
 {key:'marketplace',section:'sources',sourceTab:'marketplace',title:'Sources Marketplace',path:'Sources → Marketplace',target:'sources-marketplace-region',terms:'source sources scraper extension extensions addon provider plugin install update marketplace discover anime'},
 {key:'installed',section:'sources',sourceTab:'installed',title:'Installed sources',path:'Sources → Installed',target:'sources-installed-region',terms:'installed sources extensions providers health blocked incompatible update unavailable manage remove'},
 {key:'repositories',section:'sources',sourceTab:'repositories',title:'Repositories',path:'Sources → Repositories',target:'settings-repositories-card',terms:'source sources extension repository repo github community add manage providers'},
 {key:'official-repository',section:'sources',sourceTab:'repositories',title:'Official StrawVerse repository',path:'Sources → Repositories',target:'settings-official-repository',terms:'strawverse repository repo official default built-in extensions'},
 {key:'about',section:'about',title:'About Gallery',path:'About → Application information',target:'settings-about-card',terms:'about app application gallery version build apple silicon mac os information prototype'},
 {key:'strawverse-credits',section:'about',aboutView:'credits',title:'Acknowledgements',path:'About → Acknowledgements',target:'settings-about-credits',terms:'strawverse original author creator theyogmehta open source fork upstream github repository credits attribution'},
 {key:'license-credits',section:'about',aboutView:'licenses',title:'Open Source Licenses',path:'About → Open Source Licenses',target:'settings-about-licenses',terms:'license licensing gpl version 3 software copyright acknowledgements third party dependencies generated'},
 {key:'media-credits',section:'about',aboutView:'components',title:'Third-Party Components',path:'About → Acknowledgements → Third-Party Components',target:'settings-about-components',terms:'mpv ffmpeg media player video libraries components open source author licenses extension publishers'},
 {key:'legal',section:'about',aboutView:'legal',title:'Legal & Privacy',path:'About → Legal & Privacy',target:'settings-about-legal',terms:'legal privacy policy terms of service copyright disclaimer independent providers'},
 {key:'terms',section:'about',aboutView:'terms',title:'Terms of Service',path:'About → Legal & Privacy → Terms of Service',target:'settings-about-terms',terms:'terms conditions warranty software license user responsibility support open-source external services'},
 {key:'privacy',section:'about',aboutView:'privacy',title:'Privacy Policy',path:'About → Legal & Privacy → Privacy Policy',target:'settings-about-privacy',terms:'privacy personal data zero collection telemetry local storage tracking analytics user history external providers networks ip addresses no tracking'},
 {key:'copyright',section:'about',aboutView:'copyright',title:'Copyright & Disclaimer',path:'About → Legal & Privacy → Copyright & Disclaimer',target:'settings-about-copyright',terms:'copyright dmca disclaimer legal media sources downloads hosting third party content intellectual property'}
];
function setAppearanceTab(tab,resetScroll=true){
 if(!['theme','typography'].includes(tab))return;
 appearanceTab=tab;
 for(const pane of settingsPage.querySelectorAll('[data-appearance-pane]'))pane.hidden=pane.dataset.appearancePane!==tab;
 for(const button of settingsPage.querySelectorAll('[data-appearance-tab]')){
  const current=button.dataset.appearanceTab===tab;
  button.setAttribute('aria-selected',String(current));button.tabIndex=current?0:-1;
 }
 if(resetScroll){workspace.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});hideTabScrollOverlay();}
}
function matchedSettingsResults(query){
 const words=query.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').trim().split(/\s+/).filter(Boolean);
 if(!words.length)return [];
 return settingsSearchIndex.filter(item=>{
  if(item.key==='starting-volume'&&state.playerPreference==='vlc')return false;
  const text=(item.title+' '+item.path+' '+item.terms).toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'');
  return words.every(word=>text.includes(word));
 });
}
function renderSettingsSearchResults(){
 const container=settingsPage.querySelector('#settings-search-results');
 if(!container)return;
 const searching=searchOpen&&document.body.classList.contains('settings-view');
 settingsPage.classList.toggle('is-searching',searching);
 for(const button of settingsPage.querySelectorAll('[data-settings-section]'))button.setAttribute('aria-current',!searching&&button.dataset.settingsSection===settingsLastSection?'page':'false');
 if(!searching){
  container.hidden=true;
  for(const panel of settingsPage.querySelectorAll('[data-settings-panel]'))panel.hidden=panel.dataset.settingsPanel!==settingsLastSection;
  return;
 }
 for(const panel of settingsPage.querySelectorAll('[data-settings-panel]'))panel.hidden=true;
 container.hidden=false;
 const query=searchInput.value.trim();
 const matches=matchedSettingsResults(query);
 if(!query){
  container.innerHTML=`<header class="settings-panel-head"><h2>Search settings</h2><p class="description">Find a preference from any Settings section.</p></header><div class="settings-search-placeholder">${icon('search',22)}<div><b>What would you like to change?</b><p>Try “language”, “subtitles”, “theme”, or “sources”.</p></div></div>`;
  return;
 }
 let html=`<header class="settings-panel-head"><h2>Search results</h2><p class="description" aria-live="polite">${matches.length} ${matches.length===1?'setting':'settings'} found for “${escapeHTML(query)}”</p></header>`;
 if(!matches.length)html+=`<div class="settings-search-placeholder settings-search-no-results">${icon('search',22)}<div><b>No matching settings</b><p>Try a different term or browse the sections on the left.</p></div></div>`;
 else for(const [key,label] of settingsSections){
  const items=matches.filter(item=>item.section===key);
  if(!items.length)continue;
  html+=`<section class="settings-result-group" aria-label="${escapeHTML(label)}"><h3>${escapeHTML(label)}</h3><div class="settings-result-stack">${items.map(item=>`<button class="settings-result-item" type="button" data-settings-search-key="${item.key}" aria-label="Open ${escapeHTML(item.title)} in ${escapeHTML(label)}"><span class="settings-result-text"><strong>${escapeHTML(item.title)}</strong><small>${escapeHTML(item.path)}</small></span>${icon('chevron',18)}</button>`).join('')}</div></section>`;
 }
 container.innerHTML=html;
 for(const button of container.querySelectorAll('[data-settings-search-key]'))button.addEventListener('click',()=>navigateToSettingsResult(button.dataset.settingsSearchKey));
}
let settingsJumpTimer=null;
function navigateToSettingsResult(key){
 const item=settingsSearchIndex.find(x=>x.key===key);
 if(!item)return;
 closeInlineSearch(false);
 setSettingsSection(item.section,false);
 if(item.section==='appearance')setAppearanceTab(item.key==='font'?'typography':'theme',false);
 if(item.section==='playback')setPlaybackTab(item.playbackTab||'general',false);
 if(item.section==='sources'&&item.sourceTab)setSourcesTab(item.sourceTab,false);
 if(item.section==='about')setAboutView(item.aboutView||'overview',false);
 const el=document.getElementById(item.target);
 if(!el)return;
 el.focus({preventScroll:true});
 el.classList.remove('settings-search-target');
 void el.offsetWidth;
 el.classList.add('settings-search-target');
 clearTimeout(settingsJumpTimer);
 settingsJumpTimer=setTimeout(()=>el.classList.remove('settings-search-target'),2200);
 // Content is already mounted: move only the Settings scroll container.
 requestAnimationFrame(()=>revealSettingsControl(el));
}
function settingsResultButtons(){return [...settingsPage.querySelectorAll('.settings-result-item')];}

function setSettingsSection(key,resetScroll=true){
 cancelGalleryTextColorPopover(false);
 if(!settingsSections.some(item=>item[0]===key))return;
 if(searchOpen)closeInlineSearch(false);
 if(key==='about')setAboutView('overview',false);
 if(key==='appearance'&&settingsLastSection!=='appearance')setAppearanceTab('theme',false);
 if(key==='playback'&&settingsLastSection!=='playback')setPlaybackTab('general',false);
 // Pick the landing tab when navigating into Sources, not on every render.
 // A user's explicit tab choice remains in effect while they stay in Sources.
 if(key==='sources'&&settingsLastSection!=='sources'){
  sourcesTab=preferredSourcesTab();
  renderSourcesPreview();
 }
 settingsLastSection=key;
 updateSettingsBackButton();
 for(const button of settingsPage.querySelectorAll('[data-settings-section]')){
  const active=button.dataset.settingsSection===key;
  button.classList.toggle('is-active',active);
  button.setAttribute('aria-current',active?'page':'false');
 }
 for(const panel of settingsPage.querySelectorAll('[data-settings-panel]'))panel.hidden=panel.dataset.settingsPanel!==key;
 if(resetScroll)workspace.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
 hideTabScrollOverlay();
}
let gallerySettingsOpening=false;
function showSettings(afterOpen=null){
 if(document.body.classList.contains('settings-view')||settingsClosing||gallerySettingsOpening||modalHost.firstChild)return;
 gallerySettingsOpening=true;
 transitionGalleryStage(()=>{
  try{
   galleryOpenSettingsNow();
   if(typeof afterOpen==='function'&&document.body.classList.contains('settings-view'))afterOpen();
  }finally{gallerySettingsOpening=false;}
 });
}
function galleryOpenSettingsNow(){
 if(document.body.classList.contains('settings-view')||settingsClosing)return;
 // Preserve Watch History DOM, filters and scroll while Settings is open.
 if(modalHost.firstChild)return;
 // Each new visit starts at Appearance; contextual deep links can select a
 // different section immediately after showSettings().
 settingsLastSection='appearance';
 appearanceTab='theme';
 playbackTab='general';
 currentAboutView='overview';
 clearTimeout(settingsReturnAnimationTimer);
 document.body.classList.remove('returning-to-gallery');
 workspace.classList.remove('returning-to-gallery');
 // A lingering entrance animation on a secondary page can restart when that
 // page becomes visible again. Clear it before Settings hides the surface.
 screen.classList.remove('surface-enter');
 closeInlineSearch(false);
 settingsReturnScroll=workspace.scrollTop;
 hideTabScrollOverlay();
 sourcesTab=preferredSourcesTab();
 settingsPage.innerHTML=settingsMarkup();
 settingsPage.hidden=false;
 document.body.classList.add('settings-view');
 workspace.classList.add('settings-mode');
 // The hidden main content is never destroyed, and cannot receive keyboard focus.
 tabPagesViewport.inert=true;
 screen.inert=true;
 document.querySelector('.tabs').inert=true;
 workspace.scrollTop=0;
 const settingsButton=document.getElementById('settings');
 configureHeaderSearchContext();
 settingsButton.setAttribute('aria-label','Close settings');
 settingsButton.setAttribute('title','Close settings');
 settingsButton.setAttribute('aria-expanded','true');
 settingsButton.setAttribute('aria-controls','settings-page');
 for(const button of settingsPage.querySelectorAll('[data-settings-section]'))button.addEventListener('click',()=>setSettingsSection(button.dataset.settingsSection));
 for(const button of settingsPage.querySelectorAll('[data-appearance-tab]'))button.addEventListener('click',()=>setAppearanceTab(button.dataset.appearanceTab));
 for(const button of settingsPage.querySelectorAll('[data-playback-tab]'))button.addEventListener('click',()=>setPlaybackTab(button.dataset.playbackTab));
 settingsPage.querySelector('.playback-subnav')?.addEventListener('keydown',event=>{
  const button=event.target.closest('[data-playback-tab]');
  if(!button||!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();
  const tab=event.key==='Home'?'general':event.key==='End'?'subtitles':button.dataset.playbackTab==='general'?'subtitles':'general';
  setPlaybackTab(tab);settingsPage.querySelector('[data-playback-tab="'+tab+'"]')?.focus({preventScroll:true});
 });
 settingsPage.querySelector('.appearance-subnav')?.addEventListener('keydown',event=>{
  const button=event.target.closest('[data-appearance-tab]');
  if(!button||!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();
  const tab=event.key==='Home'?'theme':event.key==='End'?'typography':button.dataset.appearanceTab==='theme'?'typography':'theme';
  setAppearanceTab(tab);settingsPage.querySelector('[data-appearance-tab="'+tab+'"]')?.focus({preventScroll:true});
 });
 document.getElementById('settings-back').addEventListener('click',settingsBackAction);
 settingsPage.querySelector('#settings-about-root')?.addEventListener('click',event=>{
  const forward=event.target.closest('[data-about-open]');
  if(forward){setAboutView(forward.dataset.aboutOpen);return;}
 });
 attachSourcesPreview();
 for(const tile of settingsPage.querySelectorAll('[data-theme-button]'))tile.addEventListener('click',()=>{
  const next=tile.dataset.themeButton;
  if(next===state.theme)return;
  state.theme=next;
  document.body.dataset.theme=next;
  try{localStorage.setItem('gallery.softFuturistic.theme',next);}catch{}
  for(const option of settingsPage.querySelectorAll('[data-theme-button]'))option.setAttribute('aria-pressed',String(option.dataset.themeButton===next));
  saveDesktopPreferences();
 });
 for(const tile of settingsPage.querySelectorAll('[data-font-choice]'))tile.addEventListener('click',()=>setGalleryFont(tile.dataset.fontChoice));
 updateGalleryFontNotice();
 setupSubtitlePreview();
 for(const [id,field] of [['pref-playback' ,'defaultPlayback'],['pref-download','defaultDownload'],['player-pref','playerPreference']]){
  settingsPage.querySelector('#'+id).addEventListener('change',event=>{state[field]=event.target.value;if(field==='defaultPlayback')state.detailAudio=null;if(field==='playerPreference'){const volume=settingsPage.querySelector('#settings-starting-volume-card'),vlcNote=settingsPage.querySelector('#player-vlc-volume-note');if(volume)volume.hidden=state.playerPreference==='vlc';if(vlcNote)vlcNote.hidden=state.playerPreference!=='vlc';}saveDesktopPreferences();});
 }
 settingsPage.querySelector('#pref-subs').addEventListener('change',event=>{state.defaultSubtitles=event.target.value==='on';saveDesktopPreferences();});
  settingsPage.querySelector('#pref-autoplay').addEventListener('change',event=>{state.autoplayNextEpisode=event.target.value==='on';try{localStorage.setItem('gallery.autoplayNextEpisode',state.autoplayNextEpisode?'on':'off');}catch{}});
 for(const radio of settingsPage.querySelectorAll('input[name="starting-volume-mode"]')){
  radio.addEventListener('change',event=>{
   if(!event.target.checked)return;
   galleryVolumePreferences.mode=event.target.value==='user'?'user':'gallery';
   settingsPage.querySelector('#starting-volume-fixed').hidden=galleryVolumePreferences.mode!=='user';
   saveGalleryVolumePreferences();
  });
 }
 const preferredVolumeSlider=settingsPage.querySelector('#starting-volume-slider');
 const volumeSliderWrap=settingsPage.querySelector('#starting-volume-slider-wrap');
 const volumeOutput=settingsPage.querySelector('#starting-volume-output');
 function syncStartingVolumeSlider(){
  const amount=galleryVolumePreferences.preferred;
  preferredVolumeSlider.value=String(amount);
  preferredVolumeSlider.setAttribute('aria-valuetext',amount+' percent');
  volumeOutput.textContent=amount+'%';
  volumeSliderWrap.style.setProperty('--volume-pct',galleryTimelineFill(amount));
  for(const option of settingsPage.querySelectorAll('[data-volume-precision]'))option.setAttribute('aria-pressed',String(option.dataset.volumePrecision===galleryVolumePreferences.precision));
 }
 preferredVolumeSlider.addEventListener('input',()=>{
  let next=galleryVolumePercent(preferredVolumeSlider.value);
  if(galleryVolumePreferences.precision==='steps')next=Math.round(next/5)*5;
  galleryVolumePreferences.preferred=next;
  syncStartingVolumeSlider();
  saveGalleryVolumePreferences();
 });
 /* One slider, not two. Switching precision preserves the exact stored value;
    the next user adjustment snaps to 5% if that mode is selected. */
 preferredVolumeSlider.addEventListener('keydown',event=>{
  if(galleryVolumePreferences.precision!=='steps')return;
  const delta={ArrowLeft:-5,ArrowDown:-5,ArrowRight:5,ArrowUp:5,PageDown:-10,PageUp:10}[event.key];
  if(delta===undefined)return;
  event.preventDefault();
  galleryVolumePreferences.preferred=galleryVolumePercent(Math.round((galleryVolumePreferences.preferred+delta)/5)*5);
  syncStartingVolumeSlider();
  saveGalleryVolumePreferences();
 });
 for(const option of settingsPage.querySelectorAll('[data-volume-precision]'))option.addEventListener('click',()=>{
  galleryVolumePreferences.precision=option.dataset.volumePrecision==='fine'?'fine':'steps';
  syncStartingVolumeSlider();
  saveGalleryVolumePreferences();
 });
 syncStartingVolumeSlider();
 for(const radio of settingsPage.querySelectorAll('input[name="download-destination"]'))radio.addEventListener('change',()=>{
  state.downloadDestination=radio.value;
  const preview=settingsPage.querySelector('#download-folder-placeholder');
  if(preview)preview.hidden=radio.value!=='custom';
 });
 settingsPage.querySelector('#locate-vlc').addEventListener('click',async()=>{
  const status=settingsPage.querySelector('#vlc-detection');
  if(!window.galleryDesktop){status.textContent='Available in the macOS application only.';return;}
  const result=await window.galleryDesktop.locateVLC();
  if(status?.isConnected)status.textContent=result.ok?'Selected: '+result.path:result.message;
 });
 settingsPage.querySelector('#settings-back').focus({preventScroll:true});
 requestAnimationFrame(updateTabScrollOverlay);
}
function closeSettings(){
 if(!document.body.classList.contains('settings-view')||settingsClosing)return;
 cancelGalleryTextColorPopover(false);
 hideTabScrollOverlay();
 if(searchOpen)closeInlineSearch(false);
 if(settingsScrollFrame!==null){cancelAnimationFrame(settingsScrollFrame);settingsScrollFrame=null;}
 subtitleResizeObserver?.disconnect();
 settingsClosing=true;
 settingsPage.inert=true;
 const button=document.getElementById('settings');
 button.focus({preventScroll:true});
 transitionGalleryStage(()=>{
  // The outgoing Settings snapshot has already been captured.
  settingsPage.classList.remove('is-leaving');
  settingsPage.hidden=true;
  settingsPage.innerHTML='';
  settingsPage.inert=false;
  screen.classList.remove('surface-enter');
  document.body.classList.remove('settings-view','returning-to-gallery');
  workspace.classList.remove('settings-mode','returning-to-gallery');
  tabPagesViewport.inert=false;
  screen.inert=false;
  document.querySelector('.tabs').inert=false;
  workspace.scrollTop=settingsReturnScroll;
  button.setAttribute('aria-label','Open settings');
  button.setAttribute('title','Settings');
  button.setAttribute('aria-expanded','false');
  settingsClosing=false;
  requestAnimationFrame(updateTabScrollOverlay);
 });
}
// Deliberate keyboard focus and scroll: Chrome must not jump-cut to an off-screen
// Settings control on Tab/Shift+Tab. Unrelated dialogs keep their existing trap.
let settingsScrollFrame=null;
function revealSettingsControl(el){
 if(!settingsPage.contains(el)||!settingsPage.offsetParent)return;
 const view=workspace.getBoundingClientRect(),rect=el.getBoundingClientRect();
 const margin=20;
 let target=workspace.scrollTop;
 if(rect.top<view.top+margin)target+=rect.top-(view.top+margin);
 else if(rect.bottom>view.bottom-margin)target+=rect.bottom-(view.bottom-margin);
 target=Math.max(0,Math.min(target,workspace.scrollHeight-workspace.clientHeight));
 if(settingsScrollFrame!==null)cancelAnimationFrame(settingsScrollFrame);
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){workspace.scrollTop=target;settingsScrollFrame=null;return;}
 const from=workspace.scrollTop;const distance=target-from;if(Math.abs(distance)<1){settingsScrollFrame=null;return;}
 let started=null;const duration=Math.min(380,Math.max(190,190+Math.sqrt(Math.abs(distance))*5));
 function step(time){if(started===null)started=time;const p=Math.min(1,(time-started)/duration);workspace.scrollTop=from+distance*(1-Math.pow(1-p,3));if(p<1)settingsScrollFrame=requestAnimationFrame(step);else settingsScrollFrame=null;}
 settingsScrollFrame=requestAnimationFrame(step);
}
workspace.addEventListener('wheel',()=>{if(settingsScrollFrame!==null){cancelAnimationFrame(settingsScrollFrame);settingsScrollFrame=null;}},{passive:true});
document.addEventListener('keydown',event=>{
if(!document.body.classList.contains('settings-view')||modalHost.firstChild||document.querySelector('.gallery-color-popover'))return;
 if(event.key==='Escape'){event.preventDefault();event.stopImmediatePropagation();if(searchOpen)closeInlineSearch();else closeSettings();return;}
 if(event.key!=='Tab'||event.altKey||event.ctrlKey||event.metaKey)return;
 const controls=[searchToggle,searchInput,searchClear,searchClose,document.getElementById('settings'),...settingsPage.querySelectorAll('button:not([disabled]),input:not([disabled]),select:not([disabled]),a[href]')].filter(el=>el.getClientRects().length&&!el.closest('[hidden]')&&!el.hidden&&!el.closest('[inert]'));
 if(!controls.length)return;
 const index=controls.indexOf(document.activeElement);
 const back=event.shiftKey;
 const next=controls[index<0?(back?controls.length-1:0):(index+(back?-1:1)+controls.length)%controls.length];
 event.preventDefault();
 next.focus({preventScroll:true});
 revealSettingsControl(next);
},true);

function showFilters(){modal('Discovery filters',`<p class="description">Combinable filters, independent of sorting. Missing data must be represented as Unknown in production.</p><div class="field"><label for="status-filter">Airing status</label><select id="status-filter"><option>All</option><option>Completed</option><option>Ongoing</option></select></div><div class="field"><label for="audio-filter">Available audio</label><select id="audio-filter"><option>All</option><option>Sub</option><option>Dub</option></select></div>`,`<button class="btn" id="reset-filters">Reset</button><button class="btn primary" id="apply-filters">Apply filters</button>`);document.getElementById('status-filter').value=state.filterStatus;document.getElementById('audio-filter').value=state.filterAudio;document.getElementById('reset-filters').onclick=()=>{state.filterStatus='All';state.filterAudio='All';closeModal();render();};document.getElementById('apply-filters').onclick=()=>{state.filterStatus=document.getElementById('status-filter').value;state.filterAudio=document.getElementById('audio-filter').value;closeModal();render();};}
/* v55 — Library and Downloads retain their ordinary controls and layout until
   the user actually types. The tag/status selection remains unmodified. */
/* v54 — Search is a contextual tool in the active tab, never a new tab.
   Search field is absolutely anchored LEFT of the stationary header icon.
   Discover's Continue Watching stays mounted so its collapse animates. */
const searchToggle=document.getElementById('search');
const headerSearch=document.getElementById('header-search');
const headerRow=document.querySelector('.brand-row');
const searchField=document.getElementById('header-search-field');
const searchInput=document.getElementById('header-search-input');
const searchClear=document.getElementById('header-search-clear');
const searchClose=document.getElementById('header-search-close');
let searchOpen=false;
let searchScrollBefore=0;
function searchPlaceholder(){
 if(document.body.classList.contains('settings-view'))return 'Search settings…';
 if(whOpen)return 'Search watch history…';
 return state.view==='library'?'Search your library…':state.view==='downloads'?'Search downloads…':'Search anime…';
}
function configureHeaderSearchContext(){
 const isSettings=document.body.classList.contains('settings-view');
 const label=isSettings?'Search settings':whOpen?'Search watch history':state.view==='library'?'Search library':state.view==='downloads'?'Search downloads':'Search anime';
 if(!searchOpen)searchToggle.setAttribute('aria-label',label);
 searchToggle.title=searchOpen?'Close search':label;
 searchInput.placeholder=searchPlaceholder();
 searchField.querySelector('label').textContent=label;
}
function searchResultButtons(){return [...tabPages[state.view].querySelectorAll('.poster-button[data-detail]')];}
function updateDiscoverSearchResults(){
 const content=tabPages.discover.querySelector('.tab-page-content');
 const results=content.querySelector('.discover-result-region');
 if(!results)return;
 const model=getSourceCataloguePreview();
 const titles=searchOpen?searchItems(model.titles):model.titles.filter(x=>(state.filterStatus==='All'||x.status===state.filterStatus)&&(state.filterAudio==='All'||x.lang.includes(state.filterAudio)));
 results.innerHTML=model.titles.length?(titles.length?gallery(titles):'<div class="search-empty">No matching titles in this sample catalogue.</div>'):sourceCatalogueEmptyMarkup(model);
 content.querySelector('.discover-results-heading').textContent=searchOpen&&state.query.trim()?'Search results':'Explore the universe';
 content.querySelector('.discover-result-count').textContent=discoverSourceCount(model,titles);
 content.querySelector('#discover-browse-sources')?.addEventListener('click',()=>{closeInlineSearch(false);openSourceManagerFromDiscover();});
 // Search updates only the poster region; the Continue Watching DOM and its
 // height animation are never interrupted by live input changes.
 for(const el of results.querySelectorAll('[data-detail]'))el.addEventListener('click',()=>{closeInlineSearch(false);showDetail(el.dataset.detail);});
 requestAnimationFrame(updateTabScrollOverlay);
}
function updateInlineSearchResults(){
 if(!searchOpen)return;
 state.query=searchInput.value;
 searchClear.hidden=!state.query;
 searchClose.hidden=!!state.query;
 if(document.body.classList.contains('settings-view')){renderSettingsSearchResults();requestAnimationFrame(updateTabScrollOverlay);return;}
 if(whOpen){whSearch=state.query;whRender();return;}
 if(state.view==='discover')updateDiscoverSearchResults();
 else {
  renderTabPage(state.view);
  tabPages[state.view].scrollTop=state.query.trim()?0:searchScrollBefore;
 }
 requestAnimationFrame(updateTabScrollOverlay);
}
function openInlineSearch(){
 if(searchOpen){searchInput.focus({preventScroll:true});return;}
 if(state.playback||modalHost.firstChild)return;
 const searchingSettings=document.body.classList.contains('settings-view');
 if(state.detailId&&!searchingSettings)setView(state.view); // Return to the active tab, not always Discover.
 searchScrollBefore=searchingSettings?workspace.scrollTop:tabPages[state.view].scrollTop;
 searchOpen=true;
 state.query='';
 headerRow.classList.add('is-searching');
 headerSearch.classList.add('is-open');
 searchToggle.setAttribute('aria-expanded','true');
 searchToggle.setAttribute('aria-label','Close search');
 searchToggle.title='Close search';
 searchField.inert=false;
 searchField.setAttribute('aria-hidden','false');
 searchInput.placeholder=searchPlaceholder();
 searchInput.value='';
 searchClear.hidden=true;
 searchClose.hidden=false;
 if(whOpen){whSearch='';whRender();searchInput.focus({preventScroll:true});return;}
 if(searchingSettings)renderSettingsSearchResults();
 if(!searchingSettings&&state.view==='discover'){
  tabPages.discover.classList.add('search-scope-open');
  updateDiscoverSearchResults();
 }
 // Opening Search does not rerender or move Library/Downloads. Only Discover
 // animates Continue Watching, as agreed in the existing search design.
 if(!searchingSettings&&state.view==='discover')tabPages.discover.scrollTop=0;
 hideTabScrollOverlay();
 searchInput.focus({preventScroll:true});
}
function closeInlineSearch(restoreFocus=true){
 if(!searchOpen)return;
 const view=state.view;
 const searchingSettings=document.body.classList.contains('settings-view');
 const hadQuery=Boolean(state.query.trim());
 searchOpen=false;
 state.query='';
 headerRow.classList.remove('is-searching');
 headerSearch.classList.remove('is-open');
 searchToggle.setAttribute('aria-expanded','false');
 searchToggle.setAttribute('aria-label',searchingSettings?'Search settings':'Search '+(view==='library'?'library':view==='downloads'?'downloads':'anime'));
 searchToggle.title=searchingSettings?'Search settings':'Search';
 searchField.inert=true;
 searchField.setAttribute('aria-hidden','true');
 searchInput.value='';
 searchClear.hidden=true;
 searchClose.hidden=false;
 if(whOpen){whSearch='';whRender();if(restoreFocus)searchToggle.focus({preventScroll:true});return;}
 if(searchingSettings){renderSettingsSearchResults();workspace.scrollTop=searchScrollBefore;}
 else if(!state.detailId&&!state.playback){
  if(view==='discover'){
   tabPages.discover.classList.remove('search-scope-open');
   updateDiscoverSearchResults();
  }else if(hadQuery)renderTabPage(view);
  tabPages[view].scrollTop=searchScrollBefore;
 }
 if(restoreFocus)searchToggle.focus({preventScroll:true});
 requestAnimationFrame(updateTabScrollOverlay);
}
function toggleInlineSearch(){if(searchOpen)closeInlineSearch();else openInlineSearch();}
searchInput.addEventListener('input',updateInlineSearchResults);
searchInput.addEventListener('keydown',event=>{
 if(document.body.classList.contains('settings-view')){
  if(event.key==='ArrowDown'||event.key==='Enter'){
   const first=settingsResultButtons()[0];
   if(first){event.preventDefault();if(event.key==='Enter')first.click();else first.focus({preventScroll:true});}
  }
  return;
 }
 if(state.view==='downloads')return;
 if(event.key==='ArrowDown'||event.key==='Enter'){
  const first=searchResultButtons()[0];
  if(first){event.preventDefault();if(event.key==='Enter')first.click();else first.focus({preventScroll:false});}
 }
});
for(const view of ['discover','library']){
 tabPages[view].addEventListener('keydown',event=>{
  if(!searchOpen||state.view!==view||!['ArrowDown','ArrowUp'].includes(event.key))return;
  const buttons=searchResultButtons();
  const at=buttons.indexOf(document.activeElement);
  if(at<0)return;
  event.preventDefault();
  if(event.key==='ArrowDown'&&at<buttons.length-1)buttons[at+1].focus({preventScroll:false});
  else if(event.key==='ArrowUp'&&at>0)buttons[at-1].focus({preventScroll:false});
  else if(event.key==='ArrowUp'&&at===0)searchInput.focus({preventScroll:true});
 });
}
settingsPage.addEventListener('keydown',event=>{
 if(!searchOpen||!document.body.classList.contains('settings-view')||!['ArrowDown','ArrowUp'].includes(event.key))return;
 const results=settingsResultButtons();
 const i=results.indexOf(document.activeElement);
 if(i<0)return;
 event.preventDefault();
 if(event.key==='ArrowDown'&&i<results.length-1)results[i+1].focus({preventScroll:false});
 else if(event.key==='ArrowUp'&&i>0)results[i-1].focus({preventScroll:false});
 else if(event.key==='ArrowUp')searchInput.focus({preventScroll:true});
});
searchClear.addEventListener('click',()=>{searchInput.value='';updateInlineSearchResults();searchInput.focus({preventScroll:true});});
searchClose.addEventListener('click',()=>closeInlineSearch());

function showShare(){const tag=state.tag;const titles=demo.filter(x=>x.tags.includes(tag));const doc={format:'anime-gallery-tag',version:1,tag:{name:tag,type:state.kind[tag]},entries:titles.map(x=>({id:x.id,title:x.name,type:'series',source:'fictional-demo'}))};modal(`Share “${tag}”`,`<p class="description">Export a portable collection. The recipient can preview it or explicitly merge its titles into a tag.</p><div class="dialog-sample"><b>${titles.length} anime</b><p class="description">${escapeHTML(titles.slice(0,4).map(x=>x.name).join(' · '))}${titles.length>4?' …':''}</p></div><p class="tip">This demonstration exports fictional data, without videos, downloads, viewing history, or account information.</p>`,`<button class="btn" id="cancel-export">Cancel</button><button class="btn primary" id="export-tag">${icon('share',16)} Export sample file</button>`);document.getElementById('cancel-export').onclick=closeModal;document.getElementById('export-tag').onclick=()=>{const blob=new Blob([JSON.stringify(doc,null,2)],{type:'application/json'});const link=document.createElement('a');const url=URL.createObjectURL(blob);link.href=url;link.download=`${tag.toLowerCase().replace(/[^a-z0-9]+/g,'-')||'anime-tag'}.anime-collection.json`;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);closeModal();};}
function showNewTag(){modal('Create a library tag',`<p class="description">Custom tags live alongside Watching, Downloads, and Plan to Watch.</p><div class="field"><label for="tag-name">Tag name</label><input id="tag-name" maxlength="45" placeholder="e.g. Movie Night" autocomplete="off"></div><p class="error" id="tag-error" aria-live="polite"></p>`,`<button class="btn" id="cancel-tag">Cancel</button><button class="btn primary" id="create-tag">${icon('plus',16)} Create tag</button>`);document.getElementById('cancel-tag').onclick=closeModal;document.getElementById('create-tag').onclick=()=>{const raw=document.getElementById('tag-name').value.trim().replace(/\s+/g,' ');const error=document.getElementById('tag-error');if(!raw||/[\x00-\x1F\x7F]/.test(raw)){error.textContent='Enter a valid tag name.';return;}if(state.tags.some(x=>x.toLowerCase()===raw.toLowerCase())||raw.toLowerCase()==='all titles'){error.textContent='A tag with that name already exists.';return;}state.tags.push(raw);state.kind[raw]='custom';state.tag=raw;closeModal();render();};}
function showDeleteTag(){
 const tag=state.tag;if(state.kind[tag]!=='custom')return;
 const total=countTag(tag);
 modal(`Delete “${tag}”?`,`<p class="description">This removes the custom tag from <b>${total} ${total===1?'title':'titles'}</b>. The anime themselves will stay in your Library.</p><p class="tip">Changes in this HTML prototype are temporary and reset when you reload.</p>`,`<button class="btn" id="cancel-delete-tag">Cancel</button><button class="btn primary" id="confirm-delete-tag">Delete tag</button>`);
 document.getElementById('cancel-delete-tag').onclick=closeModal;
 document.getElementById('confirm-delete-tag').onclick=()=>{
  state.tags=state.tags.filter(t=>t!==tag);delete state.kind[tag];
  demo.forEach(x=>{x.tags=x.tags.filter(t=>t!==tag)});
  Object.keys(state.seasonTags).forEach(k=>{state.seasonTags[k]=state.seasonTags[k].filter(t=>t!==tag)});
  state.tag='All Titles';closeModal();render();
 };
}
function showRenameTag(){const old=state.tag;if(state.kind[old]!=='custom')return;modal('Rename custom tag',`<div class="field"><label for="tag-rename">Tag name</label><input id="tag-rename" maxlength="45" value="${escapeHTML(old)}"></div><p class="error" id="tag-error" aria-live="polite"></p>`,`<button class="btn" id="cancel-tag">Cancel</button><button class="btn primary" id="rename-tag">Save name</button>`);document.getElementById('cancel-tag').onclick=closeModal;document.getElementById('rename-tag').onclick=()=>{const raw=document.getElementById('tag-rename').value.trim();if(!raw||state.tags.some(x=>x.toLowerCase()===raw.toLowerCase()&&x!==old)){document.getElementById('tag-error').textContent='Choose a unique name.';return;}state.tags=state.tags.map(x=>x===old?raw:x);delete state.kind[old];state.kind[raw]='custom';demo.forEach(x=>x.tags=x.tags.map(t=>t===old?raw:t));state.tag=raw;closeModal();render();};}
function showImport(){state.importDoc=null;modal('Import shared collection',`<p class="description">Open a compatible, locally saved collection file. Preview it before making any changes to your sample library.</p><div class="field"><label for="import-file">Collection file (.json)</label><input id="import-file" type="file" accept=".json,application/json"></div><div id="import-status" class="dialog-sample"><p class="description">Tip: export a sample tag first, then import that file to test this flow.</p></div>`,`<button class="btn" id="cancel-import">Cancel</button><button class="btn primary" id="preview-import" disabled>Preview collection</button>`);document.getElementById('cancel-import').onclick=closeModal;document.getElementById('import-file').onchange=async(e)=>{const f=e.target.files?.[0];const status=document.getElementById('import-status');state.importDoc=null;document.getElementById('preview-import').disabled=true;if(!f)return;if(f.size>1024*1024){status.innerHTML='<p class="error">File is too large for this prototype (max 1 MB).</p>';return;}try{const parsed=JSON.parse(await f.text());if(parsed.format!=='anime-gallery-tag'||parsed.version!==1||typeof parsed.tag?.name!=='string'||!Array.isArray(parsed.entries)||parsed.entries.length>500||!parsed.entries.every(x=>typeof x.id==='string'&&typeof x.title==='string'))throw Error('Unsupported or malformed collection file.');state.importDoc=parsed;status.innerHTML=`<b>${escapeHTML(parsed.tag.name)}</b><p class="description">${parsed.entries.length} entries found. Preview them before importing.</p>`;document.getElementById('preview-import').disabled=false;}catch(err){status.innerHTML=`<p class="error">${escapeHTML(err.message)}</p>`;}};document.getElementById('preview-import').onclick=showImportPreview;}
function showImportPreview(){const d=state.importDoc;if(!d)return;const matched=d.entries.map(en=>({entry:en,found:demo.find(x=>x.id===en.id)}));let recognized=matched.filter(x=>x.found).length;let missing=matched.length-recognized;modal(`Preview “${d.tag.name}”`,`<p class="description">Nothing has been imported yet. Matches use demonstration IDs only; the real application will need reliable anime and season matching.</p><div class="dialog-sample"><b>${recognized} matches · ${missing} unmatched</b><p class="description">Only matched titles can be merged in this prototype. Unmatched titles are never guessed.</p></div><div class="result-list">${matched.slice(0,14).map(x=>`<div class="searchresult"><span>${escapeHTML(x.entry.title)}</span><span class="${x.found?'success':'muted'}">${x.found?'Matched':'Review'}</span></div>`).join('')}${matched.length>14?'<div class="tip">Showing first 14 entries.</div>':''}</div><div class="field"><label for="import-target">Import into</label><select id="import-target"><option value="__new__">New custom tag: ${escapeHTML(d.tag.name)}</option>${state.tags.map(t=>`<option value="${escapeHTML(t)}">Existing: ${escapeHTML(t)}</option>`).join('')}</select></div><p class="tip">For safety, importing into a built-in tag in this demo only changes tag membership. It never changes watched or downloaded state.</p>`,`<button class="btn" id="cancel-import-preview">Cancel</button><button class="btn primary" id="merge-import">Merge matched titles</button>`);document.getElementById('cancel-import-preview').onclick=closeModal;document.getElementById('merge-import').onclick=()=>{const dest=document.getElementById('import-target').value;let finalTag=dest;if(dest==='__new__'){let base=String(d.tag.name||'Shared collection').trim().slice(0,40)||'Shared collection';finalTag=base;let n=2;while(state.tags.some(t=>t.toLowerCase()===finalTag.toLowerCase())){finalTag=base+' ('+n++ +')';}state.tags.push(finalTag);state.kind[finalTag]='custom';}for(const record of matched){if(record.found&&!record.found.tags.includes(finalTag))record.found.tags.push(finalTag);}state.tag=finalTag;closeModal();setView('library');};}
document.addEventListener('pointerdown',event=>{
 const wrap=tabPages.library?.querySelector('.collection-menu-wrap');
 if(!wrap||wrap.contains(event.target))return;
 const menu=wrap.querySelector('.collection-menu'),button=wrap.querySelector('#tag-options');
 if(menu&&!menu.hidden){menu.hidden=true;button?.setAttribute('aria-expanded','false');}
});
document.addEventListener('keydown',event=>{
 if(event.key!=='Escape')return;
 const menu=tabPages.library?.querySelector('#tag-options-menu');
 if(menu&&!menu.hidden){menu.hidden=true;const button=tabPages.library.querySelector('#tag-options');button?.setAttribute('aria-expanded','false');button?.focus();event.preventDefault();}
});
for(const tab of document.querySelectorAll('.tab'))tab.addEventListener('click',()=>{closeInlineSearch(false);setView(tab.dataset.view);});document.getElementById('brand-icon').innerHTML=icon('clapper',25);searchToggle.innerHTML=icon('search',21);searchToggle.onclick=toggleInlineSearch;document.getElementById('settings').innerHTML=icon('settings',23);document.getElementById('settings').onclick=()=>{if(document.body.classList.contains('settings-view'))closeSettings();else showSettings();};searchClear.innerHTML=icon('close',15);searchClose.innerHTML=icon('close',16);for(const [name,ico] of [['discover','compass'],['library','library'],['downloads','download']])document.getElementById('nav-'+name).innerHTML=`<span class="tab-label-wrap">${icon(ico,19)}<span>${name[0].toUpperCase()+name.slice(1)}</span></span>`;document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(modalHost.firstChild)closeModal();else if(searchOpen){e.preventDefault();closeInlineSearch();}}else if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='f'&&!modalHost.firstChild&&!state.playback){e.preventDefault();document.documentElement.dataset.focusModality='keyboard';openInlineSearch();}});document.body.dataset.theme=state.theme;render();setupDesktopSettings();
window.addEventListener('resize',()=>tabPages.library?.querySelector('.tagbar')?.galleryRefresh?.(true));
