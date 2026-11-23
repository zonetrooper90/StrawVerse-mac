# Gallery release regression modernization — proposed cutover and rollback

**Status: REVIEW PROPOSAL ONLY — NOT APPROVED FOR ACTIVATION.**
**Prepared:** 2026-11-23. **Active branch:** `gallery/development-clean`.
**Latest verified trial infrastructure commit:** `c6406f6945adaf71f8505825832483499bfc6b5a`.
No new Gallery release, HTML build, checkpoint, original GitHub Actions check, branch-protection rule or publisher modification is authorized by this document.

## 1. Verified evidence and its limits

- Historical Stage 6 strict, G3.1-pinned, nine-shard read-only benchmark: commit `1078e20a94e349cbb82c4b305802a97157a1490b`, parallel `45074958981` success, original browser `45074958928` success and integrity `45074958975` success. Whole-workflow elapsed **20m08s** versus original **39m46s**; summed job durations 79.2 versus 76.2 minutes.
- Trial A repeatability: commit `067285845ebe482a5a2d60fa7b0b12577c6c4421`, nine-shard `45223808249`, original browser `45223808902`, integrity `45223808361`, all first-attempt success. Parallel **20m20s** versus original **37m48s**; summed job durations 79.47 versus 74.30 minutes.
- Trial B commit-dependent verification: commit `8baf3be4239a293452202aa7300ae6fe04d94100`, dynamically keyed parallel `45240712823` (preflight, all nine scripts, strict aggregate), original browser `45240712774` (full, lightweight, subtitle), integrity `45240713010`, all first-attempt success. Parallel **20m14s** versus original **38m31s**; summed job durations 80m35s versus 76m47s.
- Trial C truly byte-changed candidate comparison: GitHub real infrastructure commit `c6406f6945adaf71f8505825832483499bfc6b5a`. Separate, nonpublishing trial workflow `45256613162` **all 14 jobs passed** (preflight `137979981164`, original-style full `137980144992`, lightweight `137980145041`, subtitle `137980144994`, nine individual shards, strict aggregate `138004536459`). Original independent browser `45256612887` (all 3 jobs) and integrity `45256612896` also passed on the real commit; all three runs succeeded on attempt 1.
- Trial C scratch-only synthetic Git commit `7ab82d0b6d75ba28ba24c4bef465e641992176d0` **was never pushed or published**. The exact same locally reconstructed inert CSS-comment source candidate was used by original serial suites and parallel shards; experimental scratch full HTML **6,961,732 bytes**, SHA-256 `49d489fcd5a941c587520156380920f7132ac603841f5cf629a319ea09d15ef8`; scratch lightweight HTML **646,042 bytes**, SHA-256 `6cd42f43e04c3a678bc6e5eb67d839616bd7a3c972ef40eec0c4e69da4ad9922`. It carried a scratch experimental full checkpoint, not a new canonical GitHub pointer. Trial C whole-workflow elapsed 40m56s **includes running original serial and nine parallel groups together**; do not compare this combined duration directly to the parallel-only benchmark.
- The trial branch diff from Trial B to Trial C contains only three added scratch-trial files and four documentation updates. No app source, published full or lightweight HTML, images, assets, publisher, original test scripts, mandatory workflow or historical checkpoint changed. G3.1 approved full archive still at `2026-11-22-g31-more-actions-smooth-ripple-verified-publish`: 6,961,644 bytes / SHA-256 `2e01412a4da6874398af9e3373346208508e66be15ca3113c4c17023c05dff50`.
- **Conclusions:** Parallel execution repeatedly reduces wall clock by roughly 46–49% on this baseline while using approximately 4–7% more aggregated job time; the latter is not necessarily billed runner cost. The unchanged original assertions, both HTML modes, reduced-motion/timing cases and the nine-suite matrix have passed in baseline and scratch-changed trials. These are encouraging parity results, **not** an exact-commit, two-independent-workflow verified publication of a changed real release. A past original Watch History 130ms moving-path assertion failed on attempt 1 of `45197181695` and passed one log-inspected retry; do not hide this reliability observation.

