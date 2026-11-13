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
