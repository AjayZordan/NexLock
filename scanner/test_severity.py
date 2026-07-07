from scanner import scan_dependencies
from severity import get_highest_severity

test_deps = {"express": "4.17.1", "lodash": "4.17.15"}
findings = scan_dependencies(test_deps)

for f in findings:
    sev = get_highest_severity(f["vulnerabilities"])
    print(f"[{sev}] {f['package']}@{f['version']}")