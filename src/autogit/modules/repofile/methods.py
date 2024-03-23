import typing as t
from pathlib import Path
import json

from domain import GitController


def load_repos_file(repos_file_path: t.Union[str, Path] = "repos.json") -> dict:
    assert repos_file_path, ValueError("Missing a path to a repos.json file")
    assert isinstance(repos_file_path, str) or isinstance(
        repos_file_path, Path
    ), TypeError(
        f"repos_file_path must be of type str or Path. Got type: ({type(repos_file_path)})"
    )
    if isinstance(repos_file_path, Path):
        if "~" in f"{repos_file_path}":
            repos_file_path: Path = repos_file_path.expanduser()
    if isinstance(repos_file_path, str):
        if "~" in f"{repos_file_path}":
            repos_file_path: Path = Path(repos_file_path).expanduser()
        else:
            repos_file_path: Path = Path(repos_file_path)

    assert repos_file_path.suffix == ".json", ValueError(
        "repos_file_path must be a .json file"
    )
    assert repos_file_path.exists(), FileNotFoundError(
        f"Could not find repos .json file at path '{repos_file_path}'."
    )

    print(f"Loading repos from '{repos_file_path}'")
    try:
        with open(repos_file_path, "r") as f:
            try:
                contents = f.read()
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception reading contents of file '{f}'. Details: {exc}"
                )

            try:
                repos_data: dict = json.loads(contents)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled loading file contents to JSON. Details: {exc}"
                )

                raise msg

            return repos_data
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception opening repos file at path '{repos_file_path}'. Details: {exc}"
        )

        raise msg


def load_controllers(repos: list[dict] = None) -> list[GitController]:
    assert repos, ValueError("Missing list of repo dicts")
    assert isinstance(repos, list), TypeError(
        f"repos must be a list of dicts. Got type: ({type(repos)})"
    )

    controllers: list[GitController] = []

    for d in repos:
        if not isinstance(d, dict):
            print(f"[ERROR] List item is not a dict. Got type: ({type(d)}). Skipping.")
            continue

        try:
            controller: GitController = GitController.model_validate(d)
            controllers.append(controller)
        except Exception as exc:
            msg = Exception(
                f"Unhandled expection loading repo data into GitController object. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            continue

    return controllers
