MDMCheck checks a used Mac for MDM and ADE/DEP enrollment before you buy it.

## What it does

- Reports one verdict: `CLEAN`, `ENROLLED`, `ADE RISK`, or undetermined, with a plain explanation.
- Check 1 (instant, no password): is an MDM profile installed?
- Check 2 (admin password + internet): does Apple have this serial number assigned to an organization (ADE/DEP)? Shows the organization name when Apple returns it.
- Shows model, serial number and macOS version; copies a full report to the clipboard.
- Command-line mode: `sudo /Applications/MDMCheck.app/Contents/MacOS/MDMCheck --cli` (exit codes 0 clean, 1 enrolled, 2 ADE risk, 3 undetermined).

## Install

1. Download `MDMCheck.dmg` below, open it, drag MDMCheck onto Applications.
2. The app is not notarized, so macOS blocks the first launch: System Settings → Privacy & Security → **Open Anyway**.

Universal build for Apple silicon and Intel, macOS 12 or later.

## Known limits

- Built and smoke-tested on GitHub's macOS runners only. Not yet tried on a Mac that is actually enrolled in ADE.
- Mac only. It detects management; it does not remove or bypass it.
