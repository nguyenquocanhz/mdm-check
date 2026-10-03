import AppKit
import MDMCheckCore
import SwiftUI

@MainActor
final class CheckModel: ObservableObject {
    @Published var info = MachineInfo.read()
    @Published var status: StatusResult?
    @Published var assignment: AssignmentResult?
    @Published var statusRaw = ""
    @Published var assignmentRaw = ""
    @Published var isBusy = false

    var outcome: (verdict: Verdict, reason: String) { decide(status: status, assignment: assignment) }

    func runStatus() {
        isBusy = true
        Task {
            let check = await Task.detached { Checker.checkStatus() }.value
            status = check.result
            statusRaw = check.raw
            isBusy = false
        }
    }

    func runAssignment() {
        isBusy = true
        Task {
            let check = await Task.detached { Checker.checkAssignment() }.value
            assignment = check.result
            assignmentRaw = check.raw
            isBusy = false
        }
    }

    var report: String {
        """
        MDM: \(outcome.verdict.rawValue)
        \(outcome.reason)
        Máy: \(info.model) · Serial: \(info.serial) · \(info.osVersion)
        --- profiles status -type enrollment ---
        \(statusRaw.isEmpty ? "(chưa chạy)" : statusRaw)
        --- profiles show -type enrollment ---
        \(assignmentRaw.isEmpty ? "(chưa chạy)" : assignmentRaw)
        """
    }
}

struct ContentView: View {
    @StateObject private var model = CheckModel()

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            verdictBlock
            Divider()
            machineBlock
            Divider()
            checksBlock
            Spacer(minLength: 0)
            HStack {
                Button("Kiểm tra lại") { model.runStatus() }
                Button("Hỏi Apple về ADE (cần mật khẩu admin)") { model.runAssignment() }
                    .keyboardShortcut(.defaultAction)
                Spacer()
                if model.isBusy { ProgressView().controlSize(.small) }
                Button("Chép báo cáo") {
                    NSPasteboard.general.clearContents()
                    NSPasteboard.general.setString(model.report, forType: .string)
                }
            }
            .disabled(model.isBusy)
        }
        .padding(20)
        .frame(minWidth: 620, minHeight: 520)
        .onAppear { model.runStatus() }
    }

    private var verdictBlock: some View {
        let outcome = model.outcome
        return VStack(alignment: .leading, spacing: 6) {
            Text("MDM: \(outcome.verdict.rawValue)")
                .font(.system(size: 30, weight: .bold))
                .foregroundColor(color(for: outcome.verdict))
            Text(outcome.reason)
                .fixedSize(horizontal: false, vertical: true)
        }
    }

    private var machineBlock: some View {
        VStack(alignment: .leading, spacing: 4) {
            row("Máy", model.info.model)
            row("Số serial", model.info.serial)
            row("macOS", model.info.osVersion)
        }
    }

    private var checksBlock: some View {
        VStack(alignment: .leading, spacing: 8) {
            row("Đang cài MDM", text(for: model.status?.mdmEnrolled))
            row("Đăng ký qua ADE/DEP", text(for: model.status?.enrolledViaDEP))
            row("Apple gán serial vào tổ chức", assignmentText)
            DisclosureGroup("Kết quả gốc của lệnh") {
                ScrollView {
                    Text(model.report)
                        .font(.system(.caption, design: .monospaced))
                        .textSelection(.enabled)
                        .frame(maxWidth: .infinity, alignment: .leading)
                }
                .frame(maxHeight: 160)
            }
        }
    }

    private var assignmentText: String {
        switch model.assignment {
        case .assigned(let organization)?: return "Có" + (organization.map { " · \($0)" } ?? "")
        case .notAssigned?: return "Không"
        case .undetermined(let reason)?: return "Chưa xác định · \(reason)"
        case nil: return "Chưa kiểm tra"
        }
    }

    private func row(_ label: String, _ value: String) -> some View {
        HStack(alignment: .firstTextBaseline) {
            Text(label).foregroundColor(.secondary).frame(width: 220, alignment: .leading)
            Text(value).textSelection(.enabled)
        }
    }

    private func text(for flag: Bool?) -> String {
        switch flag {
        case true?: return "Có"
        case false?: return "Không"
        case nil: return "Chưa đọc được"
        }
    }

    private func color(for verdict: Verdict) -> Color {
        switch verdict {
        case .clean: return .green
        case .enrolled: return .orange
        case .adeRisk: return .red
        case .unknown: return .secondary
        }
    }
}

struct MDMCheckApp: App {
    var body: some Scene {
        WindowGroup("Kiểm tra MDM") {
            ContentView()
        }
    }
}
