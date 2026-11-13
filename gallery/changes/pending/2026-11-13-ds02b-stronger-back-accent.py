#!/usr/bin/env python3
"""DS02b: adjust only four existing Back-button color mixes and corresponding tests."""
import hashlib,json,re
from pathlib import Path
p=json.loads(Path('gallery/checkpoints/current.json').read_text())
assert p['folder']=='2026-11-13-ds02-tinted-back-buttons'
assert p['sha256']=='ec2a44d2bc9097441aa69dc0c615bc7a2462796762398b6555c57a1f80c20e92'
changes=[{"path":"gallery/src/styles/28-unified-headers-and-history-frame.css","sha":"a4863c48b78cfe61b31258f5ddb7993fe221ae2d","replacements":[["color-mix(in srgb,var(--panel) 88%,var(--accent) 12%)","color-mix(in srgb,var(--panel) 80%,var(--accent) 20%)"],["color-mix(in srgb,var(--panel2) 45%,var(--accent) 55%)","color-mix(in srgb,var(--panel2) 28%,var(--accent) 72%)"],["color-mix(in srgb,var(--panel) 80%,var(--accent) 20%)","color-mix(in srgb,var(--panel) 76%,var(--accent) 24%)"],["color-mix(in srgb,var(--panel2) 30%,var(--accent) 70%)","color-mix(in srgb,var(--panel2) 18%,var(--accent) 82%)"]]},{"path":"gallery/tests/test_player_settings_regression.py","sha":"09cc2ba3e9d5ed28ffa67076a4e612bbfff11e02","replacements":[["color-mix(in srgb,var(--panel) 88%,var(--accent) 12%)","color-mix(in srgb,var(--panel) 80%,var(--accent) 20%)"],["color-mix(in srgb,var(--panel2) 45%,var(--accent) 55%)","color-mix(in srgb,var(--panel2) 28%,var(--accent) 72%)"],["color-mix(in srgb,var(--panel) 80%,var(--accent) 20%)","color-mix(in srgb,var(--panel) 76%,var(--accent) 24%)"],["color-mix(in srgb,var(--panel2) 30%,var(--accent) 70%)","color-mix(in srgb,var(--panel2) 18%,var(--accent) 82%)"]]}]
extra_tests=[["    const expected=[p.color,p.backgroundColor,p.borderTopColor];\n    probe.remove();","    const expected=[p.color,p.backgroundColor,p.borderTopColor];\n    // Reference the previous DS02 strength and a representative theme panel.\n    probe.style.backgroundColor=hover?'color-mix(in srgb,var(--panel) 80%,var(--accent) 20%)':'color-mix(in srgb,var(--panel) 88%,var(--accent) 12%)';\n    probe.style.borderTopColor=hover?'color-mix(in srgb,var(--panel2) 30%,var(--accent) 70%)':'color-mix(in srgb,var(--panel2) 45%,var(--accent) 55%)';\n    const oldFill=p.backgroundColor,oldBorder=p.borderTopColor;\n    probe.style.backgroundColor='var(--panel2)';\n    const panel=p.backgroundColor;\n    probe.remove();"],["    const a=lum(s.color),b=lum(s.backgroundColor);\n    return {actual:[s.color,s.backgroundColor,s.borderTopColor],expected,","    const a=lum(s.color),b=lum(s.backgroundColor),edge=lum(s.borderTopColor),surface=lum(panel);\n    const ratio=(x,y)=>(Math.max(x,y)+.05)/(Math.min(x,y)+.05);\n    return {actual:[s.color,s.backgroundColor,s.borderTopColor],expected,\n     strongerFill:b>lum(oldFill),strongerBorder:edge>lum(oldBorder),\n     borderPanelContrast:ratio(edge,surface),"],["    check(rest['contrast']>=4.5,('DS02 text contrast',route,theme,width,rest['contrast']))","    check(rest['contrast']>=4.5,('DS02 text contrast',route,theme,width,rest['contrast']))\n    check(rest['strongerFill'] and rest['strongerBorder'] and rest['borderPanelContrast']>=3,('DS02b stronger rest separation',route,theme,width,rest))"],["    check(hover['contrast']>=4.5 and hover['geometry']==rest['geometry'],('DS02 hover contrast/geometry',route,theme,width,rest,hover))","    check(hover['contrast']>=4.5 and hover['geometry']==rest['geometry'],('DS02 hover contrast/geometry',route,theme,width,rest,hover))\n    check(hover['strongerFill'] and hover['strongerBorder'] and hover['borderPanelContrast']>=3,('DS02b stronger hover separation',route,theme,width,hover))"],["'six themes; 1440/750/420; rest/hover/focus; contrast >=4.5'","'six themes; 1440/750/420; rest/hover/focus; text >=4.5; stronger tint/border; border vs panel2 >=3'"]]
updates=[]
for item in changes:
    path=Path(item['path'])
    raw=path.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==item['sha'],str(path)
    data=raw.decode('utf-8')
    mapping=dict(item['replacements'])
    for old in mapping:
        assert data.count(old)==1,(str(path),old)
    # Simultaneous substitutions: the new rest fill equals the old hover fill.
    data=re.sub('|'.join(re.escape(old) for old in mapping),lambda m:mapping[m.group()],data)
    if path.name=='test_player_settings_regression.py':
        for old,new in extra_tests:
            assert data.count(old)==1,(str(path),old[:120])
            data=data.replace(old,new,1)
    updates.append((path,data.encode('utf-8')))
for path,data in updates:
    path.write_bytes(data)
print('DS02b: four existing color mixes refined; no other application bytes modified in source; permanent tests updated.')
