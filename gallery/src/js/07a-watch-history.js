// Recovery is deliberately scoped to the preview history key. No writes on load.
const whRecoveryKey=whStorageKey+'.recovery-original';
const whFallbackCover='linear-gradient(145deg,#414753,#737b87)';
let whStorageReadable=false,whLoadedRaw=null,whNeedsRecovery=false;
function whSeedRecords(){return whSeed.map(r=>({...r,dates:[...r.dates],episodes:r.episodes.map(e=>({...e}))}));}
function whRecordObject(v){return v!==null&&typeof v==='object'&&!Array.isArray(v);}
function whIdentity(v){return typeof v==='string'&&v.trim().length>0&&!/[\x00-\x1f\x7f]/.test(v);}
function whDateValid(v){
 if(typeof v!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(v))return false;
 const d=new Date(v+'T00:00:00Z');
 return Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===v;
}
function whCoverValue(v){
 // Preview artwork is a simple linear gradient, never an external URL or a declaration list.
 return typeof v==='string'&&/^linear-gradient\([#a-z0-9\s.,%+-]+\)$/i.test(v)&&CSS.supports('background-image',v)?v:whFallbackCover;
}
function whValidEpisode(e){
 return whRecordObject(e)&&Number.isSafeInteger(e.n)&&e.n>0&&
  typeof e.watched==='boolean'&&typeof e.started==='boolean'&&
  Number.isFinite(e.progressSeconds)&&e.progressSeconds>=0&&
  Number.isFinite(e.duration)&&e.duration>=0&&e.progressSeconds<=e.duration;
}
function whRecoverRecords(saved){
 if(!Array.isArray(saved))return [];
 const counts=new Map();
 for(const r of saved)if(whRecordObject(r)&&whIdentity(r.id))counts.set(r.id,(counts.get(r.id)||0)+1);
 const result=[];
 for(const r of saved){
  // Ambiguous record or episode identities cannot be safely edited. Do not
  // discard individual episodes and thereby misrepresent a season as complete.
  if(!whRecordObject(r)||!whIdentity(r.id)||counts.get(r.id)!==1||!Array.isArray(r.episodes)||!r.episodes.length||
   !r.episodes.every(whValidEpisode)||new Set(r.episodes.map(e=>e.n)).size!==r.episodes.length)continue;
  const dates=Array.isArray(r.dates)?r.dates.filter(whDateValid):[];
  const last=whDateValid(r.last)?r.last:[...dates].sort().at(-1)||'';
  if(last&&!dates.includes(last))dates.push(last);
  const title=typeof r.title==='string'&&r.title.trim()?r.title:typeof r.short==='string'&&r.short.trim()?r.short:'Unknown title';
  const short=typeof r.short==='string'&&r.short.trim()?r.short:title;
  const record={...r,group:whIdentity(r.group)?r.group:r.id,title,short,cover:whCoverValue(r.cover),last,dates,
   episodes:r.episodes.map(e=>{const copy={...e};if(!['never','partial','watched'].includes(copy.manualStatus))delete copy.manualStatus;return copy;})};
  if(typeof record.library!=='boolean')delete record.library;
  for(const key of ['galleryId','installmentId'])if(record[key]!==null&&!whIdentity(record[key]))delete record[key];
  if(!record.episodes.some(e=>e.n===record.latestEpisode))delete record.latestEpisode;
  result.push(record);
 }
 return result;
}
function whLoadRecords(){
 // The opt-in dense fixture neither reads nor writes the real preview history.
 if(whRecentTestMode)return whRecentTestRecords();
 try{whLoadedRaw=localStorage.getItem(whStorageKey);whStorageReadable=true;}
 catch{return whSeedRecords();} // Inaccessible storage: preview only; never write over it.
 if(whLoadedRaw===null)return whSeedRecords();
 let saved;
 try{saved=JSON.parse(whLoadedRaw);}
 catch{whNeedsRecovery=true;return [];}
 const records=whRecoverRecords(saved);
 whNeedsRecovery=JSON.stringify(records)!==JSON.stringify(saved);
 return records;
}
let whRecords=whLoadRecords();let whOpen=false,whFilter='all',whSort='newest',whSearch='',whExpanded=new Set(),whPending=new Set();
let whSuspended=null,whParentView='discover';
let whInnerScrollers=new Map();
function whSave(){
 // Do not overwrite unreadable storage or changes from another open preview.
 if(!whStorageReadable)return;
 try{
  if(localStorage.getItem(whStorageKey)!==whLoadedRaw)return;
  if(whNeedsRecovery){
   const original=localStorage.getItem(whRecoveryKey);
   // Never replace a previous distinct recovery snapshot. If the exact original
   // cannot be preserved and read back, keep the primary untouched.
   if(original!==null&&original!==whLoadedRaw)return;
   if(original===null)localStorage.setItem(whRecoveryKey,whLoadedRaw);
   if(localStorage.getItem(whRecoveryKey)!==whLoadedRaw)return;
  }
  const next=JSON.stringify(whRecords);
  localStorage.setItem(whStorageKey,next);
  whLoadedRaw=next;whNeedsRecovery=false;
 }catch{/* Private/browser file preview may forbid storage; keep in-memory changes. */}
}
/* Manual watched-state changes are an override, not a fake playback event:
   preserve saved duration/position separately from the status indicator. */
function whEpisodeStatus(ep){return ['never','partial','watched'].includes(ep.manualStatus)?ep.manualStatus:ep.watched?'watched':ep.started?'partial':'never';}
function whEpisodeNextStatus(ep){const status=whEpisodeStatus(ep);return status==='never'?'partial':status==='partial'?'watched':'never';}
function whEpisodeStatusLabel(status){return status==='watched'?'Watched':status==='partial'?'Partially watched':'Not watched';}
function whEpisodePress(status){return status==='watched'?'true':status==='partial'?'mixed':'false';}
function whCount(r){return r.episodes.reduce((n,e)=>n+(whEpisodeStatus(e)==='watched'?1:0),0)}
function whCompleted(r){return r.episodes.length>0&&whCount(r)===r.episodes.length}
function whFormatDate(date){if(!date)return 'Unknown';const d=new Date(date+'T12:00:00');return Number.isNaN(d.getTime())?date:d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});}
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
/* Recently Watched: pack covers at rest; temporarily compress the side
 * with more room for a stationary portrait's directional detail panel. */
