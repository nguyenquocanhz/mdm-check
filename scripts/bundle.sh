#!/usr/bin/env bash
# Gói file chạy thành MDMCheck.app, ký ad-hoc, rồi nén zip. Chạy trên macOS.
set -euo pipefail

BIN="${1:-.build/apple/Products/Release/MDMCheck}"
APP="dist/MDMCheck.app"

rm -rf dist
mkdir -p "$APP/Contents/MacOS"
cp "$BIN" "$APP/Contents/MacOS/MDMCheck"
chmod +x "$APP/Contents/MacOS/MDMCheck"
cp packaging/Info.plist "$APP/Contents/Info.plist"

# Ký ad-hoc: bắt buộc để chạy được trên Mac chip Apple, nhưng không thay được chứng chỉ Developer ID.
codesign --force --sign - "$APP"
codesign --verify --verbose "$APP"

ditto -c -k --keepParent "$APP" dist/MDMCheck-macos-universal.zip
ls -lh dist
