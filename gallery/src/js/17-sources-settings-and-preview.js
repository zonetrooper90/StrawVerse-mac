function getSourceCataloguePreview(){
 const installed=SOURCES_PREVIEW_CATALOG.filter(p=>!!sourceDemoState[p.id]?.installed);
 // A temporarily offline provider keeps previously known catalogue entries visible.
 // A broken/incompatible extension cannot supply a current listing in this demo.
 const catalogSources=installed.filter(p=>!['incompatible','broken'].includes(sourceDemoState[p.id].health));
 const listings=new Map();
 for(const provider of catalogSources){
  for(const id of SOURCE_PREVIEW_LISTINGS[provider.id]||[]){
   if(!listings.has(id))listings.set(id,new Set());
   listings.get(id).add(provider.id);
  }
 }
 return {
  installed, catalogSources, listings,
  titles:demo.filter(item=>listings.has(item.id)),
  duplicates:[...listings.values()].filter(providers=>providers.size>1).length,
  cached:catalogSources.some(p=>sourceDemoState[p.id].health==='offline')
 };
}
function sourceCatalogueEmptyMarkup(model){
 const hasSources=model.installed.length>0;
 const title=hasSources?'Your sources need attention':'Discover starts with a source';
 const desc=hasSources
  ?'Your installed sources cannot currently provide a catalogue. Open Sources to inspect their status or install another provider. Your Library and Downloads are still available.'
  :'Install an anime source to start exploring titles. The official StrawVerse repository is already configured.';
 return `<section class="discover-source-empty" aria-label="${hasSources?'Sources need attention':'No sources installed'}"><div class="discover-source-empty-icon">${icon(hasSources?'info':'compass',26)}</div><h2>${title}</h2><p>${desc}</p><button type="button" class="btn primary" id="discover-browse-sources">${icon('globe',16)} ${hasSources?'Manage Sources':'Browse Sources'}</button><p class="discover-source-note">Local interface simulation · no real extensions or websites are accessed.</p></section>`;
}
function discoverSourceCount(model,items){
 const count=items.length;
 return `${count} ${count===1?'sample title':'sample titles'}${model.catalogSources.length?` · ${model.catalogSources.length} ${model.catalogSources.length===1?'source':'sources'}`:''}`;
}
function openSourceManagerFromDiscover(){
 showSettings(()=>{
  // The Settings page is independent of the main navigation; use its native
  // section switch and its built-in installed-first/marketplace-first rule.
  setSettingsSection('sources');
  if(preferredSourcesTab()==='marketplace')setSourcesTab('marketplace',false);
 });
}
function refreshDiscoverFromSourcePreview(){
 if(tabPagesReady){
  const panel=tabPages.discover;
  const originalScroll=panel.scrollTop;
  renderTabPage('discover');
  panel.scrollTop=originalScroll;
 }
}
function sourcesCatalogueScenarioMarkup(){
 const preview=getSourceCataloguePreview();
 return `<details class="sources-scenario sources-catalogue-preview"><summary>Preview Discover with different installed sources</summary><p>Try zero, one, or two installed sources. These shortcuts only update sample source availability; your Library entries, viewing history, and Downloads are not changed.</p><div class="sources-catalogue-actions"><button type="button" class="btn small" data-source-action="catalogue-none">No sources</button><button type="button" class="btn small" data-source-action="catalogue-one">Anikoto only</button><button type="button" class="btn small" data-source-action="catalogue-both">Both sources</button></div><p class="sources-catalogue-current">Currently: ${preview.installed.length} installed · ${preview.titles.length} distinct Discover titles${preview.duplicates?` · ${preview.duplicates} shared titles merged`:''}. Visit Discover to see the result.</p></details>`;
}
function applySourceCatalogueScenario(mode){
 // Cancel simulated asynchronous updates before switching preview presets.
 sourceDemoOpToken++;
 sourceOperationEnd();
 for(const p of SOURCES_PREVIEW_CATALOG){
  const enabled=mode==='catalogue-both'||(mode==='catalogue-one'&&p.id==='anikoto');
  sourceDemoState[p.id]={installed:enabled?p.latest:null,health:'healthy',nextOutcome:'working',notice:null,backup:null};
 }
 sourcesExpanded.clear();
 sourcesTab=preferredSourcesTab();
 const model=getSourceCataloguePreview();
 sourcesFeedback=`Demo: ${model.installed.length} installed ${model.installed.length===1?'source':'sources'}; ${model.titles.length} distinct titles in Discover. Your Library and Downloads were preserved.`;
 renderSourcesPreview();
 refreshDiscoverFromSourcePreview();
}

