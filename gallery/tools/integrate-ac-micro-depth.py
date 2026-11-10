#!/usr/bin/env python3
"""Apply the approved A+C motion to a byte-verified Gallery HTML checkpoint.

This is a narrow, assertion-guarded patch. Never use a motion-lab HTML file
as the Gallery baseline. Keep main-tab motion and page/navigation state intact.
"""
import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_BASELINE_SHA256 = "3fc012a9251d1fe77dab164831c9c65d993a3a5631d4f0302f1e9a9e2d48659b"


def replace_once(html, old, new, label):
    occurrences = html.count(old)
    if occurrences != 1:
        raise ValueError(f"{label}: expected one anchor, found {occurrences}")
    return html.replace(old, new, 1)


def apply_patch(html):
    css_start = "/* Navigation uses a single workspace snapshot, leaving the shared top header static."
    css_end = "@keyframes gallery-about-forward"
    start = html.index(css_start)
    end = html.index(css_end, start)
    old_css = html[start:end]
    for token in (
        "@keyframes gallery-stage-leave{from{opacity:1;transform:translateY(0)}",
        "@keyframes gallery-stage-arrive{from{opacity:.94;transform:translateY(5px)}",
        "::view-transition-old(gallery-stage){animation:gallery-stage-leave .24s",
        "::view-transition-new(gallery-stage){animation:gallery-stage-arrive .24s",
    ):
        if token not in old_css:
            raise ValueError("Unexpected pre-integration motion CSS: " + token)
    new_css = """/* A+C: approved 450ms overlapping crossfade with sub-1% depth.
   The view-transition name belongs to #workspace only; the common header,
   background, and primary tab-track motion remain outside this snapshot.
   Both halves blend throughout; an interrupted route cancels its old capture. */
@keyframes gallery-stage-leave{
 0%{opacity:1;transform:scale(1)}
 48%{opacity:.83;transform:scale(.998)}
 100%{opacity:.05;transform:scale(.994)}
}
@keyframes gallery-stage-arrive{
 0%{opacity:.05;transform:scale(1.008)}
 48%{opacity:.60;transform:scale(1.004)}
 100%{opacity:1;transform:scale(1)}
}
::view-transition-image-pair(gallery-stage){isolation:isolate}
::view-transition-old(gallery-stage){animation:gallery-stage-leave .45s cubic-bezier(.38,0,.62,1) both}
::view-transition-new(gallery-stage){animation:gallery-stage-arrive .45s cubic-bezier(.22,.68,.17,1) both}
"""
    html = html[:start] + new_css + html[end:]

    # Suppress the old Settings-only entrance; Settings now joins the same
    # workspace snapshot as Anime, History and Player (no two stacked animations).
    html = replace_once(
        html,
        ".settings-page{width:100%;max-width:1170px;margin:0 auto;min-width:0;animation:settings-enter .28s cubic-bezier(.2,.75,.2,1) both}",
        ".settings-page{width:100%;max-width:1170px;margin:0 auto;min-width:0}",
        "Settings double-entrance suppression",
    )
    html = replace_once(
        html,
        "if(galleryReducedMotion.matches||document.body.classList.contains('settings-view')){mutator();return;}",
        "if(galleryReducedMotion.matches){mutator();return;}",
        "Settings page stage eligibility",
    )
    html = replace_once(
        html,
        """galleryStageFallback=workspace.animate(
   [{opacity:.96,transform:'translateY(4px)'},{opacity:1,transform:'translateY(0)'}],
   {duration:240,easing:'cubic-bezier(.2,.75,.2,1)'});""",
        """galleryStageFallback=workspace.animate(
   [{opacity:.94,transform:'scale(1.008)'},{opacity:1,transform:'scale(1)'}],
   {duration:450,easing:'cubic-bezier(.22,.68,.17,1)'});""",
        "Browser fallback micro depth",
    )

    # One existing immediate deep link opens Sources and then switches section.
    # Defer its second step until the View Transition DOM-update callback runs.
    html = replace_once(
        html,
        """function openSourceManagerFromDiscover(){
 showSettings();
 // The Settings page is independent of the main navigation; use its native
 // section switch and its built-in installed-first/marketplace-first rule.
 setSettingsSection('sources');
 if(preferredSourcesTab()==='marketplace')setSourcesTab('marketplace',false);
}""",
        """function openSourceManagerFromDiscover(){
 showSettings(()=>{
  // The Settings page is independent of the main navigation; use its native
  // section switch and its built-in installed-first/marketplace-first rule.
  setSettingsSection('sources');
  if(preferredSourcesTab()==='marketplace')setSourcesTab('marketplace',false);
 });
}""",
        "Sources deep link",
    )

    # Keep the complete original setup function. Only delay its execution
    # until the browser has captured the outgoing workspace.
    html = replace_once(
        html,
        "function showSettings(){",
        """let gallerySettingsOpening=false;
function showSettings(afterOpen=null){
 if(document.body.classList.contains('settings-view')||settingsClosing||gallerySettingsOpening||modalHost.firstChild)return;
 gallerySettingsOpening=true;
 transitionGalleryStage(()=>{
  try{
   galleryOpenSettingsNow();
   if(typeof afterOpen==='function'&&document.body.classList.contains('settings-view'))afterOpen();
  }finally{gallerySettingsOpening=false;}
 });
}
function galleryOpenSettingsNow(){""",
        "Settings View Transition entrance wrapper",
    )

    # The old Settings closure played two 140ms animations with a DOM swap
    # in between. Capture both sides once instead, keeping all teardown,
    # focus, inertness, scroll restoration and history provenance unchanged.
    start = html.index("function closeSettings(){")
    end = html.index("// Deliberate keyboard focus", start)
    old_close = html[start:end]
    for marker in ("settingsPage.inert=true;", "settingsPage.hidden=true;", "settingsReturnScroll", "settingsCloseFallback=setTimeout"):
        if marker not in old_close:
            raise ValueError("Unexpected Settings close procedure: " + marker)
    new_close = """function closeSettings(){
 if(!document.body.classList.contains('settings-view')||settingsClosing)return;
 cancelGalleryTextColorPopover(false);
 hideTabScrollOverlay();
 if(searchOpen)closeInlineSearch(false);
 if(settingsScrollFrame!==null){cancelAnimationFrame(settingsScrollFrame);settingsScrollFrame=null;}
 subtitleResizeObserver?.disconnect();
 settingsClosing=true;
 settingsPage.inert=true;
 const button=document.getElementById('settings');
 button.focus({preventScroll:true});
 transitionGalleryStage(()=>{
  // The outgoing Settings snapshot has already been captured.
  settingsPage.classList.remove('is-leaving');
  settingsPage.hidden=true;
  settingsPage.innerHTML='';
  settingsPage.inert=false;
  screen.classList.remove('surface-enter');
  document.body.classList.remove('settings-view','returning-to-gallery');
  workspace.classList.remove('settings-mode','returning-to-gallery');
  tabPagesViewport.inert=false;
  screen.inert=false;
  document.querySelector('.tabs').inert=false;
  workspace.scrollTop=settingsReturnScroll;
  button.setAttribute('aria-label','Open settings');
  button.setAttribute('title','Settings');
  button.setAttribute('aria-expanded','false');
  settingsClosing=false;
  requestAnimationFrame(updateTabScrollOverlay);
 });
}
"""
    html = html[:start] + new_close + html[end:]
    for marker in ("function showSettings(afterOpen=null)", "function galleryOpenSettingsNow()", "function closeSettings()", "animateTabTrack(", "gallery-stage-leave .45s"):
        if marker not in html:
            raise ValueError("Final Gallery feature missing: " + marker)
    return html


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    source = args.input.read_bytes()
    base_hash = hashlib.sha256(source).hexdigest()
    if base_hash != EXPECTED_BASELINE_SHA256:
        raise ValueError(f"Refusing to patch unknown Gallery baseline: {base_hash}")
    pointer = json.loads(Path("gallery/checkpoints/current.json").read_text())
    if pointer["sha256"] != EXPECTED_BASELINE_SHA256 or pointer["bytes"] != len(source):
        raise ValueError("Baseline pointer does not match verified HTML")
    html = source.decode("utf-8")
    updated = apply_patch(html).encode("utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(updated)
    print("Verified original Gallery source:", base_hash, "bytes:", len(source))
    print("A+C integrated Gallery source:", hashlib.sha256(updated).hexdigest(), "bytes:", len(updated))
    print("Unchanged: primary tab slide, shared header, artwork, playback and stored user state.")


if __name__ == "__main__":
    main()
