#!/usr/bin/env python3
"""Inspect only: locate existing Gallery transition hooks in the verified checkpoint."""
from pathlib import Path
import sys
source=Path(sys.argv[1]).read_text(encoding='utf-8')
targets=[
 '@keyframes gallery-stage-leave','@keyframes gallery-stage-arrive',
 '::view-transition-old(gallery-stage)','@keyframes gallery-about-forward',
 '@keyframes settings-enter','@keyframes settings-exit',
 '@keyframes gallery-return','.settings-page.is-leaving',
 'function transitionGalleryStage','function showSettings(',
 'function hideSettings(', 'function closeSettings(',
 'galleryStageFallback=workspace.animate(', 
]
for needle in targets:
 index=source.find(needle)
 print('\\n===',needle,'COUNT',source.count(needle),'INDEX',index,'===')
 if index>=0:print(source[max(0,index-120):index+1700])
