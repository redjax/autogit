from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import typing as t

import pytest

@pytest.fixture
def txt_file_ex() -> t.Generator[Path, t.Any, None]:
    """Test fixture for a temporary/virtual filesystem path '<TemporaryFS>/test/test.txt."""
    ## Create temporary filesystem
    temp_dir = tempfile.mkdtemp()

    ## Build path
    file_path = Path(temp_dir) / "test" / "test.txt"
    ## Create path(s)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    ## Touch test.txt
    file_path.touch()

    with open(file_path, "w") as f:
        f.write("This is a test string in a virtual filesystem.")

    ## Yield to test that called this fixture
    yield file_path

    ## Remove when function that called this fixture ends
    shutil.rmtree(temp_dir)
