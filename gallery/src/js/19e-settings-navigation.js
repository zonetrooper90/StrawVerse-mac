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

