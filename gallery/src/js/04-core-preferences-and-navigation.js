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
