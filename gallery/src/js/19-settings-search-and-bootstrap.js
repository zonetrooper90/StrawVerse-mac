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
