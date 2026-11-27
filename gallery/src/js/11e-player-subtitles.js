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
/* Player-only nonmodal, in-video settings panel. Keep the global Gallery
   modal(), its focus trap and all other dialogs completely unchanged. */
let playerSettingsMenu=null;
const PLAYER_SPEED_CHOICES=[.5,.75,1,1.25,1.5,2];
function playerSpeedName(rate){return Number(rate)===1?'Normal':Number(rate)+'×';}
function playerSubtitleName(track,index){
 const lang=track.language||'';
 const names={en:'English',da:'Danish',ja:'Japanese',de:'German',fr:'French',es:'Spanish',pt:'Portuguese',it:'Italian',ko:'Korean',zh:'Chinese'};
 return track.label||names[lang.toLowerCase().split('-')[0]]||lang||'Subtitle track '+(index+1);
}
function playerSubtitleSelection(video){
 const entries=playerSubtitleTracks(video),selected=preferredPlayerSubtitleTrack(entries);
 return {entries,selected,value:playerSubtitleState.enabled&&selected?'track-'+selected.index:'off'};
}
function positionPlayerSettingsMenu(){
 const menu=playerSettingsMenu;if(!menu||!menu.panel.isConnected)return;
 const area=menu.area.getBoundingClientRect(),button=menu.button.getBoundingClientRect();
 const right=Math.max(9,Math.min(area.width-130,area.right-button.right));
 const width=Math.max(130,Math.min(350,area.width-right-10));
 const bottom=Math.max(8,area.bottom-button.top+9);
 const available=Math.max(70,button.top-area.top-18);
 menu.panel.style.right=right+'px';
 menu.panel.style.bottom=bottom+'px';
 menu.panel.style.width=width+'px';
 menu.panel.style.maxHeight=available+'px';
}
function renderPlayerSettingsMenu(focusTarget){
 const menu=playerSettingsMenu;if(!menu)return;
 const video=menu.video,panel=menu.panel,subtitle=playerSubtitleSelection(video);
 const subtitleLabel=subtitle.value==='off'?'Off':playerSubtitleName(subtitle.selected.track,subtitle.selected.index);
 const row=(name,value,action)=>'<button type="button" id="player-'+action+'-option" class="player-settings-row-button" data-player-menu="'+action+'"><span class="player-settings-row-name">'+name+'</span><span class="player-settings-row-value">'+escapeHTML(value)+'</span><span class="player-settings-chevron" aria-hidden="true">›</span></button>';
 const header=(name,back)=>'<div class="player-settings-popover-head">'+(back?'<button type="button" class="player-settings-back" data-player-menu="back" aria-label="Back to player settings">‹</button>':'')+'<strong>'+name+'</strong></div>';
 let content;
 if(menu.view==='speed'){
  content=header('Playback speed',true)+'<div class="player-settings-popover-items">'+PLAYER_SPEED_CHOICES.map(rate=>'<button type="button" class="player-settings-choice" data-player-menu="speed:'+rate+'" aria-pressed="'+String(Number(video.playbackRate)===rate)+'"><span>'+playerSpeedName(rate)+'</span><span class="player-settings-selected" aria-hidden="true">'+(Number(video.playbackRate)===rate?'✓':'')+'</span></button>').join('')+'</div>';
 }else if(menu.view==='subtitles'){
  const options=[{value:'off',label:'Off'},...subtitle.entries.map(({track,index})=>({value:'track-'+index,label:playerSubtitleName(track,index)}))];
  content=header('Subtitles',true)+'<div class="player-settings-popover-items">'+options.map(option=>'<button type="button" class="player-settings-choice" data-player-menu="subtitle:'+option.value+'" aria-pressed="'+String(subtitle.value===option.value)+'"><span>'+escapeHTML(option.label)+'</span><span class="player-settings-selected" aria-hidden="true">'+(subtitle.value===option.value?'✓':'')+'</span></button>').join('')+'</div>';
 }else{
  content=header('Player settings',false)+'<div class="player-settings-popover-items">'+row('Playback speed',playerSpeedName(video.playbackRate),'speed')+row('Subtitles',subtitleLabel,'subtitles')+'</div>';
 }
 panel.dataset.view=menu.view;
 panel.innerHTML=content;
 positionPlayerSettingsMenu();
 if(focusTarget){
  const target=focusTarget==='back'?panel.querySelector('.player-settings-back'):panel.querySelector('[data-player-menu="'+focusTarget+'"]');
  (target||panel.querySelector('button'))?.focus({preventScroll:true});
 }
}
function closePlayerSettings({restoreFocus=false}={}){
 const menu=playerSettingsMenu;if(!menu)return;
 playerSettingsMenu=null;
 menu.panel.remove();
 if(menu.button.isConnected){
  menu.button.dataset.g1Active='false';
  menu.button.setAttribute('aria-expanded','false');
  if(restoreFocus)menu.button.focus({preventScroll:true});
 }
 if(sfPlayerOwnsVideo(menu.video))playerControlsScheduleHide();
}
function openPlayerSettings(video){
 if(!sfPlayerOwnsVideo(video))return;
 if(playerSettingsMenu?.video===video){closePlayerSettings({restoreFocus:true});return;}
 closePlayerSettings();
 const area=document.getElementById('player-area'),button=document.getElementById('player-settings');
 if(!area||!button)return;
 const panel=document.createElement('section');
 panel.id='player-settings-popover';
 panel.className='player-settings-popover';
 panel.setAttribute('role','dialog');
 panel.setAttribute('aria-modal','false');
 panel.setAttribute('aria-label','Player settings');
 panel.tabIndex=-1;
 area.appendChild(panel);
 playerSettingsMenu={video,area,button,panel,view:'main'};
 button.dataset.g1Active='true';
 button.setAttribute('aria-expanded','true');
 button.setAttribute('aria-controls',panel.id);
 panel.addEventListener('click',event=>{
  const action=event.target.closest('button[data-player-menu]');
  if(!action||!panel.contains(action)||playerSettingsMenu?.panel!==panel||!sfPlayerOwnsVideo(video))return;
  const cmd=action.dataset.playerMenu;
  if(cmd==='speed'||cmd==='subtitles'){
   playerSettingsMenu.view=cmd;
   renderPlayerSettingsMenu('back');
  }else if(cmd==='back'){
   const last=playerSettingsMenu.view;
   playerSettingsMenu.view='main';
   renderPlayerSettingsMenu(last);
  }else if(cmd.startsWith('speed:')){
   const next=Number(cmd.slice(6));
   if(!PLAYER_SPEED_CHOICES.includes(next))return;
   video.playbackRate=next;
   playerSettingsMenu.view='main';
   renderPlayerSettingsMenu('speed');
  }else if(cmd.startsWith('subtitle:')){
   const choice=cmd.slice(9),selection=playerSubtitleSelection(video);
   if(choice==='off')playerSubtitleState.enabled=false;
   else{
    const index=Number(choice.slice(6));
    const item=selection.entries.find(entry=>entry.index===index);
    if(!choice.startsWith('track-')||!item)return;
    playerSubtitleState.enabled=true;
    playerSubtitleState.lastIndex=index;
    if(item.track.language)playerSubtitleState.lastLanguage=item.track.language.toLowerCase();
   }
   if(state.playback)state.playback.subtitles=playerSubtitleState.enabled;
   applyPlayerSubtitleState(video);
   playerSettingsMenu.view='main';
   renderPlayerSettingsMenu('subtitles');
  }
 });
 renderPlayerSettingsMenu();
 panel.querySelector('button')?.focus({preventScroll:true});
 playerControlsWake();
}

function fmtTime(sec){if(!Number.isFinite(sec)||sec<0)return '00:00';const x=Math.floor(sec);return `${String(Math.floor(x/3600)).padStart(x>=3600?1:2,'0')}:${String(Math.floor(x%3600/60)).padStart(2,'0')}:${String(x%60).padStart(2,'0')}`.replace(/^00:/,'');}


