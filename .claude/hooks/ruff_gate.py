"""Claude Code Stop hook: ruff must pass on the changed hand-written files before an agent finishes.

Runs once when the agent wants to stop, not after every edit. Exit code 2 blocks the stop and
hands the ruff output back to the agent. Generated code (digikey/v4) is not checked.
"""

from __future__ import annotations

import json
import subprocess
import sys


def git(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    return result.stdout.split() if result.returncode == 0 else []


def changed_python_files() -> list[str]:
    base = git("merge-base", "HEAD", "master") or ["HEAD"]
    files = set(git("diff", "--name-only", "--diff-filter=ACMR", base[0]))
    files |= set(git("ls-files", "--others", "--exclude-standard"))
    return sorted(f for f in files if f.endswith(".py") and not f.startswith("digikey/v4/"))


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    files = changed_python_files()
    if not files:
        return 0

    problems = []
    for command in (["ruff", "check"], ["ruff", "format", "--check"]):
        result = subprocess.run([*command, *files], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            problems.append(f"$ {' '.join(command)}\n{result.stdout}{result.stderr}")
    if not problems:
        return 0
    if event.get("stop_hook_active"):
        # Already blocked once in this turn; CI is the backstop, do not loop forever.
        print("ruff still reports problems, CI will fail:\n" + "\n".join(problems), file=sys.stderr)
        return 0
    print(
        "ruff gate failed. Run `uv run ruff check --fix` and `uv run ruff format` on these files, "
        "fix what remains, then finish:\n" + "\n".join(problems),
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
