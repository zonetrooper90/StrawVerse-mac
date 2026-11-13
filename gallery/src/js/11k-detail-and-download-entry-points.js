function showDetail(id,fromHistory=false,installmentId=null){
 const x=demo.find(t=>t.id===id);if(!x)return;
 transitionGalleryStage(()=>{
  state.playback=null;state.detailReturnHistory=fromHistory;
  state.detailReturnView=state.view;state.detailReturnScroll=selectedTabScroll();
  state.detailId=id;state.detailSeason=0;state.detailRelated=null;
  if(installmentId){const index=getSeasons(x).findIndex(season=>season.id===installmentId);if(index>=0)state.detailSeason=index;}
  state.detailEpisodeFilter='all';state.detailEpisode=1;state.detailAudio=null;
  closeModal();render();workspace.scrollTop=0;
 });
}
function showFolderInfo(){modal('Downloads folder',`<p class="description">In the finished macOS application, this button will open your configured download folder in Finder.</p><div class="dialog-sample"><b>Design prototype</b><p class="description">This standalone HTML demo has no access to a real application's downloaded files or chosen folder.</p></div>`,`<button class="btn primary" id="folder-okay">Got it</button>`);document.getElementById('folder-okay').onclick=closeModal;}
