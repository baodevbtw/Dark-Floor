# Versioning Strategy

Dark Floor uses [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH).

## Version Numbering

### MAJOR (X._._ )
- Breaking changes to game mechanics
- Major feature additions
- Significant gameplay rewrites

### MINOR (_.X._ )
- New features (new items, enemies, mechanics)
- Backward compatible additions
- Balance changes

### PATCH (_._.X)
- Bug fixes
- Bug fix releases
- Minor tweaks

## Version Location

- Defined in: [main.py](../main.py) `VERSION = "X.Y.Z"`
- Also in: [CHANGELOG.md](../CHANGELOG.md)
- Git tags follow format: `v0.1.0`

## Release Workflow

1. **Development:** Work on feature branch
2. **Update Version:** Bump version in main.py
3. **Update Changelog:** Add notes to CHANGELOG.md
4. **Commit:** With message "Release v0.1.0"
5. **Tag:** `git tag -a v0.1.0 -m "Release 0.1.0"`
6. **Push:** `git push origin main && git push origin v0.1.0`

## Current Status

- **Current Version:** 0.1.0
- **Release Type:** ALPHA
- **Status:** Early Development
