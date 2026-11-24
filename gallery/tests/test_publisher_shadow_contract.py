#!/usr/bin/env python3
"""Negative publisher handoff and additive-only original publisher preservation."""
import runpy
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
validate=runpy.run_path(str(root/"gallery/tools/published-shadow-target.py"))["validate"]
request="ec5242eaf4bbf98ff96cadbb9c39e8214abd9698"
published="50bf289581c713fea36cf00e5eb6eed5b9619a5b"
good=(request,published,request,published,"zonetrooper90/StrawVerse-mac","refs/heads/gallery/development-clean","push")
assert validate(*good)==published
for index,wrong in [(0,published),(0,"bad"),(1,request),(1,"bad"),(2,published),
                    (3,request),(4,"other/repo"),(5,"refs/heads/main"),
                    (5,"refs/tags/v1"),(6,"workflow_dispatch"),(6,"workflow_call"),
                    (6,"pull_request")]:
    sample=list(good)
    sample[index]=wrong
    try: validate(*sample)
    except AssertionError: pass
    else: raise AssertionError("Accepted unsafe advisory target "+repr((index,wrong)))
original=subprocess.check_output(["git","-C",str(root),"cat-file","blob",
               "48390f61a5a81e8ac67ac69565d00752508eb71c"],text=True)
actual=(root/".github/workflows/gallery-controlled-publish.yml").read_text()
marker="\n  # BEGIN NONREQUIRED PUBLISHED-SHA SHADOW:"
assert actual.count(marker)==1 and actual.count("# END NONREQUIRED PUBLISHED-SHA SHADOW.")==1
prefix,advisory=actual.split(marker,1)
assert advisory.strip().endswith("# END NONREQUIRED PUBLISHED-SHA SHADOW.")
assert advisory.count("continue-on-error: true")==3
assert advisory.count("needs.publish.outputs.published_sha")>=4
assert advisory.count("gallery-publisher-shadow-")>=2
assert "--aggregate" in advisory and "merge-multiple: true" in advisory
assert "fail-fast: false" in advisory and advisory.count("suite: ")==9
assert "--run-attempt" in advisory and "github.run_attempt" in advisory
assert "  shadow-preflight:" in advisory and "  shadow-shards:" in advisory
assert "  shadow-aggregate:" in advisory
assert "shadow-preflight.outputs.verified" in advisory
output="    outputs:\n      published_sha: "+"$"+"{{ steps.published_commit.outputs.published_sha }}\n"
id_line="        id: published_commit\n"
emit='          echo "published_sha=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"\n'
assert prefix.count(output)==prefix.count(id_line)==prefix.count(emit)==1
assert prefix.replace(output,"").replace(id_line,"").replace(emit,"")==original, "Original publisher altered"
assert original.count("gh workflow run gallery-checkpoint-integrity.yml")==1
assert original.count("gh workflow run gallery-transition-ui.yml")==1
print("PASS additive publisher contract, strict nine-proof coverage and 12 negative target cases")
