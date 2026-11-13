function render(){
 if(!state.playback){clearTimeout(playerControlsTimer);playerControlsTimer=null;playerEventController?.abort();playerEventController=null;resetPlayNextState();}
 document.body.classList.toggle('player-view',Boolean(state.playback));
 // Both the Anime detail and Watch History are secondary pages: hide main
 // navigation, but retain the standard Gallery brand header and back buttons.
 document.body.classList.toggle('detail-view',Boolean(state.detailId&&!state.playback&&!whOpen));
 if(whOpen){
  freezeTabTrack();hideTabScrollOverlay();workspace.classList.remove('tab-pages-visible','library-view');tabPagesViewport.hidden=true;screen.hidden=false;screen.dataset.surfaceKey='watch-history';whRender({keepScroll:false});return;
 }
 if(!state.playback&&!state.detailId){showTabPages();return;}
 // Detail and player screens retain their existing layout and event handling.
 freezeTabTrack();
 hideTabScrollOverlay();
 workspace.classList.remove('tab-pages-visible');
 tabPagesViewport.hidden=true;
 screen.hidden=false;
 const oldTagScroll=screen.querySelector('.tagbar')?.scrollLeft||0;
 const priorRailScroll=screen.querySelector('#inline-installment-rail')?.scrollLeft||0;
 workspace.classList.toggle('library-view',state.view==='library'&&!state.detailId);
 // Animate actual screen navigation, not routine player updates or episode selections.
 const surfaceKey=state.playback?'playback':state.detailId?'detail:'+state.detailId:state.view==='discover'?'discover:'+state.filterStatus+':'+state.filterAudio:state.view==='library'?'library:'+state.tag:'downloads:'+state.downloadStatus;
 const surfaceChanged=screen.dataset.surfaceKey!==surfaceKey;
 screen.dataset.surfaceKey=surfaceKey;
 screen.innerHTML=state.playback?playbackPage():state.detailId?detailPage():state.view==='discover'?discover():state.view==='library'?library():downloads();
 if(surfaceChanged){
  clearGallerySurfaceEntrance();
  if(!galleryStageMutating&&!galleryReducedMotion.matches){
   void screen.offsetWidth;
   screen.classList.add('surface-enter');
  }
 }
 if(state.playback){
   document.getElementById('back-from-playback')?.addEventListener('click',backFromPlayback);
   initializePlayer();requestAnimationFrame(updateTabScrollOverlay);return;
 }
 if(state.detailId){
   document.getElementById('detail-back')?.addEventListener('click',backFromDetail);
   activeInstallmentRailObserver?.disconnect();
   activeInstallmentRailObserver=null;
   const rail=document.getElementById('inline-installment-rail');
   if(rail){
     rail.addEventListener('scroll',refreshInstallmentArrows,{passive:true});
     setupInstallmentEdgeGuards(rail.closest('.inline-release-viewport'));
     activeInstallmentRailObserver=new ResizeObserver(refreshInstallmentArrows);
     activeInstallmentRailObserver.observe(rail);
     for(const card of rail.children)activeInstallmentRailObserver.observe(card);
     requestAnimationFrame(refreshInstallmentArrows);
     rail.scrollLeft=priorRailScroll;
     for(const arrow of screen.querySelectorAll('[data-inline-scroll]'))arrow.addEventListener('click',()=>{
// One arrow click advances by exactly one discrete release, not a viewport fraction.
       const direction=Number(arrow.dataset.inlineScroll);
       // Even at the end, this click is consumed by the invisible guard.
       if(arrow.closest('.inline-release-viewport').classList.contains(direction>0?'guard-right':'guard-left'))return;
       const cards=Array.from(rail.querySelectorAll('.inline-installment-card'));
       const railX=rail.getBoundingClientRect().left;
       const offsets=cards.map(card=>card.getBoundingClientRect().left-railX+rail.scrollLeft);
       const position=rail.scrollLeft;
       const target=direction>0
         ? offsets.find(offset=>offset>position+4)
         : [...offsets].reverse().find(offset=>offset<position-4);
       const limit=Math.max(0,rail.scrollWidth-rail.clientWidth);
       if(target===undefined)return;
       rail.scrollTo({left:Math.max(0,Math.min(target,limit)),behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
     });
     for(const card of rail.querySelectorAll('[data-inline-installment]'))
       card.addEventListener('click',()=>selectInlineInstallment(card,rail));
   }
   document.getElementById('find-source')?.addEventListener('click',showFindSource);
   bindEpisodeFiltersAndActions();
     for(const el of screen.querySelectorAll('[data-detail-audio]'))el.addEventListener('click',()=>{
     const next=el.dataset.detailAudio;
     if((state.detailAudio||state.defaultPlayback)===next)return;
     changeDetailAudio(next);
   });
   document.getElementById('manage-detail-tags')?.addEventListener('click',showManageDetailTags);
   for(const el of screen.querySelectorAll('.detail-actions [data-episode-action]'))el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
   requestAnimationFrame(updateTabScrollOverlay);
   return;
 }
 if(state.view==='library'&&screen.querySelector('.tagbar'))screen.querySelector('.tagbar').scrollLeft=oldTagScroll;
 for(const el of screen.querySelectorAll('[data-detail]'))el.addEventListener('click',()=>showDetail(el.dataset.detail));
 for(const el of screen.querySelectorAll('[data-tag]'))el.addEventListener('click',()=>{state.tag=el.dataset.tag;render();});
 const on=(id,fn)=>{const el=document.getElementById(id);if(el)el.addEventListener('click',fn)};
 on('filters',showFilters);on('resume',()=>showDetail('demo:02'));on('discover-browse-sources',openSourceManagerFromDiscover);on('import',showImport);on('newtag',showNewTag);on('sharetag',showShare);on('renametag',showRenameTag);on('openfolder',showFolderInfo);
 for(const el of screen.querySelectorAll('[data-download-filter]'))el.addEventListener('click',()=>{state.downloadStatus=el.dataset.downloadFilter;render();});
}
