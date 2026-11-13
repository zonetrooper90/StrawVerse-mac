function showEpisodeAction(action,n){
 if(action==='watch'){startPlayback(n);return;}
 if(action!=='download')return;
 const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const season=activeInstallment(x);if(!season||season.sourceMatched===false)return;
 const a=episodeAvailability(season,n);
 const choices=[['sub','Japanese · Sub',a.sub],['dub','English · Dub',a.dub]];
 const available=choices.filter(choice=>choice[2]===true);if(!available.length)return;
 const defaultVersion=state.defaultDownload;
 const preferredAvailable=available.some(choice=>choice[0]===defaultVersion);
 const selected=preferredAvailable?defaultVersion:null;
 modal(`Download episode ${n}`,`<p class="description"><b>${escapeHTML(x.name)}</b> · ${escapeHTML(installmentDisplayName(x,season))} · ${escapeHTML(installmentSubLabel(season))} · Episode ${n}</p><div class="field"><span class="label">Audio version for download</span><div class="audio-choose">${choices.map(([id,name,availability])=>`<label><input type="radio" name="episode-audio" value="${id}" ${selected===id?'checked':''} ${availability!==true?'disabled':''}><span>${escapeHTML(name)}${availability===null?' · Unknown':availability===false?' · Unavailable':''}</span></label>`).join('')}</div></div>
 ${preferredAvailable?'':`<div class="preview-warning">The preferred download version (${defaultVersion==='sub'?'Sub':'Dub'}) is unavailable for this episode. Choose another available version explicitly to continue; the app will not switch automatically.</div>`}<div class="preview-warning">Available selectable subtitle tracks will be preserved independently of subtitle visibility. No silent audio-language substitution.</div><p class="tip">Choosing another download version here does not change your saved playback or download preferences.</p>`,`<button class="btn" id="episode-cancel">Cancel</button><button class="btn primary" id="episode-confirm" ${!selected?'disabled':''}>${icon('download',16)} Preview download</button>`);
 document.getElementById('episode-cancel').onclick=closeModal;
 for(const input of modalHost.querySelectorAll('input[name="episode-audio"]'))input.addEventListener('change',()=>{document.getElementById('episode-confirm').disabled=false;});
 document.getElementById('episode-confirm').onclick=()=>{
  const chosen=modalHost.querySelector('input[name="episode-audio"]:checked')?.value;
  if(!chosen||a[chosen]!==true)return;
  modal('Download preview',`<p class="description">${escapeHTML(x.name)} · ${escapeHTML(installmentDisplayName(x,season))} · ${escapeHTML(installmentSubLabel(season))} · Episode ${n}</p><div class="dialog-sample"><b>${chosen==='sub'?'Japanese (Sub)':'English (Dub)'}</b><p class="description">In the finished application, this would queue the selected download version and save accessible selectable subtitles for offline use.</p></div><p class="tip">This is a UI prototype; no downloading occurs.</p>`,`<button class="btn primary" id="episode-ok">Got it</button>`);
  document.getElementById('episode-ok').onclick=closeModal;
 };
}
function showManageDetailTags(){const x=demo.find(d=>d.id===state.detailId);if(!x)return;
 const season=activeInstallment(x);if(!season)return;const current=seasonTagList(x,season);
 modal(`Library tags · ${installmentDisplayName(x,season)}`,`<p class="description">Tags are saved for this specific installment (${escapeHTML(installmentSubLabel(season))}), independently of other seasons and their progress. This is temporary demo state only.</p><div class="tag-picker-list">${state.tags.map(tag=>`<label><input type="checkbox" data-detail-tag="${escapeHTML(tag)}" ${current.includes(tag)?'checked':''}><span>${escapeHTML(tag)}</span></label>`).join('')}</div>`,`<button class="btn" id="detail-tags-cancel">Cancel</button><button class="btn primary" id="detail-tags-save">Save tags</button>`);
 document.getElementById('detail-tags-cancel').onclick=closeModal;
 document.getElementById('detail-tags-save').onclick=()=>{const updated=Array.from(modalHost.querySelectorAll('input[data-detail-tag]:checked')).map(el=>el.dataset.detailTag);if(season.id)state.seasonTags[season.id]=updated;else x.tags=updated;closeModal();render();};
}
function showFindSource(){const x=demo.find(d=>d.id===state.detailId),s=x&&activeInstallment(x);if(!s)return;
 modal('Find a streaming source',`<p class="description"><b>${escapeHTML(installmentDisplayName(x,s))}</b> · ${escapeHTML(installmentSubLabel(s))}</p><div class="dialog-sample"><b>Not matched</b><p class="description">The finished application would search installed providers for this exact installment and ask you to confirm ambiguous matches. Nothing is silently linked here.</p></div><p class="tip">A relationship record does not prove that an episode can be streamed or downloaded.</p>`,`<button class="btn primary" id="source-ok">Got it</button>`);
 document.getElementById('source-ok').onclick=closeModal;
}

