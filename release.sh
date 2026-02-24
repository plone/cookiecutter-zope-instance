#!/usr/bin/env bash
# Release script for cookiecutter-zope-instance
#
# Usage: ./release.sh 2.3.0
#
# What it does:
# 1. Updates version in cookiecutter.json, docs/sources/conf.py, CHANGES.md
# 2. Sets today's date in CHANGES.md
# 3. Commits, tags, pushes
# 4. Creates a GitHub release with changelog entries
# 5. Bumps to next patch .dev0 with (unreleased) in CHANGES.md
# 6. Commits and pushes the dev bump

set -euo pipefail

VERSION="${1:-}"

if [[ -z "$VERSION" ]]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 2.3.0"
    exit 1
fi

# Validate version format (X.Y.Z)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in X.Y.Z format, got: $VERSION"
    exit 1
fi

# Ensure we're on main and clean
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" != "main" ]]; then
    echo "Error: Must be on 'main' branch, currently on '$BRANCH'"
    exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
    echo "Error: Working directory is not clean"
    git status --short
    exit 1
fi

# Parse version components
MAJOR=$(echo "$VERSION" | cut -d. -f1)
MINOR=$(echo "$VERSION" | cut -d. -f2)
PATCH=$(echo "$VERSION" | cut -d. -f3)
DOCS_VERSION="${MAJOR}.${MINOR}"
NEXT_PATCH=$((PATCH + 1))
NEXT_VERSION="${MAJOR}.${MINOR}.${NEXT_PATCH}.dev0"
TODAY=$(date +%Y-%m-%d)

echo "Releasing $VERSION ($TODAY)"
echo "  cookiecutter.json _version: $VERSION"
echo "  docs conf.py release: $DOCS_VERSION"
echo "  Next dev version: $NEXT_VERSION"
echo ""

# Check that CHANGES.md has the unreleased section
if ! grep -q "## ${VERSION} (unreleased)" CHANGES.md; then
    echo "Error: CHANGES.md does not contain '## ${VERSION} (unreleased)'"
    echo "Current unreleased heading:"
    grep "^## .*(unreleased)" CHANGES.md || echo "  (none found)"
    exit 1
fi

# --- Step 1: Update version strings ---

# cookiecutter.json: "_version": "X.Y.Z"
sed -i "s/\"_version\": \".*\"/\"_version\": \"${VERSION}\"/" cookiecutter.json

# docs/sources/conf.py: release = "X.Y"
sed -i "s/^release = \".*\"/release = \"${DOCS_VERSION}\"/" docs/sources/conf.py

# CHANGES.md: ## X.Y.Z (unreleased) -> ## X.Y.Z (YYYY-MM-DD)
sed -i "s/## ${VERSION} (unreleased)/## ${VERSION} (${TODAY})/" CHANGES.md

# --- Step 2: Extract changelog for this release ---
# Get lines between this version header and the next version header
CHANGELOG=$(awk "/^## ${VERSION//./\\.}/{found=1; next} /^## [0-9]/{if(found) exit} found{print}" CHANGES.md)
# Trim leading/trailing blank lines
CHANGELOG=$(echo "$CHANGELOG" | sed '/./,$!d' | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')

echo "Changelog entries:"
echo "$CHANGELOG"
echo ""

# --- Step 3: Commit and tag ---
git add cookiecutter.json docs/sources/conf.py CHANGES.md
git commit -m "Release ${VERSION}"
git tag -a "${VERSION}" -m "Release ${VERSION}"

# --- Step 4: Push commit and tag ---
git push origin main
git push origin "${VERSION}"

# --- Step 5: Create GitHub release ---
gh release create "${VERSION}" \
    --title "v${VERSION}" \
    --notes "$CHANGELOG"

echo ""
echo "GitHub release created: ${VERSION}"

# --- Step 6: Bump to next dev version ---
sed -i "s/\"_version\": \"${VERSION}\"/\"_version\": \"${NEXT_VERSION}\"/" cookiecutter.json

# Add new unreleased section to CHANGES.md
sed -i "/^# Changelog$/a\\
\\
## ${MAJOR}.${MINOR}.${NEXT_PATCH} (unreleased)\\
\\
- No changes yet." CHANGES.md

git add cookiecutter.json CHANGES.md
git commit -m "Bump to ${NEXT_VERSION} for development"
git push origin main

echo ""
echo "Done! Released ${VERSION}, now on ${NEXT_VERSION}"
