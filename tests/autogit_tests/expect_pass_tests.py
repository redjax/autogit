import typing as t
from typing import Generator
import pytest
import tempfile
from pathlib import Path
import shutil

import git

from autogit.domain import GitRepository


@pytest.mark.autogit
def test_pass_git_clone(git_tempfs: str, autogit_repo_path: Path, git_repo_url: str):
    print(
        f"Cloning git repository from '{git_repo_url}'. Output path: {autogit_repo_path}"
    )
    try:
        repo: git.Repo = git.Repo.clone_from(
            url=git_repo_url, to_path=autogit_repo_path
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception cloning git repo from url '{git_repo_url}' to tempfs '{git_tempfs}. Details: {exc}"
        )

        raise msg

    assert repo, ValueError("repo should not have been None")
    assert isinstance(repo, git.Repo), TypeError(
        f"Expected repo to be of type git.Repo. Got type: ({type(repo)})"
    )

    for p in Path(git_tempfs).rglob("**/*"):
        print(f"Path in '{git_tempfs}': {p}")


@pytest.mark.autogit
def test_pass_gitrepository(autogit_repo_path: Path, git_repo_url: str):
    print(
        f"Cloning git repository from '{git_repo_url}'. Output path: {autogit_repo_path}"
    )
    try:
        repo: git.Repo = git.Repo.clone_from(
            url=git_repo_url, to_path=autogit_repo_path
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception cloning git repo from url '{git_repo_url}' to tempfs '{autogit_repo_path}. Details: {exc}"
        )

        raise msg

    assert repo, ValueError("repo should not have been None")
    assert isinstance(repo, git.Repo), TypeError(
        f"Expected repo to be of type git.Repo. Got type: ({type(repo)})"
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
    print(
        f"Cloning git repository from '{git_repo_url}'. Output path: {autogit_repo_path}"
    )
    try:
        repo: git.Repo = git.Repo.clone_from(
            url=git_repo_url, to_path=autogit_repo_path
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception cloning git repo from url '{git_repo_url}' to tempfs '{autogit_repo_path}. Details: {exc}"
        )

        raise msg

    assert repo, ValueError("repo should not have been None")
    assert isinstance(repo, git.Repo), TypeError(
        f"Expected repo to be of type git.Repo. Got type: ({type(repo)})"
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
