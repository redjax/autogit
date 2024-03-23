from __future__ import annotations

from pathlib import Path
import typing as t

import git


def clone_repo_to_path(
    repo_url: str = None, local_path: t.Union[str, Path] = None
) -> git.Repo:
    """Clone a git repository from a URL to a local path.

    Params:
        repo_url (str): URL to a remote git repository.
        local_path (str | Path): Local path to clone remote repository to.

    Returns:
        (git.Repo): An initialized git.Repo object.

    Raises:
        (ValueError): When an invalid input is entered/returned.
        (TypeError): When an input is of an invalid type.
        (Exception): When an uncaught/unhandled exception occurs.

    """
    assert repo_url, ValueError("Missing repository URL to clone from")
    assert isinstance(repo_url, str), TypeError(
        f"repo_url should be of type str. Got type: ({type(repo_url)})"
    )

    assert local_path, ValueError("Missing a local_path to clone repository to.")
    assert isinstance(local_path, str) or isinstance(local_path, Path), TypeError(
        f"local_path should be of type str or Path. Got type: ({type(local_path)})"
    )
    if isinstance(local_path, Path):
        if "~" in f"{local_path}":
            local_path: Path = local_path.expanduser()
    elif isinstance(local_path, str):
        if "~" in local_path:
            local_path: Path = Path(local_path).expanduser()
        else:
            local_path: Path = Path(local_path)

    if not local_path.parent.exists():
        print(
            f"[WARNING] Creating missing git repository local path '{local_path.parent}'."
        )
        try:
            local_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception creating path '{local_path.parent}'. Details: {exc}"
            )

            raise msg

    print(f"Cloning git repository from '{repo_url}'. Output path: {local_path}")
    try:
        repo: git.Repo = git.Repo.clone_from(url=repo_url, to_path=local_path)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception cloning git repo from url '{repo_url}' to tempfs '{local_path}'. Details: {exc}"
        )

        raise msg

    assert repo, ValueError("repo should not have been None")
    assert isinstance(repo, git.Repo), TypeError(
        f"Expected repo to be of type git.Repo. Got type: ({type(repo)})"
    )

    return repo
