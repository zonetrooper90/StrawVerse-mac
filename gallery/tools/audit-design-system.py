#!/usr/bin/env python3
"""Read-only CSS inventory and isolated search error-recovery investigation."""
import argparse
import bisect
import collections
import hashlib
import json
import os
import re
from pathlib import Path

import tinycss2

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {"media", "supports", "container", "layer", "scope", "document", "starting-style"}
THEMES = ("ocean", "twilight", "ember", "slate", "glacier", "verdant")
DESIGN_PROPS = {
    "spacing": ("gap", "row-gap", "column-gap", "padding", "margin"),
    "typography": ("font-size", "font-weight", "font-family", "line-height", "letter-spacing"),
    "surface": ("border", "border-radius", "box-shadow", "background", "color"),
    "motion": ("transition", "animation", "animation-duration", "transition-duration"),
}

def source():
    manifest = json.loads((ROOT / "src/build-manifest.json").read_text())
    starts, files, chunks = [], [], []
    offset = 1
    for name in manifest["style"]:
        text = (ROOT / "src" / name).read_bytes().decode("utf-8")
        if not text.endswith("\n"):
            raise ValueError(f"Unexpected non-line-aligned fragment: {name}")
        starts.append(offset)
        files.append(name)
        chunks.append(text)
        offset += text.count("\n")
    def locate(line):
        idx = bisect.bisect_right(starts, line) - 1
        return {"file": files[idx], "line": line - starts[idx] + 1, "assembled_line": line}
    return "".join(chunks), files, locate

def split_selectors(tokens):
    groups = [[]]
    for token in tokens:
        if token.type == "literal" and token.value == ",":
            groups.append([])
        else:
            groups[-1].append(token)
    return [tinycss2.serialize(group).strip() for group in groups if tinycss2.serialize(group).strip()]

def analyze(css, locate):
    declarations, issues, rule_counts, conditions = [], [], collections.Counter(), collections.Counter()
    def walk(rules, context=()):
        for rule in rules:
            kind = rule.type
            if kind == "error":
                issues.append({**locate(rule.source_line), "message": rule.message, "context": list(context)})
                continue
            if kind == "at-rule":
                label = "@" + rule.lower_at_keyword + " " + tinycss2.serialize(rule.prelude).strip()
                label = label.rstrip()
                rule_counts["at-rules"] += 1
                conditions[label] += 1
                if rule.content is None:
                    continue
                if rule.lower_at_keyword in GROUPS:
                    walk(tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True), (*context, label))
                elif rule.lower_at_keyword.endswith("keyframes"):
                    rule_counts["keyframes"] += 1
                else:
                    rule_counts["other-at-rule-blocks"] += 1
                continue
            if kind != "qualified-rule":
                continue
            rule_counts["qualified-rules"] += 1
            selectors = split_selectors(rule.prelude)
            if any("}" in selector or "{" in selector for selector in selectors):
                issues.append({**locate(rule.source_line), "message": "Suspect qualified-rule prelude: " + ", ".join(selectors), "context": list(context)})
            for decl in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
                if decl.type == "error":
                    issues.append({**locate(decl.source_line), "message": decl.message, "context": list(context), "selectors": selectors})
                elif decl.type == "declaration":
                    prop = decl.name if decl.name.startswith("--") else decl.lower_name
                    declarations.append({**locate(decl.source_line), "selectors": selectors,
                        "context": list(context), "property": prop,
                        "value": tinycss2.serialize(decl.value).strip(), "important": decl.important})
                elif decl.type == "at-rule":
                    issues.append({**locate(decl.source_line), "message": "Nested declaration at-rule; review separately", "context": list(context)})
    walk(tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True))
    return declarations, issues, rule_counts, conditions

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def report(out, name, text):
    (out / name).write_text(text + "\n", encoding="utf-8")
    print(text, flush=True)
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
            summary.write(text + "\n\n")

