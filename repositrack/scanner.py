from pathlib import Path
import subprocess

DOC_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "ROADMAP.md",
    "ARCHITECTURE.md",
    "CONTRIBUTING.md"
]

def git_output(repo, args):
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""

def inspect_repo(path):

    repo = Path(path).expanduser().resolve()

    info = {}

    info["name"] = repo.name
    info["path"] = str(repo)
    info["is_git"] = (repo / ".git").exists()

    info["branch"] = ""
    info["latest_commit"] = ""
    info["dirty"] = False
    info["tags"] = ""

    if info["is_git"]:
        info["branch"] = git_output(repo, ["branch", "--show-current"])
        info["latest_commit"] = git_output(repo, ["log", "-1", "--pretty=%h %s"])
        info["dirty"] = bool(git_output(repo, ["status", "--short"]))
        info["tags"] = git_output(repo, ["tag"])

    docs = {}

    for doc in DOC_FILES:
        docs[doc] = (repo / doc).exists()

    info["docs"] = docs

    info["screenshots"] = (
        (repo / "screenshots").exists()
        and any((repo / "screenshots").iterdir())
    )

    score = 100

    if not info["is_git"]:
        score -= 25

    if info["dirty"]:
        score -= 10

    if not info["screenshots"]:
        score -= 5

    if not info["tags"]:
        score -= 5

    for exists in docs.values():
        if not exists:
            score -= 5

    info["score"] = max(0, score)

    return info


def discover_workspace(path):

    root = Path(path).expanduser().resolve()

    repos = []

    for child in sorted(root.iterdir()):

        if not child.is_dir():
            continue

        if child.name.startswith("."):
            continue

        repos.append(inspect_repo(child))

    return repos
