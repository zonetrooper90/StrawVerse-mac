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

