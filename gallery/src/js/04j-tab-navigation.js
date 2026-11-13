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
