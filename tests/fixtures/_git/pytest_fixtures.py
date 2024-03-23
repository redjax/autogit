import typing as t
from pathlib import Path
import tempfile
import shutil

import pytest
import git


@pytest.fixture
def git_repo_url() -> str:
    return "https://github.com/redjax/test_repo.git"


@pytest.fixture
def git_tempfs() -> t.Generator[str, t.Any, None]:
    temp_dir: str = tempfile.mkdtemp("test_repo")

    yield temp_dir

    print(f"Removing fixture path '{temp_dir}'")
    shutil.rmtree(temp_dir)


@pytest.fixture
def autogit_repo_path() -> t.Generator[Path, t.Any, None]:
    temp_dir: str = tempfile.mkdtemp("test_repo")
    repo_path: Path = Path(temp_dir) / "repo"

    yield repo_path

    print(f"Removing fixture path '{repo_path}'")
    shutil.rmtree(repo_path)
