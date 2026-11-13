function downloadProgressTrack(percent,label){
 const amount=Math.max(0,Math.min(100,Number(percent)||0));
 return `<span class="sf-dl-track gallery-split-timeline" role="progressbar" aria-label="${escapeHTML(label)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${amount}"><span class="sf-dl-track-done" style="flex-basis:${galleryTimelineFill(amount)}" aria-hidden="true"></span><span class="sf-dl-track-rest" aria-hidden="true"></span></span>`;
}
function downloadGroupCanDismiss(entries){return entries.length>0&&entries.every(entry=>downloadTerminalStates.has(entry.status));}
function setDownloadGroupExpanded(id,expanded){
 if(expanded)downloadDemo.expanded.add(id);else downloadDemo.expanded.delete(id);
 const group=Array.from(tabPages.downloads.querySelectorAll('[data-download-group]')).find(el=>el.dataset.downloadGroup===id);
 if(!group)return;
 group.classList.toggle('is-expanded',expanded);
 group.querySelector('.download-group-toggle')?.setAttribute('aria-expanded',String(expanded));
 const inner=group.querySelector('.download-group-body-inner');
 if(inner){inner.inert=!expanded;inner.setAttribute('aria-hidden',String(!expanded));}
}
const sfDownloadScrollPositions=new Map();
let sfDownloadUndo=null;
function captureDownloadScroll(){
 tabPages.downloads.querySelectorAll('.sf-dl-viewport[data-scroll-group]').forEach(el=>sfDownloadScrollPositions.set(el.dataset.scrollGroup,el.scrollTop));
}
function restoreDownloadScroll(){
 tabPages.downloads.querySelectorAll('.sf-dl-viewport[data-scroll-group]').forEach(el=>{
  if(sfDownloadScrollPositions.has(el.dataset.scrollGroup))el.scrollTop=sfDownloadScrollPositions.get(el.dataset.scrollGroup);
 });
}
function refreshDownloadDemo(focusAnime=null){
 captureDownloadScroll();
 renderTabPage('downloads');
 restoreDownloadScroll();
 renderDownloadUndoToast();
 if(focusAnime){
  const group=Array.from(tabPages.downloads.querySelectorAll('[data-download-group]')).find(el=>el.dataset.downloadGroup===focusAnime);
  (group?.querySelector('.download-group-toggle')||tabPages.downloads.querySelector('[data-download-filter="All"]'))?.focus({preventScroll:true});
 }
}
function dismissDownloadEpisode(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||!downloadTerminalStates.has(entry.status))return;
 sfDownloadUndo={id,animeId:entry.animeId,wasExpanded:downloadDemo.expanded.has(entry.animeId)};
 downloadDemo.dismissed.add(id);
 if(animeDownloadEntries(entry.animeId).length===0)downloadDemo.expanded.delete(entry.animeId);
 refreshDownloadDemo();
}
function renderDownloadUndoToast(){
 // The tab track is transformed; a fixed toast inside it would appear off-screen.
 // Mount it directly under body so it stays anchored to the actual viewport.
 document.getElementById('sf-dl-undo-global')?.remove();
 if(!sfDownloadUndo||state.view!=='downloads')return;
 const toast=document.createElement('div');
 toast.id='sf-dl-undo-global';toast.className='sf-dl-undo';toast.setAttribute('role','status');
 toast.innerHTML='<span>Episode dismissed from the list. File kept.</span><button type="button">Undo</button>';
 toast.querySelector('button').addEventListener('click',undoDismissDownload);
 document.body.appendChild(toast);
}
function undoDismissDownload(){
 if(!sfDownloadUndo)return;
 const {id,animeId,wasExpanded}=sfDownloadUndo;
 downloadDemo.dismissed.delete(id);
 if(wasExpanded)downloadDemo.expanded.add(animeId);
 sfDownloadUndo=null;
 refreshDownloadDemo(animeId);
}
function dismissDownloadGroup(id){
 const entries=animeDownloadEntries(id);
 if(!downloadGroupCanDismiss(entries))return;
 const anime=demo.find(item=>item.id===id);
 modal('Dismiss download notifications',`<p class="description">Remove <b>${escapeHTML(anime?.name||'this anime')}</b> and its ${entries.length} finished download ${entries.length===1?'entry':'entries'} from this page?</p><p class="tip">This only dismisses notifications. It does not delete, move or change any files.</p>`,
 `<button class="btn" id="dismiss-group-back">Keep notifications</button><button class="btn primary" id="dismiss-group-confirm">Dismiss ${entries.length} ${entries.length===1?'entry':'entries'}</button>`);
 document.getElementById('dismiss-group-back').onclick=closeModal;
 document.getElementById('dismiss-group-confirm').onclick=()=>{
  const latest=animeDownloadEntries(id);
  if(!downloadGroupCanDismiss(latest)){closeModal();return;}
  latest.forEach(entry=>downloadDemo.dismissed.add(entry.id));
  downloadDemo.expanded.delete(id);
  closeModal();refreshDownloadDemo();
 };
}
function cancelDownloadEpisode(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||!['Queued','Downloading','Paused'].includes(entry.status))return;
 modal('Cancel download',`<p class="description">Cancel <b>${escapeHTML(entry.release)} · Episode ${entry.episode}</b>?</p><p class="tip">Cancel stops the transfer. It is different from dismissing a finished notification. This preview does not download anything.</p>`,
 '<button class="btn" id="cancel-download-back">Keep downloading</button><button class="btn primary" id="cancel-download-confirm">Cancel transfer</button>');
 document.getElementById('cancel-download-back').onclick=closeModal;
 document.getElementById('cancel-download-confirm').onclick=()=>{entry.status='Canceled';closeModal();refreshDownloadDemo(entry.animeId);};
}
function toggleDownloadPause(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||!['Downloading','Paused'].includes(entry.status))return;
 entry.status=entry.status==='Downloading'?'Paused':'Downloading';
 captureDownloadScroll();renderTabPage('downloads');restoreDownloadScroll();
 const next=tabPages.downloads.querySelector(`[data-download-pause="${id}"]`);
 next?.focus({preventScroll:true});
}
function retryDownloadEpisode(id){
 const entry=downloadDemo.entries.find(e=>e.id===id);
 if(!entry||downloadDemo.dismissed.has(id)||entry.status!=='Failed')return;
 // Demo has no actual partial-file resume support: retry queues from zero.
 entry.status='Queued';entry.progress=0;
 refreshDownloadDemo(entry.animeId);
}
function dismissAllFinishedDownloads(){
 const entries=visibleDownloadEntries().filter(entry=>downloadTerminalStates.has(entry.status));
 if(!entries.length)return;
 modal('Dismiss all finished notifications',`<p class="description">Dismiss <b>${entries.length}</b> completed, failed or canceled download ${entries.length===1?'notification':'notifications'}?</p><p class="tip">Active and queued downloads will remain visible. This clears notifications only; no downloads will be stopped and no files will be changed.</p>`,
 '<button type="button" class="btn" id="dismiss-all-back">Keep notifications</button><button type="button" class="btn primary" id="dismiss-all-confirm">Dismiss finished</button>');
 document.getElementById('dismiss-all-back').onclick=closeModal;
 document.getElementById('dismiss-all-confirm').onclick=()=>{
  sfDownloadUndo=null;
  for(const entry of visibleDownloadEntries())if(downloadTerminalStates.has(entry.status))downloadDemo.dismissed.add(entry.id);
  for(const id of [...downloadDemo.expanded])if(animeDownloadEntries(id).length===0)downloadDemo.expanded.delete(id);
  closeModal();refreshDownloadDemo();
 };
}
function simulateNextDownload(){
 const target=visibleDownloadEntries().find(e=>e.status==='Downloading')||visibleDownloadEntries().find(e=>e.status==='Queued');
 if(!target)return;
 const before=downloadProgress(allAnimeDownloadEntries(target.animeId));
 if(target.status==='Downloading'){
  target.status='Completed';target.progress=100;
 }else{
  target.status='Downloading';target.progress=12;
 }
 const after=downloadProgress(allAnimeDownloadEntries(target.animeId));
 if(before<100&&after===100){
  downloadDemo.fullAt.set(target.animeId,Date.now());
  clearTimeout(downloadDemo.timers.get(target.animeId));
  const timer=setTimeout(()=>{
   const group=Array.from(tabPages.downloads.querySelectorAll('[data-download-group]')).find(el=>el.dataset.downloadGroup===target.animeId);
   group?.querySelector('.download-group-percent')?.classList.add('is-hidden');
  },DEMO_COMPLETION_HOLD_MS);
  downloadDemo.timers.set(target.animeId,timer);
 }
 refreshDownloadDemo();
}
function resetDownloadDemo(){
 for(const timer of downloadDemo.timers.values())clearTimeout(timer);
 downloadDemo.entries=makeDemoDownloadEntries();
 downloadDemo.expanded.clear();downloadDemo.dismissed.clear();downloadDemo.fullAt.clear();downloadDemo.timers.clear();
 state.downloadStatus='All';sfDownloadUndo=null;sfDownloadScrollPositions.clear();refreshDownloadDemo();
}
function downloads(){
 const isSearching=searchOpen&&state.view==='downloads'&&Boolean(state.query.trim());
 const query=isSearching?state.query.trim().toLowerCase():'';
 const all=visibleDownloadEntries();
 const statuses=['All','Downloading','Completed'];
 const filters=`<div class="download-filters" role="group" aria-label="Download status">${statuses.map(status=>`<button class="filterpill ${status===(isSearching?'All':state.downloadStatus)?'active':''}" data-download-filter="${status}" aria-pressed="${status===(isSearching?'All':state.downloadStatus)}">${status} <span class="count">${status==='All'?all.length:all.filter(entry=>entry.status===status).length}</span></button>`).join('')}</div>`;
 const dismissibleCount=all.filter(entry=>downloadTerminalStates.has(entry.status)).length;
 const dismissAllTitle=dismissibleCount?'Dismiss all completed, failed and canceled download notifications; keep files':'No finished notifications to dismiss';
 const actions=`<span class="download-dismiss-all-wrap" title="${dismissAllTitle}"><button type="button" class="download-action-btn download-action-dismiss" id="dismiss-all-downloads" aria-label="${dismissAllTitle}" ${dismissibleCount?'':'disabled'}>${downloadActionIcon('dismiss')}</button></span><button class="btn" id="openfolder">${icon('folder',16)} <span>Open Folder</span></button>`;
 const animeIds=[...new Set(all.map(entry=>entry.animeId))];
 const groups=animeIds.map(id=>{
  const anime=demo.find(item=>item.id===id);
  if(!anime)return '';
  const entries=animeDownloadEntries(id);
  const allEntries=allAnimeDownloadEntries(id);
  const titleMatches=Boolean(query&&anime.name.toLowerCase().includes(query));
  const matched=entries.filter(entry=>{
   if(isSearching)return !query||titleMatches||[entry.release,`episode ${entry.episode}`,String(entry.episode),entry.audio,entry.status].some(value=>value.toLowerCase().includes(query));
   return state.downloadStatus==='All'||entry.status===state.downloadStatus;
  });
  if(!matched.length)return '';
  const progress=downloadProgress(allEntries);
  const expanded=downloadDemo.expanded.has(id);
  const groupStatus=downloadGroupStatus(allEntries);
  const dismissible=downloadGroupCanDismiss(entries);
  const bodyId=`download-group-body-${id.replace(/[^a-z0-9]/gi,'-')}`;
  const episodes=matched.map(entry=>{
   const terminal=downloadTerminalStates.has(entry.status);
   const active=entry.status==='Downloading',paused=entry.status==='Paused',failed=entry.status==='Failed';
   const playPause=active||paused?`<button class="sf-dl-control-button" type="button" data-download-pause="${entry.id}" aria-label="${active?'Pause':'Resume'} ${escapeHTML(anime.name)} · ${escapeHTML(entry.release)} · Episode ${entry.episode}">${sfDownloadControlIcon(active?'pause':'play')}<span>${active?'Pause':'Resume'}</span></button>`:'';
   const retry=failed?`<button class="sf-dl-control-button" type="button" data-download-retry="${entry.id}" aria-label="Retry ${escapeHTML(anime.name)} · Episode ${entry.episode}">${downloadActionIcon('retry')}<span>Retry</span></button>`:'';
   const action=terminal?'dismiss':'cancel';
   const label=terminal?`Dismiss ${anime.name} · Episode ${entry.episode} from Downloads list (keep downloaded file)`:`Cancel ${anime.name} · Episode ${entry.episode} transfer (requires confirmation)`;
   const quick=`<button class="sf-dl-quick-btn" type="button" ${terminal?`data-download-dismiss="${entry.id}"`:`data-download-cancel="${entry.id}"`} aria-label="${escapeHTML(label)}" title="${terminal?'Dismiss list entry; keep file':'Cancel transfer; confirm first'}">${downloadActionIcon('dismiss')}</button>`;
   return `<div class="download-episode sf-dl-episode" data-download-episode="${entry.id}">
     <div class="sf-dl-episode-name">Episode ${String(entry.episode).padStart(2,'0')}<span class="sf-dl-release">${escapeHTML(entry.release)} · ${escapeHTML(entry.audio)}</span></div>
     <div class="sf-dl-episode-status" data-status="${entry.status}"><span class="sf-dl-dot" aria-hidden="true"></span>${escapeHTML(entry.status)}</div>
     <div class="sf-dl-episode-track">${downloadProgressTrack(entry.progress,`${anime.name} · Episode ${entry.episode} progress`)}</div>
     <div class="sf-dl-episode-control">${playPause}${retry||(!playPause?'<span class="sf-dl-control-spacer" aria-hidden="true"></span>':'')}</div>
     <span class="sf-dl-episode-percent">${entry.progress}%</span>
     <div class="sf-dl-episode-quick">${quick}</div>
    </div>`;
  }).join('');
  return `<section class="download-group sf-dl-card ${expanded?'is-expanded':''}" data-download-group="${escapeHTML(id)}" data-download-state="${groupStatus[0]}" aria-label="${escapeHTML(anime.name)} downloads">
    <div class="download-group-top sf-dl-card-top"><button type="button" class="download-group-toggle sf-dl-summary" data-download-toggle="${escapeHTML(id)}" aria-expanded="${expanded}" aria-controls="${bodyId}">
      <span class="sf-dl-cover" style="background:${anime.art}" aria-hidden="true"><span class="sf-dl-cover-ring"></span><span class="sf-dl-cover-label">${escapeHTML(anime.name.split(' ').map(part=>part[0]).slice(0,2).join('').toUpperCase())}</span></span>
      <span class="sf-dl-main"><span class="sf-dl-title">${escapeHTML(anime.name)}</span><span class="sf-dl-summary-line">${escapeHTML(downloadStatusSummary(allEntries))}</span>
        <span class="sf-dl-series-progress">${downloadProgressTrack(progress,`${anime.name} · overall download progress (weighted by file size)`)}<span class="sf-dl-series-percent">${progress}%</span></span>
      </span>
      <span class="sf-dl-right"><span class="sf-dl-status-badge" data-status="${groupStatus[0]}"><span class="sf-dl-dot" aria-hidden="true"></span>${groupStatus[1]}</span><span class="download-group-chevron sf-dl-chevron" aria-hidden="true">${icon('chevron',18)}</span></span>
    </button></div>
    <div class="download-group-body sf-dl-body" id="${bodyId}"><div class="download-group-body-inner sf-dl-body-inner" ${expanded?'':'inert aria-hidden="true"'}>
      ${matched.length===allEntries.length?'':`<p class="download-matched-count">Showing ${matched.length} of ${allEntries.length} notifications</p>`}
      <div class="sf-dl-viewport gallery-episode-scroll" data-scroll-group="${escapeHTML(id)}" role="region" tabindex="0" aria-label="Episodes of ${escapeHTML(anime.name)}">${episodes}</div>
      <p class="sf-dl-action-hint" aria-hidden="true">${downloadActionIcon('dismiss')} Hover over an episode to reveal Dismiss or Cancel. Tab to the action to use it with a keyboard.</p>
    </div></div></section>`;
 }).filter(Boolean).join('');
 const pending=all.some(entry=>entry.status==='Downloading'||entry.status==='Queued');
 return `${pageHeader('Downloads',actions,filters,'downloads')}
  <div class="sf-dl-list-heading">${isSearching?'Search results':'Grouped by series'}<span>${isSearching?'Matching download notifications':'Select a series to view its episodes'}</span></div>
  <section class="downloads-list download-groups sf-dl-list" aria-label="Grouped download notifications">${groups||(isSearching?'<div class="search-empty">No matching download notifications.</div>':'<div class="empty">No download notifications match this filter.</div>')}
   <div class="demo-download-footer"><p class="tip">Demonstration only · Download statuses and file sizes are fictional. Retry requeues failed episodes; dismiss only clears notifications, never files. Pause and Resume control simulated transfers. No files are downloaded or searched.</p><div class="demo-download-actions"><button type="button" class="demo-download-control" id="demo-next-download" ${pending?'':'disabled'}>Simulate next step</button><button type="button" class="demo-download-control" id="demo-reset-downloads">Reset demo</button></div></div>
  </section>`;
}

