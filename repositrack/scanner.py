from pathlib import Path
import subprocess


REQUIRED_DOCS = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "ROADMAP.md",
    "ARCHITECTURE.md",
    "CONTRIBUTING.md",
]


def git_output(path, *args):
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), *args],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return ""


def inspect_repo(path):

    path = Path(path)

    docs = {}
    for doc in REQUIRED_DOCS:
        docs[doc] = (path / doc).exists()

    info = {
        "name": path.name,
        "branch": git_output(path, "branch", "--show-current") or "-",
        "dirty": bool(git_output(path, "status", "--porcelain")),
        "latest_commit": git_output(path, "log", "-1", "--pretty=%h %s"),
        "docs": docs,
        "tags": git_output(path, "tag").splitlines(),
    }

    score = 100

    if info["dirty"]:
        score -= 5

    if not info["latest_commit"]:
        score -= 10

    if not info["tags"]:
        score -= 5

    for exists in docs.values():
        if not exists:
            score -= 5

    info["score"] = max(0, score)

    return info


def discover_workspace(path):

    root = Path(path).expanduser().resolve()

    # If the supplied path is itself a Git repository,
    # inspect only that repository.
    if (root / ".git").exists():
        return [inspect_repo(root)]

    repos = []

    # Otherwise inspect immediate child repositories.
    for child in sorted(root.iterdir()):

        if not child.is_dir():
            continue

        if child.name.startswith("."):
            continue

        if not (child / ".git").exists():
            continue

        repos.append(inspect_repo(child))

    return repos
