import XCTest
@testable import MDMCheckCore

final class VerdictTests: XCTestCase {
    func testStatusPersonalMac() {
        let status = Parser.parseStatus("Enrolled via DEP: No\nMDM enrollment: No\n")
        XCTAssertEqual(status, StatusResult(enrolledViaDEP: false, mdmEnrolled: false, userApproved: false))
    }

    func testStatusEnrolledViaDEP() {
        let status = Parser.parseStatus("Enrolled via DEP: Yes\nMDM enrollment: Yes (User Approved)\nMDM server: https://mdm.example.com/mdm\n")
        XCTAssertEqual(status, StatusResult(enrolledViaDEP: true, mdmEnrolled: true, userApproved: true))
    }

    func testAssignmentNotDEP() {
        XCTAssertEqual(Parser.parseAssignment("Error fetching Device Enrollment configuration: Client is not DEP enabled."), .notAssigned)
        XCTAssertEqual(Parser.parseAssignment("Device Enrollment configuration:\n(null)\n"), .notAssigned)
    }

    func testAssignmentAssigned() {
        let output = """
        Device Enrollment configuration:
        {
            AllowPairing = 1;
            ConfigurationURL = "https://mdm.example.com/cloudenroll";
            IsMDMUnremovable = 1;
            OrganizationName = "Example Corp";
            OrganizationPhone = "(null)";
        }
        """
        XCTAssertEqual(Parser.parseAssignment(output), .assigned(organization: "Example Corp"))
    }

    func testAssignmentNetworkErrorIsUndetermined() {
        let result = Parser.parseAssignment("Error fetching Device Enrollment configuration: The Internet connection appears to be offline.")
        guard case .undetermined = result else { return XCTFail("phải là undetermined, nhận được \(result)") }
    }

    func testAssignmentCancelledIsUndetermined() {
        let result = Parser.parseAssignment("execution error: User canceled. (-128)")
        XCTAssertEqual(result, .undetermined(reason: "đã huỷ nhập mật khẩu admin"))
    }

    func testCleanNeedsBothChecks() {
        let clean = StatusResult(enrolledViaDEP: false, mdmEnrolled: false)
        XCTAssertEqual(decide(status: clean, assignment: .notAssigned).verdict, .clean)
        XCTAssertEqual(decide(status: clean, assignment: nil).verdict, .unknown)
        XCTAssertEqual(decide(status: clean, assignment: .undetermined(reason: "mất mạng")).verdict, .unknown)
        XCTAssertEqual(decide(status: nil, assignment: .notAssigned).verdict, .unknown)
    }

    func testAssignedAlwaysWins() {
        let clean = StatusResult(enrolledViaDEP: false, mdmEnrolled: false)
        XCTAssertEqual(decide(status: clean, assignment: .assigned(organization: nil)).verdict, .adeRisk)
        XCTAssertEqual(decide(status: StatusResult(enrolledViaDEP: true, mdmEnrolled: true), assignment: nil).verdict, .adeRisk)
    }

    func testEnrolledWithoutADE() {
        let enrolled = StatusResult(enrolledViaDEP: false, mdmEnrolled: true)
        XCTAssertEqual(decide(status: enrolled, assignment: .notAssigned).verdict, .enrolled)
        XCTAssertEqual(decide(status: enrolled, assignment: nil).verdict, .enrolled)
    }
}