let whRecentController=null;
function whSetupRecentPreview(content){
 if(whRecentController){whRecentController.destroy();whRecentController=null;}
 const row=content.querySelector('.wh-recent-row');if(!row)return;
 const items=[...row.querySelectorAll('.wh-recent-item')],historyTile=row.querySelector('#wh-view-history');
 const motion=matchMedia('(prefers-reduced-motion: reduce)'),hover=matchMedia('(any-hover: hover) and (any-pointer: fine)');
 const scope=row.closest('.tab-page'),pitch=76,stackPitch=18;
 let count=0,limit=0,active=null,pending=null,observer=null,scopeObserver=null,destroyed=false;
 let pointerX=0,pointerY=0,lastChosenX=null,lastChosenY=null,pointerInside=false;
 const allowed=()=>!destroyed&&!motion.matches&&hover.matches&&!searchOpen;
 const cancelPending=()=>{if(pending){clearTimeout(pending.timer);pending=null;}};
 const visible=()=>items.slice(0,count);
 function paint(positions){
  visible().forEach((item,i)=>{
   item.style.transform='translate3d('+(positions[i]-i*pitch)+'px,0,0)';
   item.style.zIndex=item===active?'1000':String(i+1);
  });
 }
 function close(){
  cancelPending();active=null;lastChosenX=lastChosenY=null;row.classList.remove('is-stacking');
  items.forEach(item=>item.classList.remove('is-active'));
  paint(visible().map((_,i)=>i*pitch));
 }
 function reset(){
  row.classList.add('is-fitting');close();void row.offsetWidth;row.classList.remove('is-fitting');
 }
 function activate(item,pointer=null){
  cancelPending();
  if(!allowed()||!item||item.classList.contains('is-preview-hidden')){close();return;}
  if(active===item)return;
  const i=items.indexOf(item),left=i,right=count-i-1;
  if(i<0||i>=count)return;
  const required=k=>k?pitch+(k-1)*stackPitch:0;
  const low=required(left),high=limit-required(right);if(high<low)return;
  const current=item.getBoundingClientRect().left-row.getBoundingClientRect().left;
  const anchor=Math.max(low,Math.min(high,current));
  if(pointer!==null&&(pointer<anchor||pointer>anchor+66))return;
  const leftRoom=anchor-required(left),rightRoom=limit-anchor-required(right);
  const side=rightRoom>=leftRoom?'right':'left';
  const panel=Math.min(188,Math.floor(Math.max(leftRoom,rightRoom)));
  if(panel<55){close();return;}
  const positions=visible().map((_,j)=>j*pitch);positions[i]=anchor;
  let edge=anchor-pitch-(side==='left'?panel:0);
  for(let j=i-1;j>=0;j--){positions[j]=Math.min(positions[j],edge);edge=positions[j]-stackPitch;}
  edge=anchor+pitch+(side==='right'?panel:0);
  for(let j=i+1;j<count;j++){positions[j]=Math.max(positions[j],edge);edge=positions[j]+stackPitch;}
  active=item;item.dataset.whSide=side;item.style.setProperty('--wh-panel-width',panel+'px');
  row.classList.add('is-stacking');items.forEach(x=>x.classList.toggle('is-active',x===item));paint(positions);
 }
 function onPointerMove(event){
  if(event.pointerType!=='mouse'||!event.isPrimary||!allowed())return;
  pointerInside=true;pointerX=event.clientX;pointerY=event.clientY;
  const item=event.target.closest('.wh-recent-card')?.closest('.wh-recent-item');
  if(!item||item.classList.contains('is-preview-hidden')){
   cancelPending();if(event.target.closest('#wh-view-history'))close();return;
  }
  if(item===active){cancelPending();return;}
  if(active&&lastChosenX!==null&&Math.hypot(pointerX-lastChosenX,pointerY-lastChosenY)<18)return;
  const choose=()=>{
   activate(item,pointerX-row.getBoundingClientRect().left);
   if(active===item){lastChosenX=pointerX;lastChosenY=pointerY;}
  };
  if(active){choose();return;}
  if(pending?.item===item)return;
  cancelPending();const request={item,timer:null};pending=request;
  request.timer=setTimeout(()=>{
   if(destroyed||pending!==request||!pointerInside||!allowed()){cancelPending();return;}
   if(document.elementFromPoint(pointerX,pointerY)?.closest('.wh-recent-card')?.closest('.wh-recent-item')!==item){cancelPending();return;}
   pending=null;choose();
  },100);
 }
 function onPointerLeave(event){if(event.pointerType==='mouse'){pointerInside=false;close();}}
 row.addEventListener('pointermove',onPointerMove);row.addEventListener('pointerleave',onPointerLeave);
 const focusHandlers=[];
 for(const item of items){
  const button=item.querySelector('.wh-recent-card');
  const onFocus=()=>{if(button.matches(':focus-visible')&&allowed())activate(item);};
  const onFocusOut=event=>{if(!item.contains(event.relatedTarget)&&active===item)close();};
  button.addEventListener('focus',onFocus);item.addEventListener('focusout',onFocusOut);
  focusHandlers.push({item,button,onFocus,onFocusOut});
 }
 function fit(){
  if(destroyed)return;
  const width=row.clientWidth;if(width<1)return;
  count=Math.max(0,Math.min(items.length,Math.floor((width-66)/pitch)));
  limit=Math.max(0,width-142);
  items.forEach((item,i)=>{
   const hidden=i>=count;
   if(hidden&&item.contains(document.activeElement))historyTile.focus({preventScroll:true});
   item.classList.toggle('is-preview-hidden',hidden);item.style.left=(i*pitch)+'px';
  });
  reset();
 }
 if(typeof ResizeObserver==='function'){observer=new ResizeObserver(fit);observer.observe(row);}
 else window.addEventListener('resize',fit,{passive:true});
 if(scope&&typeof MutationObserver==='function'){
  scopeObserver=new MutationObserver(()=>{if(searchOpen||scope.classList.contains('search-scope-open'))reset();});
  scopeObserver.observe(scope,{attributes:true,attributeFilter:['class']});
 }
 motion.addEventListener('change',reset);hover.addEventListener('change',reset);fit();
 whRecentController={destroy(){
  reset();destroyed=true;observer?.disconnect();scopeObserver?.disconnect();
  if(!observer)window.removeEventListener('resize',fit);
  motion.removeEventListener('change',reset);hover.removeEventListener('change',reset);
  row.removeEventListener('pointermove',onPointerMove);row.removeEventListener('pointerleave',onPointerLeave);
  focusHandlers.forEach(({item,button,onFocus,onFocusOut})=>{
   button.removeEventListener('focus',onFocus);item.removeEventListener('focusout',onFocusOut);
  });
 }};
}
function whPreviewMarkup(){
 const seen=new Set();const recent=[...whRecords].sort((a,b)=>b.last.localeCompare(a.last)).filter(r=>{if(seen.has(r.group))return false;seen.add(r.group);return true;});
 return `<div class="continue-shell"><div class="continue-clip"><section class="continue wh-recent" aria-label="Recently Watched">
 <div class="wh-recent-header">Recently Watched${whRecentTestMode?' · Test data':''}</div>
 <div class="wh-recent-row">${recent.map(r=>`<div class="wh-recent-item"><button class="wh-recent-card" type="button" data-wh-recent="${escapeHTML(r.id)}" style="--cover:${escapeHTML(whCoverValue(r.cover))}" aria-label="Open ${escapeHTML(r.title)}; ${whCompleted(r)?'Completed':`Episode ${whLastEpisode(r).n}`}"><span class="wh-recent-card-label">${escapeHTML(r.short)}</span></button><div class="wh-recent-info" aria-hidden="true"><strong>${escapeHTML(r.title)}</strong><span>${whCompleted(r)?'Completed':`Episode ${whLastEpisode(r).n}`}</span></div></div>`).join('')}
 <button class="wh-recent-view" type="button" id="wh-view-history">${whSmallIcon('history')}<span>View History</span></button></div></section></div></div>`;
}
function whEpisodeMarkup(r,ep){
 const status=whEpisodeStatus(ep),label=whEpisodeStatusLabel(status),next=whEpisodeStatusLabel(whEpisodeNextStatus(ep));
 return `<button type="button" class="wh-episode wh-episode-row" data-wh-episode="${escapeHTML(r.id)}:${ep.n}" aria-pressed="${whEpisodePress(status)}" aria-label="Episode ${ep.n}: ${label}. Next: ${next}" title="${label} — click to mark ${next}"><span class="wh-episode-main"><span class="wh-episode-number">Episode ${ep.n}</span>${status==='partial'&&ep.started&&ep.progressSeconds>0?`<span class="wh-episode-position">${whFmt(ep.progressSeconds)} / ${whFmt(ep.duration)}</span>`:''}</span><span class="wh-episode-toggle"><span class="wh-status-icon is-${status}">${status==='watched'?whSmallIcon('check'):''}</span><span class="wh-episode-label">${label}</span></span></button>`;
}
/* Watch History only: a shared, visibility-scoped clock drives the approved
 * capsule geometry and reversible 280ms progress changes. No playback or storage edits. */
