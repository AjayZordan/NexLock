import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["nexlock"]
scans_collection = db["scans"]


def save_scan_result(findings, source="manual"):
    """
    Saves a full scan result to MongoDB.
    findings: list of {package, version, vulnerabilities, severity}
    """
    document = {
        "timestamp": datetime.now(timezone.utc),
        "source": source,
        "total_vulnerabilities_found": len(findings),
        "findings": findings
    }
    result = scans_collection.insert_one(document)
    print(f"Saved scan result to MongoDB with id: {result.inserted_id}")
    return result.inserted_id


def get_recent_scans(limit=10):
    """Fetches the most recent scan results."""
    return list(scans_collection.find().sort("timestamp", -1).limit(limit))