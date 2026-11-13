function connectedFor(x){return connectedMetadata[x.id]||null;}
function getRelated(x){return connectedFor(x)?.related||[];}
function activeInstallment(x){const related=getRelated(x);return state.detailRelated?related.find(r=>r.id===state.detailRelated):getSeasons(x)[state.detailSeason];}
function seasonTagList(x,season){if(!season?.id)return x.tags;return state.seasonTags[season.id]??(season.id==='solo-s1'?['Watching']:season.id==='solo-s2'?['Plan to Watch']:[]);}
function installmentDisplayName(x,s){return s.title||x.name;}
function installmentSubLabel(s){return s.kind?`${s.kind} · ${s.year}`:s.label;}
function getSeasons(x){
 if(connectedFor(x))return connectedFor(x).seasons;
 if(x.id==='demo:01')return [
  {id:'moon-s1',title:'Moonlit Signals',label:'Season 1',total:12,status:'Completed',sub:12,dub:8,year:'2025',sourceMatched:true,watched:5,downloaded:2},
  {id:'moon-s2',title:'Moonlit Signals',label:'Season 2',total:10,status:'Ongoing',sub:6,dub:2,year:'2026',sourceMatched:true,watched:0,downloaded:0}
 ];
 if(x.id==='demo:04')return [{label:'Season 1',total:13,status:'Completed',sub:13,dub:null,year:'2024'}];
 const supportsSub=x.lang.includes('Sub'),supportsDub=x.lang.includes('Dub');
 const available=x.status==='Ongoing'?Math.max(1,Math.ceil(x.episodes*.63)):x.episodes;
 const dubCount=supportsDub?(x.status==='Ongoing'?Math.max(0,available-2):x.episodes):0;
 return [{label:'Season 1',total:x.episodes,status:x.status,sub:supportsSub?available:0,dub:dubCount,year:x.status==='Ongoing'?'2026':'2025'}];
}
function availabilityText(count,total){return count===null?'Unknown':`${count} / ${total}`;}
function episodeAvailability(season,n){return {sub:season.sub!==null?n<=season.sub:null,dub:season.dub!==null?n<=season.dub:null};}
function audioName(lang){return lang==='dub'?'English (Dub)':'Japanese (Sub)';}
function installmentReleaseYear(item){
 // Use only the year recorded for the installment; undated/"Various" records
 // go after dated releases rather than inventing a release date.
 const match=String(item.year||'').match(/^\d{4}/);
 return match?Number(match[0]):Number.POSITIVE_INFINITY;
}
function installmentRail(x){
 const seasons=getSeasons(x),related=getRelated(x);
 if(seasons.length+related.length<=1)return '';
 // One continuous, chronological strip. Preserve each item's original
 // identity, so a movie or special never becomes a synthetic TV season.
 const releases=[
   ...seasons.map((item,index)=>({...item,_index:index,_kind:'season',_sourceOrder:index})),
   ...related.map((item,index)=>({...item,_kind:'related',_sourceOrder:seasons.length+index}))
 ].sort((a,b)=>installmentReleaseYear(a)-installmentReleaseYear(b)||a._sourceOrder-b._sourceOrder);
 const totals={};
 for(const item of releases)if(item._kind==='related')totals[item.kind]=(totals[item.kind]||0)+1;
 const counters={};
 const cards=releases.map(item=>{
   const current=item._kind==='season'?!state.detailRelated&&item._index===state.detailSeason:state.detailRelated===item.id;
   const title=installmentDisplayName(x,item);
   let label;
   if(item._kind==='season')label=`${item.label}${item.year?' · '+item.year:''}`;
   else {
     const type=item.kind||'Special';
     counters[type]=(counters[type]||0)+1;
     label=`${type}${totals[type]>1?' '+counters[type]:''}${item.year&&item.year!=='Various'?' · '+item.year:''}`;
   }
   return `<button type="button" class="inline-installment-card" data-inline-installment="${escapeHTML(item.id||'')}" data-inline-index="${item._index??''}" data-inline-kind="${item._kind}" aria-current="${current}" aria-label="${escapeHTML(title)}, ${escapeHTML(label)}${current?', selected':''}"><span class="installment-copy"><span class="installment-name">${escapeHTML(title)}</span><span class="installment-number">${escapeHTML(label)}</span></span></button>`;
 }).join('');
 return `<nav class="inline-installments" aria-label="Releases in chronological order"><div class="inline-release-viewport"><div class="inline-installment-rail" id="inline-installment-rail" aria-label="Releases in chronological order" tabindex="0">${cards}</div><div class="inline-release-fade inline-release-fade-left" aria-hidden="false"><button type="button" class="inline-arrow previous" data-inline-scroll="-1" aria-label="Scroll releases one card left" title="Previous release" disabled>${icon('chevron',17)}</button></div><div class="inline-release-fade inline-release-fade-right" aria-hidden="false"><button type="button" class="inline-arrow" data-inline-scroll="1" aria-label="Scroll releases one card right" title="Next release" disabled>${icon('chevron',17)}</button></div></div></nav>`;
}
let activeInstallmentRailObserver=null;
function refreshInstallmentArrows(){
 const rail=screen.querySelector('#inline-installment-rail');
 const viewport=rail?.closest('.inline-release-viewport');
 if(!rail||!viewport)return;
 const maxScroll=Math.max(0,rail.scrollWidth-rail.clientWidth);
 const left=maxScroll>3&&rail.scrollLeft>2;
 const right=maxScroll>3&&rail.scrollLeft<maxScroll-2;
 // A scrolling arrow can vanish under a stationary cursor on the final card.
 // Keep an INVISIBLE full-height hit shield until the pointer leaves the edge.
 const guardLeft=!left&&viewport.dataset.pointerLeft==='true';
 const guardRight=!right&&viewport.dataset.pointerRight==='true';
viewport.classList.toggle('guard-left',guardLeft);
 viewport.classList.toggle('guard-right',guardRight);
 viewport.classList.toggle('can-left',left);
 viewport.classList.toggle('can-right',right);
 const previous=viewport.querySelector('[data-inline-scroll="-1"]');
 const next=viewport.querySelector('[data-inline-scroll="1"]');
 if(previous)previous.disabled=!(left||guardLeft);
 if(next)next.disabled=!(right||guardRight);
}
function setupInstallmentEdgeGuards(viewport){
 if(!viewport)return;
 for(const side of ['left','right']){
   const fade=viewport.querySelector('.inline-release-fade-'+side);
   if(!fade)continue;
   const prop=side==='left'?'pointerLeft':'pointerRight';
   fade.addEventListener('pointerenter',event=>{
     if(event.pointerType==='touch')return;
     viewport.dataset[prop]='true';
     refreshInstallmentArrows();
   });
   fade.addEventListener('pointerleave',()=>{
     viewport.dataset[prop]='false';
     refreshInstallmentArrows();
   });
 }
}
/* Update only release-dependent sections; the rail itself never gets
   destroyed, so its scroll position, pointer target and buttons survive. */
function selectInlineInstallment(card,rail){
 if(card.getAttribute('aria-current')==='true')return;
 const savedScroll=workspace.scrollTop;
 if(card.dataset.inlineKind==='season'){
   state.detailSeason=Number(card.dataset.inlineIndex);
   state.detailRelated=null;
 }else state.detailRelated=card.dataset.inlineInstallment;
 state.detailEpisode=1;
 // Keep All/Playable-only while moving among releases of the same anime.
 // Opening a different anime still starts at All (see showDetail).
 const template=document.createElement('div');
 template.innerHTML=detailPage();
 const newDetail=template.querySelector('.anime-detail');
 if(!newDetail)return;
 // The release rail remains the actual, mounted DOM element.
 for(const selector of ['.detail-overview','.detail-control-panel']){
   const oldPart=screen.querySelector(selector);
   const newPart=newDetail.querySelector(selector);
   if(oldPart&&newPart)oldPart.replaceWith(newPart);
 }
 const section=screen.querySelector('.detail-section');
 const newSection=newDetail.querySelector('.detail-section');
 if(section&&newSection){
   const releaseNav=section.querySelector('.inline-installments');
   section.replaceChildren(releaseNav,...Array.from(newSection.children).filter(node=>!node.classList.contains('inline-installments')));
 }
 for(const release of rail.querySelectorAll('.inline-installment-card')){
   const selected=release===card;
   release.setAttribute('aria-current',String(selected));
   const name=release.getAttribute('aria-label').replace(/, selected$/,'');
   release.setAttribute('aria-label',name+(selected?', selected':''));
 }
 // Controls inside the replaced sections require their own event handlers.
 document.getElementById('manage-detail-tags')?.addEventListener('click',showManageDetailTags);
 document.getElementById('find-source')?.addEventListener('click',showFindSource);
 for(const el of screen.querySelectorAll('[data-detail-audio]'))el.addEventListener('click',()=>{
   if((state.detailAudio||state.defaultPlayback)!==el.dataset.detailAudio)changeDetailAudio(el.dataset.detailAudio);
 });
 bindEpisodeFiltersAndActions();
 for(const el of screen.querySelectorAll('.detail-actions [data-episode-action]'))el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
 workspace.scrollTop=savedScroll;
 requestAnimationFrame(updateTabScrollOverlay);
}

// v27 — Update playback availability in place when changing Sub/Dub.
// A full screen render would destroy the old selected button and its ::before
// before CSS could animate it from opacity 1 to opacity 0.

/* v38 — Keep the count mounted when filtering so the count and its
   divider can fade rather than snapping in with a newly created toolbar. */
