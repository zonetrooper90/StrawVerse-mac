/* Electron bridge is narrowly scoped; standalone preview still renders. */
let localVideoName='',isLocalVideoReady=false,lastExternalPlayerStatus='not checked';
let savingPreference=false;
async function saveDesktopPreferences(){
 if(!window.galleryDesktop)return;
 try {await window.galleryDesktop.saveSettings({theme:state.theme,font:state.font,defaultPlayback:state.defaultPlayback,defaultDownload:state.defaultDownload,defaultSubtitles:state.defaultSubtitles,playerPreference:state.playerPreference||'built-in'});}catch(err){console.warn('Settings save failed:',err)}
}
async function setupDesktopSettings(){
 if(!window.galleryDesktop)return;
 document.body.classList.add('desktop-build');
 try{
  const prefs=await window.galleryDesktop.getSettings();
  if(SOFT_FUTURISTIC_THEMES.includes(prefs.theme))state.theme=prefs.theme;
  if(supportedGalleryFonts.includes(prefs.font)){state.font=prefs.font;document.body.dataset.font=state.font;try{localStorage.setItem('gallery.font',state.font)}catch{}}
  if(['sub','dub'].includes(prefs.defaultPlayback))state.defaultPlayback=prefs.defaultPlayback;
  if(['sub','dub'].includes(prefs.defaultDownload))state.defaultDownload=prefs.defaultDownload;
  if(typeof prefs.defaultSubtitles==='boolean')state.defaultSubtitles=prefs.defaultSubtitles;
  state.playerPreference=prefs.playerPreference||'built-in';
  document.body.dataset.theme=state.theme;
  render();
 }catch(err){console.warn('Could not load local settings:',err)}
}
