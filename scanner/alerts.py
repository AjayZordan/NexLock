import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(finding):
    """
    Sends a formatted Slack message for a single vulnerability finding.
    finding = {package, version, vulnerabilities, severity}
    """
    if not SLACK_WEBHOOK_URL:
        print("No Slack webhook URL configured — skipping alert.")
        return

    package = finding["package"]
    version = finding["version"]
    severity = finding.get("severity", "UNKNOWN")
    vuln_count = len(finding["vulnerabilities"])

    severity_emoji = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢",
        "UNKNOWN": "⚪"
    }.get(severity, "⚪")

    message = {
        "text": (
            f"{severity_emoji} *[{severity}] Vulnerability Found*\n"
            f"*Package:* `{package}@{version}`\n"
            f"*Vulnerabilities found:* {vuln_count}\n"
            f"_Scanned by Nexlock_"
        )
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=10)
        response.raise_for_status()
        print(f"Slack alert sent for {package}@{version}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack alert: {e}")


def send_alerts_for_findings(findings):
    """Sends one Slack alert per vulnerable package found."""
    for finding in findings:
        send_slack_alert(finding)