function syncEpisodeToolbar(updated){
 const current=screen.querySelector('.episode-toolbar');
 if(!current||!updated)return;
 const oldValues=current.querySelectorAll('.availability-value');
 const newValues=updated.querySelectorAll('.availability-value');
 for(let i=0;i<Math.min(oldValues.length,newValues.length);i++)
   oldValues[i].textContent=newValues[i].textContent;
 const oldCount=current.querySelector('.episode-shown');
 const newCount=updated.querySelector('.episode-shown');
 if(oldCount&&newCount){
   const hidden=newCount.classList.contains('is-hidden');
   if(!hidden)oldCount.textContent=newCount.textContent;
   oldCount.classList.toggle('is-hidden',hidden);
   if(hidden){oldCount.setAttribute('aria-hidden','true');oldCount.removeAttribute('role');}
   else{oldCount.removeAttribute('aria-hidden');oldCount.setAttribute('role','status');}
 }
 // Replace only the filter control (not its surrounding box) so fresh
 // click handlers can be attached without duplicating listeners.
 const oldFilter=current.querySelector('.episode-filter');
 const newFilter=updated.querySelector('.episode-filter');
 if(oldFilter&&newFilter)oldFilter.replaceWith(newFilter);
}
function changeEpisodeFilter(next){
 if(state.detailEpisodeFilter===next)return;
 const y=workspace.scrollTop;
 state.detailEpisodeFilter=next;
 const holder=document.createElement('div');
 holder.innerHTML=detailPage();
 syncEpisodeToolbar(holder.querySelector('.episode-toolbar'));
 const currentList=screen.querySelector('.episode-list');
 const updatedList=holder.querySelector('.episode-list');
 if(currentList&&updatedList)currentList.replaceWith(updatedList);
 bindEpisodeFiltersAndActions();
 workspace.scrollTop=y;
 requestAnimationFrame(updateTabScrollOverlay);
}
function bindEpisodeFiltersAndActions(){
 for(const el of screen.querySelectorAll('[data-episode-filter]')){
   el.addEventListener('click',()=>changeEpisodeFilter(el.dataset.episodeFilter));
 }
 for(const el of screen.querySelectorAll('.episode-list [data-episode-action]')){
   el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
 }
}

function changeDetailAudio(next){
 const toggle=screen.querySelector('.detail-audio-toggle');
 if(!toggle || (state.detailAudio||state.defaultPlayback)===next)return;
 const scroll=workspace.scrollTop;
 state.detailAudio=next;
 // Build the new markup offscreen so other episode controls update immediately,
 // while the original toggle retains its DOM identity and animation state.
 const container=document.createElement('div');
 container.innerHTML=detailPage();
 const updatedToggle=container.querySelector('.detail-audio-toggle');
 for(const lang of ['sub','dub']){
   const current=toggle.querySelector(`[data-detail-audio="${lang}"]`);
   const updated=updatedToggle?.querySelector(`[data-detail-audio="${lang}"]`);
   if(!current||!updated)continue;
   for(const attr of ['aria-label','title'])current.setAttribute(attr,updated.getAttribute(attr));
   current.setAttribute('aria-pressed',String(lang===next));
 }
 toggle.dataset.active=next;
 // The selected button owns its gradient; no shared indicator follows the pointer.
 // These pieces depend on playback language. Replacing them, rather than the
 // whole detail page, also keeps the user's scroll position and hover animation.
 syncEpisodeToolbar(container.querySelector('.episode-toolbar'));
 for(const selector of ['.detail-actions','.episode-list']){
   const current=screen.querySelector(selector);
   const updated=container.querySelector(selector);
   if(current && updated)current.replaceWith(updated);
 }
 document.getElementById('manage-detail-tags')?.addEventListener('click',showManageDetailTags);
 for(const el of screen.querySelectorAll('.detail-actions [data-episode-action]'))
   el.addEventListener('click',()=>showEpisodeAction(el.dataset.episodeAction,Number(el.dataset.episode)));
 bindEpisodeFiltersAndActions();
 workspace.scrollTop=scroll;
 toggle.querySelector(`[data-detail-audio="${next}"]`)?.focus({preventScroll:true});
 requestAnimationFrame(updateTabScrollOverlay);
}