def inventory(out):
    css, files, locate = source()
    ds, issues, counts, conditions = analyze(css, locate)
    chains = collections.defaultdict(list)
    values = {key: collections.Counter() for key in DESIGN_PROPS}
    custom = collections.defaultdict(list)
    refs = collections.Counter()
    theme_tokens = {theme: set() for theme in THEMES}
    for d in ds:
        prop, val = d["property"], d["value"]
        for selector in d["selectors"]:
            chains[(selector, tuple(d["context"]), prop)].append(d)
            if prop.startswith("--"):
                for theme in THEMES:
                    if re.search(r'data-theme\s*=\s*["\']?' + theme + r'["\']?', selector):
                        theme_tokens[theme].add(prop)
        if prop.startswith("--"):
            custom[prop].append(d)
        for category, properties in DESIGN_PROPS.items():
            if any(prop == p or prop.startswith(p + "-") for p in properties):
                values[category][(prop, val)] += 1
        refs.update(re.findall(r"var\(\s*(--[\w-]+)", val))
    candidates = []
    for (selector, context, prop), chain in chains.items():
        if len(chain) < 2:
            continue
        distinct = {(d["value"], d["important"]) for d in chain}
        candidates.append({"selector": selector, "context": list(context), "property": prop,
                           "classification": "same-value candidate" if len(distinct) == 1 else "different-value chain",
                           "declarations": chain})
    candidates.sort(key=lambda c: (-len(c["declarations"]), c["selector"], c["property"], c["context"]))
    bases = [d for d in ds if any(s in (":root", "html", "body", "*", "button", "input", "select",
             ".app", ".btn", ".iconbtn", ".tab", ".workspace", "h1", "h2", "h3",
             ".heading-row", ".section-row", ".collections-head") for s in d["selectors"])]
    data = {"commit": os.getenv("GITHUB_SHA", "local"), "sha256": hashlib.sha256(css.encode()).hexdigest(),
            "files": files, "counts": dict(counts), "conditional_contexts": dict(conditions),
            "declarations": len(ds), "important": sum(d["important"] for d in ds),
            "theme_token_names": {k: sorted(v) for k, v in theme_tokens.items()},
            "custom_properties": dict(custom), "var_references_heuristic": dict(refs),
            "global_and_shared_defaults": bases, "parse_review": issues,
            "design_values": {k: [{"property": p, "value": v, "count": n}
                              for (p, v), n in counter.most_common()] for k, counter in values.items()},
            "candidate_override_chains": candidates, "declaration_inventory": ds}
    write_json(out / "design-inventory.json", data)
    same = sum(c["classification"] == "same-value candidate" for c in candidates)
    lines = ["## Read-only design-system inventory", "",
             f"- Stylesheet: {len(files)} fragments; {len(css.encode()):,} bytes.",
             f"- Qualified rules: {counts['qualified-rules']:,}; declarations: {len(ds):,}; important declarations: {data['important']:,}.",
             f"- Custom property names: {len(custom)}; parse-review findings: {len(issues)}.",
             f"- Same-selector/property/context chains: {len(candidates):,} ({same:,} same-value candidates, {len(candidates)-same:,} different-value chains).",
             "- Theme palette token counts: " + ", ".join(f"{k}: {len(v)}" for k,v in theme_tokens.items()) + ".", "",
             "### Frequent design values (inventory, not recommendations)"]
    for category, counter in values.items():
        lines += ["", f"**{category.title()}**: " + "; ".join(f"{p}: {v} ({n})" for (p,v),n in counter.most_common(5))]
    lines += ["", "### Longest candidate chains", ""]
    for item in candidates[:12]:
        locations = ", ".join(f"{d['file']}:{d['line']}" for d in item["declarations"][:8])
        lines.append(f"- {item['selector']} / {item['property']}: {len(item['declarations'])} declarations ({item['classification']}); {locations}.")
    lines += ["", "Exact selector/property/context matching is only a screening heuristic. It does not resolve specificity, shorthand interactions, cross-selector overrides, conditional overlap, inheritance, CSSOM error recovery or state-dependent computed styles. Same-value declarations are not proven redundant. Theme, responsive, focus, motion and state exceptions must be reviewed manually. No CSS was changed. Full machine-readable evidence is in design-inventory.json."]
    report(out, "design-inventory.md", "\n".join(lines))

