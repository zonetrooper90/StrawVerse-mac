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
