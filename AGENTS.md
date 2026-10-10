# Daneel: Sunholo blog changes

This is the Docusaurus blog at https://www.sunholo.com/blog/. Read `CLAUDE.md`
for authoring conventions and `scripts/MIRRORING-GUIDE.md` for a mirror request.

Change only the requested post, necessary `blog/img/` or `static/img/` assets,
and directly related author/tag metadata when the request requires it. Preserve
existing slugs and published URLs unless Mark asks to change them. Do not modify
deployment workflows, dependencies, scripts, application components, credentials
or domain settings as part of a content task. Do not fetch private product repos
or search for credentials; use supplied evidence, accessible public sources and
the material already in this repository. Say BLOCKED when necessary evidence is
unavailable instead of inventing release facts or attributed quotes.

New AI-written content uses author `solaris` and the existing AI disclosure
admonition format. Human-authored posts retain their author when being edited.
Substack mirrors remain verbatim except for conversion fixes, as the mirroring
guide requires. Existing screenshots are preferred; do not invent screenshot
content or alt text for an image you cannot inspect.

Validate with Node >=20, `yarn install --frozen-lockfile` and `yarn build`.
Do not change the lockfile to make a content build work. Report the actual checks
run and any failure or unavailable check. Review the diff for unintended edits.

Commit the change on the task branch. The coordinator opens one PR against
`main`; for a requested revision, amend the existing PR branch according to the
task's site skill. Never push directly to `main`, approve or merge a PR.
Mark reviews and merges. The existing Pages workflow builds and publishes only
after merge; a completed task or open PR is not a deployed blog change.
