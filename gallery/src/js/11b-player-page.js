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
