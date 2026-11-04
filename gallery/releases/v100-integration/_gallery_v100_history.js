/* Gallery v100 · Watch History integrated from approved Layout Experiment 03.
 * UI demo records remain clearly labeled samples; local-video playback can additionally
 * produce local browser-preview records. No provider streams are fabricated. */
const whStorageKey='gallery.watchHistory.v100.preview';
function whMakeEpisodes(count, watchedCount=0, partialEpisode=null, partialSeconds=0, duration=1440){
 return Array.from({length:count},(_,i)=>{const n=i+1,watched=n<=watchedCount;return {n,watched,started:watched||n===partialEpisode,progressSeconds:watched?duration:(n===partialEpisode?partialSeconds:0),duration};});
}
const whSeed=[
 {id:'q2',library:true,group:'quints',galleryId:'demo:quints',installmentId:'quints-s2',title:'The Quintessential Quintuplets ∬',short:'Quints ∬',cover:'linear-gradient(145deg,#413759,#7e6694 48%,#cda1ba)',last:'2026-11-04',dates:['2026-11-04','2026-11-03'],episodes:whMakeEpisodes(12,7,8,872)},
 {id:'pkm',library:false,group:'pokemon',galleryId:null,installmentId:'pokemon-ind',title:'Pokémon — Indigo League',short:'Pokémon',cover:'linear-gradient(145deg,#285886,#5c8cc6 52%,#f4c36e)',last:'2026-11-03',dates:['2025-06-21','2026-11-03'],episodes:whMakeEpisodes(100,74,75,608,1320)},
 {id:'frieren',library:true,group:'frieren',galleryId:null,installmentId:'frieren-s1',title:"Frieren: Beyond Journey's End",short:'Frieren',cover:'linear-gradient(147deg,#3f6569,#8cbcb4 48%,#b9bd95)',last:'2026-10-30',dates:['2026-10-30'],episodes:whMakeEpisodes(28,16,17,914)},
 {id:'q1',library:true,group:'quints',galleryId:'demo:quints',installmentId:'quints-s1',title:'The Quintessential Quintuplets',short:'Quints',cover:'linear-gradient(145deg,#533a60,#b67f9b 52%,#ebbaa4)',last:'2026-10-28',dates:['2025-06-19','2026-10-28'],episodes:whMakeEpisodes(12,12)},
 {id:'solo',library:false,group:'solo',galleryId:'demo:solo',installmentId:'solo-s1',title:'Solo Leveling',short:'Solo',cover:'linear-gradient(148deg,#121b36,#49618e 49%,#8b6ab1)',last:'2026-09-12',dates:['2026-09-12'],episodes:whMakeEpisodes(12,8,9,430)},
 {id:'violet',library:true,group:'violet',galleryId:null,installmentId:'violet-s1',title:'Violet Evergarden',short:'Violet',cover:'linear-gradient(145deg,#465b8a,#7b99ba 51%,#cfb69b)',last:'2025-08-20',dates:['2025-08-20'],episodes:whMakeEpisodes(13,13)},
 {id:'moon',library:false,group:'moon',galleryId:'demo:01',installmentId:'moon-s1',title:'Moonlit Signals 2025',short:'Moonlit',cover:'linear-gradient(145deg,#322554,#74548f 51%,#c48b9c)',last:'2026-01-15',dates:['2026-01-15'],episodes:whMakeEpisodes(12,3,4,319)},
 {id:'aot',library:true,group:'aot',galleryId:'demo:aot',installmentId:'aot-final',title:'Attack on Titan: The Final Season',short:'AoT',cover:'linear-gradient(150deg,#334447,#697b77 50%,#958c76)',last:'2025-04-10',dates:['2025-04-10'],episodes:whMakeEpisodes(16,9,10,611)},
 {id:'astra',library:false,group:'astra',galleryId:'demo:02',installmentId:'astra-s1',title:'Astra Afterlight',short:'Astra',cover:'linear-gradient(145deg,#213654,#386e88 50%,#88c2c1)',last:'2024-12-16',dates:['2024-12-16'],episodes:whMakeEpisodes(12,12)}
];
function whLoadRecords(){
 try{const saved=JSON.parse(localStorage.getItem(whStorageKey));if(Array.isArray(saved)&&saved.every(r=>typeof r.id==='string'&&Array.isArray(r.episodes)))return saved;}
 catch{}
 return whSeed.map(r=>({...r,dates:[...r.dates],episodes:r.episodes.map(e=>({...e}))}));
}
let whRecords=whLoadRecords();let whOpen=false,whFilter='all',whSort='newest',whSearch='',whExpanded=new Set(),whPending=new Set();
let whInnerScrollers=new Map();
function whSave(){try{localStorage.setItem(whStorageKey,JSON.stringify(whRecords));}catch{/* Private/browser file preview may forbid storage */}}
function whCount(r){return r.episodes.reduce((n,e)=>n+(e.watched?1:0),0)}
function whCompleted(r){return r.episodes.length>0&&whCount(r)===r.episodes.length}
function whFormatDate(date){const d=new Date(date+'T12:00:00');return Number.isNaN(d.getTime())?date:d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});}
function whFmt(sec){const n=Math.max(0,Math.floor(Number(sec)||0));return `${Math.floor(n/60)}:${String(n%60).padStart(2,'0')}`;}
function whLastEpisode(r){return r.episodes.find(e=>e.n===r.latestEpisode)||[...r.episodes].reverse().find(e=>e.started)||r.episodes[0]}
function whSorted(list){return [...list].sort((a,b)=>whSort==='newest'?b.last.localeCompare(a.last):a.last.localeCompare(b.last));}
const whMonths=['january','february','march','april','may','june','july','august','september','october','november','december'];
function whSearchGroups(list){
 const q=whSearch.trim().toLowerCase();if(!q)return [{label:null,items:whSorted(list)}];
 const m=q.match(/^([a-z]+)\s+((?:19|20)\d{2})$/),month=m?whMonths.indexOf(m[1]):-1;
 const year=/^(?:19|20)\d{2}$/.test(q)?q:q==='last year'?String(new Date().getFullYear()-1):m&&month!==-1?m[2]:null;
 if(year!==null){
  const byDate=whSorted(list.filter(r=>r.dates.some(d=>d.startsWith(year)&&(month===-1||Number(d.slice(5,7))===month+1))));
  const seen=new Set(byDate.map(r=>r.id));const title=whSorted(list.filter(r=>!seen.has(r.id)&&r.title.toLowerCase().includes(q)));
  const label=month===-1?`Watched in ${year}`:`Watched in ${whMonths[month].slice(0,1).toUpperCase()+whMonths[month].slice(1)} ${year}`;
  return [{label,items:byDate},{label:'Title matches',items:title}].filter(group=>group.items.length);
 }
 return [{label:null,items:whSorted(list.filter(r=>r.title.toLowerCase().includes(q)))}];
}
function whGroups(){return whSearchGroups(whRecords.filter(r=>!whPending.has(r.id)&&(whFilter==='all'||(whFilter==='completed')===whCompleted(r))));}
function whSmallIcon(name){const glyph={
  back:'<path d="m14 6-6 6 6 6"/><path d="M8 12h12"/>',
  sort:'<path d="M8 3v18m-4-4 4 4 4-4M16 21V3m-4 4 4-4 4 4"/>',
  trash:'<path d="M4 7h16M10 4h4M6 7l1 14h10l1-14M10 11v6m4-6v6"/>',
  check:'<path d="m5 12 4 4L19 6"/>',
  completed:'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
  chevron:'<path d="m6 9 6 6 6-6"/>',
  history:'<path d="M3 12a9 9 0 1 0 2.7-6.3L3 8"/><path d="M3 3v5h5M12 7v5l4 2"/>'
 };
 return `<svg class="icon" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${glyph[name]||''}</svg>`;
}
function whPreviewMarkup(){
 const seen=new Set();const recent=[...whRecords].sort((a,b)=>b.last.localeCompare(a.last)).filter(r=>{if(seen.has(r.group))return false;seen.add(r.group);return true;});
 return `<div class="continue-shell"><div class="continue-clip"><section class="continue wh-recent" aria-label="Recently Watched">
 <div class="wh-recent-header">Recently Watched</div>
 <div class="wh-recent-row">${recent.map(r=>`<button class="wh-recent-card" type="button" data-wh-recent="${escapeHTML(r.id)}" style="--cover:${r.cover}" title="${escapeHTML(r.title)}"><span class="wh-recent-card-label">${escapeHTML(r.short)}</span><span class="wh-recent-card-detail"><strong>${escapeHTML(r.title)}</strong><span>${whCompleted(r)?'Completed':`Episode ${whLastEpisode(r).n}`}</span></span></button>`).join('')}
 <button class="wh-recent-view" type="button" id="wh-view-history">${whSmallIcon('history')}<span>View History</span></button></div></section></div></div>`;
}
function whEpisodeMarkup(r,ep){
 const status=ep.watched?'is-watched':ep.started?'is-partial':'is-never';
 const label=ep.watched?'Watched':ep.started?'Partially watched':'Not watched';
 return `<div class="wh-episode"><div class="wh-episode-main"><span class="wh-episode-number">Episode ${ep.n}</span>${ep.started&&!ep.watched?`<span class="wh-episode-position">${whFmt(ep.progressSeconds)} / ${whFmt(ep.duration)}</span>`:''}</div><button type="button" class="wh-episode-toggle" data-wh-episode="${escapeHTML(r.id)}:${ep.n}" aria-pressed="${ep.watched}" title="${ep.watched?'Unmark as Watched':'Mark as Watched'}"><span class="wh-status-icon ${status}">${ep.watched?whSmallIcon('check'):''}</span><span class="wh-episode-label">${label}</span></button></div>`;
}
function whSummaryMarkup(r){
 const watched=whCount(r),total=r.episodes.length,complete=whCompleted(r),open=whExpanded.has(r.id),pct=total?watched/total*100:0;
 const last=whLastEpisode(r);
 return `<div class="wh-summary">
 <button class="wh-cover-button" type="button" data-wh-open="${escapeHTML(r.id)}" title="Open anime details"><span class="wh-cover" style="--cover:${r.cover}"><span>${escapeHTML(r.short)}</span></span></button>
 <div class="wh-info"><button class="wh-anime-title" type="button" data-wh-open="${escapeHTML(r.id)}">${escapeHTML(r.title)}</button>
 ${complete?`<div class="wh-completed">${whSmallIcon('completed')} Completed</div>`:`<div class="wh-meta">Episode ${last?.n||1} · ${whFmt(last?.progressSeconds)} / ${whFmt(last?.duration)}</div><div class="wh-meta">${watched} of ${total} episodes watched</div><div class="wh-progress" aria-hidden="true"><div class="wh-progress-done" style="width:calc(${pct}% - ${pct>0&&pct<100?'3px':'0px'})"></div>${pct<100?'<div class="wh-progress-rest"></div>':''}</div>`}
 <div class="wh-meta">Last watched ${whFormatDate(r.last)}</div></div>
 <div class="wh-actions"><button class="wh-action wh-expand" type="button" data-wh-expand="${escapeHTML(r.id)}" aria-expanded="${open}" aria-label="${open?'Collapse':'Expand'} episodes for ${escapeHTML(r.title)}" title="${open?'Collapse episodes':'Manage watched episodes'}">${whSmallIcon('chevron')}</button><button class="wh-action wh-trash" type="button" data-wh-remove="${escapeHTML(r.id)}" aria-label="Remove ${escapeHTML(r.title)} from history" title="Remove from history">${whSmallIcon('trash')}</button></div>
 </div>`;
}
function whRowMarkup(r){const open=whExpanded.has(r.id);return `<section class="wh-season ${open?'is-expanded':''}" data-wh-row="${escapeHTML(r.id)}" aria-label="${escapeHTML(r.title)}">${whSummaryMarkup(r)}${open?`<div class="wh-episodes"><div class="wh-episode-head"><strong>Episodes</strong><span>${whCount(r)} / ${r.episodes.length} watched</span></div><div class="wh-episode-shell" data-wh-shell="${escapeHTML(r.id)}"><div class="wh-episode-scroll" role="region" tabindex="0" aria-label="Scrollable episodes for ${escapeHTML(r.title)}">${r.episodes.map(ep=>whEpisodeMarkup(r,ep)).join('')}</div><div class="wh-inner-overlay" aria-hidden="true"><div class="wh-inner-thumb"></div></div></div><p class="wh-episode-hint">Mark or unmark individual episodes here. Saved playback position is kept separately.</p></div>`:''}</section>`;}
function whPageMarkup(){
 const groups=whGroups(),total=groups.reduce((n,g)=>n+g.items.length,0),removed=whRecords.filter(r=>whPending.has(r.id));
 return `<section id="wh-root" aria-label="Watch History">
 <button type="button" class="wh-back" data-wh-exit>${whSmallIcon('back')} Discover</button>
 <h1 class="wh-title">Watch History</h1><p class="wh-caption">Your viewing history, one entry per anime season.</p><div class="wh-header-rule"></div>
 <div class="wh-controls"><div class="wh-segmented" role="group" aria-label="Filter Watch History">${[['all','All'],['progress','In Progress'],['completed','Completed']].map(([name,label])=>`<button type="button" data-wh-filter="${name}" aria-pressed="${whFilter===name}">${label}</button>`).join('')}</div>
 <button type="button" class="wh-sort" data-wh-sort title="Reverse watch history sorting">${whSmallIcon('sort')} ${whSort==='newest'?'Newest First':'Oldest First'}</button></div>
 ${removed.length?`<aside class="wh-undo" aria-label="Pending removals"><div class="wh-undo-top"><div><strong>${removed.length} ${removed.length===1?'season':'seasons'} removed from view</strong><div class="wh-undo-hint">Undo is available until you leave Watch History.</div></div><button type="button" class="btn small" data-wh-undo-all>Undo all</button></div><div class="wh-undo-items">${removed.map(r=>`<div class="wh-undo-item"><span>${escapeHTML(r.title)}</span><button type="button" data-wh-undo="${escapeHTML(r.id)}" aria-label="Undo removal of ${escapeHTML(r.title)}">Undo</button></div>`).join('')}</div></aside>`:''}
 <div class="wh-result-count">${total} ${total===1?'season':'seasons'} ${whSearch?'matching your search':'in this view'}</div>
 ${total?groups.map(g=>`${g.label?`<div class="wh-match-heading">${escapeHTML(g.label)}</div>`:''}<div class="wh-list">${g.items.map(whRowMarkup).join('')}</div>`).join(''):`<div class="wh-empty">Nothing to show. ${whSearch?'Try a different title or viewing date.':'Try another filter, or undo a removal.'}</div>`}
 <div class="wh-prototype-note">Gallery v100 design preview: the initial history entries and covers are sample data for testing the UI. Actual source streaming isn't yet connected in this HTML prototype. When a supported local video plays, this preview can record its progress on this device.</div>
 </section>`;
}
function whAttachInner(area,overlay){
 const thumb=overlay.querySelector('.wh-inner-thumb');let timer=null,dragging=false,dragY=0,dragTop=0,intent=0;
 const update=()=>{const max=area.scrollHeight-area.clientHeight,track=overlay.clientHeight;if(max<=1||track<=0){overlay.classList.remove('is-visible');return false}const h=Math.min(track,Math.max(40,Math.round(track*area.clientHeight/area.scrollHeight)));thumb.style.height=h+'px';thumb.style.transform=`translate3d(0,${(track-h)*area.scrollTop/max}px,0)`;return true;};
 const reveal=()=>{if(!update())return;overlay.classList.add('is-visible');clearTimeout(timer);timer=setTimeout(()=>{if(!dragging)overlay.classList.remove('is-visible');},950);};
 const intentScroll=()=>{intent=performance.now()+1400;reveal();};
 const onScroll=()=>{update();if(performance.now()<intent||dragging)reveal();};
 const onKey=e=>{if(['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(e.key))intentScroll();};
 const down=e=>{if(e.button!==0||!update())return;e.preventDefault();dragging=true;dragY=e.clientY;dragTop=area.scrollTop;overlay.classList.add('is-dragging','is-visible');clearTimeout(timer);thumb.setPointerCapture(e.pointerId);};
 const move=e=>{if(!dragging)return;const distance=overlay.clientHeight-thumb.getBoundingClientRect().height,max=area.scrollHeight-area.clientHeight;if(distance>0)area.scrollTop=dragTop+(e.clientY-dragY)*max/distance;reveal();};
 const up=()=>{if(!dragging)return;dragging=false;overlay.classList.remove('is-dragging');reveal();};
 area.addEventListener('wheel',intentScroll,{passive:true});area.addEventListener('touchmove',intentScroll,{passive:true});area.addEventListener('scroll',onScroll,{passive:true});area.addEventListener('keydown',onKey);
 thumb.addEventListener('pointerdown',down);thumb.addEventListener('pointermove',move);thumb.addEventListener('pointerup',up);thumb.addEventListener('pointercancel',up);thumb.addEventListener('lostpointercapture',up);
 return {area,update,destroy(){clearTimeout(timer);area.removeEventListener('wheel',intentScroll);area.removeEventListener('touchmove',intentScroll);area.removeEventListener('scroll',onScroll);area.removeEventListener('keydown',onKey);thumb.removeEventListener('pointerdown',down);thumb.removeEventListener('pointermove',move);thumb.removeEventListener('pointerup',up);thumb.removeEventListener('pointercancel',up);thumb.removeEventListener('lostpointercapture',up);}};
}
function whDestroyInner(){for(const scroller of whInnerScrollers.values())scroller.destroy();whInnerScrollers.clear();}
function whRender({keepScroll=true}={}){
 if(!whOpen)return;
 const old=keepScroll?workspace.scrollTop:0;
 const prevPositions=new Map([...whInnerScrollers.entries()].map(([id,scroller])=>[id,scroller.area.scrollTop]));
 whDestroyInner();screen.innerHTML=whPageMarkup();
 for(const id of whExpanded){
  const shell=[...screen.querySelectorAll('[data-wh-shell]')].find(x=>x.dataset.whShell===id);if(!shell)continue;
  const area=shell.querySelector('.wh-episode-scroll');const scroller=whAttachInner(area,shell.querySelector('.wh-inner-overlay'));whInnerScrollers.set(id,scroller);
  if(prevPositions.has(id))area.scrollTop=prevPositions.get(id);
  else {const r=whRecords.find(r=>r.id===id);const ep=r&&whLastEpisode(r);const columns=matchMedia('(max-width:820px)').matches?1:2;if(r&&r.episodes.length>6*columns&&ep)area.scrollTop=Math.max(0,(Math.floor((ep.n-1)/columns)-2)*42);}
  scroller.update();
 }
 workspace.scrollTop=old;
 requestAnimationFrame(updateTabScrollOverlay);
}
function whUpdateEpisodeInPlace(button,r,ep){
 const status=ep.watched?'is-watched':ep.started?'is-partial':'is-never';
 const label=ep.watched?'Watched':ep.started?'Partially watched':'Not watched';
 button.setAttribute('aria-pressed',String(ep.watched));button.title=ep.watched?'Unmark as Watched':'Mark as Watched';
 const mark=button.querySelector('.wh-status-icon');mark.className='wh-status-icon '+status;mark.innerHTML=ep.watched?whSmallIcon('check'):'';
 button.querySelector('.wh-episode-label').textContent=label;
 const main=button.closest('.wh-episode').querySelector('.wh-episode-main');let position=main.querySelector('.wh-episode-position');
 if(ep.started&&!ep.watched){if(!position){position=document.createElement('span');position.className='wh-episode-position';main.append(position)}position.textContent=`${whFmt(ep.progressSeconds)} / ${whFmt(ep.duration)}`;}else position?.remove();
 const row=button.closest('.wh-season');const replacement=document.createElement('template');replacement.innerHTML=whSummaryMarkup(r);row.querySelector('.wh-summary').replaceWith(replacement.content.firstElementChild);
 row.querySelector('.wh-episode-head span').textContent=`${whCount(r)} / ${r.episodes.length} watched`;
 // No rebuild of episode panel; its scrollbar, selected control and scroll position stay stationary.
}
function whEnter(){if(whOpen)return;if(searchOpen)closeInlineSearch(false);whOpen=true;whFilter='all';whSort='newest';whSearch='';whExpanded.clear();whPending.clear();hideTabScrollOverlay();render();workspace.scrollTop=0;}
function whExit({renderAfter=true}={}){
 if(!whOpen)return;whOpen=false;whDestroyInner();if(whPending.size){whRecords=whRecords.filter(r=>!whPending.has(r.id));whSave();}whPending.clear();whExpanded.clear();whFilter='all';whSort='newest';whSearch='';
 if(searchOpen)closeInlineSearch(false);
 if(renderAfter){render();requestAnimationFrame(updateTabScrollOverlay);}
}
function whOpenTitle(r){
 if(!r.galleryId||!demo.some(x=>x.id===r.galleryId)){
  modal('Sample Watch History entry',`<p class="description">${escapeHTML(r.title)} is a layout-testing record; this HTML version has no matching anime detail page. The Watch History entry remains editable here.</p>`,`<button class="btn primary" id="wh-sample-okay">Got it</button>`);
  document.getElementById('wh-sample-okay')?.addEventListener('click',closeModal);return;
 }
 const targetView=r.library?'library':'discover';
 whExit({renderAfter:false});state.view=targetView;updateActiveTab(targetView);showDetail(r.galleryId);state.detailReturnScroll=tabPages[targetView].scrollTop;
 const x=demo.find(x=>x.id===r.galleryId);const index=getSeasons(x).findIndex(s=>s.id===r.installmentId);
 if(index>=0){state.detailSeason=index;state.detailRelated=null;render();}
}
/* All page actions live in one delegated listener; episode toggles don't rebuild their list. */
screen.addEventListener('click',event=>{
 if(!whOpen)return;const b=event.target.closest('button');if(!b)return;
 if(b.hasAttribute('data-wh-exit')){whExit();return;}
 if(b.dataset.whFilter){whFilter=b.dataset.whFilter;whRender();return;}
 if(b.hasAttribute('data-wh-sort')){whSort=whSort==='newest'?'oldest':'newest';whRender();return;}
 if(b.dataset.whExpand){const id=b.dataset.whExpand;whExpanded.has(id)?whExpanded.delete(id):whExpanded.add(id);whRender();return;}
 if(b.dataset.whRemove){whPending.add(b.dataset.whRemove);whExpanded.delete(b.dataset.whRemove);whRender();return;}
 if(b.dataset.whUndo){whPending.delete(b.dataset.whUndo);whRender();return;}
 if(b.hasAttribute('data-wh-undo-all')){whPending.clear();whRender();return;}
 if(b.dataset.whOpen){const record=whRecords.find(r=>r.id===b.dataset.whOpen);if(record)whOpenTitle(record);return;}
 if(b.dataset.whEpisode){const divider=b.dataset.whEpisode.lastIndexOf(':'),id=b.dataset.whEpisode.slice(0,divider),n=Number(b.dataset.whEpisode.slice(divider+1));const r=whRecords.find(r=>r.id===id),ep=r?.episodes.find(ep=>ep.n===n);if(!ep)return;ep.watched=!ep.watched;whUpdateEpisodeInPlace(b,r,ep);whSave();return;}
});
/* Playback tracking is limited to a user-opened local video in the HTML preview.
 * An episode becomes Watched only by continuous active playback crossing into
 * its final 20 seconds, never because the user seeks directly into that range. */
let whPlayerSession=null;
function whInitPlayerSession(){whPlayerSession={lastTime:0,hasPlayedOutsideFinal:false,lastSavedAt:0};}
function whRecordLocalPlayback(video,markWatched=false){
 if(!state.playback||!state.detailId||!Number.isFinite(video.duration)||video.duration<=0)return;
 const anime=demo.find(x=>x.id===state.detailId),installment=anime&&activeInstallment(anime);if(!anime||!installment)return;
 const id='local:'+anime.id+':'+String(installment.id||installment.label||'s1');let rec=whRecords.find(r=>r.galleryId===anime.id&&r.installmentId===(installment.id||null))||whRecords.find(r=>r.id===id);
 if(!rec){
  rec={id,group:anime.id,library:state.view==='library',galleryId:anime.id,installmentId:installment.id||null,title:installmentDisplayName(anime,installment),short:anime.name.split(' ').slice(0,2).join(' '),cover:anime.art,last:'',dates:[],latestEpisode:state.playback.episode,episodes:whMakeEpisodes(installment.total||1)};
  whRecords.unshift(rec);
 }
 const n=state.playback.episode;let ep=rec.episodes.find(e=>e.n===n);if(!ep){ep={n,watched:false,started:false,progressSeconds:0,duration:Math.floor(video.duration)};rec.episodes.push(ep);rec.episodes.sort((a,b)=>a.n-b.n);}
 ep.started=true;ep.duration=Math.floor(video.duration);ep.progressSeconds=Math.floor(video.currentTime);if(markWatched)ep.watched=true;
 rec.latestEpisode=n;
 const now=new Date(),day=[now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');
 rec.last=day;if(!rec.dates.includes(day))rec.dates.push(day);
 whSave();
}
function whOnVideoTick(video){
 if(!whPlayerSession||video.paused||video.seeking||!Number.isFinite(video.duration)||video.duration<=0)return;
 const current=video.currentTime,threshold=Math.max(0,video.duration-20),past=whPlayerSession.lastTime;
 if(current<threshold)whPlayerSession.hasPlayedOutsideFinal=true;
 const completed=whPlayerSession.hasPlayedOutsideFinal&&past<threshold&&current>=threshold&&current-past<3;
 if(completed||current-whPlayerSession.lastSavedAt>=3||!whPlayerSession.lastSavedAt){whRecordLocalPlayback(video,completed);whPlayerSession.lastSavedAt=current;}
 whPlayerSession.lastTime=current;
}
function whOnVideoSeek(video){if(!whPlayerSession)return;whPlayerSession.lastTime=video.currentTime;whPlayerSession.hasPlayedOutsideFinal=false;}
