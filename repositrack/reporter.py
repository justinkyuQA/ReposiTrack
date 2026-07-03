import json
from pathlib import Path


# ---------------------------
# Terminal Dashboard
# ---------------------------

def print_dashboard(repos):
    print()
    print("ReposiTrack Dashboard")
    print("=" * 80)

    header = f"{'Score':<6} {'Name':<20} {'Branch':<12} {'Dirty':<6} {'Docs':<6}"
    print(header)
    print("-" * 80)

    for repo in sorted(repos, key=lambda r: r["score"], reverse=True):
        docs_ok = sum(1 for v in repo["docs"].values() if v)
        docs_total = len(repo["docs"])

        print(
            f"{repo['score']:<6} "
            f"{repo['name']:<20} "
            f"{repo['branch'][:12]:<12} "
            f"{str(repo['dirty']):<6} "
            f"{docs_ok}/{docs_total:<6}"
        )

    print("-" * 80)
    print(f"Repositories : {len(repos)}")

    if repos:
        avg = sum(r["score"] for r in repos) / len(repos)
        print(f"Average Score: {round(avg, 1)}")

    print()


# ---------------------------
# Markdown Report
# ---------------------------

def markdown_report(repos):
    lines = []

    lines.append("# ReposiTrack Report")
    lines.append("")

    lines.append("| Score | Name | Branch | Dirty | Docs |")
    lines.append("|------:|------|--------|-------|------|")

    for repo in sorted(repos, key=lambda r: r["score"], reverse=True):
        docs_ok = sum(1 for v in repo["docs"].values() if v)
        docs_total = len(repo["docs"])

        lines.append(
            f"| {repo['score']} | "
            f"{repo['name']} | "
            f"{repo['branch']} | "
            f"{repo['dirty']} | "
            f"{docs_ok}/{docs_total} |"
        )

    return "\n".join(lines)


# ---------------------------
# JSON + Markdown Save
# ---------------------------

def save_reports(repos):
    out = Path("reports")
    out.mkdir(exist_ok=True)

    md_path = out / "repositrack_report.md"
    json_path = out / "repositrack_report.json"

    md_path.write_text(markdown_report(repos))
    json_path.write_text(json.dumps(repos, indent=2))

    return md_path, json_path
