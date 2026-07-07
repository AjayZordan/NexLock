from scanner import scan_dependencies
from severity import get_highest_severity
from alerts import send_alerts_for_findings

test_deps = {"express": "4.17.1", "lodash": "4.17.15"}
findings = scan_dependencies(test_deps)

for f in findings:
    f["severity"] = get_highest_severity(f["vulnerabilities"])

send_alerts_for_findings(findings)