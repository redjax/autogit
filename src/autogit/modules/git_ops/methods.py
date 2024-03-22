from __future__ import annotations

from pathlib import Path
import typing as t

import git
from git import Repo


def validate_git_repo(repo: Repo = None) -> Repo:
    assert repo, ValueError("Missing a git.Repo() object")
    assert isinstance(repo, Repo), TypeError(
        f"repo must be of type git.Repo. Got type: ({type(repo)})"
    )
    assert Path(repo.working_tree_dir).exists(), Exception(
        f"Repo working directory is not a git repository. Repository: {repo.working_tree_dir}."
    )

    return repo


def validate_git_origin(origin: git.Remote = None) -> git.Remote:
    assert origin, ValueError("Missing a git origin")
    assert isinstance(origin, git.Remote), TypeError(
        f"origin must be of type git.RemoteReference. Got type: ({type(origin)})"
    )

    return origin


def validate_git_branch(branch: git.Head = None) -> git.Head:
    assert branch, ValueError("Missing branch (a git.head object)")
    assert isinstance(branch, git.Head), TypeError(
        f"Expected head to be of type git.Head. Got type: ({type(branch)})"
    )

    return branch


def load_repopath(repo_file: t.Union[str, Path] = Path("repo_path")) -> Path:
    assert repo_file, ValueError("Missing a repo path")
    assert isinstance(repo_file, str) or isinstance(repo_file, Path), ValueError(
        f"filename must be a string or Path. Got type: ({type(repo_file)})"
    )
    if isinstance(repo_file, str):
        if "~" in repo_file:
            repo_file: Path = Path(repo_file).expanduser()
        else:
            repo_file: Path = Path(repo_file)

    if not Path(repo_file).exists():
        raise FileNotFoundError(f"Could not find repo_file at path '{repo_file}'.")

    try:
        with open(repo_file, "r") as f:
            f_data = f.read()
            assert f_data, ValueError(
                "repo_file must contain a path to a git repository."
            )

        return f_data

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception loading repository path from file '{repo_file}'. Details:  {exc}"
        )

        raise msg


def load_git_repo(repo_path: t.Union[str, Path] = None) -> Repo:
    assert repo_path, ValueError("Missing a repo path")
    assert isinstance(repo_path, str) or isinstance(repo_path, Path), ValueError(
        f"repo_path must be a string or Path. Got type: ({type(repo_path)})"
    )
    if isinstance(repo_path, str):
        if "~" in repo_path:
            repo_path: Path = Path(repo_path).expanduser()
        else:
            repo_path: Path = Path(repo_path)

    assert Path(repo_path).exists()

    try:
        _repo: Repo = Repo(path=repo_path)

        return _repo

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception loading git repository at path '{repo_path}'. Details: {exc}"
        )

        raise msg


def get_untracked(repo: Repo = None) -> list[str]:
    repo = validate_git_repo(repo)

    try:
        _untracked: list[str] = repo.untracked_files

        return _untracked

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting untracked files in repository '{repo.working_tree_dir}'. Details: {exc}"
        )

        raise msg


def get_branchnames(repo: Repo = None) -> list[git.HEAD]:
    repo = validate_git_repo(repo)

    try:
        branches: list[git.HEAD] = repo.heads

        return branches

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting branches from repo.heads. Details: {exc}"
        )

        raise msg


def get_remotes(repo: Repo = None) -> list[git.Remote]:
    repo = validate_git_repo(repo)

    try:
        origins: list[git.Remote] = repo.remotes

        return origins

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting remoted from repo.remotes. Details: {exc}"
        )

        raise msg


def get_repo_name(repo: git.Repo = None) -> str:
    repo = validate_git_repo(repo)

    return repo.working_tree_dir.split("/"[-1])
