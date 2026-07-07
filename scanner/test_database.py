from scanner import scan_dependencies
from severity import get_highest_severity
from database import save_scan_result, get_recent_scans

test_deps = {"express": "4.17.1", "lodash": "4.17.15"}
findings = scan_dependencies(test_deps)

for f in findings:
    f["severity"] = get_highest_severity(f["vulnerabilities"])

save_scan_result(findings, source="test")

print("\nRecent scans in MongoDB:")
for scan in get_recent_scans(5):
    print(f"- {scan['timestamp']}: {scan['total_vulnerabilities_found']} vulnerabilities found")