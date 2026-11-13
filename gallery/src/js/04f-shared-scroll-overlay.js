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

