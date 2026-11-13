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

