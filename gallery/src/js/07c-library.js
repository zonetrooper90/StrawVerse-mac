// Keep unfinished JSON collection transfers for a future redesign.
const GALLERY_COLLECTION_TRANSFER_UI_ENABLED=false;
function library(){
 const isSearching=searchOpen&&state.view==='library'&&Boolean(state.query.trim());
 const visibleTag=isSearching?'All Titles':state.tag;
 // Search spans all library tags and per-installment tags; the selected tag is preserved.
 const titles=isSearching?searchItems(demo):visibleTag==='All Titles'?demo:demo.filter(x=>x.tags.includes(visibleTag));
 const isCustom=state.kind[visibleTag]==='custom';
 const isAll=visibleTag==='All Titles';
 const actions=`${GALLERY_COLLECTION_TRANSFER_UI_ENABLED?`<button class="btn" id="import">${icon('import',16)} <span>Import</span></button>`:''}<button class="btn primary" id="newtag">${icon('plus',17)} <span>New Tag</span></button>`;
 const tagChip=(tag)=>{const active=visibleTag===tag,custom=state.kind[tag]==='custom',count=countTag(tag);return `<button type="button" class="tagchip ${active?'active':''}" data-tag="${escapeHTML(tag)}" aria-pressed="${active}" aria-label="${escapeHTML(tag)}${custom?', custom tag':''}, ${count} titles" title="${custom?'Custom tag':'Built-in collection'}"><span>${escapeHTML(tag)}</span>${custom?`<span class="custom-tag-icon">${icon('bookmark',11)}</span>`:''}<span class="count">${count}</span></button>`;};
 const tags=`<div class="library-tag-row"><button type="button" class="library-tag-arrow library-tag-prev" id="library-tag-prev" aria-label="Scroll collections left">${icon('chevron',16)}</button><div class="tagbar" role="group" aria-label="Library collections">${tagChip('All Titles')}${state.tags.map(tagChip).join('')}</div><button type="button" class="library-tag-arrow library-tag-next" id="library-tag-next" aria-label="Scroll collections right">${icon('chevron',16)}</button></div>`;
 const shareAction=isAll||!GALLERY_COLLECTION_TRANSFER_UI_ENABLED?'':`<button class="btn small" id="sharetag" title="Share ${escapeHTML(state.tag)}">${icon('share',15)} <span>Share</span></button>`;
 const menu=isCustom?`<div class="collection-menu-wrap"><button class="btn small collection-options" id="tag-options" aria-label="More actions for ${escapeHTML(state.tag)}" aria-haspopup="menu" aria-expanded="false">${icon('dots',19)}</button><div class="collection-menu" id="tag-options-menu" role="menu" hidden><button type="button" role="menuitem" id="renametag">${icon('bookmark',15)} Rename tag</button><button type="button" role="menuitem" class="delete-tag-action" id="deletetag">${icon('close',15)} Delete tag</button></div></div>`:'';
 const kind=isAll?'All anime in your library':isCustom?'Custom tag':'Built-in collection';
 const label=visibleTag;
 const subtitle=isSearching?`${titles.length} ${titles.length===1?'match':'matches'} · Across all tags`: `${titles.length} ${titles.length===1?'title':'titles'} · ${kind}`;
 const cards=isSearching?`<div class="poster-grid">${titles.map(librarySearchCard).join('')}</div>`:gallery(titles);
 return `${pageHeader('My Library',actions,tags,'library')}
 <section class="library-collection" aria-label="${isSearching?'Library search results':'Selected library collection'}"><div class="collections-head"><div class="col-title-row"><div><h2>${escapeHTML(label)}</h2><div class="meta">${subtitle}</div></div></div>${isSearching?'':`<div class="collection-actions">${menu}${shareAction}</div>`}</div><div class="col-contents">${titles.length?cards:'<div class="search-empty">No matching titles in your library.</div>'}</div>${GALLERY_COLLECTION_TRANSFER_UI_ENABLED&&!isSearching&&!isAll?'<p class="tip">Shared collections include titles and identifiers only — not videos, watch history, or private settings.</p>':''}</section>`;
}
function librarySearchCard(item){
 const seasons=connectedMetadata[item.id]?.seasons||[];
 const labels=[...item.tags];
 for(const season of seasons){
  const tags=seasonTagList(item,season);
  // Show the release-specific statuses where multiple seasons differ.
  if(tags.length && (state.seasonTags[season.id]||seasons.some(s=>s.id!==season.id&&seasonTagList(item,s).join('|')!==tags.join('|')))){
   for(const tag of tags)labels.push(`${season.label}: ${tag}`);
  }
 }
 const unique=[...new Set(labels)];
 const pills=unique.length?unique.map(tag=>`<span>${escapeHTML(tag)}</span>`).join(''):'<span>Untagged</span>';
 return artCard(item).replace('</article>',`<div class="library-search-tags" aria-label="Tags for ${escapeHTML(item.name)}">${pills}</div></article>`);
}
