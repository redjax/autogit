from __future__ import annotations

from pathlib import Path
import typing as t

import git
from modules import git_ops

def _checkout(branch: git.Head = None) -> git.Head:
    assert branch, ValueError("Missing branch (a git.head object)")
    assert isinstance(branch, git.Head), TypeError(
        f"Expected head to be of type git.Head. Got type: ({type(branch)})"
    )

    try:
        branch.checkout()

        return branch
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception checkout out branch '{branch}'. Details: {exc}"
        )

        raise msg


def pull(repo: git.Repo = None):
    repo = git_ops.validate_git_repo(repo)

    origin = repo.remotes.origin
    branches = repo.branches

    for b in branches:
        head = repo.heads[f"{b}"]
        # try:
        #     head.checkout()
        # except Exception as exc:
        #     msg = Exception(
        #         f"Unhandled exception checkout out branch '{b}'. Details: {exc}"
        #     )

        _checkout(head)

        print(f"Fetching changes for branch '{b}'...")
        try:
            origin.fetch()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception checking out branch '{b}'. Details: {exc}"
            )

            raise msg

        print(f"Pulling changes for branch '{b}'...")
        try:
            origin.pull()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception pulling changes for branch '{b}'. Details: {exc}"
            )

            raise msg
