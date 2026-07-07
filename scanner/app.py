import json
import os
from scanner import scan_dependencies


def parse_package_json(file_path):
    """
    Reads a package.json file and returns a combined dict of
    dependencies + devDependencies.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {file_path}")

    with open(file_path, "r") as f:
        data = json.load(f)

    dependencies = data.get("dependencies", {})
    dev_dependencies = data.get("devDependencies", {})

    all_deps = {**dependencies, **dev_dependencies}
    return all_deps


def run_full_scan(package_json_path):
    """
    Parses a package.json and scans every dependency for known CVEs.
    """
    deps = parse_package_json(package_json_path)
    print(f"Parsed {len(deps)} dependencies. Scanning each against OSV.dev...\n")

    findings = scan_dependencies(deps)

    if not findings:
        print("No known vulnerabilities found.")
    else:
        print(f"⚠️  Found vulnerabilities in {len(findings)} package(s):\n")
        for finding in findings:
            print(f"- {finding['package']}@{finding['version']}: {len(finding['vulnerabilities'])} vuln(s)")

    return findings


if __name__ == "__main__":
    run_full_scan("../web/package.json")