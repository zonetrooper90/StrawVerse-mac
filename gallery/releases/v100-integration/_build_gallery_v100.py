from pathlib import Path
import re, hashlib
src=Path('/mnt/data/Gallery-v99.html').read_text()
css=Path('/mnt/data/_gallery_v100_styles.css').read_text()
js=Path('/mnt/data/_gallery_v100_history.js').read_text()
s=src

def replace_exact(old,new,expect=1):
 global s
 count=s.count(old)
 if count!=expect: raise ValueError(f'Expected {expect} occurrences; found {count} for '+repr(old[:110]))
 s=s.replace(old,new)

def replace_first(old,new,expect=2):
 global s
 count=s.count(old)
 if count!=expect: raise ValueError(f'Expected {expect} occurrences; found {count} for '+repr(old[:110]))
 s=s.replace(old,new,1)

replace_exact('<title>Gallery v99 — Player Controls Refinements</title>','<title>Gallery v100 — Watch History and Player Scrollbars</title>')
replace_exact('</style></head>', '\n'+css+'\n</style></head>')
replace_exact('function discover(){', js+'\nfunction discover(){')
start=s.index(' const continuation=model.titles.some(')
end=s.index('\n const title=isSearching', start)
assert end-start<1600
s=s[:start]+' const continuation=whPreviewMarkup();'+s[end:]
replace_first(" on('filters',showFilters);on('resume',()=>showDetail('demo:02'));on('discover-browse-sources',openSourceManagerFromDiscover);",
              " on('filters',showFilters);on('wh-view-history',whEnter);\n for(const button of content.querySelectorAll('[data-wh-recent]'))button.addEventListener('click',()=>{const r=whRecords.find(r=>r.id===button.dataset.whRecent);if(!r)return;whEnter();whOpenTitle(r);});\n on('resume',()=>showDetail('demo:02'));on('discover-browse-sources',openSourceManagerFromDiscover);",expect=2)
replace_exact("function setView(view){\n if(!tabOrder.includes(view))return;",
              "function setView(view){\n if(!tabOrder.includes(view))return;\n if(whOpen){whExit();if(view==='discover')return;}")
replace_exact(" document.body.classList.toggle('player-view',Boolean(state.playback));\n if(!state.playback&&!state.detailId){showTabPages();return;}",
              " document.body.classList.toggle('player-view',Boolean(state.playback));\n if(whOpen){\n  freezeTabTrack();hideTabScrollOverlay();workspace.classList.remove('tab-pages-visible','library-view');tabPagesViewport.hidden=true;screen.hidden=false;screen.dataset.surfaceKey='watch-history';whRender({keepScroll:false});return;\n }\n if(!state.playback&&!state.detailId){showTabPages();return;}")
replace_exact("function searchPlaceholder(){\n if(document.body.classList.contains('settings-view'))return 'Search settings…';",
              "function searchPlaceholder(){\n if(document.body.classList.contains('settings-view'))return 'Search settings…';\n if(whOpen)return 'Search watch history…';")
replace_exact(" const label=isSettings?'Search settings':state.view==='library'?'Search library':state.view==='downloads'?'Search downloads':'Search anime';",
              " const label=isSettings?'Search settings':whOpen?'Search watch history':state.view==='library'?'Search library':state.view==='downloads'?'Search downloads':'Search anime';")
replace_exact(" if(document.body.classList.contains('settings-view')){renderSettingsSearchResults();requestAnimationFrame(updateTabScrollOverlay);return;}\n if(state.view==='discover')updateDiscoverSearchResults();",
              " if(document.body.classList.contains('settings-view')){renderSettingsSearchResults();requestAnimationFrame(updateTabScrollOverlay);return;}\n if(whOpen){whSearch=state.query;whRender();return;}\n if(state.view==='discover')updateDiscoverSearchResults();")
replace_exact(" if(searchingSettings)renderSettingsSearchResults();\n if(!searchingSettings&&state.view==='discover'){",
              " if(whOpen){whSearch='';whRender();searchInput.focus({preventScroll:true});return;}\n if(searchingSettings)renderSettingsSearchResults();\n if(!searchingSettings&&state.view==='discover'){")
replace_exact(" if(searchingSettings){renderSettingsSearchResults();workspace.scrollTop=searchScrollBefore;}\n else if(!state.detailId&&!state.playback){",
              " if(whOpen){whSearch='';whRender();if(restoreFocus)searchToggle.focus({preventScroll:true});return;}\n if(searchingSettings){renderSettingsSearchResults();workspace.scrollTop=searchScrollBefore;}\n else if(!state.detailId&&!state.playback){")
replace_exact(" v.addEventListener('loadedmetadata',()=>{isLocalVideoReady=true;",
              " whInitPlayerSession();\n v.addEventListener('timeupdate',()=>whOnVideoTick(v));\n v.addEventListener('seeked',()=>whOnVideoSeek(v));\n v.addEventListener('loadedmetadata',()=>{whInitPlayerSession();isLocalVideoReady=true;")
replace_exact("function showSettings(){\n if(document.body.classList.contains('settings-view')||settingsClosing)return;",
              "function showSettings(){\n if(document.body.classList.contains('settings-view')||settingsClosing)return;\n if(whOpen)whExit();")
replace_exact("body.player-view .workspace{padding:5px 13px 15px;scrollbar-gutter:stable}",
              "body.player-view .workspace{padding:5px 13px 15px;scrollbar-gutter:auto}")
# Switch demo brand version title label, but leave app version unchanged (v100 is HTML prototype milestone).
assert len(s)-len(src)<100000
out=Path('/mnt/data/Gallery-v100.html');out.write_text(s)
print('v99 bytes',len(src.encode()),'v100 bytes',out.stat().st_size,'delta',out.stat().st_size-len(src.encode()))
print('sha256:',hashlib.sha256(out.read_bytes()).hexdigest())
print('v100 count',s.count('Gallery v100'),'history samples',s.count('whRecords'),'favicon etc preserved')
