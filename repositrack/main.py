import sys

from . import __version__
from .scanner import inspect_repo, discover_workspace
from .reporter import print_dashboard, save_reports


HELP = f"""
ReposiTrack v{__version__}

Commands:
  version
  repo <path>
  dashboard <workspace>
  report <workspace>
  doctor <workspace>
  help
"""


def show_repo(repo):
    print()
    print("Repository")
    print("=" * 40)

    print(f"Name   : {repo['name']}")
    print(f"Score  : {repo['score']}")
    print(f"Branch : {repo['branch']}")
    print(f"Dirty  : {repo['dirty']}")
    print(f"Latest : {repo['latest_commit']}")

    print()
    print("Documentation")
    print("-" * 40)

    for doc, exists in repo["docs"].items():
        status = "OK" if exists else "MISSING"
        print(f"{status:<8} {doc}")

    print()


def doctor(workspace):
    repos = discover_workspace(workspace)

    print()
    print("ReposiTrack Doctor")
    print("=" * 60)

    ready = 0

    for repo in sorted(repos, key=lambda r: r["score"], reverse=True):
        if repo["score"] >= 90:
            status = "READY"
            ready += 1
        elif repo["score"] >= 75:
            status = "POLISH"
        else:
            status = "WORK"

        print(f"{status:<8} {repo['score']:>3}  {repo['name']}")

    print("-" * 60)
    print(f"Repositories : {len(repos)}")
    print(f"Release Ready: {ready}")
    print()


def main():
    args = sys.argv[1:]

    if not args:
        print(HELP)
        return

    cmd = args[0]

    if cmd == "version":
        print(__version__)
        return

    if cmd == "help":
        print(HELP)
        return

    target = args[1] if len(args) > 1 else "."

    if cmd == "repo":
        repo = inspect_repo(target)
        show_repo(repo)
        return

    if cmd == "dashboard":
        repos = discover_workspace(target)
        print_dashboard(repos)
        return

    if cmd == "report":
        repos = discover_workspace(target)
        print_dashboard(repos)

        md_path, json_path = save_reports(repos)

        print()
        print("Saved Reports")
        print(md_path)
        print(json_path)
        return

    if cmd == "doctor":
        doctor(target)
        return

    print(HELP)


if __name__ == "__main__":
    main()
