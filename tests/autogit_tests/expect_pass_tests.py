from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import typing as t
from typing import Generator

from autogit.domain import GitRepository
from autogit.utils import git_utils
import git
import pytest

@pytest.mark.autogit
def test_pass_git_clone(git_tempfs: str, autogit_repo_path: Path, git_repo_url: str):
    repo: git.Repo = git_utils.clone_repo_to_path(
        repo_url=git_repo_url, local_path=autogit_repo_path
    )

    for p in Path(git_tempfs).rglob("**/*"):
        print(f"Path in '{git_tempfs}': {p}")


@pytest.mark.autogit
def test_pass_gitrepository(autogit_repo_path: Path, git_repo_url: str):
    repo: git.Repo = git_utils.clone_repo_to_path(
        repo_url=git_repo_url, local_path=autogit_repo_path
    )

    _repo: GitRepository = GitRepository(
        local_path=autogit_repo_path, repo_url=git_repo_url
    )
    assert _repo.exists, FileNotFoundError(
        f"Could not find repository at path '{autogit_repo_path}'"
    )

    print(f"Repository object: {_repo}")


@pytest.mark.autogit
def test_pass_autogit_pull(autogit_repo_path: Path, git_repo_url: str):
    repo: git.Repo = git_utils.clone_repo_to_path(
        repo_url=git_repo_url, local_path=autogit_repo_path
    )

    _repo: GitRepository = GitRepository(
        local_path=autogit_repo_path, repo_url=git_repo_url
    )
    assert _repo.exists, FileNotFoundError(
        f"Could not find repository at path '{autogit_repo_path}'"
    )

    print(f"Repository object: {_repo}")

    print(f"Attempting pull with GitRepository object")
    try:
        _repo.autopull()
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception running @GitRepository.autopull(). Details: {exc}"
        )

        raise msg
