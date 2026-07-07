import os
import base64
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

gh = Github(GITHUB_TOKEN)


def create_patch_pr(finding, package_json_path="web/package.json"):
    package = finding["package"]
    version = finding["version"]
    severity = finding.get("severity", "UNKNOWN")

    try:
        repo = gh.get_repo(GITHUB_REPO)
        base_branch = repo.get_branch("main")

        branch_name = f"nexlock-patch-{package}-{version}".replace(".", "-").replace("@", "-")

        try:
            repo.get_branch(branch_name)
            print(f"Branch {branch_name} already exists, skipping.")
            return None
        except GithubException:
            pass

        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_branch.commit.sha)

        # Add a real file change so GitHub allows a PR to be opened.
        # This creates/updates a security notes file documenting the finding.
        note_path = f"security-notes/{package}.md"
        note_content = (
            f"# Security Finding: {package}@{version}\n\n"
            f"**Severity:** {severity}\n"
            f"**Vulnerabilities found:** {len(finding['vulnerabilities'])}\n\n"
            f"This file was automatically created by Nexlock after detecting known "
            f"vulnerabilities in this dependency. Please review and update `{package}` "
            f"to a patched version, then remove or resolve this note.\n"
        )

        try:
            existing_file = repo.get_contents(note_path, ref=branch_name)
            repo.update_file(
                path=note_path,
                message=f"Nexlock: update security note for {package}",
                content=note_content,
                sha=existing_file.sha,
                branch=branch_name
            )
        except GithubException:
            repo.create_file(
                path=note_path,
                message=f"Nexlock: flag vulnerability in {package}@{version}",
                content=note_content,
                branch=branch_name
            )

        pr_title = f"[Nexlock] Update {package} (currently {version}) — {severity} severity"
        pr_body = (
            f"## Nexlock Security Scan Finding\n\n"
            f"**Package:** `{package}@{version}`\n"
            f"**Severity:** {severity}\n"
            f"**Vulnerabilities found:** {len(finding['vulnerabilities'])}\n\n"
            f"This PR was automatically opened by Nexlock after detecting known vulnerabilities "
            f"in this dependency. Please review and update to a patched version.\n\n"
            f"_This is an automated PR — a security note has been added under `security-notes/`. "
            f"Manual review and version bump recommended._"
        )

        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base="main"
        )

        print(f"Created PR: {pr.html_url}")
        return pr.html_url

    except GithubException as e:
        print(f"GitHub API error: {e}")
        return None


def create_prs_for_findings(findings, package_json_path="web/package.json"):
    pr_links = []
    for finding in findings:
        link = create_patch_pr(finding, package_json_path)
        if link:
            pr_links.append(link)
    return pr_links