function readAutoplayNextEpisode(){try{return localStorage.getItem('gallery.autoplayNextEpisode')==='on';}catch{return false;}}
/* Initial player volume uses the Gallery default or the user's starting value.
   The default is 70%; session volume is not a saved starting preference. */
const GALLERY_VOLUME_STORAGE_KEY='gallery.playback.startingVolume';
const GALLERY_INITIAL_VOLUME=70;
function galleryVolumePercent(value,fallback=GALLERY_INITIAL_VOLUME){
 const n=Number(value);
 return value!==null&&value!==undefined&&value!==''&&Number.isFinite(n)?Math.min(100,Math.max(0,Math.round(n))):fallback;
}
function readGalleryVolumePreferences(){
 try{
  const saved=JSON.parse(localStorage.getItem(GALLERY_VOLUME_STORAGE_KEY)||'null');
  if(saved&&typeof saved==='object'){
   return {
    mode:saved.mode==='user'?'user':'gallery',
    preferred:galleryVolumePercent(saved.preferred),
    precision:saved.precision==='fine'?'fine':'steps'
   };
  }
 }catch{}
 return {mode:'gallery',preferred:GALLERY_INITIAL_VOLUME,precision:'steps'};
}
const galleryVolumePreferences=readGalleryVolumePreferences();
/* This default applies once, at launch. Episode changes share the session level. */
let playerSessionVolume=galleryVolumePreferences.mode==='user'?galleryVolumePreferences.preferred:GALLERY_INITIAL_VOLUME;
let playerSessionMuted=playerSessionVolume===0;
function saveGalleryVolumePreferences(){
 try{localStorage.setItem(GALLERY_VOLUME_STORAGE_KEY,JSON.stringify(galleryVolumePreferences));}catch{}
}
/* Record the in-session volume only. Muting must not change the starting
   preference, and must not overwrite the last audible level used for unmute. */
function rememberGalleryPlayerVolume(video){
 if(!video)return;
 playerSessionVolume=galleryVolumePercent(video.volume*100);
 playerSessionMuted=!!video.muted||playerSessionVolume===0;
 if(!playerSessionMuted&&playerSessionVolume>0)playerLastAudibleVolume=video.volume;
}