def anomaly(out):
    from playwright.sync_api import sync_playwright
    css, _, _ = source()
    name = "styles/09-search.css"
    fragment = (ROOT / "src" / name).read_text(encoding="utf-8")
    bad = "transition:grid-template-rows .42s cubic-bezier(.22,.72,.2,1),opacity .25s ease}\n"
    lines = fragment.splitlines(keepends=True)
    # The previous line includes indentation and closes the legitimate rule.
    indices = [i for i,line in enumerate(lines) if line == bad]
    if len(indices) != 1 or ".continue-shell .continue-clip" not in lines[indices[0]+1]:
        raise RuntimeError("Known anomaly no longer matches the reviewed source; stop for inspection.")
    i = indices[0]
    candidate_fragment = "".join(lines[:i] + lines[i+1:])
    if css.count(fragment) != 1:
        raise RuntimeError("Fragment is not unique in assembled stylesheet.")
    candidate = css.replace(fragment, candidate_fragment, 1)
    fixture = '<div class="continue-shell"><div class="continue-clip">Preview</div></div>'
    evaluate = """css => {
      const style = document.createElement('style');
      style.textContent = css;
      document.head.append(style);
      const target = document.querySelector('.continue-clip');
      const parent = target.parentElement;
      const rules = [];
      function walk(list) {
        for (const rule of list) {
          if (rule.selectorText && rule.selectorText.includes('continue-clip'))
            rules.push({selector: rule.selectorText, css: rule.cssText});
          if (rule.cssRules) walk(rule.cssRules);
        }
      }
      walk(style.sheet.cssRules);
      const cs = getComputedStyle(target), ps = getComputedStyle(parent);
      const result = {rules, clip: {minHeight: cs.minHeight, overflow: cs.overflow},
                      parent: {gridTemplateRows: ps.gridTemplateRows, transition: ps.transition}};
      style.remove();
      return result;
    }"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.set_content(fixture)
        before = page.evaluate(evaluate, css)
        after = page.evaluate(evaluate, candidate)
        browser.close()
    data = {"commit": os.getenv("GITHUB_SHA", "local"), "file": name, "line": i+1,
            "source_context": [{"line": j+1, "text": lines[j].rstrip("\n")} for j in range(max(0,i-3),min(len(lines),i+4))],
            "baseline": before, "hypothetical_in_memory_removal": after, "observed_difference": before != after}
    write_json(out / "search-anomaly.json", data)
    text = "\n".join(["## Search CSS anomaly investigation", "",
          f"- Location: {name}:{i+1}. A bare duplicate transition follows the closed Continue Watching rule.",
          f"- Baseline CSSOM rules mentioning continue-clip: {len(before['rules'])}; hypothetical removal: {len(after['rules'])}.",
          f"- Baseline fixture: min-height {before['clip']['minHeight']}, overflow {before['clip']['overflow']}.",
          f"- Hypothetical fixture: min-height {after['clip']['minHeight']}, overflow {after['clip']['overflow']}.",
          f"- Observed CSSOM/computed-style difference: {'yes' if before != after else 'no'}.",
          "", "The hypothetical deletion was tested only in an isolated Chromium fixture using the complete assembled stylesheet in memory. No application file or checkpoint was edited. A change in browser recovery is possible even if a duplicate declaration looks unnecessary; full application regression and explicit approval are required for any correction.",
          "", "STOP: audit evidence is ready for human review. No CSS consolidation, syntax correction, or dithering has been authorized."])
    report(out, "search-anomaly.md", text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["inventory", "anomaly"])
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    (inventory if args.mode == "inventory" else anomaly)(args.out)

if __name__ == "__main__":
    main()
