from scanner import scan_dependencies
from severity import get_highest_severity
from explainer import explain_vulnerability

test_deps = {"lodash": "4.17.15"}
findings = scan_dependencies(test_deps)

for f in findings:
    f["severity"] = get_highest_severity(f["vulnerabilities"])
    explanation = explain_vulnerability(f)
    print(f"\n[{f['severity']}] {f['package']}@{f['version']}")
    print(f"Explanation: {explanation}")