const whProgressMotion=matchMedia('(prefers-reduced-motion: reduce)');
const whProgressEntries=new Map();
let whProgressFrame=0,whProgressResize=null,whProgressIntersection=null,whProgressMaskId=0;
function whProgressCounts(r){
 const watched=whCount(r),total=r.episodes.length;
 const partial=r.episodes.reduce((n,e)=>n+(whEpisodeStatus(e)==='partial'?1:0),0);
 return {watched,total,done:total?watched/total:0,started:total?(watched+partial)/total:0};
}
function whProgressMarkup(r,initialComplete=false){
 const {watched,total,done,started}=whProgressCounts(r),last=whLastEpisode(r);
 const d=initialComplete?1:done,s=initialComplete?1:started,id='wh-progress-mask-'+(++whProgressMaskId);
 return '<div class="wh-meta wh-progress-episode">Episode '+(last?.n||1)+' · '+whFmt(last?.progressSeconds)+' / '+whFmt(last?.duration)+'</div>'+
  '<div class="wh-meta wh-progress-count">'+watched+' of '+total+' episodes watched</div>'+
  '<div class="wh-progress gallery-split-timeline" aria-hidden="true" data-wh-done="'+d+'" data-wh-started="'+s+'">'+
  '<div class="wh-progress-done" style="flex-basis:'+galleryTimelineFill(s*100)+'"><svg class="wh-progress-svg" width="100%" height="5" aria-hidden="true">'+
  '<defs><mask id="'+id+'" maskUnits="userSpaceOnUse" x="-2" y="-2" width="354" height="9"><rect x="-2" y="-2" width="354" height="9" fill="white"/><path class="wh-progress-cut" fill="black"/></mask></defs>'+
  '<rect class="wh-progress-end" height="5" fill="currentColor" mask="url(#'+id+')"/><path class="wh-progress-capsules" fill="currentColor"/><rect class="wh-progress-solid" height="5" fill="currentColor"/></svg></div><div class="wh-progress-rest"></div></div>';
}
function whProgressCompleted(fade=false){return '<div class="wh-completed'+(fade?' wh-progress-arrived':'')+'">'+whSmallIcon('completed')+' Completed</div>';}
function whProgressCapsule(x,w,y=0,h=5){
 if(w<=0)return '';
 const r=Math.min(w/2,h/2),right=x+w,bottom=y+h;
 return 'M'+(x+r)+' '+y+' H'+(right-r)+' A'+r+' '+r+' 0 0 1 '+right+' '+(y+r)+' V'+(bottom-r)+' A'+r+' '+r+' 0 0 1 '+(right-r)+' '+bottom+' H'+(x+r)+' A'+r+' '+r+' 0 0 1 '+x+' '+(bottom-r)+' V'+(y+r)+' A'+r+' '+r+' 0 0 1 '+(x+r)+' '+y+' Z ';
}
function whProgressRect(node,x,w){
 node.setAttribute('x',x);node.setAttribute('width',Math.max(0,w));node.setAttribute('rx',Math.min(2.5,Math.max(0,w)/2));
}
function whProgressPaint(e,now){
 const {track,fill,solid,end,capsules,cut}=e;
 const width=track.getBoundingClientRect().width,gap=parseFloat(getComputedStyle(track).columnGap)||5;
 const usable=Math.max(0,width-gap),d=usable*e.done,s=usable*e.started,partial=Math.max(0,s-d);
 const endpoint=Math.min(8,partial),edge=s-endpoint;
 fill.style.flexBasis=galleryTimelineFill(e.started*100);
 whProgressRect(solid,0,d);whProgressRect(end,edge,endpoint);
 let moving='',holes='';
 if(partial>8){
  const phase=whProgressMotion.matches?0:(now/1100*13)%13;
  // Begin underneath the solid fill. Stop when the moving capsule aligns with
  // the fixed endpoint; only the underlying endpoint is masked by the 1px cutout.
  for(let x=d-13+phase;x<edge;x+=13){
   const left=Math.max(0,x),length=Math.min(8+x-left,s-left);
   moving+=whProgressCapsule(left,length);
   if(x+9>edge)holes+=whProgressCapsule(x-1,10,-1,7);
  }
 }
 capsules.setAttribute('d',moving);cut.setAttribute('d',holes);
 e.flow=partial>8;
}
function whProgressEase(p){
 // CSS ease = cubic-bezier(.25,.1,.25,1), sampled on the same clock for both ends.
 const bez=(a,b,t)=>3*a*(1-t)*(1-t)*t+3*b*(1-t)*t*t+t*t*t;
 let lo=0,hi=1;for(let i=0;i<16;i++){const mid=(lo+hi)/2;if(bez(.25,.25,mid)<p)lo=mid;else hi=mid;}
 return p<=0?0:p>=1?1:bez(.1,1,(lo+hi)/2);
}
function whProgressSample(e,now){
 if(!e.motion)return;
 const a=e.motion,p=whProgressMotion.matches?1:Math.min(1,Math.max(0,(now-a.time)/280)),v=whProgressEase(p);
 e.done=a.fromDone+(a.done-a.fromDone)*v;e.started=a.fromStarted+(a.started-a.fromStarted)*v;
 if(p===1){e.done=a.done;e.started=a.started;e.motion=null;}
}
function whProgressRemove(e){
 whProgressResize?.unobserve(e.track);whProgressIntersection?.unobserve(e.track);whProgressEntries.delete(e.track);
}
function whProgressFinish(e){
 if(e.motion||e.done!==1||e.started!==1||!e.track.isConnected)return;
 const info=e.track.parentElement;
 e.track.insertAdjacentHTML('afterend',whProgressCompleted(!whProgressMotion.matches));
 info.querySelector('.wh-progress-episode')?.remove();info.querySelector('.wh-progress-count')?.remove();
 whProgressRemove(e);e.track.remove();
}
function whProgressSchedule(){
 if(!whOpen||document.hidden||whProgressFrame)return;
 if([...whProgressEntries.values()].some(e=>e.motion||(e.visible&&e.flow&&!whProgressMotion.matches)))
  whProgressFrame=requestAnimationFrame(whProgressTick);
}
function whProgressTick(now){
 whProgressFrame=0;if(!whOpen){whProgressStop();return;}
 for(const e of whProgressEntries.values()){
  if(!e.track.isConnected){whProgressRemove(e);continue;}
  if(e.motion||(e.visible&&e.flow)){
   whProgressSample(e,now);whProgressPaint(e,now);whProgressFinish(e);
  }
 }
 whProgressSchedule();
}
function whProgressMount(track){
 if(!track)return null;
 const e={track,fill:track.querySelector('.wh-progress-done'),solid:track.querySelector('.wh-progress-solid'),
  end:track.querySelector('.wh-progress-end'),capsules:track.querySelector('.wh-progress-capsules'),cut:track.querySelector('.wh-progress-cut'),
  done:Number(track.dataset.whDone),started:Number(track.dataset.whStarted),motion:null,flow:false,visible:true};
 whProgressEntries.set(track,e);
 if(!whProgressResize&&typeof ResizeObserver==='function')whProgressResize=new ResizeObserver(items=>{
  for(const item of items){const e=whProgressEntries.get(item.target);if(e)whProgressPaint(e,performance.now());}whProgressSchedule();
 });
 if(!whProgressIntersection&&typeof IntersectionObserver==='function')whProgressIntersection=new IntersectionObserver(items=>{
  for(const item of items){const e=whProgressEntries.get(item.target);if(e)e.visible=item.isIntersecting;}whProgressSchedule();
 });
 whProgressResize?.observe(track);whProgressIntersection?.observe(track);
 whProgressPaint(e,performance.now());whProgressSchedule();return e;
}
function whProgressStop(){
 if(whProgressFrame)cancelAnimationFrame(whProgressFrame);whProgressFrame=0;
 whProgressResize?.disconnect();whProgressIntersection?.disconnect();whProgressResize=null;whProgressIntersection=null;
 whProgressEntries.clear();
}
function whProgressUpdate(row,r){
 const {watched,total,done,started}=whProgressCounts(r),info=row.querySelector('.wh-info');
 let track=info.querySelector('.wh-progress'),e=whProgressEntries.get(track);
 if(!track){
  if(done===1)return;
  const completed=info.querySelector('.wh-completed');
  completed.insertAdjacentHTML('beforebegin',whProgressMarkup(r,true));completed.remove();
  track=info.querySelector('.wh-progress');e=whProgressMount(track);
 }else if(!e)e=whProgressMount(track);
 info.querySelector('.wh-progress-count').textContent=watched+' of '+total+' episodes watched';
 track.dataset.whDone=done;track.dataset.whStarted=started;
 const now=performance.now();whProgressSample(e,now);
 e.motion={time:now,fromDone:e.done,fromStarted:e.started,done,started};
 whProgressSample(e,now);whProgressPaint(e,now);whProgressFinish(e);whProgressSchedule();
}
whProgressMotion.addEventListener('change',()=>{
 const now=performance.now();
 for(const e of whProgressEntries.values()){whProgressSample(e,now);whProgressPaint(e,now);whProgressFinish(e);}
 whProgressSchedule();
});
document.addEventListener('visibilitychange',()=>{
 if(document.hidden){if(whProgressFrame)cancelAnimationFrame(whProgressFrame);whProgressFrame=0;}
 else whProgressSchedule();
});
function whSummaryMarkup(r){
 const complete=whCompleted(r),open=whExpanded.has(r.id);
 return `<div class="wh-summary">
 <button class="wh-summary-hit" type="button" data-wh-expand="${escapeHTML(r.id)}" aria-expanded="${open}" aria-label="${open?'Collapse':'Expand'} episodes for ${escapeHTML(r.title)}" title="${open?'Collapse episodes':'View episodes'}"></button>
 <button class="wh-cover-button" type="button" data-wh-open="${escapeHTML(r.id)}" title="Open anime details"><span class="wh-cover" style="--cover:${escapeHTML(whCoverValue(r.cover))}"><span>${escapeHTML(r.short)}</span></span></button>
 <div class="wh-info"><button class="wh-anime-title" type="button" data-wh-open="${escapeHTML(r.id)}">${escapeHTML(r.title)}</button>
 ${complete?whProgressCompleted():whProgressMarkup(r)}
 <div class="wh-meta">Last watched ${whFormatDate(r.last)}</div></div>
 <div class="wh-actions"><span class="wh-action wh-expand" aria-hidden="true">${whSmallIcon('chevron')}</span><button class="wh-action wh-trash" type="button" data-wh-remove="${escapeHTML(r.id)}" aria-label="Remove ${escapeHTML(r.title)} from history" title="Remove from history">${whSmallIcon('trash')}</button></div>
 </div>`;
}
function whRowMarkup(r){const open=whExpanded.has(r.id);return `<section class="wh-season ${open?'is-expanded':''}" data-wh-row="${escapeHTML(r.id)}" aria-label="${escapeHTML(r.title)}">${whSummaryMarkup(r)}<div class="wh-episodes"><div class="wh-episodes-inner" ${open?'':'inert aria-hidden="true"'}><div class="wh-episodes-content"><div class="wh-episode-head"><strong>Episodes</strong><span>${whCount(r)} / ${r.episodes.length} watched</span></div><div class="wh-episode-shell" data-wh-shell="${escapeHTML(r.id)}"><div class="wh-episode-scroll gallery-episode-scroll" role="region" tabindex="0" aria-label="Scrollable episodes for ${escapeHTML(r.title)}">${r.episodes.map(ep=>whEpisodeMarkup(r,ep)).join('')}</div><div class="wh-inner-overlay" aria-hidden="true"><div class="wh-inner-thumb"></div></div></div><p class="wh-episode-hint">Click an episode to cycle Not Watched, Partially Watched, and Watched. Saved playback position is kept separately.</p></div></div></div></section>`;}
function whPageMarkup(){
 const groups=whGroups(),total=groups.reduce((n,g)=>n+g.items.length,0),removed=whRecords.filter(r=>whPending.has(r.id));
 return `<section id="wh-root" aria-label="Watch History">
 <header class="detail-page-header wh-page-header">
  <h1 class="detail-title sf-optical-title">Watch History</h1>
  <button type="button" class="detail-back" data-wh-exit>${icon('back',18)} Back to Discover</button>
 </header>
 <div class="wh-controls"><div class="wh-segmented" role="group" aria-label="Filter Watch History">${[['all','All'],['progress','In Progress'],['completed','Completed']].map(([name,label])=>`<button type="button" data-wh-filter="${name}" aria-pressed="${whFilter===name}">${label}</button>`).join('')}</div>
 <button type="button" class="wh-sort" data-wh-sort title="Reverse watch history sorting">${whSmallIcon('sort')} ${whSort==='newest'?'Newest First':'Oldest First'}</button></div>
 ${removed.length?`<aside class="wh-undo" aria-label="Pending removals"><div class="wh-undo-top"><div><strong>${removed.length} ${removed.length===1?'season':'seasons'} removed from view</strong><div class="wh-undo-hint">Undo is available until you leave Watch History.</div></div><button type="button" class="btn small" data-wh-undo-all>Undo all</button></div><div class="wh-undo-items">${removed.map(r=>`<div class="wh-undo-item"><span>${escapeHTML(r.title)}</span><button type="button" data-wh-undo="${escapeHTML(r.id)}" aria-label="Undo removal of ${escapeHTML(r.title)}">Undo</button></div>`).join('')}</div></aside>`:''}
 <div class="wh-result-count">${total} ${total===1?'season':'seasons'} ${whSearch?'matching your search':'in this view'}</div>
 ${total?groups.map(g=>`${g.label?`<div class="wh-match-heading">${escapeHTML(g.label)}</div>`:''}<div class="wh-list">${g.items.map(whRowMarkup).join('')}</div>`).join(''):`<div class="wh-empty">Nothing to show. ${whSearch?'Try a different title or viewing date.':'Try another filter, or undo a removal.'}</div>`}
 <div class="wh-prototype-note">Gallery v103 design preview: the initial history entries and covers are sample data for testing the UI. Actual source streaming isn't yet connected in this HTML prototype. When a supported local video plays, this preview can record its progress on this device.</div>
 </section>`;
}
function whAttachInner(area,overlay){
 const thumb=overlay.querySelector('.wh-inner-thumb');let timer=null,dragging=false,dragY=0,dragTop=0,intent=0;
 const update=()=>{const max=area.scrollHeight-area.clientHeight,track=overlay.clientHeight;if(max<=1||track<=0){overlay.classList.remove('is-visible');return false}const h=Math.min(track,Math.max(40,Math.round(track*area.clientHeight/area.scrollHeight)));thumb.style.height=h+'px';thumb.style.transform=`translate3d(0,${(track-h)*area.scrollTop/max}px,0)`;return true;};
 const reveal=()=>{if(!update())return;overlay.classList.add('is-visible');clearTimeout(timer);timer=setTimeout(()=>{if(!dragging)overlay.classList.remove('is-visible');},950);};
 const intentScroll=()=>{intent=performance.now()+1400;reveal();};
 const onScroll=()=>{update();if(performance.now()<intent||dragging)reveal();};
 const onKey=e=>{if(['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(e.key))intentScroll();};
 /* Native scroll chaining through clipped, non-scrollable wrappers; no wheel interception. */
 const down=e=>{if(e.button!==0||!update())return;e.preventDefault();dragging=true;dragY=e.clientY;dragTop=area.scrollTop;overlay.classList.add('is-dragging','is-visible');clearTimeout(timer);thumb.setPointerCapture(e.pointerId);};
 const move=e=>{if(!dragging)return;const distance=overlay.clientHeight-thumb.getBoundingClientRect().height,max=area.scrollHeight-area.clientHeight;if(distance>0)area.scrollTop=dragTop+(e.clientY-dragY)*max/distance;reveal();};
 const up=()=>{if(!dragging)return;dragging=false;overlay.classList.remove('is-dragging');reveal();};
 area.addEventListener('wheel',intentScroll,{passive:true});area.addEventListener('touchmove',intentScroll,{passive:true});area.addEventListener('scroll',onScroll,{passive:true});area.addEventListener('keydown',onKey);
 thumb.addEventListener('pointerdown',down);thumb.addEventListener('pointermove',move);thumb.addEventListener('pointerup',up);thumb.addEventListener('pointercancel',up);thumb.addEventListener('lostpointercapture',up);
 return {area,update,destroy(){clearTimeout(timer);area.removeEventListener('wheel',intentScroll);area.removeEventListener('touchmove',intentScroll);area.removeEventListener('scroll',onScroll);area.removeEventListener('keydown',onKey);thumb.removeEventListener('pointerdown',down);thumb.removeEventListener('pointermove',move);thumb.removeEventListener('pointerup',up);thumb.removeEventListener('pointercancel',up);thumb.removeEventListener('lostpointercapture',up);}};
}
function whDestroyInner(){whProgressStop();for(const scroller of whInnerScrollers.values())scroller.destroy();whInnerScrollers.clear();}
/* Expand/collapse in place so DOM, scroll position and animated height remain stable. */
function whToggleRow(id){
 const row=[...screen.querySelectorAll('[data-wh-row]')].find(el=>el.dataset.whRow===id);
 if(!row)return;
 const opening=!whExpanded.has(id);
 if(opening)whExpanded.add(id);else whExpanded.delete(id);
 row.classList.toggle('is-expanded',opening);
 const hit=row.querySelector('.wh-summary-hit');
 const record=whRecords.find(r=>r.id===id);
 hit.setAttribute('aria-expanded',String(opening));
 hit.setAttribute('aria-label',`${opening?'Collapse':'Expand'} episodes for ${record?.title||''}`);
 hit.title=opening?'Collapse episodes':'View episodes';
 const inner=row.querySelector('.wh-episodes-inner');
 inner.inert=!opening;
 if(opening)inner.removeAttribute('aria-hidden');else inner.setAttribute('aria-hidden','true');
 if(opening&&!whInnerScrollers.has(id)){
  const shell=row.querySelector('[data-wh-shell]');
  const area=shell.querySelector('.wh-episode-scroll');
  const scroller=whAttachInner(area,shell.querySelector('.wh-inner-overlay'));
  whInnerScrollers.set(id,scroller);
  const last=record&&whLastEpisode(record);
  const columns=matchMedia('(max-width:820px)').matches?1:2;
  if(record&&record.episodes.length>6*columns&&last)
   area.scrollTop=Math.max(0,(Math.floor((last.n-1)/columns)-2)*42);
 }
 if(opening)requestAnimationFrame(()=>{if(whExpanded.has(id))whInnerScrollers.get(id)?.update();});
 row.querySelector('.wh-episodes').addEventListener('transitionend',event=>{
  if(event.propertyName==='grid-template-rows')updateTabScrollOverlay();
 },{once:true});
 requestAnimationFrame(updateTabScrollOverlay);
}
function whRender({keepScroll=true}={}){
 if(!whOpen)return;
 const old=keepScroll?workspace.scrollTop:0;
 const prevPositions=new Map([...whInnerScrollers.entries()].map(([id,scroller])=>[id,scroller.area.scrollTop]));
 whDestroyInner();screen.innerHTML=whPageMarkup();
 screen.querySelectorAll('#wh-root .wh-progress').forEach(whProgressMount);
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
 const status=whEpisodeStatus(ep),label=whEpisodeStatusLabel(status),next=whEpisodeStatusLabel(whEpisodeNextStatus(ep));
 button.setAttribute('aria-pressed',whEpisodePress(status));button.setAttribute('aria-label',`Episode ${ep.n}: ${label}. Next: ${next}`);button.title=`${label} — click to mark ${next}`;
 const mark=button.querySelector('.wh-status-icon');mark.className='wh-status-icon is-'+status;mark.innerHTML=status==='watched'?whSmallIcon('check'):'';
 button.querySelector('.wh-episode-label').textContent=label;
 const main=button.closest('.wh-episode').querySelector('.wh-episode-main');let position=main.querySelector('.wh-episode-position');
 if(status==='partial'&&ep.started&&ep.progressSeconds>0){if(!position){position=document.createElement('span');position.className='wh-episode-position';main.append(position)}position.textContent=`${whFmt(ep.progressSeconds)} / ${whFmt(ep.duration)}`;}else position?.remove();
 const row=button.closest('.wh-season');whProgressUpdate(row,r);
 row.querySelector('.wh-episode-head span').textContent=`${whCount(r)} / ${r.episodes.length} watched`;
 // No rebuild of episode panel; its scrollbar, selected control and scroll position stay stationary.
}
function whEnter(){
 if(whOpen)return;
 transitionGalleryStage(()=>{
  if(searchOpen)closeInlineSearch(false);
  whParentView=state.view;whSuspended=null;whOpen=true;
  document.body.classList.add('watch-history-view');
  whFilter='all';whSort='newest';whSearch='';whExpanded.clear();whPending.clear();
  hideTabScrollOverlay();render();workspace.scrollTop=0;
 });
}
function whSuspendForDetail(){
 whSuspended={scroll:workspace.scrollTop,inner:new Map([...whInnerScrollers].map(([id,scroller])=>[id,scroller.area.scrollTop]))};
 whDestroyInner();whOpen=false;document.body.classList.remove('watch-history-view');
}
function whResumeFromDetail(){
 const saved=whSuspended;
 whOpen=true;state.playback=null;state.detailId=null;
 state.view=whParentView;updateActiveTab(state.view);
 document.body.classList.add('watch-history-view');
 render();workspace.scrollTop=saved?.scroll||0;
 for(const [id,position] of saved?.inner||[])if(whInnerScrollers.has(id))whInnerScrollers.get(id).area.scrollTop=position;
 whSuspended=null;
}
function whExit({renderAfter=true}={}){
 if(!whOpen)return;
 const exit=()=>{
  whOpen=false;whSuspended=null;document.body.classList.remove('watch-history-view');
  whDestroyInner();if(whPending.size){whRecords=whRecords.filter(r=>!whPending.has(r.id));whSave();}
  whPending.clear();whExpanded.clear();whFilter='all';whSort='newest';whSearch='';
  if(searchOpen)closeInlineSearch(false);
  if(renderAfter){state.view=whParentView;updateActiveTab(state.view);render();requestAnimationFrame(updateTabScrollOverlay);}
 };
 if(renderAfter)transitionGalleryStage(exit);else exit();
}
function whOpenTitle(r){
 if(!r.galleryId||!demo.some(x=>x.id===r.galleryId)){
  modal('Sample Watch History entry',`<p class="description">${escapeHTML(r.title)} is a layout-testing record; this HTML version has no matching anime detail page. The Watch History entry remains editable here.</p>`,`<button class="btn primary" id="wh-sample-okay">Got it</button>`);
  document.getElementById('wh-sample-okay')?.addEventListener('click',closeModal);return;
 }
 const targetView=r.library?'library':'discover';
 transitionGalleryStage(()=>{
  whSuspendForDetail();state.view=targetView;updateActiveTab(targetView);
  showDetail(r.galleryId,true);state.detailReturnScroll=tabPages[targetView].scrollTop;
  const x=demo.find(x=>x.id===r.galleryId);const index=getSeasons(x).findIndex(s=>s.id===r.installmentId);
  if(index>=0){state.detailSeason=index;state.detailRelated=null;render();}
 });
}
/* All page actions live in one delegated listener; episode toggles don't rebuild their list. */
screen.addEventListener('click',event=>{
 if(!whOpen)return;const b=event.target.closest('button');if(!b)return;
 if(b.hasAttribute('data-wh-exit')){whExit();return;}
 if(b.dataset.whFilter){whFilter=b.dataset.whFilter;whRender();return;}
 if(b.hasAttribute('data-wh-sort')){whSort=whSort==='newest'?'oldest':'newest';whRender();return;}
 if(b.dataset.whExpand){whToggleRow(b.dataset.whExpand);return;}
 if(b.dataset.whRemove){whPending.add(b.dataset.whRemove);whExpanded.delete(b.dataset.whRemove);whRender();return;}
 if(b.dataset.whUndo){whPending.delete(b.dataset.whUndo);whRender();return;}
 if(b.hasAttribute('data-wh-undo-all')){whPending.clear();whRender();return;}
 if(b.dataset.whOpen){const record=whRecords.find(r=>r.id===b.dataset.whOpen);if(record)whOpenTitle(record);return;}
 if(b.dataset.whEpisode){const divider=b.dataset.whEpisode.lastIndexOf(':'),id=b.dataset.whEpisode.slice(0,divider),n=Number(b.dataset.whEpisode.slice(divider+1));const r=whRecords.find(r=>r.id===id),ep=r?.episodes.find(ep=>ep.n===n);if(!ep)return;ep.manualStatus=whEpisodeNextStatus(ep);whUpdateEpisodeInPlace(b,r,ep);whSave();return;}
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
 delete ep.manualStatus;ep.started=true;ep.duration=Math.floor(video.duration);ep.progressSeconds=Math.floor(video.currentTime);if(markWatched)ep.watched=true;
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

