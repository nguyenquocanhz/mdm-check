import Foundation

public enum Verdict: String, Equatable {
    case clean = "CLEAN"
    case enrolled = "ENROLLED"
    case adeRisk = "ADE RISK"
    case unknown = "CHƯA XÁC ĐỊNH"
}

/// Kết quả của `profiles status -type enrollment` (không cần quyền admin).
public struct StatusResult: Equatable {
    public var enrolledViaDEP: Bool?
    public var mdmEnrolled: Bool?
    public var userApproved: Bool

    public init(enrolledViaDEP: Bool? = nil, mdmEnrolled: Bool? = nil, userApproved: Bool = false) {
        self.enrolledViaDEP = enrolledViaDEP
        self.mdmEnrolled = mdmEnrolled
        self.userApproved = userApproved
    }
}

/// Kết quả của `profiles show -type enrollment` (cần quyền admin và mạng): Apple có gán serial này vào tổ chức nào không.
public enum AssignmentResult: Equatable {
    case assigned(organization: String?)
    case notAssigned
    case undetermined(reason: String)
}

public enum Parser {
    public static func parseStatus(_ output: String) -> StatusResult {
        var result = StatusResult()
        for line in output.split(whereSeparator: \.isNewline) {
            guard let colon = line.firstIndex(of: ":") else { continue }
            let key = line[..<colon].trimmingCharacters(in: .whitespaces).lowercased()
            let value = line[line.index(after: colon)...].trimmingCharacters(in: .whitespaces)
            let lowerValue = value.lowercased()
            let flag: Bool? = lowerValue.hasPrefix("yes") ? true : lowerValue.hasPrefix("no") ? false : nil

            if key == "enrolled via dep" {
                result.enrolledViaDEP = flag
            } else if key == "mdm enrollment" {
                result.mdmEnrolled = flag
                result.userApproved = lowerValue.contains("user approved")
            }
        }
        return result
    }

    public static func parseAssignment(_ output: String) -> AssignmentResult {
        let trimmed = output.trimmingCharacters(in: .whitespacesAndNewlines)
        let lower = trimmed.lowercased()
        if trimmed.isEmpty { return .undetermined(reason: "lệnh không trả về gì") }
        if lower.contains("user canceled") || lower.contains("(-128)") { return .undetermined(reason: "đã huỷ nhập mật khẩu admin") }
        if lower.contains("not dep enabled") { return .notAssigned }

        // Máy bị gán ADE trả về một từ điển cấu hình có các khoá này.
        let assignedKeys = ["configurationurl", "organizationname", "ismdmunremovable", "awaitdeviceconfigured", "ismandatory"]
        if assignedKeys.contains(where: { lower.contains($0) }) {
            return .assigned(organization: organizationName(in: trimmed))
        }

        if lower.contains("(null)") { return .notAssigned }
        if let errorLine = trimmed.split(whereSeparator: \.isNewline).first(where: { $0.lowercased().contains("error") }) {
            return .undetermined(reason: String(errorLine).trimmingCharacters(in: .whitespaces))
        }
        return .undetermined(reason: "không nhận ra kết quả của lệnh")
    }

    private static func organizationName(in output: String) -> String? {
        for line in output.split(whereSeparator: \.isNewline) where line.contains("OrganizationName") {
            guard let equals = line.firstIndex(of: "=") else { continue }
            let value = line[line.index(after: equals)...]
                .trimmingCharacters(in: CharacterSet(charactersIn: " \t;\""))
            if !value.isEmpty { return value }
        }
        return nil
    }
}

/// Chỉ báo CLEAN khi cả hai lệnh đều nói sạch. Báo sạch nhầm cho máy dính ADE là lỗi tệ nhất của tool này.
public func decide(status: StatusResult?, assignment: AssignmentResult?) -> (verdict: Verdict, reason: String) {
    if case .assigned(let organization)? = assignment {
        let owner = organization.map { " (\($0))" } ?? ""
        return (.adeRisk, "Apple đang gán serial này vào một tổ chức\(owner). Xoá máy cài lại thì máy tự đăng ký lại MDM.")
    }
    if status?.enrolledViaDEP == true {
        return (.adeRisk, "Máy đã đăng ký MDM qua ADE/DEP, tức serial đang thuộc một tổ chức.")
    }
    if status?.mdmEnrolled == true {
        let adeNote = assignment == .notAssigned ? " Serial không bị gán ADE." : " Chưa kiểm tra được serial có bị gán ADE không."
        return (.enrolled, "Máy đang cài hồ sơ quản lý từ xa (MDM)." + adeNote)
    }
    guard let status, status.mdmEnrolled == false, status.enrolledViaDEP == false else {
        return (.unknown, "Không đọc được trạng thái MDM từ lệnh profiles.")
    }
    switch assignment {
    case .notAssigned?:
        return (.clean, "Không có MDM và Apple xác nhận serial không bị gán vào tổ chức nào.")
    case .undetermined(let reason)?:
        return (.unknown, "Máy không cài MDM, nhưng chưa hỏi được Apple về ADE: \(reason).")
    default:
        return (.unknown, "Máy không cài MDM, nhưng chưa hỏi Apple về ADE. Bấm “Hỏi Apple” để kiểm tra.")
    }
}
