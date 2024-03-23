from __future__ import annotations

from pathlib import Path
import typing as t

from domain import GitController
from modules import git_ops

import git


def _checkout(branch: git.Head = None) -> None:
    branch = git_ops.validate_git_branch(branch)

    try:
        branch.checkout()

        # return branch
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception checkout out branch '{branch}'. Details: {exc}"
        )

        raise msg


def _fetch(origin: git.Remote = None, branch_name: str = None) -> None:
    origin = git_ops.validate_git_origin(origin=origin)

    print(f"Fetching branch '{branch_name}' changes...")
    try:
        origin.fetch()
    except Exception as exc:
        msg = Exception(f"Unhandled exception fetching branch. Details: {exc}")

        raise msg


def _pull(origin: git.Remote = None, branch_name: str = None):
    origin = git_ops.validate_git_origin(origin=origin)

    print(f"Pulling changes for branch '{branch_name}'...")
    try:
        origin.pull()
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception pulling changes for branch '{branch_name}'. Details: {exc}"
        )

        raise msg


def pull(repo: GitController = None, exclude_branches: list[str] = None):
    if exclude_branches:
        assert isinstance(exclude_branches, list), TypeError(
            f"exclude_branches must be of type list[str]. Got type: ({type(exclude_branches)})"
        )

    gitrepo = git_ops.validate_git_repo(repo._repo)

    origin = gitrepo.remotes.origin
    branches = gitrepo.branches

    for b in branches:
        if exclude_branches:
            if f"{b}" in exclude_branches:
                print(f"Skipping excluded branch '{b}'")
                continue

        head = gitrepo.heads[f"{b}"]

        _checkout(head)
        _fetch(origin=origin, branch_name=f"{b}")
        _pull(origin=origin, branch_name=f"{b}")
