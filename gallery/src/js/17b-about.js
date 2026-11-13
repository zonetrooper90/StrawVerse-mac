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

