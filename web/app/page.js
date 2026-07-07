"use client";

import { useEffect, useState } from "react";

const severityColors = {
  CRITICAL: "var(--critical)",
  HIGH: "var(--high)",
  MEDIUM: "var(--medium)",
  LOW: "var(--low)",
  UNKNOWN: "var(--text-muted)",
};

function formatTime(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function Home() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/scans")
      .then((res) => res.json())
      .then((data) => {
        setScans(data.scans || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const totalVulns = scans.reduce((sum, s) => sum + s.totalVulnerabilitiesFound, 0);
  const totalScans = scans.length;
  const uniquePackages = new Set(
    scans.flatMap((s) => s.findings.map((f) => f.package))
  ).size;
  const lastScan = scans[0];

  const severityCounts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
  scans.forEach((s) =>
    s.findings.forEach((f) => {
      if (severityCounts[f.severity] !== undefined) {
        severityCounts[f.severity]++;
      }
    })
  );
  const maxSeverityCount = Math.max(...Object.values(severityCounts), 1);

  return (
    <div className="page">
      <div className="topbar">
        <div className="logo">
          NEX<span>LOCK</span>
        </div>
        <div className="statusPill">
          <span className="statusDot" />
          MONITORING
        </div>
      </div>

      <div className="hero">
        <div className="radarSweep" />
        <div className="heroEyebrow">Total vulnerabilities detected</div>
        <div className={`heroNumber ${totalVulns === 0 ? "clean" : "hasIssues"}`}>
          {loading ? "—" : totalVulns}
        </div>
        <div className="heroLabel">
          across {totalScans} scan{totalScans !== 1 ? "s" : ""} · {uniquePackages} package
          {uniquePackages !== 1 ? "s" : ""} tracked
        </div>
      </div>

      <div className="statsRow">
        <div className="statCard">
          <div className="statValue">{totalScans}</div>
          <div className="statLabel">Total scans run</div>
        </div>
        <div className="statCard">
          <div className="statValue">{uniquePackages}</div>
          <div className="statLabel">Packages tracked</div>
        </div>
        <div className="statCard">
          <div className="statValue" style={{ color: "var(--critical)" }}>
            {severityCounts.CRITICAL + severityCounts.HIGH}
          </div>
          <div className="statLabel">Critical + High findings</div>
        </div>
        <div className="statCard">
          <div className="statValue" style={{ fontSize: "16px" }}>
            {lastScan ? formatTime(lastScan.timestamp) : "—"}
          </div>
          <div className="statLabel">Last scan</div>
        </div>
      </div>

      <div className="grid">
        <div className="panel">
          <div className="panelTitle">Severity Breakdown</div>
          {Object.entries(severityCounts).map(([label, count]) => (
            <div className="severityRow" key={label}>
              <div className="severityLabel">{label}</div>
              <div className="severityBarTrack">
                <div
                  className="severityBarFill"
                  style={{
                    width: `${(count / maxSeverityCount) * 100}%`,
                    background: severityColors[label],
                  }}
                />
              </div>
              <div className="severityCount">{count}</div>
            </div>
          ))}
        </div>

        <div className="panel">
          <div className="panelTitle">Scan History</div>
          {loading && <div className="emptyState">Loading scan history…</div>}
          {!loading && scans.length === 0 && (
            <div className="emptyState">No scans yet. Run a scan to see results here.</div>
          )}
          {!loading &&
            scans.map((scan) => (
              <div className="scanItem" key={scan.id}>
                <div className="scanItemTop">
                  <span className="scanTime">{formatTime(scan.timestamp)}</span>
                  <span className="scanSource">{scan.source}</span>
                </div>
                {scan.findings.length === 0 ? (
                  <span className="findingBadge" style={{ color: "var(--low)" }}>
                    ✓ Clean
                  </span>
                ) : (
                  scan.findings.map((f, i) => (
                    <span
                      className="findingBadge"
                      key={i}
                      style={{ color: severityColors[f.severity] }}
                    >
                      {f.package}@{f.version} · {f.severity}
                    </span>
                  ))
                )}
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}