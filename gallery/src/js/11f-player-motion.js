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

