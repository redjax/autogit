from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import typing as t
from typing import Generator
import json

from autogit.domain import GitController
from autogit.utils import git_utils
import git
import pytest

from tests.helpers import io


@pytest.mark.autogit
def test_pass_git_clone(git_tempfs: str, autogit_repo_path: Path, git_repo_url: str):
    repo: git.Repo = git_utils.clone_repo_to_path(
        repo_url=git_repo_url, local_path=autogit_repo_path
    )

    for p in Path(git_tempfs).rglob("**/*"):
        print(f"Path in '{git_tempfs}': {p}")


@pytest.mark.autogit
def test_load_controllers_from_file(repos_file: Path, repo_dict: dict):
    io.save_json(file_path=repos_file, json_data=json.dumps(repo_dict))
    data = io.read_json(repos_file)

    print(f"Repositories data loaded from file '{repos_file}': {data}")


@pytest.mark.autogit
def test_pass_gitcontroller(autogit_repo_path: Path, git_repo_url: str):
    repo: git.Repo = git_utils.clone_repo_to_path(
        repo_url=git_repo_url, local_path=autogit_repo_path
    )

    _repo: GitController = GitController(
        local_path=autogit_repo_path, repo_url=git_repo_url
    )
    assert _repo.exists, FileNotFoundError(
        f"Could not find repository at path '{autogit_repo_path}'"
    )

    print(f"Repository object: {_repo}")


@pytest.mark.autogit
def test_pass_create_gitcontrollers(repos_file: Path, repo_dict: dict):
    assert repos_file.exists(), FileNotFoundError(
        f"Could not find repos file at path '{repos_file}'."
    )

    io.save_json(file_path=repos_file, json_data=json.dumps(repo_dict))

    data = json.loads(io.read_json(repos_file))
    assert data, ValueError("JSON data should not have been None")
    assert isinstance(data, list), TypeError(
        f"Expected data to be a list of dicts. Got type: ({type(data)})"
    )

    controllers: list[GitController] = []

    for d in data:
        if isinstance(d, str):
            _data = json.loads(d)
        elif isinstance(d, dict):
            _data = d

        try:
            _controller: GitController = GitController.model_validate(_data)
            controllers.append(_controller)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception initializing GitController from data. Data ({type(d)}): {d}. Details: {exc}"
            )
            raise msg

    for c in controllers:
        assert isinstance(c, GitController), TypeError(
            f"Expected controller to be an instance of GitController. Got type: ({type(c)})"
        )
        print(f"Initialized GitController: {c}")


@pytest.mark.autogit
def test_pass_autogit_pull(autogit_repo_path: Path, git_repo_url: str):
    repo: git.Repo = git_utils.clone_repo_to_path(
        repo_url=git_repo_url, local_path=autogit_repo_path
    )

    _repo: GitController = GitController(
        local_path=autogit_repo_path, repo_url=git_repo_url
    )
    assert _repo.exists, FileNotFoundError(
        f"Could not find repository at path '{autogit_repo_path}'"
    )

    print(f"Repository object: {_repo}")

    print(f"Attempting pull with GitController object")
    try:
        _repo.autopull()
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception running @GitController.autopull(). Details: {exc}"
        )

        raise msg
