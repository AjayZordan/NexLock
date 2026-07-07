import csv
from database import scans_collection

def export_to_csv(filename="nexlock_report.csv"):
    scans = list(scans_collection.find().sort("timestamp", -1))

    rows = []
    for scan in scans:
        timestamp = scan.get("timestamp")
        source = scan.get("source", "unknown")
        findings = scan.get("findings", [])

        if not findings:
            rows.append({
                "scan_date": timestamp,
                "source": source,
                "package": "N/A",
                "version": "N/A",
                "severity": "CLEAN",
                "vuln_count": 0
            })
        else:
            for f in findings:
                rows.append({
                    "scan_date": timestamp,
                    "source": source,
                    "package": f.get("package"),
                    "version": f.get("version"),
                    "severity": f.get("severity", "UNKNOWN"),
                    "vuln_count": len(f.get("vulnerabilities", []))
                })

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "scan_date", "source", "package", "version", "severity", "vuln_count"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} rows to {filename}")


if __name__ == "__main__":
    export_to_csv()