# Manifest-driven documentation sync

`crewloom-manifest.json` is the reviewed map of source fields and documentation destinations. Source package files stay authoritative for their own versions. The manifest does not invent a unified product version.

## Scope and guardrails

- Public Core, Bridge and website source versions, exact Core `SKILL.md` file count, and exact tool registry entry count.
- Source version and latest stable GitHub release are separate columns. A website repository's GitHub releases can describe Desktop, not the website package. A GitHub release is not proof of an npm/PyPI publication or a deployed version.
- Output is a standalone `CREWLOOM_FACTS.md` in each allowlisted destination. Existing README prose, English/Arabic audit fixes, runtime metrics, download metadata, licenses and package versions are untouched.
- Product code is never imported or executed. No install, build, publish, deployment, merge or auto-merge command exists in this workflow.
- No benchmark, accuracy, latency, safety or compliance claims are generated. Structural counts do not establish quality.
- Private Agent/Pulse/Office repositories are excluded. Adding them needs owner approval for fields, audience and scoped access. Do not copy private source facts into this public repository by default.
- Canonical Bridge naming and domains remain owner decisions. Existing package names are displayed as observed metadata, not renamed.

## What runs automatically after review and merge

Daily at 07:43 UTC, or by manual dispatch, CI tests the generator, reads public default branches and release metadata, and uploads a 14-day preview artifact. Pull requests only run offline fixture tests, with read-only permissions and no sync credential.

Without `CREWLOOM_DOCS_SYNC_TOKEN`, preview mode is the full supported behavior. Nothing is pushed. The workflow says this in its summary rather than claiming cross-repository writes worked.

To enable cross-repository review PRs, the owner must separately configure a fine-grained token or GitHub App token as `CREWLOOM_DOCS_SYNC_TOKEN`, restricted to the three listed public repositories with contents and pull-request write access only. Do not paste credentials into issues or PRs. Organization policy must permit the selected bot identity to create PRs. The ordinary per-repository workflow token does not grant cross-repository write access. No permission or secret is created by this change.

With that credential, the bot creates content-addressed `bot/manifest-docs-sync-*` branches and opens docs-only PRs. It never force pushes or changes an open sync PR. While one is open, that repository is skipped; review or close it first. Retained merged branches do not prevent later, different updates. Repository rules and human merge review still apply. Enable branch protection before relying on this as a control.

The initial PR adds infrastructure only. It does not run a workflow on the default branch or start recurring activity until reviewed and merged. Existing `.github#2` and other consistency-audit PRs remain separate. This is a first rollout, not replacement of every historical hardcoded number. Once approved, the generated document can be linked from audited READMEs without overwriting their narrative changes. Website runtime metrics need a separate reviewed change.

## Local checks

Requires Python 3.11+, git and, for publishing only, authenticated GitHub CLI.

```sh
python scripts/test-sync-docs.py -v
python scripts/sync-docs.py                     # read public sources, preview only
python scripts/sync-docs.py --checkouts ../ --offline  # fixture/local preview
```

The snapshot `facts.json` includes exact source commit IDs. Generated Markdown omits commit IDs so unrelated commits and its own docs-only commits cannot create an endless PR loop. No wall-clock timestamp enters the rendered document. Repeated generation from equal facts is byte-identical.

## Failure handling

Any missing version/registry file, invalid metadata, network or authorization error fails before publishing starts. A 404 on the public latest stable release endpoint is explicitly represented as no stable GitHub release found, not as version zero. A private or moved repository must be removed or re-approved in the manifest rather than silently guessed. PR creation failures remain failed jobs; a branch pushed before a PR error is kept for inspection, never overwritten. Other repositories already processed may have PRs, so inspect the run log before retrying.