## 2. Inviolable release safeguards

1. Source-first and approved-asset edits only; deterministic full/lightweight generation from the same approved source and **same exact build commit**; original approved UI, animations, themes, accessibility and timing assertions untouched.
2. Preserve `.github/workflows/gallery-candidate-tests.yml` and all prepublication comparison jobs, publisher candidate hashes, immutable candidate patch, controlled publisher and deduplicated approved publication request. Never dispatch duplicate publishing or force-push.
3. Preserve **new immutable full archive** for every changed full release, byte count and SHA-256 pointer verification, archive reconstruction and full/lightweight source parity.
4. Maintain **two independently successful postpublication GitHub Actions workflows on the exact published build commit**: a checkpoint-integrity workflow and a browser verification workflow (original until a separately authorized replacement has independently demonstrated equivalence). Independent complete job result and exact published SHA evidence, not just a green request commit, are required.
5. Never weaken a test, remove motion/reduced-motion variants, skip an HTML mode, treat skipped or canceled jobs as passed, or treat a synthetic scratch candidate as a release.
6. Do not modify the protected recovery branch or stable/native branches. A successful HTML browser workflow is not native macOS verification and not user visual acceptance.

## 3. Proposed production architecture (not implemented)

**Checkpoint integrity:** Keep the current independent `.github/workflows/gallery-checkpoint-integrity.yml`, Git blob `b3527dfb994a571e230a40f2399eb2251730980b`, intact and separately required.

**Parallel browser verifier:** After new scoped user authorization, make a **separate production-intended workflow** from the tested read-only dynamic trial, not by silently replacing the original current workflow. Maintain fail-fast preflight, all nine original unchanged suite/mode scripts, strict aggregate, provenance of test script Git blob, two current HTML build hashes, exact source commit, full archive/pointer and run ID/attempt, and runner/compiler/browser pins. Workflow-level success must fail closed when ANY shard fails, times out, is skipped/canceled or lacks proof. No runner cache/content artifact may silently substitute for the pinned checkout. Changes to the existing fixed original script/workflow blob pins demand explicit technical re-review.

**Exact published SHA handoff:** The actual `.github/workflows/gallery-controlled-publish.yml` (current Git blob `48390f61a5a81e8ac67ac69565d00752508eb71c`) explicitly calls `gh workflow run gallery-checkpoint-integrity.yml --ref gallery/development-clean` and `gh workflow run gallery-transition-ui.yml --ref gallery/development-clean` *after pushing* the full build commit. A new trial workflow currently triggers only on selected infrastructure paths and lacks an authorized published-release dispatch. Do NOT presume GitHub Actions push events from a token-generated publisher push will schedule new checks. Any approved production handoff must pass **the exact just-pushed build commit SHA**, separately assert branch HEAD/source/build/checkpoint equality, and verify the resulting Actions runs and all jobs refer to that SHA. Guard branch movement and race conditions; never accept verification of a later HEAD or earlier request. The mechanism for dispatch and the publisher edit itself remain proposed and require review.

**Required-check mapping:** Inventory current GitHub branch protection/rulesets and named checks before activation; do not claim configuration was inspected unless access allows it. Plan the exact workflow/job-name mapping for the new required aggregate, preserve the independent checkpoint requirement, and ensure required statuses cannot go silently missing, skip, or be satisfied by a stale commit. Keep the original browser workflow as a shadow/required check through a defined observation interval.

**Runner usage:** Collect timing, rerun frequency, canceled/failed rates, and cumulative/billed GitHub Actions usage for several real builds. Parallel 9-runner peak concurrency and +4–7% observed job-minutes must be accepted explicitly as a latency/resource trade-off; reductions in billed cost are not proved.

## 4. Proposed phased activation gates (each requires explicit scope review)

A. **Evidence closure (this documentation only):** Record Trial C exact-run outcomes and this proposal. Require both existing independent workflows to pass on the documentation commit; no new generated HTML or checkpoint. This is the currently authorized action.

