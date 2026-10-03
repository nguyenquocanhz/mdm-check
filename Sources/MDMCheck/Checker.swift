import Foundation
import IOKit
import MDMCheckCore

struct CommandOutput {
    let exitCode: Int32
    let text: String
}

func runCommand(_ path: String, _ arguments: [String]) -> CommandOutput {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: path)
    process.arguments = arguments
    let pipe = Pipe()
    process.standardOutput = pipe
    process.standardError = pipe
    do {
        try process.run()
    } catch {
        return CommandOutput(exitCode: -1, text: "Không chạy được \(path): \(error.localizedDescription)")
    }
    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    process.waitUntilExit()
    return CommandOutput(exitCode: process.terminationStatus, text: String(decoding: data, as: UTF8.self))
}

struct MachineInfo {
    let model: String
    let serial: String
    let osVersion: String

    static func read() -> MachineInfo {
        MachineInfo(
            model: sysctlString("hw.model") ?? "không đọc được",
            serial: platformString("IOPlatformSerialNumber") ?? "không đọc được",
            osVersion: ProcessInfo.processInfo.operatingSystemVersionString
        )
    }

    private static func platformString(_ key: String) -> String? {
        let service = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("IOPlatformExpertDevice"))
        guard service != 0 else { return nil }
        defer { IOObjectRelease(service) }
        return IORegistryEntryCreateCFProperty(service, key as CFString, kCFAllocatorDefault, 0)?.takeRetainedValue() as? String
    }

    private static func sysctlString(_ name: String) -> String? {
        var size = 0
        guard sysctlbyname(name, nil, &size, nil, 0) == 0, size > 0 else { return nil }
        var buffer = [CChar](repeating: 0, count: size)
        guard sysctlbyname(name, &buffer, &size, nil, 0) == 0 else { return nil }
        return String(cString: buffer)
    }
}

enum Checker {
    static let profiles = "/usr/bin/profiles"

    /// Bước 1: không cần quyền admin.
    static func checkStatus() -> (result: StatusResult, raw: String) {
        let output = runCommand(profiles, ["status", "-type", "enrollment"])
        return (Parser.parseStatus(output.text), output.text)
    }

    /// Bước 2: hỏi máy chủ Apple, cần quyền admin và mạng. Chưa phải root thì macOS hiện hộp nhập mật khẩu.
    static func checkAssignment() -> (result: AssignmentResult, raw: String) {
        let output: CommandOutput
        if geteuid() == 0 {
            output = runCommand(profiles, ["show", "-type", "enrollment"])
        } else {
            // `; true` để lệnh luôn thoát 0: máy không thuộc DEP thì profiles thoát khác 0 và osascript sẽ nuốt mất kết quả.
            let script = "do shell script \"\(profiles) show -type enrollment 2>&1; true\" with administrator privileges"
            output = runCommand("/usr/bin/osascript", ["-e", script])
        }
        return (Parser.parseAssignment(output.text), output.text)
    }
}

/// Chế độ dòng lệnh: `MDMCheck --cli`. Chạy bằng sudo thì kiểm tra luôn bước 2.
func runCLI() -> Int32 {
    let info = MachineInfo.read()
    print("Máy: \(info.model) · Serial: \(info.serial) · \(info.osVersion)")

    let status = Checker.checkStatus()
    print("--- profiles status -type enrollment ---\n\(status.raw)")

    var assignment: AssignmentResult?
    if geteuid() == 0 {
        let check = Checker.checkAssignment()
        assignment = check.result
        print("--- profiles show -type enrollment ---\n\(check.raw)")
    } else {
        print("(Chưa hỏi Apple về ADE: chạy lại bằng sudo để kiểm tra bước này.)")
    }

    let outcome = decide(status: status.result, assignment: assignment)
    print("MDM: \(outcome.verdict.rawValue)\n\(outcome.reason)")
    switch outcome.verdict {
    case .clean: return 0
    case .enrolled: return 1
    case .adeRisk: return 2
    case .unknown: return 3
    }
}
