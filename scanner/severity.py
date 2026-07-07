def extract_cvss_score(vuln):
    """
    Tries to extract a CVSS score (0-10) from an OSV.dev vulnerability entry.
    OSV data isn't always consistent, so we check a few possible locations.
    """
    severity_list = vuln.get("severity", [])
    for sev in severity_list:
        if sev.get("type") == "CVSS_V3":
            score_str = sev.get("score", "")
            # CVSS_V3 scores in OSV are often full vector strings, not plain numbers.
            # Try to pull a numeric score if present elsewhere.
            try:
                return float(score_str)
            except (ValueError, TypeError):
                pass

    # Fallback: check database_specific field (some ecosystems store severity here)
    db_specific = vuln.get("database_specific", {})
    if "severity" in db_specific:
        return db_specific["severity"]  # might be a string like "HIGH"

    return None


def score_to_label(score):
    """
    Converts a numeric CVSS score (0-10) into a severity label.
    """
    if score is None:
        return "UNKNOWN"

    if isinstance(score, str):
        # Already a label like "HIGH", "CRITICAL", etc.
        return score.upper()

    if score >= 9.0:
        return "CRITICAL"
    elif score >= 7.0:
        return "HIGH"
    elif score >= 4.0:
        return "MEDIUM"
    else:
        return "LOW"


def get_highest_severity(vulnerabilities):
    """
    Given a list of vulnerability entries for one package,
    returns the single highest severity label to represent that package.
    """
    severity_order = ["UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    highest = "UNKNOWN"

    for vuln in vulnerabilities:
        score = extract_cvss_score(vuln)
        label = score_to_label(score)

        if label in severity_order and severity_order.index(label) > severity_order.index(highest):
            highest = label

    return highest