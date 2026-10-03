// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MDMCheck",
    platforms: [.macOS(.v12)],
    targets: [
        // Phần đọc kết quả lệnh `profiles` và ra kết luận: không phụ thuộc giao diện, có test.
        .target(name: "MDMCheckCore"),
        .executableTarget(name: "MDMCheck", dependencies: ["MDMCheckCore"]),
        .testTarget(name: "MDMCheckCoreTests", dependencies: ["MDMCheckCore"]),
    ]
)