B. **Shadow verification on an actually approved, changed published build:** Only when a real feature change is separately approved under the ORIGINAL publisher and all candidate checks. After the publisher atomically commits BOTH changed HTML outputs and a NEW immutable checkpoint, dispatch both current independent original checks on that **build commit**; in parallel run a separately reviewed read-only parallel verifier on that SAME exact published commit. Compare coverage, failure behavior, SHA/bytes, timestamps and consumption. Treat a difference as a blocker; do not mark the release verified until the original mandatory gates pass. Do not create a feature change solely to manufacture this evidence without approval.

C. **Proposed optional shadow period:** Repeat on at least another approved changed build or equivalent independently approved real-commit reproduction, checking historical Watch History timing sensitivity. Maintain the original postpublication checks unmodified; avoid duplicate publisher invocations.

D. **Reviewed cutover, if evidence supports it:** Seek separate user sign-off for every workflow/publisher/required-check edit and concrete rollback plan. First verify the production-intended parallel workflow in shadow mode with all original gates preserved. Only then consider substituting the single browser verifier with an exact-commit aggregate while preserving **two independent** workflows and the existing publisher/candidate/checkpoint integrity and accessibility gates. Required-check protection changes need their own atomic review and verification before they take effect. No change is authorized by this proposal.

E. **Post-cutover guardrails:** Pin and independently audit the first exact published build under the new required verifier; monitor timing failures and job resource usage. Until the new check and independent checkpoint both pass on that exact build, with user visual review as separately applicable, delivery is unverified.

## 5. Concrete rollback, without republishing or damaging the checkpoint

**Triggers:** any missing/skipped/orphaned required context; different exact SHA at candidate/publish/dispatch/check; proof aggregation mismatch; coverage or accessibility loss; reproducible failing assertion; cancelled/failed independent integrity; run/cost/runner-limit instability; or user request.

1. **Freeze promotion** and do not republish, restart an active job, force push or overwrite an immutable checkpoint. Identify exact affected build commit, publisher run, new/old browser runs, integrity run, status checks and failure logs.
2. Retain original `.github/workflows/gallery-transition-ui.yml` immutable Git blob `70a42d79ba235a775f89eea8c9d618936046ec52`, original browser script identities, and independent checkpoint integrity workflow Git blob `b3527dfb994a571e230a40f2399eb2251730980b`. Keep historical releases, archives and protected branch intact.
3. With separate authorized branch changes, restore the publisher's **original exact workflow dispatch** and old required browser context(s) only after ensuring the old workflow is still operational and has verified the current affected published SHA. Revert or disable only the new verifier's activation/gate wiring; do not delete historical run evidence, weaken assertions or modify released HTML.
4. For any affected release, require independently successful original browser and unchanged integrity workflows on the **exact existing published SHA**; if they cannot run, mark that release unverified and halt delivery rather than republishing blindly.
5. Record reason, exact reverting commit/run IDs, unchanged source/build/archive hashes and outcome in DEVELOPMENT-STATE.md. If the rollback edit itself is a documentation/workflow commit, independently verify it. No automatic retry beyond two proven transient failures and never retry deterministic failures without a reviewed correction.

## 6. Decisions intentionally open for review

- Whether to adopt nine-shard browser execution as the replacement required browser verifier given roughly half the elapsed time but slightly higher runner usage.
- Exact mechanism and input contract for publisher-to-parallel workflow dispatch, including GitHub Actions event provenance and commit identity.
- Named status-check transition/ruleset edits and minimum number of real changed-build shadow verifications.
- Handling original workflow/test Git pin updates when a future separately approved app change requires intentional new assertions.
- Whether to optimize resource consumption or historical 130ms timing flakiness *in separate, explicitly reviewed scopes* rather than weakening tests during the cutover.

**Current disposition:** PROPOSED, not approved to implement. Original publisher plus original full/lightweight/subtitle browser workflow and independent checkpoint integrity remain authoritative.
