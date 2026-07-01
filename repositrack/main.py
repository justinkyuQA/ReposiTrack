import sys

from . import __version__
from .scanner import inspect_repo, discover_workspace
from .reporter import print_dashboard, save_reports

HELP = f"""
ReposiTrack v{__version__}

Commands

version
repo <path>
dashboard <workspace>
report <workspace>
help
"""

def show_repo(repo):

    print()
    print("Repository")
    print("=" * 40)

    print("Name:", repo["name"])
    print("Score:", repo["score"])
    print("Branch:", repo["branch"])
    print("Dirty:", repo["dirty"])
    print("Latest:", repo["latest_commit"])

    print()
    print("Documentation")

    for doc, exists in repo["docs"].items():
        print(("OK      " if exists else "MISSING ") + doc)


def main():

    args = sys.argv[1:]

    if not args:
        print(HELP)
        return

    cmd = args[0]

    if cmd == "version":
        print(__version__)
        return

    target = args[1] if len(args) > 1 else "."

    if cmd == "repo":
        show_repo(inspect_repo(target))
        return

    if cmd == "dashboard":
        print_dashboard(discover_workspace(target))
        return

    if cmd == "report":
        repos = discover_workspace(target)
        print_dashboard(repos)
        md, js = save_reports(repos)
        print()
        print("Saved Reports")
        print(md)
        print(js)
        return

    print(HELP)

if __name__ == "__main__":
    main()
