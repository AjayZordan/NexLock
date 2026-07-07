from scanner import scan_dependencies
from severity import get_highest_severity
from github_pr import create_prs_for_findings

test_deps = {"lodash": "4.17.15"}
findings = scan_dependencies(test_deps)

for f in findings:
    f["severity"] = get_highest_severity(f["vulnerabilities"])

pr_links = create_prs_for_findings(findings)
print(f"\nCreated {len(pr_links)} PR(s):")
for link in pr_links:
    print(link)