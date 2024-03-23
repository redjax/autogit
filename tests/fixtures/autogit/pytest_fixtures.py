from __future__ import annotations

from pathlib import Path
import typing as t
import tempfile
import json
import shutil

from tests.helpers import io
from autogit.domain import GitController

import pytest


@pytest.fixture
def repos_file() -> t.Generator[Path, t.Any, None]:
    temp_dir: str = tempfile.mkdtemp()

    file_path: Path = Path(temp_dir) / "repos.json"
    repos_path: Path = Path(temp_dir) / "repos"
    local_path: Path = repos_path / "test_repo"

    json_data: str = json.dumps(
        [
            {
                "repo_url": "https://github.com/redjax/test_repo.git",
                "local_path": f"{local_path}",
                "exclude_branches": [],
            }
        ]
    )

    io.save_json(file_path=file_path, json_data=json_data)

    data = io.read_json(file_path=file_path)
    print(f"Loaded data from '{file_path}': {data}")

    yield file_path

    try:
        shutil.rmtree(file_path.parent)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception removing tempfile '{file_path}'. Details: {exc}"
        )

        raise msg


@pytest.fixture
def repo_dict() -> dict:
    temp_dir: str = tempfile.mkdtemp()

    file_path: Path = Path(temp_dir) / "repos.json"
    repos_path: Path = Path(temp_dir) / "repos"
    local_path: Path = repos_path / "test_repo"

    json_data: str = json.dumps(
        [
            {
                "repo_url": "https://github.com/redjax/test_repo.git",
                "local_path": f"{local_path}",
                "exclude_branches": [],
            }
        ]
    )

    return json_data
