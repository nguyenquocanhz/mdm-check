import Foundation

if CommandLine.arguments.contains("--cli") {
    exit(runCLI())
} else {
    MDMCheckApp.main()
}
