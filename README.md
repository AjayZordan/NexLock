# 🔐 Nexlock

**Detect. Alert. Remediate.**

An AI-powered, CI/CD-integrated dependency vulnerability scanner that automatically detects known security vulnerabilities in a codebase, alerts teams in real time, and opens automated GitHub Pull Requests — closing the gap between vulnerability discovery and remediation.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini%20AI-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

🔗 **Live Dashboard:** [nex-lock-rho.vercel.app](https://nex-lock-rho.vercel.app)

---

## 📌 Problem

Dependencies are added to codebases constantly, and vulnerable versions slip in unnoticed until a breach happens. Most teams either don't scan for known CVEs at all, or only do it manually and infrequently — leaving a wide window between when a vulnerability is disclosed and when it's actually patched.

## 💡 Solution

Nexlock automates the entire vulnerability lifecycle. It hooks into a repository's CI/CD pipeline, scans every dependency against a live vulnerability database (OSV.dev), scores each finding by severity, alerts the team on Slack, opens a GitHub PR flagging the issue, and stores full scan history in a database that powers both a live web dashboard and executive-level Power BI reports.

---

## ✨ Key Features

- 🔍 **Live Vulnerability Intelligence** — real-time CVE lookups via the OSV.dev API for every dependency
- 📊 **Severity Scoring** — CVSS-based classification into Critical / High / Medium / Low
- ⚡ **SQLite Caching** — avoids redundant API lookups for previously scanned package versions
- 💬 **Slack Alerts** — instant, formatted notifications the moment a vulnerability is found
- 🔧 **Automated GitHub PRs** — auto-opens a Pull Request flagging the vulnerable dependency
- 🤖 **AI-Generated Explanations** — Gemini API integration for plain-English vulnerability summaries
- 🗄️ **Persistent Scan History** — every result stored in MongoDB Atlas
- 📈 **Live Dashboard** — Next.js dashboard with real-time severity breakdowns and scan feed
- 🔄 **CI/CD Automation** — GitHub Actions triggers a full scan on every push
- 🐳 **Dockerized Microservice** — the scanner runs as a portable, containerized service
- 📉 **Power BI Reporting** — executive-facing severity and trend visualizations

---

## 🏗️ Architecture

The system follows a two-service architecture connected by a shared data layer:

| Layer | Responsibility |
|---|---|
| 🎨 Presentation Layer | Live dashboard (Next.js, deployed on Vercel) |
| 🔄 Automation Layer | GitHub Actions CI/CD, GitHub PR automation |
| ⚙️ Service Layer | Dependency parsing, OSV.dev scanning, severity scoring, Gemini AI explanations |
| 🗄️ Data Layer | MongoDB Atlas (persistent history), SQLite (local cache) |
| 📊 Reporting Layer | Power BI (executive dashboards) |

### Architecture Diagram

```mermaid
flowchart TD
    A["👨‍💻 Developer Push"] --> B["⚙️ GitHub Actions CI/CD"]
    B --> C["🐍 Flask Scanner Microservice (Docker)"]
    C --> D["📦 Parse package.json"]
    D --> E["🔍 OSV.dev Vulnerability Check"]
    E --> F["⚡ SQLite Cache Layer"]
    E --> G["📊 Severity Scoring (CVSS)"]
    G --> H["🤖 Gemini AI Explanation"]
    G --> I["🗄️ MongoDB Atlas Storage"]
    G --> J["💬 Slack Alert"]
    G --> K["🔧 GitHub Auto-PR"]
    I --> L["📈 Next.js Dashboard (Vercel)"]
    I --> M["📉 Power BI Executive Report"]

    style A fill:#1f2937,stroke:#4ce0e6,color:#fff
    style B fill:#2088FF,stroke:#0a1a28,color:#fff
    style C fill:#3776AB,stroke:#0a1a28,color:#fff
    style E fill:#0a1a28,stroke:#4ce0e6,color:#fff
    style I fill:#47A248,stroke:#0a1a28,color:#fff
    style L fill:#000000,stroke:#4ce0e6,color:#fff
    style M fill:#F2C811,stroke:#0a1a28,color:#000
```

### Process Flow
Code Push → GitHub Actions → Flask Scanner
→ Parse package.json → Check OSV.dev → Cache in SQLite
→ Score Severity → Save to MongoDB
→ Slack Alert + GitHub Auto-PR
→ Next.js Dashboard (live view) → Power BI (executive report)

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Frontend | Next.js, React, Tailwind CSS |
| Hosting | Vercel |
| Backend | Python, Flask |
| Vulnerability Data | OSV.dev API |
| Caching | SQLite |
| Database | MongoDB Atlas |
| Alerts | Slack Incoming Webhooks |
| AI | Google Gemini API |
| Git Automation | GitHub REST API (PyGithub) |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Reporting | Power BI |

---

## 🚀 Getting Started

### Prerequisites
Python 3.11+, Node.js 20+, Docker, MongoDB Atlas account

### Installation

**Scanner:**
```bash
git clone https://github.com/AjayZordan/NexLock.git
cd NexLock/scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

**Dashboard:**
```bash
cd ../web
npm install
npm run dev
```

---

## 📁 Project Structure
nexlock/
├── web/                → Next.js dashboard (deployed on Vercel)
├── scanner/             → Python/Flask scanning microservice (Dockerized)
├── .github/workflows/    → GitHub Actions CI/CD pipeline
└── README.md
---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free to use, modify, and distribute with attribution.

---

## 👤 Author

**R. Ajay Kumar**
[GitHub](https://github.com/AjayZordan) · [LinkedIn](https://linkedin.com/in/ajaykumar-secdev)
