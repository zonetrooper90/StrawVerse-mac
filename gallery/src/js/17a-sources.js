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

