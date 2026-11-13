function artCard(item){return `<article class="poster-item"><button class="poster-button" data-detail="${escapeHTML(item.id)}" title="View ${escapeHTML(item.name)}"><div class="poster" style="background:${item.art}"><span class="art-orb"></span><span class="poster-name">${escapeHTML(item.name)}</span></div><div class="poster-title">${escapeHTML(item.name)}</div><div class="meta">${escapeHTML(item.status)} · ${escapeHTML(item.lang)}</div></button></article>`;}
function gallery(items){return items.length?`<div class="poster-grid">${items.map(artCard).join('')}</div>`:'<div class="empty">No matching anime in this sample collection.</div>';}
function searchItems(items){if(!state.query.trim())return items;let q=state.query.trim().toLowerCase();return items.filter(x=>x.name.toLowerCase().includes(q));}
function pageHeader(title, actions='', secondary='', view=''){
  // Unified minimal page titles on Discover, Library and Downloads.
  // Keep the existing page actions, filters, tags and navigation unchanged.
  const heading=`<div class="sf-page-title sf-optical-title"><h1>${escapeHTML(title)}</h1></div>`;
  return `<section class="page-header page-header-${escapeHTML(view)}" aria-label="${escapeHTML(title)} page header"><div class="page-header-primary">${heading}<div class="page-header-actions">${actions}</div></div><div class="page-header-divider" aria-hidden="true"></div>${secondary?`<div class="page-header-secondary">${secondary}</div>`:''}</section>`;
}
