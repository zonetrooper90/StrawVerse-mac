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
