// The controls fade out during playback and stay visible for keyboard users.
let playerControlsTimer=null;
let playerEventController=null;
let playerKeyboardFocus=false;
// One mounted video owns its callbacks and latest asynchronous request.
let sfPlayerSession=null;
let playerFocusTimer=null;
function sfPlayerOwnsVideo(video){
 const owner=sfPlayerSession;
 return Boolean(owner?.active&&video&&owner.video===video&&owner.playback===state.playback&&
  video.isConnected&&document.getElementById('local-video')===video);
}
function sfPlayerOwnsRequest(owner,request){
 return Boolean(owner&&sfPlayerSession===owner&&sfPlayerOwnsVideo(owner.video)&&owner.request===request);
}
function sfPlayerRetire(){
 const owner=sfPlayerSession;if(!owner?.active)return;
 owner.active=false;++owner.request;
 playerEventController?.abort();playerEventController=null;
 clearTimeout(playerControlsTimer);playerControlsTimer=null;
 clearTimeout(playerFocusTimer);playerFocusTimer=null;
 sfPlayerDemoStop();owner.video.pause();resetPlayNextState();
 cancelAnimationFrame(sfPlayMorph.frame);sfPlayMorph.frame=0;
 whPlayerSession=null;isLocalVideoReady=false;
}
function sfPlayerTeardown(){
 const owner=sfPlayerSession;if(!owner)return;
 sfPlayerRetire();sfPlayerSession=null;
 // Release the old decoder without altering the next mounted video.
 owner.video.removeAttribute('src');owner.video.load();
 sfPlayerReleaseBrowserVideo();localVideoName='';
}
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
 if(!sfPlayerOwnsVideo(video))return;
 const playingNow=sfPlayerDemo.active?sfPlayerDemo.playing:(!video.paused&&!video.ended);
 if((!isLocalVideoReady&&!sfPlayerDemo.active)||!playingNow||playNextShown){area.classList.remove('controls-hidden');return;}
 const focused=document.activeElement;
 if(playerKeyboardFocus&&focused&&area.contains(focused)&&focused!==area)return;
 if(document.getElementById('modal-host')?.firstElementChild)return;
 playerControlsTimer=setTimeout(()=>{
  if(!sfPlayerOwnsVideo(video))return;
  playerControlsTimer=null;
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
 const owner=sfPlayerSession={active:true,video:v,playback:state.playback,request:0};
 const owns=()=>sfPlayerOwnsVideo(v)&&sfPlayerSession===owner;
 const signal=playerEventController.signal;
 const on=(target,name,handler)=>target?.addEventListener?.(name,event=>{if(owns())handler(event);},{signal});
 isLocalVideoReady=false;localVideoName='';
 resetPlayNextState();
 sfResetPlayMorph();
 playerSubtitleState.enabled=state.playback?.subtitles!==false;
 playerSubtitleState.lastIndex=null;
 playerSubtitleState.lastLanguage='en';
 v.volume=playerSessionVolume/100;v.muted=playerSessionMuted;v.autoplay=false;v.loop=false;
 whInitPlayerSession();
 on(v,'timeupdate',()=>whOnVideoTick(v));
 on(v,'seeked',()=>whOnVideoSeek(v));
 on(v,'loadedmetadata',()=>{whInitPlayerSession();isLocalVideoReady=true;document.getElementById('player-empty').hidden=true;applyPlayerSubtitleState(v);updatePlaybackUI();});
 on(v.textTracks,'addtrack',()=>applyPlayerSubtitleState(v));
 on(v,'error',()=>{isLocalVideoReady=false;document.getElementById('player-empty').hidden=false;showPlayerNotice('The selected file cannot be decoded in the integrated Chromium player. You may try VLC, if installed, or another compatible file.');updatePlaybackUI();});
 for(const name of ['timeupdate','seeked','durationchange','play','pause','ended','ratechange'])on(v,name,updatePlaybackUI);
 on(v,'volumechange',()=>{rememberGalleryPlayerVolume(v);updatePlaybackUI();});
 on(v,'play',playerControlsWake);
  on(v,'ended',()=>{if(state.autoplayNextEpisode&&!playNextCanceled&&playerCanAdvance()&&!playNextPreview)showPlayerNotice('This local-file test ended. Play Next cannot load the following episode until a real episode source is connected.');});
 for(const name of ['pause','ended','emptied'])on(v,name,()=>{clearTimeout(playerControlsTimer);playerControlsTimer=null;document.getElementById('player-area')?.classList.remove('controls-hidden');});
 const playerArea=document.getElementById('player-area');
 on(playerArea,'pointermove',()=>{playerKeyboardFocus=false;playerControlsWake();});
 on(playerArea,'pointerdown',()=>{playerKeyboardFocus=false;playerControlsWake();});
 on(playerArea,'keydown',()=>{playerKeyboardFocus=true;playerControlsWake();});
 on(document,'keydown',e=>{if(e.key==='Tab')playerKeyboardFocus=true;});
 on(playerArea,'focusin',playerControlsWake);
 on(playerArea,'focusout',()=>{clearTimeout(playerFocusTimer);playerFocusTimer=setTimeout(()=>{playerFocusTimer=null;if(owns())playerControlsScheduleHide();},0);});
 on(document,'fullscreenchange',playerControlsWake);
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
  document.getElementById('sf-start-over').onclick=()=>{if(!owns())return;sfPlayerDemoSeek(0);closeModal();};
  document.getElementById('sf-resume-now').onclick=()=>{if(!owns())return;sfPlayerDemoSeek(730);closeModal();};
 };

 document.getElementById('change-local-video').onclick=openLocalForPlayer;
 document.getElementById('pause-play').onclick=()=>{if(sfPlayerDemo.active){sfPlayerDemoPlayPause();return;}if(!isLocalVideoReady)return;if(v.paused)v.play().catch(e=>{if(owns())showPlayerNotice('Unable to play file: '+e.message);});else v.pause();};
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
 const fullscreen=()=>{const area=document.getElementById('player-area');if(!document.fullscreenElement)area.requestFullscreen?.().catch(()=>{if(owns())showPlayerNotice('Fullscreen is not available in this environment.');});else document.exitFullscreen?.();};
 document.getElementById('fullscreen').onclick=fullscreen;
 on(document.getElementById('previous-episode'),'click',()=>advanceEpisode(-1));
 on(document.getElementById('next-episode'),'click',()=>advanceEpisode(1));
 document.getElementById('open-external-vlc').onclick=async()=>{
  if(!window.galleryDesktop||!owns())return;
  const request=++owner.request;
  let result;
  try{result=await window.galleryDesktop.openInVLC();}
  catch(error){result={ok:false,message:error.message};}
  if(!sfPlayerOwnsRequest(owner,request))return;
  if(!result.ok)showPlayerNotice(`${result.message} Use Settings to locate VLC manually if automatic detection fails. External-player compatibility and progress tracking are not guaranteed.`);
  else showPlayerNotice('The selected local file was handed to VLC. Watch progress in Gallery is not tracked for external playback.');
 };
 // Guard property handlers against delivery to the retired screen.
 for(const el of screen.querySelectorAll('*')){
  for(const name of ['onclick','onchange','oninput']){
   const handler=el[name];if(typeof handler==='function')el[name]=function(event){if(owns())return handler.call(this,event);};
  }
 }
 updatePlaybackUI();
}

