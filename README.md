# MDMCheck — check a used Mac for MDM and ADE/DEP enrollment before you buy

MDMCheck is a small free macOS app (and command-line tool) that tells you whether a Mac is managed by an organization. Run it on a second-hand MacBook, iMac or Mac mini before paying, and it prints one verdict:

| Verdict | Meaning |
|---|---|
| `MDM: CLEAN` | No MDM profile, and Apple confirms the serial number is not assigned to any organization. |
| `MDM: ENROLLED` | A remote-management (MDM) profile is installed right now. |
| `MDM: ADE RISK` | The serial number is assigned to an organization in Apple Business Manager / Apple School Manager (Automated Device Enrollment, formerly DEP). The Mac will re-enroll itself after every erase; only that organization can release it. |
| `MDM: CHƯA XÁC ĐỊNH` (undetermined) | A check could not finish (no network, no admin password). MDMCheck never reports CLEAN on incomplete data. |

**Status: early version.** It builds and its unit tests pass on GitHub's macOS runners, but it has not yet been tried on a Mac that is actually enrolled in ADE. Treat the result as a strong hint, and see [Limits](#limits).

## Features

- **One-word verdict** with a plain explanation: `CLEAN`, `ENROLLED`, `ADE RISK`, or undetermined.
- **Two checks in one window:** the installed MDM profile (instant, no password) and the ADE/DEP assignment that Apple holds for the serial number (admin password + internet).
- **Shows which organization** the Mac is assigned to, when Apple returns its name.
- **Machine details** next to the result: model identifier, serial number, macOS version.
- **Copy report** button: verdict plus the raw output of both commands, ready to paste to the seller or to a chat.
- **Command-line mode** (`--cli`) with exit codes, for scripting or for running over SSH.
- **Universal build:** one app for Apple silicon and Intel, macOS 12 or later, about 120 KB.
- **No network calls of its own:** only macOS's own request to Apple. No account, no telemetry.

## How it works

MDMCheck runs the two commands Apple ships with macOS and reads their output for you:

1. `profiles status -type enrollment` — is an MDM profile installed, and did it come through DEP? No admin rights needed.
2. `sudo profiles show -type enrollment` — asks Apple's servers whether this serial number is assigned to an organization. Needs an admin password and an internet connection.

Nothing is sent anywhere except the request macOS itself makes to Apple in step 2. There is no account, no tracking and no serial-number lookup service.

## Install

1. Download `MDMCheck.dmg` from the [latest release](../../releases/latest).
2. Open the DMG and drag **MDMCheck** onto **Applications** (or run it straight from the DMG on a Mac you are only inspecting).
3. Open MDMCheck. It is not notarized by Apple, so macOS blocks it the first time: open **System Settings → Privacy & Security**, scroll down and click **Open Anyway**. On macOS 12–14 you can instead right-click the app and choose **Open**.
4. The first check runs by itself. Click **Hỏi Apple về ADE** ("Ask Apple about ADE") and enter the admin password to run the second one.

A plain `MDMCheck-macos-universal.zip` is attached to each release too. If macOS still refuses to open the app, run `xattr -dr com.apple.quarantine /Applications/MDMCheck.app` in Terminal.

Command line, one shot:

```bash
sudo /Applications/MDMCheck.app/Contents/MacOS/MDMCheck --cli
```

Exit codes: `0` clean, `1` enrolled, `2` ADE risk, `3` undetermined.

## Build from source

```bash
swift test
swift build -c release --arch arm64 --arch x86_64
bash scripts/bundle.sh
```

The result is `dist/MDMCheck.app` and `dist/MDMCheck.dmg`. Every push is also built by [GitHub Actions](.github/workflows/build.yml).

## Limits

- **Mac only.** iPhone and iPad apps are not allowed to read MDM or ADE state. For those, check *Settings → General → VPN & Device Management*, and ask the seller to erase and re-activate the device in front of you: an ADE-assigned device shows a "Remote Management" screen during setup.
- The ADE check needs internet access. Offline, the verdict is "undetermined", not "clean".
- MDMCheck only detects management. It does not remove or bypass MDM, and it never will.

## Tiếng Việt

MDMCheck là app macOS miễn phí để kiểm tra máy Mac cũ có bị dính MDM hoặc ADE/DEP (máy công ty, máy trường học) trước khi mua. Mở app, bấm "Hỏi Apple về ADE", nhập mật khẩu admin, app sẽ báo một trong bốn kết luận ở bảng trên. `ADE RISK` nghĩa là số serial đang thuộc một tổ chức: xoá máy cài lại thì máy tự đăng ký lại MDM, chỉ tổ chức đó gỡ được, không nên mua.

Tính năng: một kết luận rõ ràng kèm giải thích; hiện tên tổ chức đang giữ máy nếu Apple trả về; hiện model, số serial, phiên bản macOS; nút chép báo cáo để gửi cho người bán; chế độ dòng lệnh `--cli`; chạy được trên cả Mac chip Apple và Intel.

Cài đặt: tải `MDMCheck.dmg` ở mục Releases, mở ra, kéo MDMCheck vào Applications. Lần đầu macOS sẽ chặn vì app chưa được Apple chứng nhận: vào System Settings → Privacy & Security, bấm **Open Anyway**.

App chỉ phát hiện, không gỡ và không bẻ khoá MDM. Đây là bản đầu, chưa được thử trên máy thật đang dính ADE.

## License

[MIT](LICENSE)
