# Release Process

## Prerequisites

- You are on the `main` branch with a clean working directory
- The `gh` CLI is installed and authenticated
- `CHANGES.md` has an `## X.Y.Z (unreleased)` section with entries

## Automated Release

Run the release script:

```bash
./release.sh 2.3.0
```

The script performs the following steps:

1. **Validate** -- checks branch, clean state, version format, and that CHANGES.md has the matching unreleased section
2. **Update versions** -- sets the version in:
   - `cookiecutter.json` (`_version`)
   - `docs/sources/conf.py` (`release`)
   - `CHANGES.md` (replaces `(unreleased)` with today's date)
3. **Commit and tag** -- creates a release commit and annotated git tag
4. **Push** -- pushes the commit and tag to origin
5. **GitHub release** -- creates a GitHub release using `gh release create` with the changelog entries as description
6. **Dev bump** -- bumps to next patch `.dev0`, adds a new `(unreleased)` section in CHANGES.md, commits and pushes

## Version Locations

| File | Field | Example |
|---|---|---|
| `cookiecutter.json` | `_version` | `"2.3.0"` |
| `docs/sources/conf.py` | `release` | `"2.3"` |
| `CHANGES.md` | Section heading | `## 2.3.0 (2026-02-24)` |
| Git tag | Tag name | `2.3.0` |

## Manual Release (if needed)

If you prefer not to use the script:

1. Update `_version` in `cookiecutter.json`
2. Update `release` in `docs/sources/conf.py`
3. Replace `(unreleased)` with today's date in `CHANGES.md`
4. Commit: `git commit -m "Release X.Y.Z"`
5. Tag: `git tag -a X.Y.Z -m "Release X.Y.Z"`
6. Push: `git push origin main && git push origin X.Y.Z`
7. Create GitHub release: `gh release create X.Y.Z --title "vX.Y.Z" --notes "..."`
8. Bump `_version` to next patch `.dev0`
9. Add new `(unreleased)` section to `CHANGES.md`
10. Commit: `git commit -m "Bump to X.Y.(Z+1).dev0 for development"`
11. Push: `git push origin main`
