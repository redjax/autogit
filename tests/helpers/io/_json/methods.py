import typing as t
from pathlib import Path
import json


def save_json(file_path: Path = None, json_data: str = None) -> None:
    try:
        with open(file=file_path, mode="w") as f:
            try:
                f.write(json_data)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception writing JSON data to file. Details: {exc}"
                )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception opening path for writing: '{file_path}'. Details: {exc}"
        )

        raise msg


def read_json(file_path: Path = None) -> str:
    try:
        with open(file=file_path, mode="r") as f:
            contents: str = f.read()

        data: t.Any = json.loads(contents)
        return data

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception opening path for reading: '{file_path}'. Details: {exc}"
        )

        raise msg
