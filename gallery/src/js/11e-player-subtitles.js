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


