/* Discover integration: Soft Futuristic visuals, v103 source/search/history behavior. */
function discover(){
 const model=getSourceCataloguePreview();
 const isSearching=searchOpen&&state.view==='discover'&&!document.body.classList.contains('settings-view');
 const matching=isSearching?searchItems(model.titles):model.titles.filter(x=>(state.filterStatus==='All'||x.status===state.filterStatus)&&(state.filterAudio==='All'||x.lang.includes(state.filterAudio)));
 const actions=model.titles.length?`<button class="btn ghost page-filter-button" id="filters">${icon('filter',18)} Filters${state.filterStatus!=='All'||state.filterAudio!=='All'?' · Active':''}</button>`:'';
 const title=isSearching&&state.query.trim()?'Search results':'Explore the universe';
 const cards=model.titles.length?(matching.length?gallery(matching):'<div class="search-empty">No matching titles in this sample catalogue.</div>'):sourceCatalogueEmptyMarkup(model);
 const note=model.catalogSources.length>1?`<p class="discover-source-note">Shared sample titles are combined into one catalogue entry, even when both sources list them.</p>`:model.cached?`<p class="discover-source-note">Previously known titles from an unavailable provider are kept visible in this simulation; availability has not been rechecked.</p>`:'';
 return `<div class="sf-discover-page">
 ${pageHeader('Discover','','','discover')}
 ${whPreviewMarkup()}
 <section class="gallery-section sf-discover-explore" id="sf-discover-explore" aria-label="Explore anime">
 <div class="section-row sf-discover-explore-heading"><div class="sf-explore-heading-text"><h2 class="discover-results-heading">${title}</h2><span class="sf-explore-star" aria-hidden="true">✦</span><span class="muted discover-result-count" aria-live="polite">${discoverSourceCount(model,matching)}</span></div>${actions}</div>
 <div class="discover-result-region">${cards}</div>${note}</section>
 </div>`;
}
