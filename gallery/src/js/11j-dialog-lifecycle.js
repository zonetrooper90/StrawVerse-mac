/* v39: Modal lifecycle and keyboard focus stay stable across every Gallery dialog.
   Preserve the original opener even when a dialog replaces another (e.g. import preview). */
const galleryApp=document.querySelector('.app');
let modalReturnFocus=null;
let modalExitController=null;
function cancelModalExit(){
 modalExitController?.abort();modalExitController=null;
 clearTimeout(modalExitTimer);modalExitTimer=null;
}
const modalFocusable='button:not([disabled]),[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';
function visibleModalControls(){
 const dialog=modalHost.querySelector('.dialog');
 return dialog?Array.from(dialog.querySelectorAll(modalFocusable)).filter(el=>!el.closest('[hidden]')&&el.getClientRects().length>0&&!el.inert):[];
}
function modal(title,inner,actions=''){
 const outgoing=modalHost.querySelector('.overlay');
 const previouslyOpen=!!outgoing;
 if(!previouslyOpen){
  const opener=document.activeElement;
  modalReturnFocus=opener instanceof HTMLElement&&opener!==document.body&&!modalHost.contains(opener)?opener:null;
 }
 cancelModalExit();
 if(outgoing){outgoing.dispatchEvent(new Event('gallery-modal-will-close'));retireModalWork(outgoing);}
 modalHost.innerHTML=`<div class="overlay" role="presentation"><div class="dialog" role="dialog" aria-modal="true" aria-label="${escapeHTML(title)}" tabindex="-1"><div class="dialog-scroll"><div class="dialog-head"><h2>${escapeHTML(title)}</h2><button class="iconbtn" aria-label="Close dialog" id="close-dialog">${icon('close',20)}</button></div>${inner}${actions?`<div class="dialog-actions">${actions}</div>`:''}</div></div></div>`;
 galleryApp.inert=true;
 modalHost.querySelector('.overlay').addEventListener('click',e=>{if(e.target.classList.contains('overlay'))closeModal()});
 document.getElementById('close-dialog').addEventListener('click',closeModal);
 (modalHost.querySelector('button:not(#close-dialog),input,select')||document.getElementById('close-dialog')).focus({preventScroll:true});
}
function finishModalClose(overlay){
 if(modalHost.firstElementChild!==overlay)return;
 cancelModalExit();
 retireModalWork(overlay);
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
 // Notify only this dialog before its exit (or reduced-motion removal).
 overlay.dispatchEvent(new Event('gallery-modal-will-close'));
 cancelModalExit();
 if(galleryReducedMotion.matches){finishModalClose(overlay);return;}
 // Read the current animated values before changing the animation name.
 // A settled entrance uses the original exit keyframes without overrides.
 const dialog=overlay.querySelector('.dialog');
 const backdropOpacity=getComputedStyle(overlay).opacity;
 const front=getComputedStyle(dialog);
 const dialogOpacity=front.opacity,dialogTransform=front.transform;
 if(Number(backdropOpacity)<1)overlay.style.setProperty('--gallery-backdrop-exit-opacity',backdropOpacity);
 if(Number(dialogOpacity)<1){
  dialog.style.setProperty('--gallery-dialog-exit-opacity',dialogOpacity);
  if(dialogTransform!=='none')dialog.style.setProperty('--gallery-dialog-exit-transform',dialogTransform);
 }
 retireModalWork(overlay);
 // Listen before starting the exits; only this overlay and its dialog can
 // complete their own pair. A replacement aborts the entire old owner.
 const controller=new AbortController();
 modalExitController=controller;
 const owned=()=>modalExitController===controller&&modalHost.firstElementChild===overlay&&overlay.classList.contains('is-closing');
 let backdropDone=false,dialogDone=false;
 overlay.addEventListener('animationend',event=>{
  if(!owned()||!event.isTrusted||event.pseudoElement)return;
  if(event.target===overlay&&event.animationName==='gallery-backdrop-out')backdropDone=true;
  if(event.target===dialog&&event.animationName==='gallery-dialog-out')dialogDone=true;
  if(backdropDone&&dialogDone)finishModalClose(overlay);
 },{signal:controller.signal});
 overlay.classList.add('is-closing');
 // Safety only: missing completion events must not strand inert input.
 // Settle any remaining owned exit animations before fallback removal.
 const timer=setTimeout(()=>{
  if(!owned()||modalExitTimer!==timer)return;
  for(const [node,name] of [[overlay,'gallery-backdrop-out'],[dialog,'gallery-dialog-out']]){
   for(const animation of node.getAnimations?.()||[]){
    if(animation.animationName===name){try{animation.finish()}catch(_){}}
   }
  }
  finishModalClose(overlay);
 },300);
 modalExitTimer=timer;
}
// A live preference change cancels the owned exit timer and releases focus
// and inert state in the same handler. An open dialog stays open.
galleryReducedMotion.addEventListener('change',event=>{
 if(!event.matches)return;
 const overlay=modalHost.querySelector('.overlay.is-closing');
 if(overlay&&modalHost.firstElementChild===overlay)finishModalClose(overlay);
});
/* v41: All Tab / Shift+Tab focus changes in dialogs are managed here.
   Prevent Chrome's instant implicit focus scroll, then reveal the newly
   focused control through the same smooth scroll path as wraparound.
   Keep focus itself immediate, the dialog stationary and Reduce Motion intact. */
let modalScrollFrame=null;
let modalScrollGoal=null;
let modalScrollContainer=null;
let modalScrollGeneration=0;
let modalFocusRevealFrame=null;
function retireModalWork(overlay){
 cancelModalKeyboardScroll();
 if(modalFocusRevealFrame!==null)cancelAnimationFrame(modalFocusRevealFrame);
 modalFocusRevealFrame=null;modalKeyboardFocusTarget=null;
 const stage=overlay.querySelector('#subtitle-expanded-stage');
 if(stage)subtitleResizeObserver?.unobserve(stage);
}
function cancelModalKeyboardScroll(){
 modalScrollGeneration++;
 if(modalScrollFrame!==null)cancelAnimationFrame(modalScrollFrame);
 modalScrollFrame=null;modalScrollGoal=null;modalScrollContainer=null;
}
function revealModalControl(control,edge='nearest'){
 const overlay=modalHost.querySelector('.overlay');
 const scroller=overlay?.querySelector('.dialog-scroll');
 if(!scroller||overlay.classList.contains('is-closing')||!control||!scroller.contains(control))return;
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
 const generation=modalScrollGeneration;
 function step(time){
  if(generation!==modalScrollGeneration||modalScrollContainer!==scroller)return;
  if(modalHost.firstElementChild!==overlay||overlay.classList.contains('is-closing')||!scroller.isConnected){cancelModalKeyboardScroll();return;}
  if(started===null)started=time;
  const fraction=galleryReducedMotion.matches?1:Math.min(1,(time-started)/duration);
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
  if(modalFocusRevealFrame!==null)cancelAnimationFrame(modalFocusRevealFrame);
  const frame=requestAnimationFrame(()=>{
   if(modalFocusRevealFrame!==frame)return;
   modalFocusRevealFrame=null;
   if(modalHost.firstElementChild===overlay&&!overlay.classList.contains('is-closing')&&overlay.contains(focused)&&document.activeElement===focused)revealModalControl(focused);
  });
  modalFocusRevealFrame=frame;
  return;
 }
 const first=visibleModalControls()[0]||overlay.querySelector('.dialog');
 first?.focus({preventScroll:true});
 revealModalControl(first);
},true);