function sourceVersionNewer(current,latest){if(!current)return false;const x=current.split('.').map(Number),y=latest.split('.').map(Number);for(let i=0;i<Math.max(x.length,y.length);i++){if((x[i]||0)!==(y[i]||0))return (x[i]||0)<(y[i]||0);}return false;}
// The prototype distinguishes installed files, extension validation, and provider health.
// Update outcomes are chosen by the tester, not inferred from real network activity.
const SOURCE_UPDATE_PHASES=['Preparing update','Downloading update','Validating extension','Activating version','Checking provider'];
function sourcesStatus(p){
 const d=sourceDemoState[p.id];
 if(sourceDemoBusy===p.id)return {label:sourceDemoBusyAction==='retry'?'Checking…':sourceDemoBusyAction==='update'?'Updating…':'Installing…',kind:'',description:'The demonstration is progressing through validation and activation.'};
 if(!d.installed)return {label:'Not installed',kind:'',description:'This provider has not been installed.'};
 if(d.notice?.kind==='error')return {label:'Update failed',kind:'needs-attention',description:d.notice.text};
 if(d.health==='incompatible')return {label:'Update required',kind:'needs-attention',description:`The v${d.installed} file remains installed but cannot load. Updating may repair it; the previous version is not assumed to work.`};
 if(d.health==='broken')return {label:'Source broken',kind:'needs-attention',description:`The v${d.installed} extension is known not to work in this simulated scenario. An update may repair it.`};
 if(d.health==='offline')return {label:'Source unavailable',kind:'offline',description:`The installed v${d.installed} extension is intact, but its provider cannot currently be reached. This is not proof of broken code or missing episodes.`};
 if(sourceVersionNewer(d.installed,p.latest))return {label:'Update available',kind:'needs-attention',description:`A newer version is available. Gallery validates it before activation and retains a recovery copy of a previously working version.`};
 return {label:'Installed',kind:'',description:'The extension is installed and loaded successfully in this sample.'};
}
function sourceUpdateStageMarkup(){
 const retry=sourceDemoBusyAction==='retry';
 const i=Math.max(0,sourceDemoPhase);
 const stage=retry?'Checking provider':SOURCE_UPDATE_PHASES[i];
 const step=retry?'':' · '+(i+1)+' of '+SOURCE_UPDATE_PHASES.length;
 const progress=retry?60:((i+1)*100/SOURCE_UPDATE_PHASES.length);
 return {
  inline:`<span class="sources-inline-progress" title="${escapeHTML(stage+step)}">${icon('refresh',13)}<span>${escapeHTML(stage+step)}</span></span>`,
  track:`<div class="sources-update-track" role="progressbar" aria-label="${escapeHTML(stage)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${progress}"><span class="sources-update-track-fill" style="width:${progress}%"></span></div>`
 };
}
function sourceResultSummary(p,d){
 if(!d.notice)return `v${escapeHTML(p.latest)} available${d.installed?` · <b>v${escapeHTML(d.installed)} installed</b>`:''}`;
 let summary;
 if(d.notice.kind==='error')summary=`Update failed · ${d.installed?'v'+d.installed+' preserved':'Nothing installed'}`;
 else if(d.notice.kind==='warning')summary=`v${d.installed} installed · Provider unavailable`;
 else summary=`v${d.installed} installed · Provider verified`;
 return `<span class="sources-inline-result is-${d.notice.kind}" title="${escapeHTML(d.notice.text)}">${icon(d.notice.kind==='success'?'check':'info',13)}<span>${escapeHTML(summary)}</span></span>`;
}
function sourcesProviderMarkup(p){
 const d=sourceDemoState[p.id],st=sourcesStatus(p),isInstalled=!!d.installed,busy=!!sourceDemoBusy,active=sourceDemoBusy===p.id,expanded=sourcesExpanded.has(p.id);
 const action=isInstalled?(sourceVersionNewer(d.installed,p.latest)?'Update':null):'Install';
 const primary=action?`<button type="button" class="btn small primary" data-source-action="${action.toLowerCase()}" data-source-id="${p.id}" ${busy?'disabled':''}>${action}</button>`:'';
 const backup=d.backup;
 const recovery=backup?`<p class="sources-recovery-note">Recovery copy: <b>v${escapeHTML(backup.version)}</b> · ${backup.usable?'last known working version':'not confirmed working'}. ${backup.usable?'You may choose to restore it.':'Gallery will not suggest restoring a known-broken or unverified version.'}</p>${backup.usable?`<div class="sources-recovery-actions"><button type="button" class="btn small" data-source-action="restore" data-source-id="${p.id}" ${busy?'disabled':''}>Restore v${escapeHTML(backup.version)}…</button></div>`:''}`:'';
 const needsAlternative=isInstalled&&(d.health==='offline'||d.health==='broken'||d.health==='incompatible');
 const alternatives=needsAlternative?`<div class="sources-recovery-actions"><button type="button" class="btn small" data-source-action="retry" data-source-id="${p.id}" ${busy?'disabled':''}>Retry source check</button><button type="button" class="btn small" data-source-action="other-sources" data-source-id="${p.id}">Other Sources</button></div>`:'';
 const progress=active?sourceUpdateStageMarkup():null;
 const subline=progress?progress.inline:sourceResultSummary(p,d);
 const content=`<div class="sources-provider-main"><div class="sources-provider-icon" aria-hidden="true">${p.name[0].toUpperCase()}</div><div class="sources-provider-copy"><div class="sources-provider-name"><strong>${escapeHTML(p.name)}</strong><span class="sources-publisher">@${escapeHTML(p.publisher)}</span></div><div class="sources-version" ${active?'role="status" aria-live="polite"':''}>${subline}</div></div><div class="sources-provider-controls"><span class="sources-status ${st.kind}">${escapeHTML(st.label)}</span><span class="sources-action-slot">${primary}</span><button type="button" class="sources-detail-toggle" data-source-action="details" data-source-id="${p.id}" aria-expanded="${expanded}">${expanded?'Less':'Details'} ${icon('chevron',13)}</button></div></div>`;
 const details=expanded?`<div class="sources-provider-detail"><p>${escapeHTML(st.description)}</p><div class="sources-detail-meta"><span><strong>Publisher</strong> @${escapeHTML(p.publisher)}</span><span><strong>Requires</strong> StrawVerse ${escapeHTML(p.minApp)}+</span><span><strong>Repository</strong> Official</span></div>${recovery}${alternatives}<div class="sources-detail-actions"><a class="sources-link" href="${SOURCES_PREVIEW_REPO.url}" target="_blank" rel="noopener noreferrer">View repository ↗</a>${isInstalled?`<button type="button" class="sources-danger" data-source-action="remove" data-source-id="${p.id}" ${busy?'disabled':''}>Remove extension…</button>`:''}</div></div>`:'';
 return `<article class="sources-provider" data-source-entry="${p.id}">${content}${progress?progress.track:''}${details}</article>`;
}
function sourcesScenarioMarkup(){
 return `<details class="sources-scenario"><summary>Preview other source and update states</summary><p>Pick a source condition and the outcome of its next update. No files or provider websites are accessed.</p><div class="field"><label for="sources-scenario-provider">Provider</label><select id="sources-scenario-provider">${SOURCES_PREVIEW_CATALOG.map(p=>`<option value="${p.id}">${escapeHTML(p.name)}</option>`).join('')}</select></div><div class="field"><label for="sources-scenario-state">Current extension condition</label><select id="sources-scenario-state"><option value="healthy">Working</option><option value="offline">Provider temporarily unavailable</option><option value="broken">Old source no longer works</option><option value="incompatible">Extension cannot load</option></select></div><div class="field"><label for="sources-scenario-outcome">Next update result</label><select id="sources-scenario-outcome"><option value="working">New source works</option><option value="rejected">New extension fails validation</option><option value="unreachable">New extension loads, but provider is unavailable</option></select></div><button type="button" class="btn small" data-source-action="simulate" style="margin-top:12px">Apply scenario</button><p class="sources-scenario-footnote">A provider outage alone does not prove an old extension is broken. Only a previously working version is offered as a recovery option.</p></details>`;
}
function sourcesRepoMarkup(r,official){
 const hint=official?'Official repository · always configured':`${r.kind==='github'?'GitHub repository':'Direct marketplace manifest'} · Format checked only`;
 return `<div class="sources-repo" ${official?'id="settings-official-repository" tabindex="-1"':''} title="${escapeHTML(hint)}"><div class="sources-repo-icon" aria-hidden="true">${icon(official?'check':'globe',18)}</div><div class="sources-repo-copy"><strong title="${escapeHTML(r.name)}">${escapeHTML(r.name)}</strong><small title="${escapeHTML(r.url)}">${escapeHTML(r.url)}</small></div><div class="sources-repo-actions"><span class="sources-repo-status">${official?'Built in':'Not verified'}</span>${official?'':`<button type="button" class="sources-danger" data-source-action="remove-repo" data-repo-id="${escapeHTML(r.id)}" aria-label="Remove ${escapeHTML(r.name)} repository">Remove</button>`}</div></div>`;
}
function renderSourcesPreview(){
 const shell=settingsPage.querySelector('#sources-shell');if(!shell)return;
 for(const el of shell.querySelectorAll('[data-source-tab]')){
  const current=el.dataset.sourceTab===sourcesTab;
  el.setAttribute('aria-selected',String(current));el.tabIndex=current?0:-1;
 }
 const count=SOURCES_PREVIEW_CATALOG.filter(p=>!!sourceDemoState[p.id].installed).length;
 const number=shell.querySelector('#sources-installed-count');if(number)number.textContent=count;
 const region=shell.querySelector('#sources-dynamic-content');
 const feedback=shell.querySelector('#sources-status-message');if(feedback)feedback.textContent=sourcesFeedback;
 if(!region)return;
 if(sourcesTab==='marketplace'||sourcesTab==='installed'){
  const available=sourcesTab==='marketplace'?SOURCES_PREVIEW_CATALOG:SOURCES_PREVIEW_CATALOG.filter(p=>!!sourceDemoState[p.id].installed);
  region.innerHTML=`<div id="sources-${sourcesTab}-region" tabindex="-1"><div class="sources-section-top"><div><h3>${sourcesTab==='marketplace'?'Marketplace':'Installed sources'}</h3><p>${sourcesTab==='marketplace'?'Browse sources from the built-in StrawVerse repository.':'Extensions remain listed here even if they are unable to load.'}</p></div><button class="sources-preview-reset" type="button" data-source-action="reset">Reset demo</button></div>${available.length?`<div class="sources-provider-list">${available.map(sourcesProviderMarkup).join('')}</div>`:'<div class="sources-empty">No sources installed in this demonstration.<br><button type="button" class="btn small" data-source-action="browse-marketplace" style="margin-top:14px">Browse Marketplace</button></div>'}${sourcesCatalogueScenarioMarkup()}${sourcesTab==='installed'?sourcesScenarioMarkup():''}</div>`;
 }else{
  region.innerHTML=`<div id="settings-repositories-card" tabindex="-1"><div class="sources-section-top"><div><h3>Repositories</h3><p>The official repository is always configured. You can add or remove community repository entries.</p></div><button class="sources-preview-reset" type="button" data-source-action="reset">Reset demo</button></div><div class="sources-repo-list">${sourcesRepoMarkup(SOURCES_PREVIEW_REPO,true)}${sourceDemoRepos.map(r=>sourcesRepoMarkup(r,false)).join('')}</div><div class="sources-repo-add"><button type="button" class="btn small" data-source-action="add-repo">${icon('plus',16)} Add repository…</button></div><p class="settings-card-note">Links are checked for format and duplicates locally. This prototype does not fetch manifests or install sources. The desktop application will verify repository contents before listing extensions.</p></div>`;
 }
}
function setSourcesTab(next,resetScroll=true){
 if(!['marketplace','installed','repositories'].includes(next))return;
 sourcesTab=next;renderSourcesPreview();
 if(resetScroll)requestAnimationFrame(()=>{
  const el=settingsPage.querySelector('.sources-subnav');if(el)revealSettingsControl(el);
 });
}
function sourceOperationEnd(){sourceDemoBusy=null;sourceDemoBusyAction=null;sourceDemoPhase=-1;}
function beginPreviewUpdate(p,entry,action){
 const id=p.id;
 const previous={version:entry.installed,health:entry.health,working:entry.health==='healthy'};
 const result=entry.nextOutcome||'working';
 sourceDemoBusy=id;sourceDemoBusyAction=action;sourceDemoPhase=0;entry.notice=null;
 const token=++sourceDemoOpToken;
 sourcesFeedback=`Preview: ${action==='install'?'installing':'updating'} ${p.name}. No real files are touched.`;
 renderSourcesPreview();
 function advance(phase){
  if(token!==sourceDemoOpToken||sourceDemoBusy!==id)return;
  sourceDemoPhase=phase;
  sourcesFeedback=`${p.name}: ${SOURCE_UPDATE_PHASES[phase].toLowerCase()} (simulation).`;
  renderSourcesPreview();
  if(result==='rejected'&&phase===SOURCE_UPDATE_PHASES.indexOf('Validating extension')){
   setTimeout(()=>{
    if(token!==sourceDemoOpToken)return;
    sourceOperationEnd();
    entry.notice={kind:'error',text:`Update validation failed. ${previous.version?`v${previous.version} remains installed ${previous.working?'and working':'but was already unavailable'}.`:'No version was installed.'} Nothing was replaced.`};
    sourcesFeedback=`Preview: ${p.name} update rejected. Existing installation preserved.`;
    renderSourcesPreview();
   },850);return;
  }
  if(phase<SOURCE_UPDATE_PHASES.length-1){setTimeout(()=>advance(phase+1),850);return;}
  setTimeout(()=>{
   if(token!==sourceDemoOpToken)return;
   // Extension passed validation/activation. Provider reachability is a separate test.
   entry.installed=p.latest;
   if(previous.version&&previous.version!==p.latest){entry.backup={version:previous.version,usable:previous.working,health:previous.health};}
   if(result==='unreachable'){
    entry.health='offline';
    entry.notice={kind:'warning',text:`v${p.latest} activated, but the provider could not be reached. The new version stays installed; no automatic rollback was made.`};
    sourcesFeedback=`Preview: ${p.name} updated, but its provider is unavailable. Retry or select another source.`;
   }else{
    entry.health='healthy';
    entry.notice={kind:'success',text:`v${p.latest} activated and the provider check passed. ${entry.backup?.usable?'The previous working version is retained as a recovery copy.':''}`};
    sourcesFeedback=`Preview: ${p.name} v${p.latest} installed successfully. No files were downloaded.`;
   }
   sourceOperationEnd();renderSourcesPreview();refreshDiscoverFromSourcePreview();
  },900);
 }
 setTimeout(()=>advance(1),700);
}
function previewSourceAction(action,id){
 const p=SOURCES_PREVIEW_CATALOG.find(x=>x.id===id);if(!p)return;
 const entry=sourceDemoState[id];
 if(action==='details'){
  if(sourcesExpanded.has(id))sourcesExpanded.delete(id);else sourcesExpanded.add(id);
  renderSourcesPreview();
  settingsPage.querySelector(`[data-source-action="details"][data-source-id="${id}"]`)?.focus({preventScroll:true});
  return;
 }
 if(action==='other-sources'){
  sourcesFeedback=`Select another provider for the episode if needed. ${p.name} remains the preferred source until you change it.`;
  setSourcesTab('marketplace');return;
 }
 if(sourceDemoBusy)return;
 if(action==='remove'){
  modal('Remove source?',`<p class="description"><strong>${escapeHTML(p.name)}</strong> will be marked as removed in this interface preview. In the real app, removing a source will not delete your Library, watch history, or downloaded files.</p><p class="tip">No files on your Mac are changed here.</p>`,`<button class="btn" id="source-remove-cancel">Cancel</button><button class="btn primary" id="source-remove-confirm">Remove in preview</button>`);
  document.getElementById('source-remove-cancel').onclick=closeModal;
  document.getElementById('source-remove-confirm').onclick=()=>{
   entry.installed=null;entry.health='healthy';entry.backup=null;entry.notice=null;sourcesFeedback=`Preview: ${p.name} removed. Your anime library remains untouched.`;closeModal();
   if(sourcesTab==='installed'&&preferredSourcesTab()==='marketplace')sourcesTab='marketplace';
   renderSourcesPreview();refreshDiscoverFromSourcePreview();
  };
  return;
 }
 if(action==='restore'){
  const backup=entry.backup;
  if(!backup||!backup.usable)return;
  modal('Restore previous extension?',`<p class="description">Restore the last known working version of <b>${escapeHTML(p.name)}</b> (v${escapeHTML(backup.version)})? Gallery would check the recovery copy before activating it. It will not automatically replace the current version.</p><p class="tip">This is a simulated restoration.</p>`,`<button class="btn" id="source-restore-cancel">Cancel</button><button class="btn primary" id="source-restore-confirm">Restore in preview</button>`);
  document.getElementById('source-restore-cancel').onclick=closeModal;
  document.getElementById('source-restore-confirm').onclick=()=>{
   entry.installed=backup.version;entry.health=backup.health;entry.backup=null;
   entry.notice={kind:'success',text:`v${entry.installed} was restored in the preview. A real app would verify the recovery copy and recheck provider health.`};
   sourcesFeedback=`Preview: ${p.name} restored to v${entry.installed}.`;
   closeModal();renderSourcesPreview();refreshDiscoverFromSourcePreview();
  };
  return;
 }
 if(action==='retry'){
  if(!entry.installed)return;
  sourceDemoBusy=id;sourceDemoBusyAction='retry';sourceDemoPhase=SOURCE_UPDATE_PHASES.length-1;const token=++sourceDemoOpToken;
  entry.notice=null;sourcesFeedback=`Preview: checking ${p.name}'s provider again…`;renderSourcesPreview();
  setTimeout(()=>{
   if(token!==sourceDemoOpToken)return;
   sourceOperationEnd();
   if(entry.nextOutcome==='working'){
    entry.health='healthy';entry.notice={kind:'success',text:'The simulated provider recheck succeeded. The selected source was not changed.'};
    sourcesFeedback=`Preview: ${p.name} provider is available again.`;
   }else{
    entry.health='offline';entry.notice={kind:'warning',text:'The simulated provider recheck still failed. Keep the installed version and choose Retry or Other Sources.'};
    sourcesFeedback=`Preview: ${p.name} provider is still unavailable.`;
   }
   renderSourcesPreview();refreshDiscoverFromSourcePreview();
  },950);
  return;
 }
 if(!['install','update'].includes(action))return;
 beginPreviewUpdate(p,entry,action);
}
// Local-only URL shape checks; these do NOT establish that a remote repository exists
// or that an extension is trusted, compatible, or safe to install.
function parsePreviewRepoUrl(text){
 let url;
 try{url=new URL(text.trim());}catch(_){return {error:'Enter a complete HTTPS repository URL.'};}
 if(url.protocol!=='https:'||url.username||url.password){return {error:'Use an HTTPS URL without a username or password.'};}
 if(url.search||url.hash){return {error:'Remove query parameters and fragments from the URL.'};}
 const host=url.hostname.toLowerCase();
 if(!host||host==='localhost'||host.endsWith('.localhost')||host==='127.0.0.1'||host==='[::1]')return {error:'Use a public repository URL.'};
 const pieces=url.pathname.split('/').filter(Boolean);
 if(host==='github.com'){
  if(pieces.length!==2||!pieces.every(x=>/^[a-z0-9_.-]+$/i.test(x))){return {error:'Use a GitHub URL like https://github.com/owner/repository.'};}
  const owner=pieces[0],repo=pieces[1].replace(/\.git$/i,'');
  if(!repo)return {error:'Include the repository name in the GitHub URL.'};
  return {url:`https://github.com/${owner}/${repo}`,key:`github:${owner.toLowerCase()}/${repo.toLowerCase()}`,name:`${owner}/${repo}`,kind:'github'};
 }
 if(host==='raw.githubusercontent.com'){
  let path=pieces;
  if(path[2]==='refs'&&path[3]==='heads')path=[path[0],path[1],...path.slice(4)];
  if(path.length<4||path.at(-1).toLowerCase()!=='marketplace.json'||!path.slice(0,2).every(x=>/^[a-z0-9_.-]+$/i.test(x))){return {error:'Use a raw GitHub marketplace.json URL, including its branch.'};}
  const [owner,repo]=path;
  return {url:`https://raw.githubusercontent.com/${pieces.join('/')}`,key:`github:${owner.toLowerCase()}/${repo.toLowerCase()}`,name:`${owner}/${repo}`,kind:'manifest'};
 }
 if(pieces.at(-1)?.toLowerCase()!=='marketplace.json')return {error:'Use a GitHub repository URL or a direct marketplace.json URL.'};
 if(!host.includes('.'))return {error:'Enter a valid repository hostname.'};
 return {url:url.origin+url.pathname.replace(/\/$/,''),key:`manifest:${host}${url.pathname.replace(/\/$/,'')}`,name:`${host} / marketplace.json`,kind:'manifest'};
}
function sourceRepoIsDuplicate(parsed){
 const official=parsePreviewRepoUrl(SOURCES_PREVIEW_REPO.url);
 return parsed.key===official.key||sourceDemoRepos.some(r=>r.key===parsed.key);
}
function previewRepoInput(){
 modal('Add repository',`<p class="description">Add a StrawVerse-compatible repository to the <b>local preview</b>. No internet connection or extension download occurs.</p><div class="field"><label for="source-repo-url">GitHub repository or direct marketplace.json URL</label><input type="url" id="source-repo-url" placeholder="https://github.com/owner/extensions" autocomplete="off" spellcheck="false" aria-describedby="source-repo-validation"></div><p class="sources-repo-validation" id="source-repo-validation" aria-live="polite">Paste a repository link to check its URL format.</p>`,`<button class="btn" id="source-repo-cancel">Cancel</button><button class="btn primary" id="source-repo-add-preview" disabled>Add preview entry</button>`);
 const input=document.getElementById('source-repo-url');
 const hint=document.getElementById('source-repo-validation');
 const add=document.getElementById('source-repo-add-preview');
 document.getElementById('source-repo-cancel').onclick=closeModal;
 let candidate=null;
 function validate(){
  const value=input.value.trim();
  candidate=value?parsePreviewRepoUrl(value):null;
  if(candidate&&!candidate.error&&sourceRepoIsDuplicate(candidate))candidate={error:'This repository is already configured, possibly through a different URL format.'};
  const error=candidate?.error;
  const valid=!!candidate&&!error;
  add.disabled=!valid;
  input.setAttribute('aria-invalid',error?'true':'false');
  hint.className='sources-repo-validation'+(error?' is-error':valid?' is-valid':'');
  hint.textContent=error|| (valid?'URL format accepted. Repository contents are NOT verified.':'Paste a repository link to check its URL format.');
 }
 input.addEventListener('input',validate);
 input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!add.disabled){e.preventDefault();add.click();}});
 add.onclick=()=>{
  validate();if(!candidate||candidate.error)return;
  const id='preview-'+(sourceDemoRepos.length+1)+'-'+Date.now();
  sourceDemoRepos.push({id,...candidate});
  sourcesFeedback=`Added ${candidate.name} to the local preview. Its contents have not been fetched or verified.`;
  closeModal();renderSourcesPreview();
 };
 input.focus({preventScroll:true});
}
function previewRemoveRepo(id){
 const r=sourceDemoRepos.find(r=>r.id===id);if(!r)return;
 modal('Remove repository?',`<p class="description">Remove <strong>${escapeHTML(r.name)}</strong> from the Marketplace preview?</p><p class="tip">Installed extensions from this repository would remain on your Mac. They would stop receiving updates through this repository until it is added again. This prototype changes no files.</p>`,`<button class="btn" id="source-repo-keep">Keep repository</button><button class="btn" id="source-repo-remove">Remove repository</button>`);
 document.getElementById('source-repo-keep').onclick=closeModal;
 document.getElementById('source-repo-remove').onclick=()=>{
  sourceDemoRepos=sourceDemoRepos.filter(x=>x.id!==id);
  sourcesFeedback=`Removed ${r.name} from preview. Installed extension state is unchanged.`;
  closeModal();renderSourcesPreview();
 };
}
function attachSourcesPreview(){
 const shell=settingsPage.querySelector('#sources-shell');if(!shell)return;
 renderSourcesPreview();
 shell.addEventListener('click',event=>{
  const tab=event.target.closest('[data-source-tab]');if(tab){setSourcesTab(tab.dataset.sourceTab);return;}
  const action=event.target.closest('[data-source-action]');if(!action)return;
  const mode=action.dataset.sourceAction;
  if(mode==='reset'){resetSourcesPreview();return;}
  if(mode==='browse-marketplace'){setSourcesTab('marketplace');return;}
  if(mode==='simulate'){
   const id=shell.querySelector('#sources-scenario-provider').value;
   const health=shell.querySelector('#sources-scenario-state').value;
   const outcome=shell.querySelector('#sources-scenario-outcome').value;
   if(sourceDemoState[id]){
    sourceDemoState[id].health=health;sourceDemoState[id].nextOutcome=outcome;sourceDemoState[id].notice=null;
    sourcesFeedback=`Preview: ${id} is ${health}; next update will ${outcome==='working'?'succeed':outcome==='rejected'?'fail validation':'leave the provider unreachable'}.`;
    renderSourcesPreview();refreshDiscoverFromSourcePreview();
   }
   return;
  }
  if(['catalogue-none','catalogue-one','catalogue-both'].includes(mode)){applySourceCatalogueScenario(mode);return;}
  if(mode==='add-repo'){previewRepoInput();return;}
  if(mode==='remove-repo'){previewRemoveRepo(action.dataset.repoId);return;}
  previewSourceAction(mode,action.dataset.sourceId);
 });
 shell.addEventListener('keydown',event=>{
  const current=event.target.closest('[data-source-tab]');if(!current||!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();
  const keys=['installed','marketplace','repositories'];const i=keys.indexOf(current.dataset.sourceTab);
  const index=event.key==='Home'?0:event.key==='End'?2:(i+(event.key==='ArrowLeft'?-1:1)+3)%3;
  setSourcesTab(keys[index]);shell.querySelector(`[data-source-tab="${keys[index]}"]`)?.focus({preventScroll:true});
 });
}

/* v75 · About & Legal — quiet hierarchy, with Gallery v74 Settings visual language. */
function galleryBuildDisplay(){
 const brandVersion=(document.querySelector('.brand .subtitle')?.textContent||'').match(/v\d+(?:\.\d+)*/)?.[0]||'prototype';
 const revision=(document.title.match(/–\s*v(\d+)\s*·/)||[])[1]||'?';
 return {brandVersion,revision};
}
function aboutMarkup(){
 const build=galleryBuildDisplay();
 const link=(href,label)=>`<a href="${href}" target="_blank" rel="noopener noreferrer">${label}</a>`;
 const row=(id,ico,title,detail,context='')=>`<button class="about-menu-item" type="button" data-about-open="${id}">${icon(ico,19)}<span class="about-menu-copy"><strong>${title}</strong><small>${detail}</small></span>${context?`<span class="about-menu-context">${context}</span>`:''}${icon('chevron',17)}</button>`;
 const page=(id,title,description,html)=>`<section class="about-detail" data-about-view="${id}" aria-label="${title}" hidden><h3 class="about-detail-title" id="settings-about-${id}" tabindex="-1">${title}</h3><p class="about-detail-description">${description}</p>${html}</section>`;
 const miniNote='<p class="about-legal-note">Draft content for the proposed native Gallery application. These statements are design commitments, not a verified description of this HTML prototype or a final legal policy.</p>';
 return `<div class="about-shell" id="settings-about-root">
  <section class="about-overview" data-about-view="overview" aria-label="About Gallery">
   <div class="about-identity" id="settings-about-card" tabindex="-1">
    <div class="about-identity-primary">
     <span class="about-identity-logo" aria-hidden="true">${icon('clapper',34)}</span>
     <div class="about-identity-copy"><h3>Gallery</h3><p class="about-identity-description">Your anime library and player for macOS.</p><p class="about-identity-version">Interface prototype ${escapeHTML(build.revision)}</p></div>
    </div>
    <dl class="about-identity-facts" aria-label="Application details">
     <div class="about-identity-fact"><dt>Version</dt><dd>${escapeHTML(build.brandVersion)}</dd></div>
     <div class="about-identity-fact"><dt>Platform</dt><dd>macOS · Apple Silicon</dd></div>
     <div class="about-identity-fact"><dt>Based on</dt><dd>StrawVerse</dd></div>
    </dl>
   </div>
   <p class="about-group-label">PROJECT</p>
   <div class="about-menu" aria-label="Project details">
    ${row('credits','heart','Acknowledgements','Projects and contributors','StrawVerse · TheYogMehta')}
    ${row('licenses','info','Open Source Licenses','Software licenses and notices','GPL-3.0')}
   </div>
   <p class="about-group-label about-group-gap">LEGAL</p>
   <div class="about-menu" aria-label="Legal information">
    ${row('legal','globe','Legal &amp; Privacy','Terms, privacy and copyright information','Privacy-conscious by design')}
   </div>
   <p class="about-footnote">Gallery is an independent project based on ${link('https://github.com/TheYogMehta/StrawVerse','StrawVerse')} by TheYogMehta. Not an official StrawVerse release.</p>
  </section>
  ${page('credits','Acknowledgements','The people and open-source projects behind Gallery.',`
   <div class="about-detail-card">
    <h4>Built on StrawVerse</h4>
    <p>Gallery is being developed as an independent macOS application based on <strong>StrawVerse</strong>, created by <strong>TheYogMehta</strong>. Gallery is not an official StrawVerse release.</p>
    <div class="about-detail-links">${link('https://github.com/TheYogMehta/StrawVerse','StrawVerse on GitHub ↗')}${link('https://github.com/TheYogMehta/extensions','Official extensions ↗')}</div>
   </div>
   <div class="about-menu about-nested-menu" aria-label="Additional acknowledgements">
    ${row('components','play','Third-Party Components','Playback tools, extensions and dependencies')}
   </div>
   <p class="about-detail-footnote">Credits and licenses for dependencies actually bundled with the future native release will be generated from its build inventory and reviewed.</p>
  `)}
  ${page('licenses','Open Source Licenses','Software licenses and attribution notices.',`
   <div class="about-detail-card">
    <div class="about-detail-line"><span><strong>StrawVerse</strong><small>GNU General Public License, version 3 (GPL-3.0-only)</small></span>${link('https://github.com/TheYogMehta/StrawVerse/blob/main/LICENSE','Read GPL-3.0 ↗')}</div>
    <div class="about-detail-line"><span><strong>Gallery's future native release</strong><small>Applicable source, copyright notices and full license texts will accompany the distributed app, as required.</small></span></div>
    <div class="about-detail-line"><span><strong>Third-party dependencies</strong><small>License inventory will reflect the libraries and binaries actually shipped, not an assumed dependency list.</small></span></div>
   </div>
   <p class="about-detail-footnote">This standalone HTML prototype is not the finished macOS distribution. No generated native license inventory exists yet.</p>
  `)}
  ${page('components','Third-Party Components','Media and extension technologies under consideration.',`
   <div class="about-detail-card">
    <div class="about-detail-line"><span><strong>mpv</strong><small>Planned native video playback integration</small></span>${link('https://github.com/mpv-player/mpv','Project ↗')}</div>
    <div class="about-detail-line"><span><strong>FFmpeg</strong><small>Possible media processing dependency; shipped configuration and license must be verified</small></span>${link('https://ffmpeg.org/','Project ↗')}</div>
    <div class="about-detail-line"><span><strong>StrawVerse-compatible sources</strong><small>Individual extensions are provided by their respective maintainers.</small></span></div>
   </div>
   <p class="about-detail-footnote">These are plans, not a claim that any native media binary is included in this HTML prototype.</p>
  `)}
  ${page('legal','Legal &amp; Privacy','How Gallery is intended to work and what third parties can see.',`
   <div class="about-privacy-summary"><span class="about-privacy-symbol">${icon('info',21)}</span><div><h4>Privacy-conscious by design</h4><p>No developer analytics, telemetry or tracking is planned. External providers can still receive network requests and may collect information independently.</p></div></div>
   <div class="about-menu" aria-label="Legal documents">
    ${row('terms','info','Terms of Service','Use of Gallery, sources and responsibilities')}
    ${row('privacy','globe','Privacy Policy','Local data and third-party network requests')}
    ${row('copyright','film','Copyright &amp; Disclaimer','External content and copyright enquiries')}
   </div>
   <p class="about-detail-footnote">These are working drafts based on Gallery's intended behavior, not copied StrawVerse legal terms. They must be checked against the finished native implementation before release.</p>
  `)}
  ${page('terms','Terms of Service','Proposed terms for the future Gallery macOS application.',`
   ${miniNote}
   <article class="about-legal-document">
    <h4>1. Open-source software</h4><p>Gallery is being developed from the GPL-licensed StrawVerse project. Rights to copy, modify and distribute covered software are governed by the applicable open-source licenses, including GNU GPL v3.0; these terms do not replace those rights.</p>
    <h4>2. Application and external services</h4><p>Gallery is intended as a macOS client that retrieves information and content through user-selected third-party sources. Availability and operation of those external services are outside Gallery's control. Local downloads and application data may be stored on the user's Mac.</p>
    <h4>3. User responsibility</h4><p>Users are responsible for their choices of sources and for complying with applicable laws and the terms of external services.</p>
    <h4>4. Warranty</h4><p>GPL-covered software is provided subject to the disclaimer of warranty in its license, to the extent permitted by applicable law. Any additional terms for Gallery must be reviewed before public distribution.</p>
    <h4>5. Support</h4><p>Support and issue-reporting contact details for Gallery will be provided when the project is released. The StrawVerse community is independent from Gallery.</p>
   </article>
  `)}
  ${page('privacy','Privacy Policy','Proposed privacy commitments for the future Gallery app.',`
   ${miniNote}
   <div class="about-privacy-summary about-privacy-summary-compact"><span class="about-privacy-symbol">${icon('info',20)}</span><div><h4>No developer data collection</h4><p>Our goal is zero analytics, developer telemetry, tracking identifiers or automatic crash-report uploads.</p></div></div>
   <article class="about-legal-document">
    <h4>1. Data stored on your device</h4><p>Gallery is intended to store your library, watch progress, downloads and preferences on your Mac, rather than sending those records to Gallery's developers. Locally stored information remains under your control.</p>
    <h4>2. No developer analytics</h4><p>Gallery will not deliberately include developer usage analytics, advertising trackers or automatic diagnostic uploads. This commitment must be verified in the native release and its included dependencies.</p>
    <h4>3. Third-party connections</h4><p>To search for anime, retrieve metadata, play video, use source extensions or check for updates, Gallery may contact external websites and services directly. Those services can receive your IP address and information about requested content, and may independently log or analyze requests under their own policies.</p>
    <h4>4. Optional integrations</h4><p>If external accounts or synchronization are introduced later, they should be optional and clearly explain what data will be shared. Gallery does not require a developer-operated account by design.</p>
    <h4>5. Your choices</h4><p>Users will be able to manage local app data and their installed sources. Detailed storage, export and deletion instructions will be confirmed for the native release.</p>
   </article>
  `)}
  ${page('copyright','Copyright &amp; Disclaimer','Proposed statement about content and third-party providers.',`
   ${miniNote}
   <article class="about-legal-document">
    <h4>1. Independent client</h4><p>Gallery is intended as an independent macOS application that interacts with external content providers. It is not an official StrawVerse release and does not operate a developer-hosted library of third-party media.</p>
    <h4>2. Local retrieval and downloads</h4><p>Metadata requests, playback and user-initiated downloads may involve external sources and files stored on the user's device. Gallery therefore should not claim that no content is ever indexed, cached or downloaded.</p>
    <h4>3. Third-party rights</h4><p>Content and services accessible through sources belong to their respective owners and providers. Users should respect applicable copyright law and provider terms.</p>
    <h4>4. Copyright enquiries</h4><p>Requests relating to content hosted by third parties should normally be directed to the appropriate host or provider. Gallery-specific contact information and an appropriate handling process must be established before distribution; this disclaimer does not remove any applicable legal obligations.</p>
   </article>
  `)}
 </div>`;
}
let currentAboutView='overview';
const aboutViewParents={overview:null,credits:'overview',licenses:'overview',components:'credits',legal:'overview',terms:'legal',privacy:'legal',copyright:'legal'};
function updateSettingsBackButton(){
 const back=settingsPage.querySelector('#settings-back');
 if(!back)return;
 const inDetail=settingsLastSection==='about'&&currentAboutView!=='overview';
 const parent=inDetail?aboutViewParents[currentAboutView]:null;
 const dest=parent==='overview'?'About':parent==='legal'?'Legal & Privacy':parent==='credits'?'Acknowledgements':'Gallery';
 back.setAttribute('aria-label',inDetail?'Back to '+dest:'Back to Gallery');
 back.setAttribute('title',inDetail?'Back to '+dest:'Back to Gallery');
 const label=back.querySelector('span');
 if(label)label.textContent=inDetail?dest:'Back';
}
function settingsBackAction(){
 if(settingsLastSection==='about'&&currentAboutView!=='overview')setAboutView(aboutViewParents[currentAboutView]||'overview');
 else closeSettings();
}
function setAboutView(view,focusHeading=true){
 const root=settingsPage.querySelector('#settings-about-root');
 if(!root)return;
 const active=Object.hasOwn(aboutViewParents,view)?view:'overview';
 if(active===currentAboutView){updateSettingsBackButton();return;}
  const returning=aboutViewParents[currentAboutView]===active;
  root.dataset.aboutDirection=returning?'back':'forward';
  currentAboutView=active;
  updateSettingsBackButton();
  for(const section of root.querySelectorAll('[data-about-view]'))section.hidden=section.dataset.aboutView!==active;
 if(active==='overview'){
  if(focusHeading)root.querySelector('#settings-about-card')?.focus({preventScroll:true});
 }else if(focusHeading){
  root.querySelector(`[data-about-view="${active}"] .about-detail-title`)?.focus({preventScroll:true});
 }
 workspace.scrollTop=0;
 requestAnimationFrame(updateTabScrollOverlay);
}

function subtitleAppearanceMarkup(){
 const fontOptions=[['system','System (San Francisco)'],['atkinson','Atkinson Hyperlegible Next'],['inter','Inter']];
 const choices=(items,value)=>items.map(([id,title])=>`<option value="${id}" ${value===id?'selected':''}>${title}</option>`).join('');
 const styles=[['outline','Outline'],['shadow','Drop Shadow'],['box','Background Box'],['none','None']];
 const activePreset=({outline:'outlinePreset',shadow:'shadowPreset',box:'boxPreset'})[subtitlePrefs.effect];
 return `<section class="sf-subtitle-workbench" aria-label="Subtitle appearance and live preview">
   <div class="sf-subtitle-heading" id="settings-subtitle-appearance" tabindex="-1">
    <div class="sf-subtitle-preview-heading"><div><h3><span class="sf-subtitle-full-title">Subtitle preview</span><span class="sf-subtitle-compact-title">Subtitle appearance</span></h3>
     <p class="sf-subtitle-compact-description">Fine-tune your subtitles, then open the preview to inspect the results.</p>
    </div>${subtitleSceneToggle()}</div>
    <button type="button" class="sf-subtitle-reset" id="subtitle-reset">Reset to defaults</button>
   </div>
   <div class="sf-subtitle-compact-preview"><button type="button" class="sf-subtitle-compact-button" id="subtitle-compact-preview" aria-label="Preview subtitles">${icon('maximize',16)}Preview subtitles</button></div>
   <div class="sf-subtitle-main">
    <div class="sf-subtitle-video">
     <div class="sf-subtitle-stage subtitle-stage" id="subtitle-preview-stage" data-position="bottom" aria-label="Subtitle preview">
      <button type="button" class="sf-subtitle-expand" id="subtitle-expand-preview" aria-label="Expand subtitle preview" title="Expand preview">${icon('maximize',17)}</button>
      <img class="sf-day subtitle-stage-image subtitle-stage-day" alt="" draggable="false"><img class="sf-night subtitle-stage-image subtitle-stage-night" alt="" draggable="false">
      <div class="sf-subtitle-shade subtitle-stage-shade" aria-hidden="true"></div><div class="sf-subtitle-caption subtitle-preview-caption" id="subtitle-live-caption" aria-live="off"></div>
     </div>
    </div>
    <div class="sf-subtitle-controls" aria-label="Subtitle appearance controls">
     <div class="sf-subtitle-group" data-subtitle-group="font"><label class="sf-subtitle-label" for="subtitle-font">Font</label><select class="sf-subtitle-font" id="subtitle-font">${choices(fontOptions,subtitlePrefs.font)}</select></div>
     <div class="sf-subtitle-group" data-subtitle-group="size"><div class="sf-subtitle-size-heading"><span class="sf-subtitle-label" id="subtitle-size-label">Text size</span><span class="sf-subtitle-current" id="subtitle-size-current">${(SUBTITLE_SIZES.find(p=>p.id===subtitlePrefs.size)||SUBTITLE_SIZES[2]).label}</span></div>
      <div class="sf-subtitle-five" role="group" aria-labelledby="subtitle-size-label">${SUBTITLE_SIZES.map((preset,i)=>`<button type="button" class="sf-subtitle-choice" data-subtitle-size="${preset.id}" aria-label="${preset.label}" title="${preset.label}" aria-pressed="${subtitlePrefs.size===preset.id}">${['XS','S','N','L','XL'][i]}</button>`).join('')}</div></div>
     <div class="sf-subtitle-group" data-subtitle-group="text"><span class="sf-subtitle-label" id="subtitle-text-color-label">Text color</span>
      <div class="sf-subtitle-colors" role="group" aria-labelledby="subtitle-text-color-label">
       <button type="button" class="sf-subtitle-choice" data-subtitle-text-color="white" aria-label="Soft White" title="Soft White" aria-pressed="${subtitlePrefs.colorMode==='white'}"><span class="sf-subtitle-swatch subtitle-choice-swatch" style="background:#F8F8F8" aria-hidden="true"></span>White</button>
       <button type="button" class="sf-subtitle-choice" data-subtitle-text-color="yellow" aria-label="Yellow" title="Yellow" aria-pressed="${subtitlePrefs.colorMode==='yellow'}"><span class="sf-subtitle-swatch subtitle-choice-swatch" style="background:#FFE066" aria-hidden="true"></span>Yellow</button>
       <button type="button" class="sf-subtitle-choice" data-subtitle-text-color="custom" aria-label="Custom text color" aria-pressed="${subtitlePrefs.colorMode==='custom'}"><span class="sf-subtitle-custom-indicator" aria-hidden="true"><span id="subtitle-custom-palette" ${subtitlePrefs.customColorSet?'hidden':''}>${icon('palette',14)}</span><span class="sf-subtitle-swatch subtitle-choice-swatch" id="subtitle-custom-swatch" style="background:${subtitlePrefs.customColor}" ${subtitlePrefs.customColorSet?'':'hidden'}></span></span>Custom</button>
      </div></div>
     <div class="sf-subtitle-group" data-subtitle-group="style"><span class="sf-subtitle-label" id="subtitle-effect-label">Subtitle style</span>
      <div class="sf-subtitle-styles" role="group" aria-labelledby="subtitle-effect-label">${styles.map(([id,label])=>`<button type="button" class="sf-subtitle-choice" data-subtitle-effect="${id}" aria-pressed="${subtitlePrefs.effect===id}">${label}</button>`).join('')}</div></div>
     <div class="sf-subtitle-effects" id="subtitle-tuning-grid" data-subtitle-style="${subtitlePrefs.effect}">
      <div id="subtitle-strength-field"><div class="sf-subtitle-effect-heading"><span class="sf-subtitle-label" id="subtitle-effect-amount-label">Effect intensity</span>
       <span id="subtitle-effect-color-field"><button type="button" class="sf-subtitle-effect-color" id="subtitle-effect-color" aria-label="Edit outline color" title="Edit outline color" aria-haspopup="dialog"><span class="sf-subtitle-swatch subtitle-choice-swatch" id="subtitle-effect-color-swatch" style="background:${subtitlePrefs.outlineColor}" aria-hidden="true"></span>Color</button><output class="only-sr" id="subtitle-effect-color-value">${subtitlePrefs.outlineColor.toUpperCase()}</output></span></div>
       <div class="sf-subtitle-three" role="group" aria-labelledby="subtitle-effect-amount-label">${['light','normal','strong'].map((value,i)=>`<button type="button" class="sf-subtitle-choice" data-effect-strength="${value}" aria-pressed="${activePreset?subtitlePrefs[activePreset]===value:false}">${SUBTITLE_EFFECT_LABELS[i]}</button>`).join('')}</div>
      </div>
     </div>
    </div>
   </div>
   <span class="only-sr" id="subtitle-saved-status" role="status" aria-live="polite"></span>
  </section>`;
}
function setPlaybackTab(tab,resetScroll=true){
 cancelGalleryTextColorPopover(false);
 if(!['general','subtitles'].includes(tab))return;
 playbackTab=tab;
 for(const pane of settingsPage.querySelectorAll('[data-playback-pane]'))pane.hidden=pane.dataset.playbackPane!==tab;
 for(const button of settingsPage.querySelectorAll('[data-playback-tab]')){
  const current=button.dataset.playbackTab===tab;
  button.setAttribute('aria-selected',String(current));button.tabIndex=current?0:-1;
 }
 if(resetScroll){workspace.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});hideTabScrollOverlay();}
 if(tab==='subtitles')requestAnimationFrame(renderSubtitlePreview);
}
let subtitleResizeObserver=null;
function renderSubtitleStage(stage){
 const caption=stage?.querySelector('.subtitle-preview-caption');
 if(!stage||!caption)return;
 // Size relative to the displayed video area in logical CSS pixels.
 const displayedHeight=stage.getBoundingClientRect().height||720;
 const scale=displayedHeight/1080;
 caption.textContent=SUBTITLE_PREVIEW_TEXT;
 caption.style.fontFamily=SUBTITLE_FONTS[subtitlePrefs.font];
 caption.style.fontSize=(subtitleReferenceSize(subtitlePrefs.size)*scale).toFixed(2)+'px';
 caption.style.webkitTextStroke='0px transparent';
 caption.style.textShadow='none';
 caption.style.backgroundColor='transparent';
 caption.style.padding='0';
 caption.style.borderRadius='0';
 const style=subtitlePrefs.effect;
 if(style==='outline'){
  caption.style.webkitTextStroke=(subtitlePrefs.outline*scale).toFixed(2)+'px '+subtitlePrefs.outlineColor;
 }else if(style==='shadow'){
  const strength=subtitlePrefs.shadow*scale;
  caption.style.textShadow=strength>0?`${(strength*.48).toFixed(2)}px ${(strength*.68).toFixed(2)}px ${(strength*1.65).toFixed(2)}px ${subtitlePrefs.shadowColor}`:'none';
 }else if(style==='box'){
  const h=subtitlePrefs.boxColor.replace('#','');
  const r=parseInt(h.slice(0,2),16),g=parseInt(h.slice(2,4),16),b=parseInt(h.slice(4,6),16);
  caption.style.backgroundColor=`rgba(${r},${g},${b},${subtitlePrefs.boxOpacity/100})`;
  caption.style.padding='0.24em .55em';
  caption.style.borderRadius='0.25em';
 }
 caption.style.paintOrder='stroke fill';
 caption.style.color=subtitlePrefs.color;
}
// One manually selected scene is shared by both preview surfaces.
let subtitlePreviewScene='day';
function subtitleSceneToggle(){
 const option=(scene,label,symbol)=>`<button type="button" class="scene-${scene}" data-subtitle-scene="${scene}" aria-pressed="${subtitlePreviewScene===scene}">${icon(symbol,14)}${label}</button>`;
 return `<div class="sf-subtitle-scene-toggle" role="group" aria-label="Subtitle preview scene" data-active="${subtitlePreviewScene}">${option('day','Day','sun')}${option('night','Night','moon')}</div>`;
}
function subtitleStages(){
 return [settingsPage.querySelector('#subtitle-preview-stage'),modalHost.querySelector('#subtitle-expanded-stage')].filter(Boolean);
}
function applySubtitlePreviewScene(){
 const night=subtitlePreviewScene==='night';
 for(const stage of subtitleStages()){
  const layer=stage.querySelector('.subtitle-stage-night');
  if(layer)layer.style.opacity=night?'1':'0';
 }
 for(const root of [settingsPage,modalHost]){
  for(const toggle of root.querySelectorAll('.sf-subtitle-scene-toggle')){
   toggle.dataset.active=subtitlePreviewScene;
   for(const button of toggle.querySelectorAll('[data-subtitle-scene]'))
    button.setAttribute('aria-pressed',String(button.dataset.subtitleScene===subtitlePreviewScene));
  }
 }
}
function bindSubtitleSceneToggle(root){
 for(const button of root.querySelectorAll('[data-subtitle-scene]'))button.addEventListener('click',()=>{
  const next=button.dataset.subtitleScene;
  if(next===subtitlePreviewScene)return;
  subtitlePreviewScene=next;
  applySubtitlePreviewScene();
  button.focus({preventScroll:true});
 });
}
function updateSubtitlePreviewScaleControl(){
 const stage=modalHost.querySelector('#subtitle-expanded-stage');
 const viewport=modalHost.querySelector('#subtitle-expanded-viewport');
 const actual=modalHost.querySelector('#subtitle-actual-size');
 if(!stage||!viewport||!actual)return;
 const manual=viewport.classList.contains('is-actual-size');
 // Use layout dimensions, not transformed bounds during the dialog entrance.
 // 100% is the established 1280 × 720 logical CSS-pixel stage, independent of DPR.
 const alreadyFull=stage.offsetWidth===1280&&stage.offsetHeight===720;
 const hide=!manual&&alreadyFull;
 if(hide&&document.activeElement===actual)
  modalHost.querySelector('.sf-subtitle-scene-toggle [aria-pressed="true"]')?.focus({preventScroll:true});
 actual.hidden=hide;
 actual.setAttribute('aria-pressed',String(manual));
 actual.textContent=manual?'Fit':'100%';
 actual.setAttribute('aria-label',manual?'Fit to window':'View at 100%');
 actual.title=manual?'Fit the preview to the window':'View at 100% (1280 × 720 CSS pixels; scroll to inspect)';
}
function renderSubtitlePreview(){
 renderSubtitleStage(settingsPage.querySelector('#subtitle-preview-stage'));
 renderSubtitleStage(modalHost.querySelector('#subtitle-expanded-stage'));
 applySubtitlePreviewScene();
 updateSubtitlePreviewScaleControl();
}
function showExpandedSubtitlePreview(){
 // Reuse Gallery's established dialog lifecycle, focus trapping and Escape key.
 modal('Expanded subtitle preview',`<div class="subtitle-expanded-header-controls"><button type="button" class="btn small" id="subtitle-actual-size" aria-pressed="false" aria-label="View at 100%" title="View at 100% (1280 × 720 CSS pixels; scroll to inspect)">100%</button>${subtitleSceneToggle()}</div>
  <div class="subtitle-expanded-viewport" id="subtitle-expanded-viewport">
   <div class="subtitle-stage" id="subtitle-expanded-stage" data-position="bottom" aria-label="Expanded subtitle preview">
    <img class="subtitle-stage-image subtitle-stage-day" alt="" draggable="false"><img class="subtitle-stage-image subtitle-stage-night" alt="" draggable="false"><div class="subtitle-stage-shade" aria-hidden="true"></div><div class="subtitle-preview-caption" aria-live="off"></div>
   </div>
  </div>`);
 const dialog=modalHost.querySelector('.dialog');
 dialog.classList.add('subtitle-preview-dialog');
 const headerControls=dialog.querySelector('.subtitle-expanded-header-controls');
 dialog.querySelector('.dialog-head').insertBefore(headerControls,dialog.querySelector('#close-dialog'));
 bindSubtitleSceneToggle(dialog);
 const stage=dialog.querySelector('#subtitle-expanded-stage');
 stage.querySelector('.subtitle-stage-day').src=SHRINE_DAY_IMAGE;
 stage.querySelector('.subtitle-stage-night').src=SHRINE_NIGHT_IMAGE;
 const viewport=dialog.querySelector('#subtitle-expanded-viewport');
 const actual=dialog.querySelector('#subtitle-actual-size');
 actual.addEventListener('click',()=>{
  const enabled=viewport.classList.toggle('is-actual-size');
  viewport.scrollLeft=enabled?(viewport.scrollWidth-viewport.clientWidth)/2:0;
  if(!enabled)viewport.scrollTop=0;
  renderSubtitlePreview();
 });
 subtitleResizeObserver?.observe(stage);
 renderSubtitlePreview();
 (actual.hidden?dialog.querySelector('.sf-subtitle-scene-toggle [aria-pressed="true"]'):actual)?.focus({preventScroll:true});
 requestAnimationFrame(renderSubtitlePreview);
}
/* A12: Small, theme-aware color editor with live preview, explicit commit and
   cancel, pointer and keyboard access. Kept outside Gallery's clipped .app. */
let cancelGalleryTextColorPopover=()=>{};
