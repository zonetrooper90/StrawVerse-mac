/* v59 — Search settings across sections without changing their preferences.
   This index mirrors real v59 controls. Unimplemented Sources features remain previews. */
const settingsSearchIndex=[
 {key:'theme',section:'appearance',title:'Theme',path:'Appearance → Theme',target:'settings-theme-card',terms:'appearance color colour style light dark display theme look interface personalize customise neon reel midnight cinema paper lantern'},
 {key:'font',section:'appearance',title:'Typography',path:'Appearance → Typography',target:'settings-font-card',terms:'font fonts typeface typography atkinson hyperlegible next braille institute dyslexia reading readability low vision accessible accessibility inter san francisco system text characters letters alphabet language locale numbers special symbols preview'},
 {key:'subtitle-appearance',section:'playback',playbackTab:'subtitles',title:'Subtitle appearance',path:'Playback → Subtitles',target:'settings-subtitle-appearance',terms:'subtitles captions outline thickness drop shadow shadow strength font size effects customize appearance preview live position border text colour color white soft white yellow custom background box opacity none night day shrine video accessibility'},
 {key:'audio',section:'playback',title:'Default playback audio',path:'Playback → Playback preferences',target:'pref-playback',terms:'language sound voice dialogue dub sub japanese english audio playback preferred'},
 {key:'subtitles',section:'playback',title:'Subtitles when playback starts',path:'Playback → Playback preferences',target:'pref-subs',terms:'subtitle subtitles captions cc closed caption language text on off playback accessibility'},
  {key:'starting-volume',section:'playback',playbackTab:'general',title:'Starting volume',path:'Playback → General → Player integration',target:'settings-starting-volume-card',terms:'volume audio sound loudness starting user gallery preferred default fine slider percent steps playback mute level'},
 {key:'player',section:'playback',title:'Preferred player for local files',path:'Playback → Player integration',target:'player-pref',terms:'vlc mpv built-in player playback video external default local files'},
 {key:'vlc',section:'playback',title:'Locate VLC manually',path:'Playback → Player integration',target:'locate-vlc',terms:'vlc external media player find locate choose app macos'},
 {key:'download-language',section:'downloads',title:'Default download language',path:'Downloads → Download preferences',target:'pref-download',terms:'download language audio dub sub english japanese preferred'},
 {key:'destination',section:'downloads',title:'Destination folder',path:'Downloads → Destination folder',target:'settings-download-location',terms:'download location path save files folder directory standard downloads custom storage drive disk destination'},
 {key:'marketplace',section:'sources',sourceTab:'marketplace',title:'Sources Marketplace',path:'Sources → Marketplace',target:'sources-marketplace-region',terms:'source sources scraper extension extensions addon provider plugin install update marketplace discover anime'},
 {key:'installed',section:'sources',sourceTab:'installed',title:'Installed sources',path:'Sources → Installed',target:'sources-installed-region',terms:'installed sources extensions providers health blocked incompatible update unavailable manage remove'},
 {key:'repositories',section:'sources',sourceTab:'repositories',title:'Repositories',path:'Sources → Repositories',target:'settings-repositories-card',terms:'source sources extension repository repo github community add manage providers'},
 {key:'official-repository',section:'sources',sourceTab:'repositories',title:'Official StrawVerse repository',path:'Sources → Repositories',target:'settings-official-repository',terms:'strawverse repository repo official default built-in extensions'},
 {key:'about',section:'about',title:'About Gallery',path:'About → Application information',target:'settings-about-card',terms:'about app application gallery version build apple silicon mac os information prototype'},
 {key:'strawverse-credits',section:'about',aboutView:'credits',title:'Acknowledgements',path:'About → Acknowledgements',target:'settings-about-credits',terms:'strawverse original author creator theyogmehta open source fork upstream github repository credits attribution'},
 {key:'license-credits',section:'about',aboutView:'licenses',title:'Open Source Licenses',path:'About → Open Source Licenses',target:'settings-about-licenses',terms:'license licensing gpl version 3 software copyright acknowledgements third party dependencies generated'},
 {key:'media-credits',section:'about',aboutView:'components',title:'Third-Party Components',path:'About → Acknowledgements → Third-Party Components',target:'settings-about-components',terms:'mpv ffmpeg media player video libraries components open source author licenses extension publishers'},
 {key:'legal',section:'about',aboutView:'legal',title:'Legal & Privacy',path:'About → Legal & Privacy',target:'settings-about-legal',terms:'legal privacy policy terms of service copyright disclaimer independent providers'},
 {key:'terms',section:'about',aboutView:'terms',title:'Terms of Service',path:'About → Legal & Privacy → Terms of Service',target:'settings-about-terms',terms:'terms conditions warranty software license user responsibility support open-source external services'},
 {key:'privacy',section:'about',aboutView:'privacy',title:'Privacy Policy',path:'About → Legal & Privacy → Privacy Policy',target:'settings-about-privacy',terms:'privacy personal data zero collection telemetry local storage tracking analytics user history external providers networks ip addresses no tracking'},
 {key:'copyright',section:'about',aboutView:'copyright',title:'Copyright & Disclaimer',path:'About → Legal & Privacy → Copyright & Disclaimer',target:'settings-about-copyright',terms:'copyright dmca disclaimer legal media sources downloads hosting third party content intellectual property'}
];
function setAppearanceTab(tab,resetScroll=true){
 if(!['theme','typography'].includes(tab))return;
 appearanceTab=tab;
 for(const pane of settingsPage.querySelectorAll('[data-appearance-pane]'))pane.hidden=pane.dataset.appearancePane!==tab;
 for(const button of settingsPage.querySelectorAll('[data-appearance-tab]')){
  const current=button.dataset.appearanceTab===tab;
  button.setAttribute('aria-selected',String(current));button.tabIndex=current?0:-1;
 }
 if(resetScroll){workspace.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});hideTabScrollOverlay();}
}
function matchedSettingsResults(query){
 const words=query.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').trim().split(/\s+/).filter(Boolean);
 if(!words.length)return [];
 return settingsSearchIndex.filter(item=>{
  if(item.key==='starting-volume'&&state.playerPreference==='vlc')return false;
  const text=(item.title+' '+item.path+' '+item.terms).toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'');
  return words.every(word=>text.includes(word));
 });
}
function renderSettingsSearchResults(){
 const container=settingsPage.querySelector('#settings-search-results');
 if(!container)return;
 const searching=searchOpen&&document.body.classList.contains('settings-view');
 settingsPage.classList.toggle('is-searching',searching);
 for(const button of settingsPage.querySelectorAll('[data-settings-section]'))button.setAttribute('aria-current',!searching&&button.dataset.settingsSection===settingsLastSection?'page':'false');
 if(!searching){
  container.hidden=true;
  for(const panel of settingsPage.querySelectorAll('[data-settings-panel]'))panel.hidden=panel.dataset.settingsPanel!==settingsLastSection;
  return;
 }
 for(const panel of settingsPage.querySelectorAll('[data-settings-panel]'))panel.hidden=true;
 container.hidden=false;
 const query=searchInput.value.trim();
 const matches=matchedSettingsResults(query);
 if(!query){
  container.innerHTML=`<header class="settings-panel-head"><h2>Search settings</h2><p class="description">Find a preference from any Settings section.</p></header><div class="settings-search-placeholder">${icon('search',22)}<div><b>What would you like to change?</b><p>Try “language”, “subtitles”, “theme”, or “sources”.</p></div></div>`;
  return;
 }
 let html=`<header class="settings-panel-head"><h2>Search results</h2><p class="description" aria-live="polite">${matches.length} ${matches.length===1?'setting':'settings'} found for “${escapeHTML(query)}”</p></header>`;
 if(!matches.length)html+=`<div class="settings-search-placeholder settings-search-no-results">${icon('search',22)}<div><b>No matching settings</b><p>Try a different term or browse the sections on the left.</p></div></div>`;
 else for(const [key,label] of settingsSections){
  const items=matches.filter(item=>item.section===key);
  if(!items.length)continue;
  html+=`<section class="settings-result-group" aria-label="${escapeHTML(label)}"><h3>${escapeHTML(label)}</h3><div class="settings-result-stack">${items.map(item=>`<button class="settings-result-item" type="button" data-settings-search-key="${item.key}" aria-label="Open ${escapeHTML(item.title)} in ${escapeHTML(label)}"><span class="settings-result-text"><strong>${escapeHTML(item.title)}</strong><small>${escapeHTML(item.path)}</small></span>${icon('chevron',18)}</button>`).join('')}</div></section>`;
 }
 container.innerHTML=html;
 for(const button of container.querySelectorAll('[data-settings-search-key]'))button.addEventListener('click',()=>navigateToSettingsResult(button.dataset.settingsSearchKey));
}
let settingsJumpTimer=null;
function navigateToSettingsResult(key){
 const item=settingsSearchIndex.find(x=>x.key===key);
 if(!item)return;
 closeInlineSearch(false);
 setSettingsSection(item.section,false);
 if(item.section==='appearance')setAppearanceTab(item.key==='font'?'typography':'theme',false);
 if(item.section==='playback')setPlaybackTab(item.playbackTab||'general',false);
 if(item.section==='sources'&&item.sourceTab)setSourcesTab(item.sourceTab,false);
 if(item.section==='about')setAboutView(item.aboutView||'overview',false);
 const el=document.getElementById(item.target);
 if(!el)return;
 el.focus({preventScroll:true});
 el.classList.remove('settings-search-target');
 void el.offsetWidth;
 el.classList.add('settings-search-target');
 clearTimeout(settingsJumpTimer);
 settingsJumpTimer=setTimeout(()=>el.classList.remove('settings-search-target'),2200);
 // Content is already mounted: move only the Settings scroll container.
 requestAnimationFrame(()=>revealSettingsControl(el));
}
function settingsResultButtons(){return [...settingsPage.querySelectorAll('.settings-result-item')];}

