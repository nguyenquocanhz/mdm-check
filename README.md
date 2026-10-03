# MDMCheck — check a used Mac for MDM and ADE/DEP enrollment before you buy

MDMCheck is a small free macOS app (and command-line tool) that tells you whether a Mac is managed by an organization. Run it on a second-hand MacBook, iMac or Mac mini before paying, and it prints one verdict:

| Verdict | Meaning |
|---|---|
| `MDM: CLEAN` | No MDM profile, and Apple confirms the serial number is not assigned to any organization. |
| `MDM: ENROLLED` | A remote-management (MDM) profile is installed right now. |
| `MDM: ADE RISK` | The serial number is assigned to an organization in Apple Business Manager / Apple School Manager (Automated Device Enrollment, formerly DEP). The Mac will re-enroll itself after every erase; only that organization can release it. |
| `MDM: CHƯA XÁC ĐỊNH` (undetermined) | A check could not finish (no network, no admin password). MDMCheck never reports CLEAN on incomplete data. |

**Status: early version.** It builds and its unit tests pass on GitHub's macOS runners, but it has not yet been tried on a Mac that is actually enrolled in ADE. Treat the result as a strong hint, and see [Limits](#limits).

## How it works

MDMCheck runs the two commands Apple ships with macOS and reads their output for you:

1. `profiles status -type enrollment` — is an MDM profile installed, and did it come through DEP? No admin rights needed.
2. `sudo profiles show -type enrollment` — asks Apple's servers whether this serial number is assigned to an organization. Needs an admin password and an internet connection.

Nothing is sent anywhere except the request macOS itself makes to Apple in step 2. There is no account, no tracking and no serial-number lookup service.

## Download and run

1. Download `MDMCheck-macos-universal.zip` from the [latest release](../../releases/latest) (Apple silicon and Intel, macOS 12 or later).
2. Unzip and open `MDMCheck.app`. The app is not notarized, so macOS blocks it the first time: open **System Settings → Privacy & Security** and click **Open Anyway**, or run `xattr -dr com.apple.quarantine MDMCheck.app`.
3. Click **Hỏi Apple về ADE** ("Ask Apple about ADE") and enter the admin password to run the second check.

Command line, one shot:

```bash
sudo MDMCheck.app/Contents/MacOS/MDMCheck --cli
```

Exit codes: `0` clean, `1` enrolled, `2` ADE risk, `3` undetermined.

## Build from source

```bash
swift test
swift build -c release --arch arm64 --arch x86_64
bash scripts/bundle.sh
```

The result is `dist/MDMCheck.app`. Every push is also built by [GitHub Actions](.github/workflows/build.yml).

## Limits

- **Mac only.** iPhone and iPad apps are not allowed to read MDM or ADE state. For those, check *Settings → General → VPN & Device Management*, and ask the seller to erase and re-activate the device in front of you: an ADE-assigned device shows a "Remote Management" screen during setup.
- The ADE check needs internet access. Offline, the verdict is "undetermined", not "clean".
- MDMCheck only detects management. It does not remove or bypass MDM, and it never will.

## Tiếng Việt

MDMCheck là app macOS miễn phí để kiểm tra máy Mac cũ có bị dính MDM hoặc ADE/DEP (máy công ty, máy trường học) trước khi mua. Mở app, bấm "Hỏi Apple về ADE", nhập mật khẩu admin, app sẽ báo một trong bốn kết luận ở bảng trên. `ADE RISK` nghĩa là số serial đang thuộc một tổ chức: xoá máy cài lại thì máy tự đăng ký lại MDM, chỉ tổ chức đó gỡ được, không nên mua.

App chỉ phát hiện, không gỡ và không bẻ khoá MDM. Đây là bản đầu, chưa được thử trên máy thật đang dính ADE.

## License

[MIT](LICENSE)
