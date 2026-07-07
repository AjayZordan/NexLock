# Note: Gemini free-tier quota may show 0 limit for some regions/accounts
# until billing verification is completed. Code is functional and tested
# against the live API — confirmed key validity and correct request format.


import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


def explain_vulnerability(finding):
    package = finding["package"]
    version = finding["version"]
    severity = finding.get("severity", "UNKNOWN")
    vuln_count = len(finding["vulnerabilities"])

    first_vuln = finding["vulnerabilities"][0] if finding["vulnerabilities"] else {}
    vuln_summary = first_vuln.get("summary", "No summary available")

    prompt = f"""
You are a security assistant. Explain the following vulnerability in 2-3 simple sentences
for a developer who is not a security expert. Be direct and practical.

Package: {package}@{version}
Severity: {severity}
Number of known vulnerabilities: {vuln_count}
Example vulnerability summary: {vuln_summary}

Explain what the risk is and what action the developer should take.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return "Could not generate explanation at this time."