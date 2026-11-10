#!/usr/bin/env python3
"""Apply the user-approved Gallery A+C hybrid motion to the verified full HTML.

A standalone, unnumbered design integration. The caller must restore/checksum
verify gallery/checkpoints/current.json before invoking this patch script.
It intentionally does not mutate route state, player data, theme art, or tabs.
"""
from pathlib import Path
import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, type=Path)
parser.add_argument('--output', required=True, type=Path)
args=parser.parse_args()
original=args.input.read_bytes()
html=original.decode('utf-8')

def replace_one(old,new,description):
    global html
    count=html.count(old)
    if count != 1:
        raise ValueError(f'{description}: expected exactly one source match, got {count}')
    html=html.replace(old,new,1)
    print('PATCHED',description)

# View-Transitions API: exact A's three-point overlapping opacity curves,
# with only the 0.6–0.8% micro-depth of the accepted A+C experiment.
replace_one(
    '@keyframes gallery-stage-leave{from{opacity:1;transform:translateY(0)}to{opacity:.94;transform:translateY(-5px)}}',
    '@keyframes gallery-stage-leave{0%{opacity:1;transform:scale(1)}48%{opacity:.83;transform:scale(.998)}100%{opacity:.05;transform:scale(.994)}}',
    'coordinated outgoing A+C fade')
replace_one(
    '@keyframes gallery-stage-arrive{from{opacity:.94;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}',
    '@keyframes gallery-stage-arrive{0%{opacity:.05;transform:scale(1.008)}48%{opacity:.60;transform:scale(1.004)}100%{opacity:1;transform:scale(1)}}',
    'coordinated incoming A+C fade')
replace_one(
    '::view-transition-old(gallery-stage){animation:gallery-stage-leave .24s cubic-bezier(.4,0,.4,1) both}',
    '::view-transition-old(gallery-stage){animation:gallery-stage-leave .45s cubic-bezier(.38,0,.62,1) both}',
    'outgoing duration and easing')
replace_one(
    '::view-transition-new(gallery-stage){animation:gallery-stage-arrive .24s cubic-bezier(.2,.75,.2,1) both}',
    '::view-transition-new(gallery-stage){animation:gallery-stage-arrive .45s cubic-bezier(.22,.68,.17,1) both}',
    'incoming duration and easing')

# Nested About routes are single-surface entrances, not shared-element snapshots:
# retain the visible content when navigating so there is no blank frame.
replace_one(
    '@keyframes gallery-about-forward{from{opacity:.94;transform:translateX(7px)}to{opacity:1;transform:translateX(0)}}',
    '@keyframes gallery-about-forward{from{opacity:.86;transform:scale(1.008)}to{opacity:1;transform:scale(1)}}',
    'About forward micro depth')
replace_one(
    '@keyframes gallery-about-back{from{opacity:.94;transform:translateX(-7px)}to{opacity:1;transform:translateX(0)}}',
    '@keyframes gallery-about-back{from{opacity:.86;transform:scale(1.008)}to{opacity:1;transform:scale(1)}}',
    'About reverse micro depth')
replace_one(
    '#settings-about-root [data-about-view]:not([hidden]){animation:gallery-about-forward .22s cubic-bezier(.2,.75,.2,1) both}',
    '#settings-about-root [data-about-view]:not([hidden]){animation:gallery-about-forward .45s cubic-bezier(.22,.68,.17,1) both}',
    'About entrance duration')

# Settings keeps its already-tested open/close sequence and lengths (280 ms
# open, 140 ms outgoing plus 140 ms incoming), with micro-depth replacing lift.
# Its source is only partly visible at a time, so never fade Settings to zero.
replace_one(
    '@keyframes settings-enter{from{opacity:.97;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}',
    '@keyframes settings-enter{from{opacity:.97;transform:scale(1.008)}to{opacity:1;transform:scale(1)}}',
    'Settings entrance micro depth')
replace_one(
    '@keyframes settings-exit{from{opacity:1;transform:translateY(0)}to{opacity:.97;transform:translateY(5px)}}',
    '@keyframes settings-exit{from{opacity:1;transform:scale(1)}to{opacity:.97;transform:scale(.994)}}',
    'Settings exit micro depth')
replace_one(
    '@keyframes gallery-return{from{opacity:.97;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}',
    '@keyframes gallery-return{from{opacity:.97;transform:scale(1.008)}to{opacity:1;transform:scale(1)}}',
    'Settings return micro depth')

# Browser fallback and first-render entrances remain one-sided, so use a light
# surface effect instead of deliberately showing an empty page.
replace_one(
    "[{opacity:.96,transform:'translateY(4px)'},{opacity:1,transform:'translateY(0)'}],\n   {duration:240,easing:'cubic-bezier(.2,.75,.2,1)'}",
    "[{opacity:.96,transform:'scale(1.008)'},{opacity:1,transform:'scale(1)'}],\n   {duration:450,easing:'cubic-bezier(.22,.68,.17,1)'}",
    'fallback for browsers without View Transitions')
replace_one(
    '#screen.surface-enter{animation:gallery-surface-in .24s cubic-bezier(.2,.7,.2,1) both}',
    '#screen.surface-enter{animation:gallery-surface-in .45s cubic-bezier(.22,.68,.17,1) both}',
    'standalone secondary entrance duration')
replace_one(
    '@keyframes gallery-surface-in{\n from{opacity:0;transform:translateY(6px)}\n to{opacity:1;transform:translateY(0)}\n}',
    '@keyframes gallery-surface-in{\n from{opacity:.96;transform:scale(1.008)}\n to{opacity:1;transform:scale(1)}\n}',
    'standalone secondary entrance avoids opacity zero')

# Critical regression guards. Other than the intended animation statements,
# keep all other route logic and main-tab slides exactly as in the source.
for marker in ('function transitionGalleryStage(mutator)', 'galleryStageTransition.skipTransition()',
               'galleryStageMutating=true', 'function closeSettings()', 'function whEnter(',
               'function whExit(', 'tab-pages-track', 'player-episode-nav',
               'player-upnext', 'Watch History', 'prefers-reduced-motion'):
    if marker not in html:raise ValueError(f'Gallery functionality marker missing: {marker}')
assert html.count('::view-transition-old(gallery-stage)') == 2
assert 'transition:transform .31s' not in html or 'tab-pages-track' in html
new=html.encode('utf-8')
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_bytes(new)
print('Baseline SHA-256:',hashlib.sha256(original).hexdigest(),len(original))
print('Updated SHA-256:',hashlib.sha256(new).hexdigest(),len(new))
print('Changed bytes:',len(new)-len(original))
