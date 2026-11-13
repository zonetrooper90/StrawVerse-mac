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

