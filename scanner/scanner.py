import requests

OSV_API_URL = "https://api.osv.dev/v1/query"


def check_package_vulnerability(package_name, version, ecosystem="npm"):
    """
    Checks a single package+version against the OSV.dev database.
    Returns a list of vulnerabilities found (empty list if none).
    """
    payload = {
        "package": {
            "name": package_name,
            "ecosystem": ecosystem
        },
        "version": version
    }

    try:
        response = requests.post(OSV_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("vulns", [])
    except requests.exceptions.RequestException as e:
        print(f"Error checking {package_name}@{version}: {e}")
        return []


def scan_dependencies(dependencies: dict, ecosystem="npm"):
    """
    dependencies: a dict like {"express": "4.17.1", "lodash": "4.17.15"}
    Returns a list of findings: [{package, version, vulnerabilities}]
    """
    results = []

    for package_name, version in dependencies.items():
        clean_version = version.replace("^", "").replace("~", "").strip()
        vulns = check_package_vulnerability(package_name, clean_version, ecosystem)

        if vulns:
            results.append({
                "package": package_name,
                "version": clean_version,
                "vulnerabilities": vulns
            })

    return results


# Quick test when running this file directly
if __name__ == "__main__":
    test_deps = {
        "express": "4.17.1",
        "lodash": "4.17.15"
    }
    findings = scan_dependencies(test_deps)
    print(f"Found vulnerabilities in {len(findings)} package(s)")
    for finding in findings:
        print(f"- {finding['package']}@{finding['version']}: {len(finding['vulnerabilities'])} vuln(s)")