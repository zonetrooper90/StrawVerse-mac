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
