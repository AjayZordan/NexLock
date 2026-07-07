import clientPromise from "../../../lib/mongodb";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db("nexlock");
    const scans = await db
      .collection("scans")
      .find({})
      .sort({ timestamp: -1 })
      .limit(50)
      .toArray();

    const serialized = scans.map((scan) => ({
      id: scan._id.toString(),
      timestamp: scan.timestamp,
      source: scan.source,
      totalVulnerabilitiesFound: scan.total_vulnerabilities_found,
      findings: (scan.findings || []).map((f) => ({
        package: f.package,
        version: f.version,
        severity: f.severity || "UNKNOWN",
        vulnCount: (f.vulnerabilities || []).length,
      })),
    }));

    return NextResponse.json({ scans: serialized });
  } catch (error) {
    console.error("Error fetching scans:", error);
    return NextResponse.json(
      { error: "Failed to fetch scan history" },
      { status: 500 }
    );
  }
}