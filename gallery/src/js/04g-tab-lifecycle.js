let tabPagesReady=false;
let tabTrackAnimation=null;
let tabTrackTarget='discover';
function updateActiveTab(view){
 for(const tab of document.querySelectorAll('.tab')){
  const active=tab.dataset.view===view;
  tab.classList.toggle('active',active);
  if(active)tab.setAttribute('aria-current','page');else tab.removeAttribute('aria-current');
 }
}
function tabViewContent(view){
 return view==='discover'?discover():view==='library'?library():downloads();
}
function selectedTabScroll(){
 return workspace.classList.contains('tab-pages-visible')
  ?tabPages[state.view].scrollTop:workspace.scrollTop;
}
function syncTabPanelAccessibility(){
 for(const view of tabOrder){
  const panel=tabPages[view];const active=view===state.view;
  panel.inert=!active;
  panel.setAttribute('aria-hidden',String(!active));
 }
}
