import json
from pathlib import Path

def print_dashboard(repos):

    print()
    print("ReposiTrack Dashboard")
    print("=" * 60)

    print(f"{'Score':<8}{'Repository'}")
    print("-" * 60)

    for repo in sorted(repos, key=lambda r: r["score"], reverse=True):
        print(f"{repo['score']:<8}{repo['name']}")

    print("-" * 60)
    print("Repositories:", len(repos))

    if repos:
        average = sum(r["score"] for r in repos) / len(repos)
        print("Average Score:", round(average, 1))


def markdown_report(repos):

    lines = []

    lines.append("# ReposiTrack Report")
    lines.append("")

    lines.append("| Score | Repository |")
    lines.append("|------:|------------|")

    for repo in sorted(repos, key=lambda r: r["score"], reverse=True):
        lines.append(f"| {repo['score']} | {repo['name']} |")

    return "\n".join(lines)


def save_reports(repos):

    out = Path("reports")
    out.mkdir(exist_ok=True)

    md = out / "repositrack_report.md"
    js = out / "repositrack_report.json"

    md.write_text(markdown_report(repos))
    js.write_text(json.dumps(repos, indent=2))

    return md, js
