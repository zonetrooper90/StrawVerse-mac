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

