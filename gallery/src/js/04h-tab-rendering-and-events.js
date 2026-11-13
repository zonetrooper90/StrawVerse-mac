function bindTabPageEvents(view){
 const content=tabPages[view].querySelector('.tab-page-content');
 const on=(id,fn)=>{const el=content.querySelector('#'+id);if(el)el.addEventListener('click',fn)};
 for(const el of content.querySelectorAll('[data-detail]'))el.addEventListener('click',()=>{if(searchOpen)closeInlineSearch(false);showDetail(el.dataset.detail);});
 for(const el of content.querySelectorAll('[data-tag]'))el.addEventListener('click',()=>{if(searchOpen)closeInlineSearch(false);hideTabScrollOverlay();state.tag=el.dataset.tag;render();});
 for(const el of content.querySelectorAll('[data-download-filter]'))el.addEventListener('click',()=>{if(searchOpen)closeInlineSearch(false);hideTabScrollOverlay();state.downloadStatus=el.dataset.downloadFilter;render();});
 on('filters',showFilters);on('wh-view-history',whEnter);
 if(view==='discover')whSetupRecentPreview(content);
 for(const button of content.querySelectorAll('[data-wh-recent]'))button.addEventListener('click',()=>{
  const r=whRecords.find(r=>r.id===button.dataset.whRecent);
  if(!r)return;
  if(!r.galleryId||!demo.some(x=>x.id===r.galleryId)){
   modal('Sample Recently Watched entry','<p class="description">This preview record has no matching anime detail page yet.</p>','<button class="btn primary" id="wh-sample-okay">Got it</button>');
   document.getElementById('wh-sample-okay')?.addEventListener('click',closeModal);
   return;
  }
  // This card is on Discover, not inside Watch History. Back must return to Discover.
  showDetail(r.galleryId,false,r.installmentId);
 });
 on('resume',()=>showDetail('demo:02'));on('discover-browse-sources',openSourceManagerFromDiscover);
 on('import',showImport);on('newtag',showNewTag);on('sharetag',showShare);
 on('renametag',showRenameTag);on('deletetag',showDeleteTag);
 on('tag-options',()=>{
  const menu=content.querySelector('#tag-options-menu'),button=content.querySelector('#tag-options');
  if(!menu||!button)return;
  menu.hidden=!menu.hidden;
  button.setAttribute('aria-expanded',String(!menu.hidden));
 });
 on('openfolder',showFolderInfo);
 for(const el of content.querySelectorAll('[data-download-toggle]'))el.addEventListener('click',()=>setDownloadGroupExpanded(el.dataset.downloadToggle,!downloadDemo.expanded.has(el.dataset.downloadToggle)));
 for(const el of content.querySelectorAll('[data-download-dismiss]'))el.addEventListener('click',()=>dismissDownloadEpisode(el.dataset.downloadDismiss));
 for(const el of content.querySelectorAll('[data-dismiss-group]'))el.addEventListener('click',()=>dismissDownloadGroup(el.dataset.dismissGroup));
 for(const el of content.querySelectorAll('[data-download-cancel]'))el.addEventListener('click',()=>cancelDownloadEpisode(el.dataset.downloadCancel));
 for(const el of content.querySelectorAll('[data-download-retry]'))el.addEventListener('click',()=>retryDownloadEpisode(el.dataset.downloadRetry));
 for(const el of content.querySelectorAll('[data-download-pause]'))el.addEventListener('click',()=>toggleDownloadPause(el.dataset.downloadPause));
 on('dismiss-all-downloads',dismissAllFinishedDownloads);
 on('demo-next-download',simulateNextDownload);on('demo-reset-downloads',resetDownloadDemo);
}
function updateLibraryTagRail(content,revealActive=false){
 const rail=content.querySelector('.tagbar');
 const row=content.querySelector('.library-tag-row');
 if(!rail||!row)return;
const back=content.querySelector('#library-tag-prev');
 const next=content.querySelector('#library-tag-next');
 const refresh=()=>{
  const max=Math.max(0,rail.scrollWidth-rail.clientWidth);
  const overflow=max>2;
  row.classList.toggle('has-overflow',overflow);
  const left=overflow&&rail.scrollLeft>2,right=overflow&&rail.scrollLeft<max-2;
  back.disabled=!left;next.disabled=!right;
  rail.classList.toggle('can-left',left);
  rail.classList.toggle('can-right',right);
 };
 const pan=(direction)=>rail.scrollBy({left:direction*Math.max(140,rail.clientWidth*.7),behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
 back.addEventListener('click',()=>pan(-1));
 next.addEventListener('click',()=>pan(1));
 rail.addEventListener('scroll',refresh,{passive:true});
 const showActive=()=>{
  const selected=rail.querySelector('.tagchip.active');
  if(!selected)return;
  const r=rail.getBoundingClientRect(),a=selected.getBoundingClientRect();
  if(a.left<r.left+12)rail.scrollLeft-=r.left+12-a.left;
  else if(a.right>r.right-12)rail.scrollLeft+=a.right-r.right+12;
 };
 rail.galleryRefresh=(reveal=false)=>{
  // The arrows take up space when overflow begins. Measure only after
  // they've appeared, so selected tags stay visible when resizing.
  refresh();if(reveal)showActive();refresh();
 };
 rail.galleryRefresh(revealActive);
}
function renderTabPage(view){
 const panel=tabPages[view];
 const scroll=panel.scrollTop;
 const content=panel.querySelector('.tab-page-content');
 const priorTag=content.querySelector('.tagchip.active')?.dataset.tag;
 const tagScroll=content.querySelector('.tagbar')?.scrollLeft||0;
 if(view==='downloads')captureDownloadScroll();
 content.innerHTML=tabViewContent(view);
 panel.classList.toggle('search-scope-open',searchOpen&&state.view===view);
 panel.dataset.initialized='true';
 bindTabPageEvents(view);
 if(view==='downloads')restoreDownloadScroll();
 panel.scrollTop=scroll;
 requestAnimationFrame(updateTabScrollOverlay);
 if(view==='library'&&content.querySelector('.tagbar')){
  content.querySelector('.tagbar').scrollLeft=tagScroll;
  updateLibraryTagRail(content,priorTag!==state.tag);
 }
}
