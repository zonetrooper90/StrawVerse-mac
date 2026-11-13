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
