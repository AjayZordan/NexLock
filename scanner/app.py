import json
import os
from flask import Flask, request, jsonify
from scanner import scan_dependencies
from severity import get_highest_severity
from alerts import send_alerts_for_findings
from database import save_scan_result

app = Flask(__name__)


def parse_package_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {file_path}")

    with open(file_path, "r") as f:
        data = json.load(f)

    dependencies = data.get("dependencies", {})
    dev_dependencies = data.get("devDependencies", {})

    all_deps = {**dependencies, **dev_dependencies}
    return all_deps


def run_full_scan(package_json_path, source="manual"):
    deps = parse_package_json(package_json_path)
    print(f"Parsed {len(deps)} dependencies. Scanning each against OSV.dev...")

    findings = scan_dependencies(deps)

    for finding in findings:
        finding["severity"] = get_highest_severity(finding["vulnerabilities"])

    save_scan_result(findings, source=source)

    if findings:
        print(f"Found vulnerabilities in {len(findings)} package(s). Sending Slack alerts...")
        send_alerts_for_findings(findings)
    else:
        print("No known vulnerabilities found.")

    return findings


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Nexlock scanner is running"})


@app.route("/webhook/github", methods=["POST"])
def github_webhook():
    payload = request.json
    print("Received GitHub webhook event")

    try:
        findings = run_full_scan("../web/package.json", source="github_webhook")
        return jsonify({
            "status": "scan complete",
            "vulnerabilities_found": len(findings)
        }), 200
    except Exception as e:
        print(f"Error during scan: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/scan", methods=["GET"])
def manual_scan():
    try:
        findings = run_full_scan("../web/package.json", source="manual")
        return jsonify({
            "status": "scan complete",
            "vulnerabilities_found": len(findings)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)