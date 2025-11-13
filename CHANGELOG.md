# Changelog

All notable changes to this project will be documented in this file, starting with version 0.3.0.

## [0.3.0] - 2025-10-31

### Added

- New Models, Schemas, and Services for upcoming changes.

### Changed

- Reworked user onboarding flow inspired by Instagram.
- [Figma Design](https://www.figma.com/design/E8XTlerY7KqXDNfFLhXNOE/ig-from-mobbin?node-id=0-1&t=BumhPaaBpEHiWObK-1)
- Registration: kept only the email flow (removed mobile option).

### Fixed

- (Add your fixes here)

---

Perfect. Do this:

1. Combine your 3 commits into 1:

```bash
git rebase -i HEAD~3
```

In the editor:

- Keep the first as `pick`
- Change the other two to `squash` (or `s`)
- Save and edit the commit message

2. Rebase on top of main:

```bash
git fetch origin
git rebase origin/main
```

3. (Optional) Force push if branch already pushed:

```bash
git push -f
```

You’ll now have one clean commit on top of main.
Wanna squash with a specific commit message, or keep the first one’s?