// Informational language availability: labels are not actions.
// Null means unchecked, never "unavailable"; omit that marker until a provider confirms a result.
function episodeAudioIndicator(kind,available){
 if(available===null)return '';
 const isSub=kind==='sub';
 const word=isSub?'Sub':'Dub';
 const typeSvg=isSub
  ? '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M7.5 10h4m-4 4h3m3-4h3m-3 4h3"/>'
  : '<path d="M4 11a8 8 0 0 1 16 0v7a2 2 0 0 1-2 2h-1v-7h3M4 13h3v7H6a2 2 0 0 1-2-2v-7"/>';
 const stateSvg=available
  ? '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>'
  : '<circle cx="12" cy="12" r="9"/><path d="M8 12h8"/>';
 const name=isSub?'Japanese audio / subtitles':'English dub';
 const status=available?'available':'unavailable';
 const svg=path=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${path}</svg>`;
 return `<span class="audio-flag ${available?'available':'unavailable'}" role="img" aria-label="${name} ${status}" title="${name}: ${status}">${svg(typeSvg)}<span>${word}</span><span class="audio-state-icon">${svg(stateSvg)}</span></span>`;
}

function detailPage(){
 const x=demo.find(d=>d.id===state.detailId);if(!x)return '';
 const seasons=getSeasons(x);const si=Math.max(0,Math.min(state.detailSeason,seasons.length-1));
 const s=activeInstallment(x)||seasons[si];const related=Boolean(state.detailRelated);
 const sourceMatched=s.sourceMatched!==false;
 const targetEpisode=Math.max(1,Math.min((Number.isFinite(s.watched)?s.watched:0)+1,s.total)); // Top Watch resumes the next unwatched episode; individual row actions use their own episode.
 const targetAvail=sourceMatched?episodeAvailability(s,targetEpisode):{sub:null,dub:null};
 const audio=state.detailAudio||state.defaultPlayback;
 const canWatch=sourceMatched&&targetAvail[audio]===true;
 const audioOption=(lang,label)=>{
   const available=targetAvail[lang];const status=sourceMatched?(available===true?'available':available===false?'unavailable':'unverified'):'source not matched';
   const info=`${lang==='sub'?'Japanese':'English'} audio · ${status} for ${s.kind||s.label}, episode ${targetEpisode}${state.defaultPlayback===lang?' · your default':''}`;
   return `<button type="button" data-detail-audio="${lang}" aria-pressed="${audio===lang}" aria-label="${escapeHTML(info)}" title="${escapeHTML(info)}">${label}</button>`;
 };
 const audioControl=`<div class="detail-audio-control"><div class="detail-audio-toggle" data-active="${audio}" role="group" aria-label="Audio version for playback">${audioOption('sub','Sub')}${audioOption('dub','Dub')}</div></div>`;
 const playableCount=sourceMatched?Array.from({length:s.total},(_,i)=>episodeAvailability(s,i+1)[audio]===true).filter(Boolean).length:0;
 const playableOnly=state.detailEpisodeFilter==='playable';
 const episodeFilter=sourceMatched?`<div class="episode-filter" role="group" aria-label="Filter episodes by playback availability"><button type="button" data-episode-filter="all" aria-pressed="${!playableOnly}">All</button><button type="button" data-episode-filter="playable" aria-pressed="${playableOnly}" title="Show episodes playable in ${audio==='sub'?'Sub':'Dub'}">Playable only</button></div>`:'';
 const visibleEpisodeNumbers=sourceMatched?Array.from({length:s.total},(_,i)=>i+1).filter(n=>!playableOnly||episodeAvailability(s,n)[audio]===true):[];
 const entries=sourceMatched?(visibleEpisodeNumbers.length?visibleEpisodeNumbers.map(n=>{
 const i=n-1,avail=episodeAvailability(s,n),active=avail.sub===true||avail.dub===true;
 const selectedAudioAvailable=avail[audio]===true;
 const name=(s.id==='moon-s1'?seasonStories[x.id]?.[i]:null)||`Episode ${n}`;
 const stateText=selectedAudioAvailable?'Ready in '+(audio==='sub'?'Sub':'Dub'):
   active?'Not in '+(audio==='sub'?'Sub':'Dub')+' · other audio available':
   (avail.sub===null||avail.dub===null)?'Checking audio availability':'Not available yet';
 return `<div class="episode-item ${!selectedAudioAvailable?'episode-not-playable':''}" role="listitem"><span class="episode-no">${String(n).padStart(2,'0')}</span><div class="episode-copy"><div class="episode-name">${escapeHTML(name)}</div><div class="episode-subtext">${escapeHTML(stateText)}</div></div><div class="episode-tools"><div class="episode-flags" aria-label="Audio availability">${episodeAudioIndicator('sub',avail.sub)}${episodeAudioIndicator('dub',avail.dub)}</div><div class="episode-actions"><button class="iconbtn" type="button" data-episode-action="watch" data-episode="${n}" ${!selectedAudioAvailable?'disabled':''} aria-label="Watch ${escapeHTML(x.name)} ${escapeHTML(s.label||s.kind)} episode ${n}" title="${selectedAudioAvailable?`Watch episode ${n} · ${audioName(audio)}`:`${audioName(audio)} unavailable or unverified for episode ${n}`} ">${icon('play',18)}</button><button class="iconbtn" type="button" data-episode-action="download" data-episode="${n}" ${!active?'disabled':''} aria-label="Download ${escapeHTML(x.name)} ${escapeHTML(s.label||s.kind)} episode ${n}" title="Download episode ${n}">${icon('download',17)}</button></div></div></div>`;
 }).join('<div class="episode-divider" aria-hidden="true"></div>'):'<div class="episode-empty-filter">No episodes are currently confirmed playable in this audio version. Choose <strong>All</strong> to see every episode, or switch the audio option above.</div>'):'<div class="provider-unmatched">'+icon('info',19)+'<div><strong>No streaming source matched</strong><p>This installment is linked through the example relationship graph, but no provider entry is confirmed. The app must not invent episodes or assume a Sub/Dub version is available.</p></div><button class="btn" type="button" id="find-source">Find source</button></div>';
 const seasonInfo=related?`${escapeHTML(s.kind)} · Related release`:`${escapeHTML(s.label)}`;
 const showInstallmentTitle=connectedFor(x)||seasons.length>1;
 const tagList=seasonTagList(x,s);
 const shownCount=visibleEpisodeNumbers.length;
 const reduced=sourceMatched&&playableOnly&&shownCount<s.total;
 const breakdown=sourceMatched?`<div class="availability episode-availability" aria-label="Episode audio availability and filtering"><div class="episode-stats"><span class="availability-label">${icon('headphones',16)} Sub <strong class="availability-value">${availabilityText(s.sub,s.total)}</strong></span><span class="availability-label">Dub <strong class="availability-value">${availabilityText(s.dub,s.total)}</strong></span><span class="episode-shown${reduced?'':' is-hidden'}" ${reduced?'role="status"':'aria-hidden="true"'}>${shownCount} of ${s.total} shown</span></div>${episodeFilter}</div>`:'';
 return `<div class="anime-detail" aria-label="Anime detail: ${escapeHTML(x.name)}">
 <header class="detail-page-header">
  <h1 class="detail-title sf-optical-title">${escapeHTML(x.name)}</h1>
  <button type="button" id="detail-back" class="detail-back">${icon('back',18)} Back to ${state.detailReturnHistory?'Watch History':state.detailReturnView==='library'?'Library':state.detailReturnView==='downloads'?'Downloads':'Discover'}</button>
 </header>
 <section class="detail-hero">
 <div class="detail-cover" style="background:${x.art}"><span class="detail-cover-name">${escapeHTML(x.name)}</span></div>
 <div class="detail-overview"><div class="detail-badges"><span class="detail-badge">${seasons.length} ${seasons.length===1?'season':'seasons'}</span><span class="detail-badge">${escapeHTML(s.year)}</span><span class="detail-badge">${s.kind==='Movie'?'Status':'Airing'}: <strong>${escapeHTML(s.status)}</strong>${related?` · ${escapeHTML(s.kind)}`:''}</span></div>
 <p class="detail-description">${escapeHTML(related?(s.note||x.blurb):x.blurb)}</p>
 <div class="detail-browsing"><span class="detail-browsing-caption">Currently browsing</span><strong>${escapeHTML(installmentSubLabel(s))} <span class="detail-browsing-sep">·</span> ${s.total} ${s.total===1?'episode':'episodes'}</strong>${Number.isInteger(s.watched)?`<span class="detail-browsing-progress">${s.watched} of ${s.total} watched <small>(demo)</small></span>`:''}</div></div>
 <aside class="detail-control-panel" aria-label="Playback and library actions">${audioControl}
 <div class="detail-actions"><button class="btn primary" type="button" aria-label="${s.kind==='Movie'?'Watch movie':`Watch episode ${targetEpisode}`}" data-episode-action="watch" data-episode="${targetEpisode}" ${!canWatch?`disabled title="${sourceMatched?'Audio unavailable or unverified':'No matched provider'}"`:''}>${icon('play',17)} <span class="detail-action-label-long">${s.kind==='Movie'?'Watch movie':`Watch episode ${targetEpisode}`}</span><span class="detail-action-label-short">Watch</span></button><button class="btn" type="button" id="manage-detail-tags" aria-label="${tagList.length?'Manage tags':'Add to Library'}">${icon('bookmark',17)} <span class="detail-action-label-long">${tagList.length?'Manage tags':'Add to Library'}</span><span class="detail-action-label-short">${tagList.length?'Tags':'Add'}</span></button></div></aside>
 </section>
 <section class="detail-section" aria-label="Episodes and availability">${installmentRail(x)}
 <div class="episode-toolbar"><div class="episode-heading"><h2>${s.kind==='Movie'?'Movie':s.kind==='Special'?'Special episodes':'Episodes'}</h2></div>${breakdown}</div>
 <div class="episode-list" role="list">${entries}</div>
 <p class="episode-note">${related?'Related releases remain separate from numbered seasons. ':'Each season has its own identity, tag assignments, and watch/download history. '}Provider availability and progress are fictional for this UI demonstration; unknown coverage is never treated as confirmed.</p>
 </section></div>`;
}
function backFromDetail(){
 transitionGalleryStage(()=>{
  state.playback=null;
  if(state.detailReturnHistory){state.detailReturnHistory=false;whResumeFromDetail();return;}
  state.detailId=null;state.view=state.detailReturnView;
  render();tabPages[state.view].scrollTop=state.detailReturnScroll;
 });
}
function startPlayback(n){
 const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const installment=activeInstallment(x);if(!installment||installment.sourceMatched===false)return;
 const audio=state.detailAudio||state.defaultPlayback;
 const availability=episodeAvailability(installment,n);
 if(availability[audio]!==true)return; // Never fall back to the other version silently.
 transitionGalleryPlayer(()=>{
  state.playbackReturnScroll=workspace.scrollTop;
  state.detailEpisode=n;
  state.playback={episode:n,audio,installmentId:installment.id,subtitles:state.defaultSubtitles};
  closeModal();render();workspace.scrollTop=0;
 });
}
function playbackPage(){
 const x=demo.find(d=>d.id===state.detailId),p=state.playback,s=x&&activeInstallment(x);
 if(!x||!s||!p)return '';
 const label=s.kind==='Movie'?'Movie':`Episode ${p.episode}`;
 const prev=playbackNeighbor(-1),next=playbackNeighbor(1);
 const autoplayNext=playerCanAdvance();
 const centerPrimary=s.kind==='Movie'?installmentDisplayName(x,s):`Episode ${p.episode}`;
 const centerSecondary=s.kind?(s.kind==='Movie'?'Movie':s.kind):s.label;
 const buttonText=(action,side)=>`<span class="nav-label-full">${escapeHTML(action.label)}</span><span class="nav-label-compact">${side==='previous'?'Previous':'Next'}</span>`;
 return `<section class="playback-page" aria-label="Gallery video player">
  <div class="playback-compactbar">
   <div class="playback-title-inline"><strong class="sf-optical-title">${escapeHTML(x.name)}</strong></div>
   <button type="button" class="detail-back" id="back-from-playback">${icon('back',18)} Back to episodes</button>
  </div>
  <div class="player-area" id="player-area" tabindex="0" aria-label="Video and controls">
   <input type="file" id="sf-player-browser-file" accept="video/*" hidden aria-label="Choose a local video to play">
   <video id="local-video" playsinline preload="metadata" aria-label="Local video playback"></video>
   <div class="sf-player-demo-scene" id="sf-player-demo-scene" hidden aria-hidden="true"><div class="sf-player-demo-horizon"></div><div class="sf-player-demo-mark">Gallery<small>Simulated playback · no media loaded</small></div></div>
   <div class="player-no-media" id="player-empty"><div class="player-empty-inner">${icon('film',35)}<strong>No streaming source connected yet</strong><p>The anime entries in this development build are examples. Open a local video file to test our actual player controls.</p><button type="button" class="btn primary" id="open-local-video">${icon('folder',16)} Open local video…</button><button type="button" class="btn sf-player-preview-button" id="sf-player-demo-start">Preview player controls</button></div></div>
   <div class="player-overlay" id="player-overlay">
    <div class="player-bottom"><div class="player-progress-row"><span class="player-time" id="current-time">00:00</span><div class="player-progress" id="timeline"><div class="player-progress-bar gallery-split-timeline"><div class="player-watched" id="watched"></div><div class="player-remaining" id="seek-remaining"></div></div><input type="range" id="seek" min="0" max="1000" value="0" aria-label="Seek within episode" disabled></div><span class="player-time" id="duration-time">00:00</span></div>
    <div class="player-controls"><div class="controls-left"><button type="button" class="player-icon" id="mute" aria-label="Mute" aria-pressed="false" title="Mute"><svg class="player-volume-icon" data-level="4" viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path class="volume-speaker" d="M4 9h4l5 -4v14l-5 -4H4z"/><path class="volume-wave volume-wave-1" d="M15.5 10.5a2.25 2.25 0 0 1 0 3"/><path class="volume-wave volume-wave-2" d="M17 8a5.2 5.2 0 0 1 0 8"/><path class="volume-wave volume-wave-3" d="M18.5 5.5a8.3 8.3 0 0 1 0 13"/><path class="volume-muted-x" d="M17.3 9.5l4.6 5m0 -5l-4.6 5"/></svg></button><input type="range" class="player-volume" id="volume" min="0" max="100" value="${playerSessionVolume}" aria-label="Volume"></div><div class="controls-middle"><button type="button" class="player-icon player-track-control" id="rewind10" aria-label="Rewind 10 seconds" title="Rewind 10 seconds">${icon('rewind10',29)}</button><button type="button" class="player-main-action" id="pause-play" aria-label="Play" title="Play" disabled><svg id="player-play-morph-svg" class="player-play-morph" width="25" height="25" viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true" focusable="false"><g id="player-play-morph-group"><path id="player-play-morph-first" d=""/><path id="player-play-morph-second" d=""/></g></svg></button><button type="button" class="player-icon player-track-control" id="forward10" aria-label="Forward 10 seconds" title="Forward 10 seconds"><svg id="player-morph-icon" class="icon" width="29" height="29" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline id="player-morph-first" points="3,5 3,19 11,12 3,5"></polyline><polyline id="player-morph-second" points="14,5 14,19 22,12 14,5"></polyline></svg></button></div><div class="controls-right"><div class="player-upnext" id="player-upnext" aria-hidden="true"><button type="button" class="player-upnext-cancel" id="player-upnext-cancel" aria-label="Cancel Play Next" title="Cancel Play Next" disabled>${icon('close',17)}</button><div class="player-upnext-text"><strong id="player-upnext-title">Next episode</strong><span id="player-upnext-countdown">Next in 00:20</span></div><span class="player-upnext-divider" aria-hidden="true"></span></div><button type="button" class="player-icon" id="player-settings" aria-label="Player settings">${icon('settings',21)}</button><button type="button" class="player-icon" id="fullscreen" aria-label="Toggle fullscreen">${icon('maximize',21)}</button></div></div></div>
   </div>
  </div>
  <div class="player-episode-nav" aria-label="Episode navigation">
    <div class="player-episode-slot is-previous">${prev?`<button type="button" class="btn small player-episode-previous" id="previous-episode" aria-label="${escapeHTML(prev.label)}">${icon('back',15)}${buttonText(prev,'previous')}</button>`:''}</div>
    <div class="player-episode-label"><strong>${escapeHTML(centerPrimary)}</strong><small>${escapeHTML(centerSecondary||'')}</small></div>
    <div class="player-episode-slot is-next">${next?`<button type="button" class="btn small player-episode-next" id="next-episode" aria-label="${escapeHTML(next.label)}">${buttonText(next,'next')}${icon('chevron',15)}</button>`:''}</div>
  </div>
  <details class="player-dev-tools" data-development-only="true"><summary>Development tools · Local playback / VLC</summary>
   <div class="sf-player-demo-tools"><label class="sf-player-accent-preview"><input type="checkbox" id="sf-player-play-accent" checked> Secondary Play/Pause accent</label><label class="sf-player-accent-preview" for="sf-player-volume-test">Volume thresholds <select id="sf-player-volume-test" aria-label="Preview volume threshold"><option value="">Use slider</option><option value="0">0%</option><option value="1">1%</option><option value="25">25%</option><option value="26">26%</option><option value="50">50%</option><option value="51">51%</option><option value="75">75%</option><option value="76">76%</option><option value="100">100%</option></select></label><button class="btn small" type="button" id="sf-player-demo-toggle">Start simulation</button><button class="btn small" type="button" id="sf-player-demo-jump" disabled>Jump to last 25 s</button><button class="btn small" type="button" id="sf-player-demo-resume" disabled>Resume / Start Over demo</button><label class="sf-player-demo-autoplay" style="display:inline-flex;gap:5px;align-items:center;font-size:11px"><input type="checkbox" id="sf-player-demo-autoplay" checked> Demo autoplay next</label></div>
   <div class="player-file-actions"><button class="btn small" id="preview-play-next" type="button" aria-pressed="false" ${!autoplayNext?'disabled title="Play Next only applies within the current season"':''}>Preview Play Next transition</button><button class="btn small" id="change-local-video">${icon('folder',15)} Open local video…</button><button class="btn small" id="open-external-vlc" disabled>Open in VLC</button><span class="muted" id="local-file-label" style="align-self:center;font-size:12px">No local file selected</span></div>
   <div class="player-notice" id="player-notice">Local-file playback is functional where Electron supports the file's codec. Actual provider streams, bundled MPV rendering, and subtitle imports are not connected yet. Next-episode media is not yet connected, so the Play Next UI is visual/testable but cannot automatically load a following episode.</div>
  </details>
 </section>`;
}
function backFromPlayback(){
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 document.getElementById("local-video")?.pause();resetPlayNextState();isLocalVideoReady=false;
 transitionGalleryPlayer(()=>{
  state.playback=null;render();workspace.scrollTop=state.playbackReturnScroll;
 });
}
function showEpisodeAction(action,n){
 if(action==='watch'){startPlayback(n);return;}
 if(action!=='download')return;
 const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const season=activeInstallment(x);if(!season||season.sourceMatched===false)return;
 const a=episodeAvailability(season,n);
 const choices=[['sub','Japanese · Sub',a.sub],['dub','English · Dub',a.dub]];
 const available=choices.filter(choice=>choice[2]===true);if(!available.length)return;
 const defaultVersion=state.defaultDownload;
 const preferredAvailable=available.some(choice=>choice[0]===defaultVersion);
 const selected=preferredAvailable?defaultVersion:null;
 modal(`Download episode ${n}`,`<p class="description"><b>${escapeHTML(x.name)}</b> · ${escapeHTML(installmentDisplayName(x,season))} · ${escapeHTML(installmentSubLabel(season))} · Episode ${n}</p><div class="field"><span class="label">Audio version for download</span><div class="audio-choose">${choices.map(([id,name,availability])=>`<label><input type="radio" name="episode-audio" value="${id}" ${selected===id?'checked':''} ${availability!==true?'disabled':''}><span>${escapeHTML(name)}${availability===null?' · Unknown':availability===false?' · Unavailable':''}</span></label>`).join('')}</div></div>
 ${preferredAvailable?'':`<div class="preview-warning">The preferred download version (${defaultVersion==='sub'?'Sub':'Dub'}) is unavailable for this episode. Choose another available version explicitly to continue; the app will not switch automatically.</div>`}<div class="preview-warning">Available selectable subtitle tracks will be preserved independently of subtitle visibility. No silent audio-language substitution.</div><p class="tip">Choosing another download version here does not change your saved playback or download preferences.</p>`,`<button class="btn" id="episode-cancel">Cancel</button><button class="btn primary" id="episode-confirm" ${!selected?'disabled':''}>${icon('download',16)} Preview download</button>`);
 document.getElementById('episode-cancel').onclick=closeModal;
 for(const input of modalHost.querySelectorAll('input[name="episode-audio"]'))input.addEventListener('change',()=>{document.getElementById('episode-confirm').disabled=false;});
 document.getElementById('episode-confirm').onclick=()=>{
  const chosen=modalHost.querySelector('input[name="episode-audio"]:checked')?.value;
  if(!chosen||a[chosen]!==true)return;
  modal('Download preview',`<p class="description">${escapeHTML(x.name)} · ${escapeHTML(installmentDisplayName(x,season))} · ${escapeHTML(installmentSubLabel(season))} · Episode ${n}</p><div class="dialog-sample"><b>${chosen==='sub'?'Japanese (Sub)':'English (Dub)'}</b><p class="description">In the finished application, this would queue the selected download version and save accessible selectable subtitles for offline use.</p></div><p class="tip">This is a UI prototype; no downloading occurs.</p>`,`<button class="btn primary" id="episode-ok">Got it</button>`);
  document.getElementById('episode-ok').onclick=closeModal;
 };
}
function showManageDetailTags(){const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const season=activeInstallment(x);if(!season)return;const current=seasonTagList(x,season);
 modal(`Library tags · ${installmentDisplayName(x,season)}`,`<p class="description">Tags are saved for this specific installment (${escapeHTML(installmentSubLabel(season))}), independently of other seasons and their progress. This is temporary demo state only.</p><div class="tag-picker-list">${state.tags.map(tag=>`<label><input type="checkbox" data-detail-tag="${escapeHTML(tag)}" ${current.includes(tag)?'checked':''}><span>${escapeHTML(tag)}</span></label>`).join('')}</div>`,`<button class="btn" id="detail-tags-cancel">Cancel</button><button class="btn primary" id="detail-tags-save">Save tags</button>`);
 document.getElementById('detail-tags-cancel').onclick=closeModal;
 document.getElementById('detail-tags-save').onclick=()=>{const updated=Array.from(modalHost.querySelectorAll('input[data-detail-tag]:checked')).map(el=>el.dataset.detailTag);if(season.id)state.seasonTags[season.id]=updated;else x.tags=updated;closeModal();render();};
}
function showFindSource(){const x=demo.find(d=>d.id===state.detailId),s=x&&activeInstallment(x);if(!s)return;
 modal('Find a streaming source',`<p class="description"><b>${escapeHTML(installmentDisplayName(x,s))}</b> · ${escapeHTML(installmentSubLabel(s))}</p><div class="dialog-sample"><b>Not matched</b><p class="description">The finished application would search installed providers for this exact installment and ask you to confirm ambiguous matches. Nothing is silently linked here.</p></div><p class="tip">A relationship record does not prove that an episode can be streamed or downloaded.</p>`,`<button class="btn primary" id="source-ok">Got it</button>`);
 document.getElementById('source-ok').onclick=closeModal;
}

/* Electron bridge is narrowly scoped; standalone preview still renders. */
let localVideoName='',isLocalVideoReady=false,lastExternalPlayerStatus='not checked';
let savingPreference=false;
async function saveDesktopPreferences(){
 if(!window.galleryDesktop)return;
 try {await window.galleryDesktop.saveSettings({theme:state.theme,font:state.font,defaultPlayback:state.defaultPlayback,defaultDownload:state.defaultDownload,defaultSubtitles:state.defaultSubtitles,playerPreference:state.playerPreference||'built-in'});}catch(err){console.warn('Settings save failed:',err)}
}
async function setupDesktopSettings(){
 if(!window.galleryDesktop)return;
 document.body.classList.add('desktop-build');
 try{
  const prefs=await window.galleryDesktop.getSettings();
  if(SOFT_FUTURISTIC_THEMES.includes(prefs.theme))state.theme=prefs.theme;
  if(supportedGalleryFonts.includes(prefs.font)){state.font=prefs.font;document.body.dataset.font=state.font;try{localStorage.setItem('gallery.font',state.font)}catch{}}
  if(['sub','dub'].includes(prefs.defaultPlayback))state.defaultPlayback=prefs.defaultPlayback;
  if(['sub','dub'].includes(prefs.defaultDownload))state.defaultDownload=prefs.defaultDownload;
  if(typeof prefs.defaultSubtitles==='boolean')state.defaultSubtitles=prefs.defaultSubtitles;
  state.playerPreference=prefs.playerPreference||'built-in';
  document.body.dataset.theme=state.theme;
  render();
 }catch(err){console.warn('Could not load local settings:',err)}
}
/* v99 — The player menu selects subtitle tracks; audio language is chosen before playback.
   Remember the last track when Off is selected so the user can restore it easily. */
const playerSubtitleState={enabled:true,lastIndex:null,lastLanguage:'en'};
function playerSubtitleTracks(video){
 return Array.from(video?.textTracks||[]).map((track,index)=>({track,index})).filter(({track})=>track.kind==='subtitles'||track.kind==='captions');
}
function preferredPlayerSubtitleTrack(entries){
 return entries.find(({index})=>index===playerSubtitleState.lastIndex)
  ||entries.find(({track})=>track.language?.toLowerCase()===playerSubtitleState.lastLanguage)
  ||entries.find(({track})=>track.language?.toLowerCase().startsWith('en'))
  ||entries[0]||null;
}
function applyPlayerSubtitleState(video){
 const entries=playerSubtitleTracks(video),selected=preferredPlayerSubtitleTrack(entries);
 Array.from(video?.textTracks||[]).forEach(track=>{
  if(track.kind==='subtitles'||track.kind==='captions')track.mode=playerSubtitleState.enabled&&selected?.track===track?'showing':'disabled';
 });
 if(playerSubtitleState.enabled&&selected){
  playerSubtitleState.lastIndex=selected.index;
  if(selected.track.language)playerSubtitleState.lastLanguage=selected.track.language.toLowerCase();
 }
}
function openPlayerSettings(video){
 const entries=playerSubtitleTracks(video);
 const selected=preferredPlayerSubtitleTrack(entries);
 const selectedValue=playerSubtitleState.enabled&&selected?`track-${selected.index}`:'off';
 const choices=entries.map(({track,index})=>{
  const lang=track.language||'';
  const languageNames={en:'English',da:'Danish',ja:'Japanese',de:'German',fr:'French',es:'Spanish',pt:'Portuguese',it:'Italian',ko:'Korean',zh:'Chinese'};
  const displayName=track.label||languageNames[lang.toLowerCase().split('-')[0]]||lang||`Subtitle track ${index+1}`;
  return `<option value="track-${index}" ${selectedValue===`track-${index}`?'selected':''}>${escapeHTML(displayName)}</option>`;
 }).join('');
 const trackInfo=entries.length
  ?'<p class="tip">Choose a subtitle track or turn subtitles Off. Changing subtitles does not change the audio language.</p>'
  :'<p class="tip">No selectable subtitle tracks are available in this video. External subtitle imports are not connected in this HTML build.</p>';
 modal('Player settings',`<div class="field"><label for="video-rate">Playback speed</label><select id="video-rate">${[0.5,0.75,1,1.25,1.5,2].map(r=>`<option value="${r}" ${video.playbackRate===r?'selected':''}>${r}×</option>`).join('')}</select></div><div class="field"><label for="player-subtitle-track">Subtitles</label><select id="player-subtitle-track"><option value="off" ${selectedValue==='off'?'selected':''}>Off</option>${choices}</select>${trackInfo}</div>`,`<button class="btn primary" id="save-player-settings">Apply</button>`);
 document.getElementById('save-player-settings').onclick=()=>{
  video.playbackRate=Number(document.getElementById('video-rate').value);
  const value=document.getElementById('player-subtitle-track').value;
  if(value==='off')playerSubtitleState.enabled=false;
  else{
   const index=Number(value.slice('track-'.length));
   const item=entries.find(entry=>entry.index===index);
   if(item){
    playerSubtitleState.enabled=true;
    playerSubtitleState.lastIndex=index;
    if(item.track.language)playerSubtitleState.lastLanguage=item.track.language.toLowerCase();
   }
  }
  if(state.playback)state.playback.subtitles=playerSubtitleState.enabled;
  applyPlayerSubtitleState(video);
  closeModal();
 };
}
function fmtTime(sec){if(!Number.isFinite(sec)||sec<0)return '00:00';const x=Math.floor(sec);return `${String(Math.floor(x/3600)).padStart(x>=3600?1:2,'0')}:${String(Math.floor(x%3600/60)).padStart(2,'0')}:${String(x%60).padStart(2,'0')}`.replace(/^00:/,'');}


/* The approved Player Morph Refinement 02, now linked to real HTML5 and simulated
   playback states. No dependency or external assets; button markup is persistent. */
const SF_PLAY_MORPH_DURATION=260;
const SF_PLAY_FROM=[[[5.7,4],[13.4,8.1],[13.4,15.9],[5.7,20]],[[13.4,8.1],[20.4,11.35],[20.4,12.65],[13.4,15.9]]];
const SF_PLAY_TO=[[[5.6,4],[10.5,4],[10.5,20],[5.6,20]],[[13.5,4],[18.4,4],[18.4,20],[13.5,20]]];
let sfPlayMorph={amount:0,target:0,frame:0};
function sfPlayMorphPath(quad,radius){
 const corners=[];
 for(let i=0;i<4;i++){
  const prev=quad[(i+3)%4],now=quad[i],next=quad[(i+1)%4];
  const back=Math.hypot(prev[0]-now[0],prev[1]-now[1])||1;
  const ahead=Math.hypot(next[0]-now[0],next[1]-now[1])||1;
  const before=[now[0]+(prev[0]-now[0])*radius/back,now[1]+(prev[1]-now[1])*radius/back];
  const after=[now[0]+(next[0]-now[0])*radius/ahead,now[1]+(next[1]-now[1])*radius/ahead];
  corners.push({before,after,now});
 }
 const fmt=x=>Number(x).toFixed(3);
 let d=`M${fmt(corners[0].before[0])} ${fmt(corners[0].before[1])}`;
 for(let i=0;i<4;i++){
  const c=corners[i],n=corners[(i+1)%4];
  d+=` Q${fmt(c.now[0])} ${fmt(c.now[1])} ${fmt(c.after[0])} ${fmt(c.after[1])}`;
  d+=` L${fmt(n.before[0])} ${fmt(n.before[1])}`;
 }
 return d+' Z';
}
function sfDrawPlayMorph(){
 const first=document.getElementById('player-play-morph-first');
 const second=document.getElementById('player-play-morph-second');
 if(!first||!second)return;
 const t=Math.min(1,Math.max(0,sfPlayMorph.amount));
 for(let i=0;i<2;i++){
  const quad=SF_PLAY_FROM[i].map((point,j)=>point.map((value,k)=>value+(SF_PLAY_TO[i][j][k]-value)*t));
  // Both halves of the play triangle formerly touched at an antialiased seam.
  // Overlap their shared inner edge while in Play, fading that overlap away
  // as the halves morph into independent Pause bars. Outer contours stay put.
  const sharedOverlap=.85*(1-t);
  if(i===0){quad[1][0]+=sharedOverlap;quad[2][0]+=sharedOverlap;}
  else{quad[0][0]-=sharedOverlap;quad[3][0]-=sharedOverlap;}
  (i===0?first:second).setAttribute('d',sfPlayMorphPath(quad,.4+(.75*t)));
 }
 // The play triangle's mass sits left of its bounding box. Nudge it optically
 // toward the center; the pause bars stay precisely centered at t=1.
 const group=document.getElementById('player-play-morph-group');
 if(group)group.setAttribute('transform',`translate(${(1.05*(1-t)).toFixed(3)} 0)`);
}
function sfSetPlayMorph(playing,{instant=false}={}){
 const to=playing?1:0;
 const button=document.getElementById('pause-play');
 if(button){button.setAttribute('aria-label',playing?'Pause':'Play');button.title=playing?'Pause':'Play';}
 if(!instant && sfPlayMorph.target===to)return;
 cancelAnimationFrame(sfPlayMorph.frame);sfPlayMorph.frame=0;
 sfPlayMorph.target=to;
 const from=sfPlayMorph.amount;
 if(instant||window.matchMedia('(prefers-reduced-motion: reduce)').matches||Math.abs(from-to)<.001){
  sfPlayMorph.amount=to;sfDrawPlayMorph();return;
 }
 const duration=SF_PLAY_MORPH_DURATION*Math.abs(to-from);
 const start=performance.now();
 function tick(now){
  const p=Math.min(1,Math.max(0,(now-start)/duration));
  const eased=p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
  sfPlayMorph.amount=from+(to-from)*eased;
  sfDrawPlayMorph();
  if(p<1)sfPlayMorph.frame=requestAnimationFrame(tick);else sfPlayMorph.frame=0;
 }
 sfPlayMorph.frame=requestAnimationFrame(tick);
}
function sfResetPlayMorph(){
 cancelAnimationFrame(sfPlayMorph.frame);
 sfPlayMorph={amount:0,target:0,frame:0};
 sfDrawPlayMorph();
}

/* v98 — The user-approved, interruptible SVG morph: Tabler Player Track Next
   becomes Player Skip Forward, with an independent, reversible Up Next fade.
   This player currently handles local test media; provider episode URLs are not
   connected, so we never pretend an actual next-episode stream can start. */
const PLAYER_MORPH_MS=280;
const PLAYER_MORPH_FIRST_FROM=[[3,5],[3,19],[11,12],[3,5]];
const PLAYER_MORPH_FIRST_TO=[[4,5],[4,19],[16,12],[4,5]];
const PLAYER_MORPH_SECOND_FROM=[[14,5],[14,19],[22,12],[14,5]];
const PLAYER_MORPH_SECOND_TO=[[20,5],[20,19],[20,19],[20,5]];
let playNextMorph={amount:0,frame:0};
let playNextShown=false,playNextCanceled=false,playNextPreview=false;

/* Previous/Next may change episode, season or explicitly linked movie/special.
   Available audio must be verified for the destination. `watchNextId` and
   `watchPreviousId` are optional, provider-confirmed watch-order link IDs;
   never infer a movie's narrative position from release dates alone. */
function playbackNeighbor(step,{sameInstallmentOnly=false}={}){
 if(step!==1&&step!==-1)return null;
 const p=state.playback,x=demo.find(item=>item.id===state.detailId);
 const current=x&&activeInstallment(x);
 if(!p||!current)return null;
 const episode=p.episode+step;
 if(episode>=1&&episode<=current.total){
  if(episodeAvailability(current,episode)[p.audio]!==true)return null;
  return {episode,installment:current,seasonIndex:state.detailSeason,
   relatedId:state.detailRelated||null,kind:'episode',label:step>0?'Next episode':'Previous episode'};
 }
 if(sameInstallmentOnly)return null;
 const seasons=getSeasons(x),related=getRelated(x),all=[...seasons,...related];
 let target=null;
 const explicitId=step>0?current.watchNextId:current.watchPreviousId;
 if(explicitId){
  target=all.find(entry=>entry.id===explicitId)||null;
 }else{
  const reverseKey=step>0?'watchPreviousId':'watchNextId';
  const reverse=all.filter(entry=>entry.id!==current.id&&entry[reverseKey]===current.id);
  if(reverse.length===1)target=reverse[0];
  else if(reverse.length>1)return null; // Conflicting watch-order links.
  else if(!state.detailRelated){
   const index=state.detailSeason+step;
   target=seasons[index]||null;
  }
 }
 if(!target||target.sourceMatched===false)return null;
 const targetEpisode=step>0?1:target.total;
 if(!Number.isInteger(targetEpisode)||targetEpisode<1||episodeAvailability(target,targetEpisode)[p.audio]!==true)return null;
 const seasonIndex=seasons.findIndex(item=>item===target||(item.id&&item.id===target.id));
 const relatedId=seasonIndex<0?target.id:null;
 if(seasonIndex<0&&!relatedId)return null;
 const kind=seasonIndex>=0?'season':target.kind==='Movie'?'movie':
  target.kind==='OVA'?'OVA':(target.kind||'special').toLowerCase();
 const label=`${step>0?'Next':'Previous'} ${kind}`;
 return {episode:targetEpisode,installment:target,seasonIndex:seasonIndex>=0?seasonIndex:state.detailSeason,
  relatedId,kind,label};
}
function playerCanAdvance(){
 return Boolean(playbackNeighbor(1,{sameInstallmentOnly:true}));
}
function setPlayerMorphGeometry(amount){
 const first=document.getElementById('player-morph-first'),second=document.getElementById('player-morph-second');
 if(!first||!second)return;
 function points(a,b){return a.map((point,i)=>point.map((val,j)=>(val+(b[i][j]-val)*amount).toFixed(3)).join(',')).join(' ');}
 first.setAttribute('points',points(PLAYER_MORPH_FIRST_FROM,PLAYER_MORPH_FIRST_TO));
 second.setAttribute('points',points(PLAYER_MORPH_SECOND_FROM,PLAYER_MORPH_SECOND_TO));
}
function morphPlayerTo(target){
 cancelAnimationFrame(playNextMorph.frame);playNextMorph.frame=0;
 const button=document.getElementById('forward10');
 if(button){button.setAttribute('aria-label',target?'Next episode':'Forward 10 seconds');button.title=target?'Next episode':'Forward 10 seconds';}
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
  playNextMorph.amount=target?1:0;setPlayerMorphGeometry(playNextMorph.amount);return;
 }
 const from=playNextMorph.amount,to=target?1:0;
 if(Math.abs(from-to)<.0001){playNextMorph.amount=to;setPlayerMorphGeometry(to);return;}
 const duration=PLAYER_MORPH_MS*Math.abs(to-from);
 const beginning=performance.now();
 const frame=time=>{
  const progress=Math.min(1,Math.max(0,(time-beginning)/duration));
  const eased=progress<.5?4*progress*progress*progress:1-Math.pow(-2*progress+2,3)/2;
  playNextMorph.amount=from+(to-from)*eased;
  setPlayerMorphGeometry(playNextMorph.amount);
  if(progress<1)playNextMorph.frame=requestAnimationFrame(frame);else playNextMorph.frame=0;
 };
 playNextMorph.frame=requestAnimationFrame(frame);
}
function setPlayNextVisible(show){
 if(show===playNextShown)return;
 playNextShown=show;
 const area=document.getElementById('player-area'),upnext=document.getElementById('player-upnext');
 if(!area||!upnext)return;
 area.classList.toggle('play-next-active',show);
 upnext.setAttribute('aria-hidden',String(!show));
 const cancel=document.getElementById('player-upnext-cancel');if(cancel)cancel.disabled=!show;
 morphPlayerTo(show);
 if(show){area.classList.remove('controls-hidden');clearTimeout(playerControlsTimer);playerControlsTimer=null;}
 else playerControlsScheduleHide();
}

/* Standalone browser-review aid. Real provider streams are not simulated here.
   The existing v103 HTML5 video handlers remain responsible for actual playback. */
const SF_PLAYER_DEMO_DURATION=1470;
let sfPlayerDemo={active:false,playing:false,time:462,frame:0,lastStamp:0,autoplay:true};
let sfPlayerLocalObjectURL=null;
function sfPlayerDemoStop(){
 cancelAnimationFrame(sfPlayerDemo.frame);
 sfPlayerDemo={active:false,playing:false,time:462,frame:0,lastStamp:0,autoplay:true};
 document.getElementById('sf-player-demo-scene')?.setAttribute('hidden','');
 const btn=document.getElementById('sf-player-demo-toggle');if(btn)btn.textContent='Start simulation';
 for(const id of ['sf-player-demo-jump','sf-player-demo-resume']){
  const el=document.getElementById(id);if(el)el.disabled=true;
 }
}
function sfPlayerDemoStart(){
 const video=document.getElementById('local-video');if(!video)return;
 video.pause();
 sfPlayerDemoStop();
 sfPlayerDemo.active=true;
 sfPlayerDemo.autoplay=document.getElementById('sf-player-demo-autoplay')?.checked??true;
 sfPlayerDemo.lastStamp=0;
 document.getElementById('player-empty').hidden=true;
 document.getElementById('sf-player-demo-scene').hidden=false;
 const btn=document.getElementById('sf-player-demo-toggle');if(btn)btn.textContent='Stop simulation';
 for(const id of ['sf-player-demo-jump','sf-player-demo-resume']){
  const el=document.getElementById(id);if(el)el.disabled=false;
 }
 showPlayerNotice('SIMULATION ONLY: no video stream or episode is playing. Use the controls to examine Gallery’s player animations.');
 updatePlaybackUI();
 sfPlayerDemo.frame=requestAnimationFrame(sfPlayerDemoTick);
}
function sfPlayerDemoTick(stamp){
 if(!sfPlayerDemo.active)return;
 if(sfPlayerDemo.playing){
  if(sfPlayerDemo.lastStamp)sfPlayerDemo.time=Math.min(SF_PLAYER_DEMO_DURATION,sfPlayerDemo.time+Math.min((stamp-sfPlayerDemo.lastStamp)/1000,.10));
  if(sfPlayerDemo.time>=SF_PLAYER_DEMO_DURATION){
   sfPlayerDemo.playing=false;
   showPlayerNotice('Simulation reached the end. A real next episode cannot be loaded without a connected source.');
  }
  updatePlaybackUI();
 }
 sfPlayerDemo.lastStamp=stamp;
 sfPlayerDemo.frame=requestAnimationFrame(sfPlayerDemoTick);
}
function sfPlayerDemoSeek(t){
 sfPlayerDemo.time=Math.max(0,Math.min(SF_PLAYER_DEMO_DURATION,t));
 if(sfPlayerDemo.time<SF_PLAYER_DEMO_DURATION-20)playNextCanceled=false;
 updatePlaybackUI();playerControlsWake();
}
function sfPlayerDemoPlayPause(){
 if(sfPlayerDemo.time>=SF_PLAYER_DEMO_DURATION)sfPlayerDemoSeek(0);
 sfPlayerDemo.playing=!sfPlayerDemo.playing;
 sfPlayerDemo.lastStamp=0;
 updatePlaybackUI();playerControlsWake();
}
function sfPlayerReleaseBrowserVideo(){
 if(sfPlayerLocalObjectURL){URL.revokeObjectURL(sfPlayerLocalObjectURL);sfPlayerLocalObjectURL=null;}
}
function sfPlayerPickBrowserVideo(file){
 if(!file)return;
 const video=document.getElementById('local-video');if(!video)return;
 sfPlayerDemoStop();video.pause();sfPlayerReleaseBrowserVideo();
 sfPlayerLocalObjectURL=URL.createObjectURL(file);
 video.src=sfPlayerLocalObjectURL;video.load();
 document.getElementById('player-empty').hidden=true;
 document.getElementById('local-file-label').textContent=file.name;
 showPlayerNotice('Local video loaded in this browser preview. Playback depends on browser codec support; no file has been uploaded.');
}

function updatePlayNext(){
 const video=document.getElementById('local-video');if(!video)return;
 const title=document.getElementById('player-upnext-title'),countdown=document.getElementById('player-upnext-countdown');
 const remaining=sfPlayerDemo.active?Math.max(0,SF_PLAYER_DEMO_DURATION-sfPlayerDemo.time):Number.isFinite(video.duration)?Math.max(0,video.duration-video.currentTime):Infinity;
 const triggered=playerCanAdvance()&&(playNextPreview||(
  (sfPlayerDemo.active?sfPlayerDemo.autoplay:state.autoplayNextEpisode) && !playNextCanceled &&
  (sfPlayerDemo.active||isLocalVideoReady) && !(sfPlayerDemo.active?sfPlayerDemo.time>=SF_PLAYER_DEMO_DURATION:video.ended) && Number.isFinite(remaining) && remaining<=20 && (sfPlayerDemo.active?sfPlayerDemo.time:video.currentTime)>0
 ));
 if(title){const p=state.playback;title.textContent=p?`Episode ${p.episode+1}`:'Next episode';}
 if(countdown)countdown.textContent=playNextPreview?'Next in 00:12':`Next in ${fmtTime(Math.ceil(remaining))}`;
 setPlayNextVisible(triggered);
}
function cancelPlayNext(){
 playNextCanceled=true;playNextPreview=false;
 const demoButton=document.getElementById('preview-play-next');
 if(demoButton){demoButton.setAttribute('aria-pressed','false');demoButton.textContent='Preview Play Next transition';}
 setPlayNextVisible(false);
 const area=document.getElementById('player-area');if(area&&area.contains(document.activeElement))area.focus({preventScroll:true});
}
function resetPlayNextState(){
 cancelAnimationFrame(playNextMorph.frame);
 playNextMorph={amount:0,frame:0};playNextShown=false;playNextCanceled=false;playNextPreview=false;
}

/* Volume indicator is state-derived; keep the DOM stable so its waves can fade. */
let playerLastAudibleVolume=(playerSessionVolume>0?playerSessionVolume:GALLERY_INITIAL_VOLUME)/100;
function playerVolumeLevel(video){
 if(!video||video.muted||video.volume<=0)return 0;
 const pct=Math.round(video.volume*100);
 if(pct<=25)return 1;
 if(pct<=50)return 2;
 if(pct<=75)return 3;
 return 4;
}
function updatePlayerVolumeIcon(video){
 if(!video)return;
 const button=document.getElementById('mute');
 const svg=button?.querySelector('.player-volume-icon');
 if(!button||!svg)return;
 const level=playerVolumeLevel(video);
 svg.dataset.level=String(level);
 const muted=level===0;
 button.setAttribute('aria-label',muted?'Unmute':'Mute');
 button.setAttribute('aria-pressed',String(muted));
 button.title=muted?'Unmute':'Mute';
 const slider=document.getElementById('volume');
 if(slider){
  slider.value=String(Math.round(video.volume*100));
  slider.setAttribute('aria-valuetext',`${Math.round(video.volume*100)} percent${video.muted?' (muted)':''}`);
 }
 if(!video.muted&&video.volume>0)playerLastAudibleVolume=video.volume;
}

function updatePlaybackUI(){
 const video=document.getElementById('local-video');if(!video)return;
 const duration=sfPlayerDemo.active?SF_PLAYER_DEMO_DURATION:Number.isFinite(video.duration)?video.duration:0;
 const currentTime=sfPlayerDemo.active?sfPlayerDemo.time:video.currentTime;
 const paused=sfPlayerDemo.active?!sfPlayerDemo.playing:video.paused;
 const portion=duration?Math.min(1,Math.max(0,currentTime/duration)):0;
 const watched=document.getElementById('watched'),seek=document.getElementById('seek');
 if(watched)watched.style.flexBasis=galleryTimelineFill(portion*100);
 if(seek){seek.value=String(Math.round(portion*1000));seek.disabled=!duration;}
 document.getElementById('current-time').textContent=fmtTime(currentTime);
 document.getElementById('duration-time').textContent=fmtTime(duration);
 const play=document.getElementById('pause-play');if(play)play.disabled=!(isLocalVideoReady||sfPlayerDemo.active);sfSetPlayMorph(!paused);
 updatePlayerVolumeIcon(video);
 updatePlayNext();
}
function showPlayerNotice(text){const n=document.getElementById('player-notice');if(n)n.textContent=text;}
async function openLocalForPlayer(){
 if(!window.galleryDesktop){document.getElementById('sf-player-browser-file')?.click();return;}
 let chosen;
 try{chosen=await window.galleryDesktop.openVideo();}
 catch(error){showPlayerNotice(`Unable to open file: ${error.message}`);return;}
 if(!chosen)return;
 const video=document.getElementById('local-video');if(!video)return;
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 video.pause();isLocalVideoReady=false;localVideoName=chosen.name;
 video.src=chosen.fileURL;video.load();
 document.getElementById('player-empty').hidden=true;
 document.getElementById('local-file-label').textContent=chosen.name;
 document.getElementById('open-external-vlc').disabled=false;
 showPlayerNotice(`Selected local file: ${chosen.name}. The codec must be supported by Electron for in-app playback. Subtitles and streaming providers are not wired in this milestone.`);
 if(state.playerPreference==='vlc'){
  const result=await window.galleryDesktop.openInVLC();
  if(result.ok){
   video.pause();showPlayerNotice(`Opened ${chosen.name} in VLC as requested. Gallery cannot reliably track external playback progress; player compatibility is not guaranteed.`);
  }else{
   video.pause();showPlayerNotice(`VLC is your selected player, but it could not open the file: ${result.message}. You can press Play to use the built-in player for this file, or locate VLC in Settings.`);
  }
 }
 // User action picked a file; no automatic next-episode transition.
}
function advanceEpisode(step,{sameInstallmentOnly=false}={}){
 const destination=playbackNeighbor(step,{sameInstallmentOnly});
 if(!destination)return;
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 resetPlayNextState();
 const p=state.playback;
 state.detailSeason=destination.seasonIndex;
 state.detailRelated=destination.relatedId;
 state.detailEpisode=destination.episode;
 state.playback={...p,episode:destination.episode,installmentId:destination.installment.id};
 isLocalVideoReady=false;localVideoName='';render();workspace.scrollTop=0;
}
// The controls fade out during playback and stay visible for keyboard users.
let playerControlsTimer=null;
let playerEventController=null;
let playerKeyboardFocus=false;
const PLAYER_CONTROLS_IDLE_MS=2600;
function playerControlsWake(){
 const area=document.getElementById('player-area');if(!area)return;
 area.classList.remove('controls-hidden');
 playerControlsScheduleHide();
}
function playerControlsScheduleHide(){
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 const area=document.getElementById('player-area'),video=document.getElementById('local-video');
 if(!area||!video)return;
 const playingNow=sfPlayerDemo.active?sfPlayerDemo.playing:(!video.paused&&!video.ended);
 if((!isLocalVideoReady&&!sfPlayerDemo.active)||!playingNow||playNextShown){area.classList.remove('controls-hidden');return;}
 const focused=document.activeElement;
 if(playerKeyboardFocus&&focused&&area.contains(focused)&&focused!==area)return;
 if(document.getElementById('modal-host')?.firstElementChild)return;
 playerControlsTimer=setTimeout(()=>{
  const currentVideo=document.getElementById('local-video'),currentArea=document.getElementById('player-area');
  if(!currentArea||!currentVideo||currentVideo!==video||!(sfPlayerDemo.active?sfPlayerDemo.playing:(!currentVideo.paused&&!currentVideo.ended))||playNextShown)return;
  const active=document.activeElement;
  if(playerKeyboardFocus&&active&&currentArea.contains(active)&&active!==currentArea)return;
  if(document.getElementById('modal-host')?.firstElementChild)return;
  currentArea.classList.add('controls-hidden');
 },PLAYER_CONTROLS_IDLE_MS);
}
function initializePlayer(){
 sfPlayerDemoStop();sfPlayerReleaseBrowserVideo();
 const v=document.getElementById('local-video');if(!v)return;
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 playerEventController?.abort();playerEventController=new AbortController();
 isLocalVideoReady=false;localVideoName='';
 resetPlayNextState();
 sfResetPlayMorph();
 playerSubtitleState.enabled=state.playback?.subtitles!==false;
 playerSubtitleState.lastIndex=null;
 playerSubtitleState.lastLanguage='en';
 v.volume=playerSessionVolume/100;v.muted=playerSessionMuted;v.autoplay=false;v.loop=false;
 whInitPlayerSession();
 v.addEventListener('timeupdate',()=>whOnVideoTick(v));
 v.addEventListener('seeked',()=>whOnVideoSeek(v));
 v.addEventListener('loadedmetadata',()=>{whInitPlayerSession();isLocalVideoReady=true;document.getElementById('player-empty').hidden=true;applyPlayerSubtitleState(v);updatePlaybackUI();});
 v.textTracks?.addEventListener?.('addtrack',()=>applyPlayerSubtitleState(v));
 v.addEventListener('error',()=>{isLocalVideoReady=false;document.getElementById('player-empty').hidden=false;showPlayerNotice('The selected file cannot be decoded in the integrated Chromium player. You may try VLC, if installed, or another compatible file.');updatePlaybackUI();});
 for(const name of ['timeupdate','seeked','durationchange','play','pause','ended','ratechange'])v.addEventListener(name,updatePlaybackUI);
 v.addEventListener('volumechange',()=>{rememberGalleryPlayerVolume(v);updatePlaybackUI();});
 v.addEventListener('play',playerControlsWake);
  v.addEventListener('ended',()=>{if(state.autoplayNextEpisode&&!playNextCanceled&&playerCanAdvance()&&!playNextPreview)showPlayerNotice('This local-file test ended. Play Next cannot load the following episode until a real episode source is connected.');});
 for(const name of ['pause','ended','emptied'])v.addEventListener(name,()=>{clearTimeout(playerControlsTimer);document.getElementById('player-area')?.classList.remove('controls-hidden');});
 const playerArea=document.getElementById('player-area');
 playerArea.addEventListener('pointermove',()=>{playerKeyboardFocus=false;playerControlsWake();});
 playerArea.addEventListener('pointerdown',()=>{playerKeyboardFocus=false;playerControlsWake();});
 playerArea.addEventListener('keydown',()=>{playerKeyboardFocus=true;playerControlsWake();});
 document.addEventListener('keydown',e=>{if(e.key==='Tab')playerKeyboardFocus=true;},{signal:playerEventController.signal});
 playerArea.addEventListener('focusin',playerControlsWake);
 playerArea.addEventListener('focusout',()=>setTimeout(playerControlsScheduleHide,0));
 document.addEventListener('fullscreenchange',playerControlsWake,{signal:playerEventController.signal});
 document.getElementById('open-local-video').onclick=openLocalForPlayer;
 document.getElementById('sf-player-browser-file').onchange=e=>{sfPlayerPickBrowserVideo(e.target.files?.[0]);e.target.value='';};
 document.body.dataset.sfPlayAccent='secondary';
 document.getElementById('sf-player-play-accent').onchange=e=>{document.body.dataset.sfPlayAccent=e.target.checked?'secondary':'original';};
 document.getElementById('sf-player-demo-start').onclick=sfPlayerDemoStart;
 document.getElementById('sf-player-demo-toggle').onclick=()=>{
  if(sfPlayerDemo.active){sfPlayerDemoStop();document.getElementById('player-empty').hidden=!!isLocalVideoReady;updatePlaybackUI();}
  else sfPlayerDemoStart();
 };
 document.getElementById('sf-player-demo-jump').onclick=()=>{playNextCanceled=false;sfPlayerDemoSeek(SF_PLAYER_DEMO_DURATION-25);};
 document.getElementById('sf-player-demo-autoplay').onchange=e=>{sfPlayerDemo.autoplay=e.target.checked;updatePlaybackUI();};
 document.getElementById('sf-player-demo-resume').onclick=()=>{
  sfPlayerDemo.playing=false;updatePlaybackUI();
  modal('Resume or start over · simulation',`<p class="description">This is a simulated watch-history prompt. The saved position is 12:18. Resume starts eight seconds earlier; no real watch history is changed.</p>`,
  '<button class="btn" id="sf-resume-cancel">Cancel</button><button class="btn" id="sf-start-over">Start over</button><button class="btn primary" id="sf-resume-now">Resume</button>');
  document.getElementById('sf-resume-cancel').onclick=closeModal;
  document.getElementById('sf-start-over').onclick=()=>{sfPlayerDemoSeek(0);closeModal();};
  document.getElementById('sf-resume-now').onclick=()=>{sfPlayerDemoSeek(730);closeModal();};
 };

 document.getElementById('change-local-video').onclick=openLocalForPlayer;
 document.getElementById('pause-play').onclick=()=>{if(sfPlayerDemo.active){sfPlayerDemoPlayPause();return;}if(!isLocalVideoReady)return;if(v.paused)v.play().catch(e=>showPlayerNotice('Unable to play file: '+e.message));else v.pause();};
 document.getElementById('rewind10').onclick=()=>{if(sfPlayerDemo.active){sfPlayerDemoSeek(sfPlayerDemo.time-10);return;}if(Number.isFinite(v.duration))v.currentTime=Math.max(0,v.currentTime-10);};
 document.getElementById('forward10').onclick=()=>{if(playNextShown){if(sfPlayerDemo.active){showPlayerNotice('Simulation: Next episode is not connected.');sfPlayerDemo.playing=false;updatePlaybackUI();return;}advanceEpisode(1,{sameInstallmentOnly:true});return;}if(sfPlayerDemo.active){sfPlayerDemoSeek(sfPlayerDemo.time+10);return;}if(Number.isFinite(v.duration))v.currentTime=Math.min(v.duration,v.currentTime+10);};
  document.getElementById('player-upnext-cancel').onclick=cancelPlayNext;
  document.getElementById('preview-play-next').onclick=e=>{playNextPreview=!playNextPreview;playNextCanceled=false;e.currentTarget.setAttribute('aria-pressed',String(playNextPreview));e.currentTarget.textContent=playNextPreview?'Stop Play Next preview':'Preview Play Next transition';updatePlayNext();};
 document.getElementById('seek').oninput=e=>{if(sfPlayerDemo.active){sfPlayerDemoSeek(SF_PLAYER_DEMO_DURATION*Number(e.target.value)/1000);return;}if(Number.isFinite(v.duration))v.currentTime=v.duration*Number(e.target.value)/1000;};
 const thresholdPreview=document.getElementById('sf-player-volume-test');
 if(thresholdPreview)thresholdPreview.onchange=()=>{
  if(thresholdPreview.value==='')return;
  const percentage=Number(thresholdPreview.value);
  v.volume=percentage/100;
  v.muted=percentage===0;
  rememberGalleryPlayerVolume(v);
  updatePlayerVolumeIcon(v);
 };
 const volume=document.getElementById('volume');volume.oninput=()=>{
  if(thresholdPreview)thresholdPreview.value='';
  v.volume=Number(volume.value)/100;
  v.muted=v.volume===0;
  rememberGalleryPlayerVolume(v);
  updatePlayerVolumeIcon(v);
 };
 document.getElementById('mute').onclick=()=>{
  if(v.muted||v.volume===0){
   if(v.volume===0)v.volume=playerLastAudibleVolume>0?playerLastAudibleVolume:GALLERY_INITIAL_VOLUME/100;
   v.muted=false;
  }else{
   playerLastAudibleVolume=v.volume;
   v.muted=true;
  }
  rememberGalleryPlayerVolume(v);
  updatePlayerVolumeIcon(v);
 };
 document.getElementById('player-settings').onclick=()=>openPlayerSettings(v);
 const fullscreen=()=>{const area=document.getElementById('player-area');if(!document.fullscreenElement)area.requestFullscreen?.().catch(()=>showPlayerNotice('Fullscreen is not available in this environment.'));else document.exitFullscreen?.();};
 document.getElementById('fullscreen').onclick=fullscreen;
 document.getElementById('previous-episode')?.addEventListener('click',()=>advanceEpisode(-1));
 document.getElementById('next-episode')?.addEventListener('click',()=>advanceEpisode(1));
 document.getElementById('open-external-vlc').onclick=async()=>{
  if(!window.galleryDesktop)return;
  const result=await window.galleryDesktop.openInVLC();
  if(!result.ok)showPlayerNotice(`${result.message} Use Settings to locate VLC manually if automatic detection fails. External-player compatibility and progress tracking are not guaranteed.`);
  else showPlayerNotice('The selected local file was handed to VLC. Watch progress in Gallery is not tracked for external playback.');
 };
 updatePlaybackUI();
}

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
/* v39: Modal lifecycle and keyboard focus stay stable across every Gallery dialog.
   Preserve the original opener even when a dialog replaces another (e.g. import preview). */
const galleryApp=document.querySelector('.app');
let modalReturnFocus=null;
const modalFocusable='button:not([disabled]),[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';
function visibleModalControls(){
 const dialog=modalHost.querySelector('.dialog');
 return dialog?Array.from(dialog.querySelectorAll(modalFocusable)).filter(el=>!el.closest('[hidden]')&&el.getClientRects().length>0&&!el.inert):[];
}
function modal(title,inner,actions=''){
 const previouslyOpen=!!modalHost.querySelector('.overlay');
 if(!previouslyOpen){
  const opener=document.activeElement;
  modalReturnFocus=opener instanceof HTMLElement&&opener!==document.body&&!modalHost.contains(opener)?opener:null;
 }
 clearTimeout(modalExitTimer);modalExitTimer=null;
 modalHost.innerHTML=`<div class="overlay" role="presentation"><div class="dialog" role="dialog" aria-modal="true" aria-label="${escapeHTML(title)}" tabindex="-1"><div class="dialog-scroll"><div class="dialog-head"><h2>${escapeHTML(title)}</h2><button class="iconbtn" aria-label="Close dialog" id="close-dialog">${icon('close',20)}</button></div>${inner}${actions?`<div class="dialog-actions">${actions}</div>`:''}</div></div></div>`;
 galleryApp.inert=true;
 modalHost.querySelector('.overlay').addEventListener('click',e=>{if(e.target.classList.contains('overlay'))closeModal()});
 document.getElementById('close-dialog').addEventListener('click',closeModal);
 (modalHost.querySelector('button:not(#close-dialog),input,select')||document.getElementById('close-dialog')).focus({preventScroll:true});
}
function finishModalClose(overlay){
 if(modalHost.firstElementChild!==overlay)return;
 const expandedStage=overlay.querySelector('#subtitle-expanded-stage');
 if(expandedStage)subtitleResizeObserver?.unobserve(expandedStage);
 modalHost.innerHTML='';
 galleryApp.inert=false;
 const target=modalReturnFocus;
 modalReturnFocus=null;
 if(target?.isConnected&&!target.disabled)target.focus({preventScroll:true});
 else document.getElementById('settings')?.focus({preventScroll:true});
}
function closeModal(){
 const overlay=modalHost.querySelector('.overlay');
 if(!overlay||overlay.classList.contains('is-closing'))return;
clearTimeout(modalExitTimer);
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){finishModalClose(overlay);return;}
 overlay.classList.add('is-closing');
 modalExitTimer=setTimeout(()=>{
  finishModalClose(overlay);
  modalExitTimer=null;
 },150);
}
/* v41: All Tab / Shift+Tab focus changes in dialogs are managed here.
   Prevent Chrome's instant implicit focus scroll, then reveal the newly
   focused control through the same smooth scroll path as wraparound.
   Keep focus itself immediate, the dialog stationary and Reduce Motion intact. */
let modalScrollFrame=null;
let modalScrollGoal=null;
let modalScrollContainer=null;
function cancelModalKeyboardScroll(){
 if(modalScrollFrame!==null)cancelAnimationFrame(modalScrollFrame);
 modalScrollFrame=null;modalScrollGoal=null;modalScrollContainer=null;
}
function revealModalControl(control,edge='nearest'){
 const scroller=modalHost.querySelector('.dialog-scroll');
 if(!scroller||!control||!scroller.contains(control))return;
 // Compute visibility relative to the *intended* destination of any in-flight
 // keyboard scroll, not an intermediate animation frame. Repeated Tab presses
 // can therefore redirect the scroll without piling up contradictory requests.
 const base=(scroller===modalScrollContainer&&modalScrollGoal!==null)
  ?modalScrollGoal:scroller.scrollTop;
 const max=Math.max(0,scroller.scrollHeight-scroller.clientHeight);
 let target=base;
 if(edge==='start')target=0;
 else if(edge==='end')target=max;
 else{
  const view=scroller.getBoundingClientRect();
  const item=control.getBoundingClientRect();
  const itemTop=item.top-view.top+scroller.scrollTop;
  const itemBottom=item.bottom-view.top+scroller.scrollTop;
  const breathingRoom=10;
  if(itemTop<base+breathingRoom)target=itemTop-breathingRoom;
  else if(itemBottom>base+scroller.clientHeight-breathingRoom)
   target=itemBottom-scroller.clientHeight+breathingRoom;
 }
 target=Math.max(0,Math.min(target,max));
 cancelModalKeyboardScroll();
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
  scroller.scrollTop=target;return;
 }
 const start=scroller.scrollTop;
 if(Math.abs(target-start)<1)return;
 modalScrollContainer=scroller;modalScrollGoal=target;
 const distance=Math.abs(target-start);
 const duration=Math.min(410,Math.max(220,180+Math.sqrt(distance)*7));
 let started=null;
 function step(time){
  if(modalScrollContainer!==scroller)return;
  if(started===null)started=time;
  const fraction=Math.min(1,(time-started)/duration);
  const eased=1-Math.pow(1-fraction,3);
  scroller.scrollTop=start+(target-start)*eased;
  if(fraction<1)modalScrollFrame=requestAnimationFrame(step);
  else{modalScrollFrame=null;modalScrollGoal=null;modalScrollContainer=null;}
 }
 modalScrollFrame=requestAnimationFrame(step);
}
// Pointer/wheel scrolling always takes precedence over keyboard-initiated motion.
modalHost.addEventListener('wheel',cancelModalKeyboardScroll,{passive:true,capture:true});
modalHost.addEventListener('touchstart',cancelModalKeyboardScroll,{passive:true,capture:true});
/* Set before focus() and cleared synchronously by focusin. This prevents
   the focusin fallback from issuing a second, conflicting scroll request. */
let modalKeyboardFocusTarget=null;
document.addEventListener('keydown',event=>{
 const overlay=modalHost.querySelector('.overlay');
 if(!overlay)return;
 if(event.key==='Escape'){
  event.preventDefault();event.stopImmediatePropagation();closeModal();return;
 }
 if(event.key!=='Tab'||overlay.classList.contains('is-closing')||event.altKey||event.ctrlKey||event.metaKey)return;
 const controls=visibleModalControls();
 const active=document.activeElement;
 const backward=event.shiftKey;
 // Only Settings requires manual Tab navigation. Other dialogs retain native
 // Tab behavior (important for radio groups) and the original focus trap.
 if(!overlay.querySelector('#apply-preferences')){
  const first=controls[0],last=controls[controls.length-1];
  if(!first){event.preventDefault();overlay.querySelector('.dialog')?.focus({preventScroll:true});return;}
  if(!overlay.contains(active)||(backward&&active===first)||(!backward&&active===last)){
   event.preventDefault();
   const next=backward?last:first;
   modalKeyboardFocusTarget=next;
   next.focus({preventScroll:true});
   if(modalKeyboardFocusTarget===next)modalKeyboardFocusTarget=null;
   revealModalControl(next,backward?'end':'start');
  }
  return;
 }
 event.preventDefault(); // Never let Chrome jump to an off-screen Settings control.
 if(!controls.length){overlay.querySelector('.dialog')?.focus({preventScroll:true});return;}
 const index=controls.indexOf(active);
 const nextIndex=index<0?(backward?controls.length-1:0):(index+(backward?-1:1)+controls.length)%controls.length;
 const next=controls[nextIndex];
 const wrap=index>=0&&((backward&&index===0)||(!backward&&index===controls.length-1));
 modalKeyboardFocusTarget=next;
 next.focus({preventScroll:true});
 // A click or programmatic focus may already have focused next.
 if(modalKeyboardFocusTarget===next)modalKeyboardFocusTarget=null;
 revealModalControl(next,wrap?(backward?'end':'start'):'nearest');
},true);
document.addEventListener('focusin',event=>{
 const overlay=modalHost.querySelector('.overlay');
 if(!overlay||overlay.classList.contains('is-closing'))return;
 if(overlay.contains(event.target)){
  const focused=event.target;
  if(focused===modalKeyboardFocusTarget){modalKeyboardFocusTarget=null;return;}
  // Mouse/programmatic focus outside Tab should still reveal hidden controls.
  requestAnimationFrame(()=>{
   if(document.activeElement===focused)revealModalControl(focused);
  });
  return;
 }
 const first=visibleModalControls()[0]||overlay.querySelector('.dialog');
 first?.focus({preventScroll:true});
 revealModalControl(first);
},true);
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
/* v57 — Settings is a full page. Original tabs and detail DOM stay mounted,
   not rerendered, so returning preserves the active view, filters, and scroll. */
let settingsReturnScroll=0;
let settingsLastSection='appearance';
let appearanceTab='theme';
let playbackTab='general';
let settingsClosing=false;
let settingsCloseFallback=null;
let settingsReturnAnimationTimer=null;
