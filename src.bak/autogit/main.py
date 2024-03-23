from __future__ import annotations

import time
import json
from pathlib import Path
import typing as t

from core import PLATFORM
from domain import GitController
import git
from modules import git_ops
from packages import git_puller
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from contextlib import contextmanager

from rich import print as rprint, pretty, inspect
from rich.console import Console

console: Console = Console()

try:
    pretty.install()
except Exception as exc:
    msg = Exception(
        f"Unhandled exception installing rich.pretty. Console text will not be 'prettified'. Details: {exc}"
    )
    print(msg)


@contextmanager
def benchmark(name: str = "Unnamed benchmark", description: str = None):
    start_time = time.process_time()

    yield

    end_time = time.process_time()

    total_time = end_time - start_time

    if description:
        msg = f"{description}.\n{name} execution time: {total_time}"
    else:
        msg = f"Execution time: {total_time}"

    rprint(msg)


class WelcomeMsgData(BaseModel):
    app_name: str = Field(default="Autogit")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    repo_name: str = Field(default=None)
    current_branch: git.Head = Field(default=None)
    local_path: t.Union[str, Path] = Field(default=None)

    @field_validator("local_path")
    def validate_local_path(cls, v) -> Path:
        if isinstance(v, Path):
            if "~" in f"{v}":
                return v.expanduser()
            else:
                return v

        if isinstance(v, str):
            if "~" in f"{v}":
                return Path(v).expanduser()
            else:
                return v

        raise ValidationError


def welcome_msg_bak(msg_data: WelcomeMsgData = None) -> None:
    if not msg_data:
        print(
            f"<Welcome message skipping, no message data detected. Continuing script execution.>"
        )
        return

    app_name_chars: int = len(msg_data.app_name)
    top_hyphens: int = app_name_chars + 4
    separator_hyphens: int = int(
        ((len(msg_data.local_path)) * 2) - (round(len(msg_data.local_path) * 0.75, 1))
    )
    print(f"Separator hyphens: {separator_hyphens}")

    app_info_msg: str = (
        f"""{'-' * top_hyphens}
| {msg_data.app_name} |
{'-' * separator_hyphens}
| Repository Name: {msg_data.repo_name}
| Current Branch: {msg_data.current_branch}
| Local Path: {msg_data.local_path}
{'=' * separator_hyphens}
"""
    )

    print(app_info_msg)


def welcome_msg(msg_data: WelcomeMsgData = None) -> None:
    if not msg_data:
        print(
            f"<Welcome message skipping, no message data detected. Continuing script execution.>"
        )
        return

    console.print(
        f"""
[green underline]> {msg_data.app_name}[/green underline]

[bold blue]Repository Name[/]: {msg_data.repo_name}                  
[bold blue]Current Branch[/]: [green]{msg_data.current_branch}[/]
[bold blue]Local Path[/]: {msg_data.local_path}
"""
    )


def main(exclude_branches: list[str] | None = None):
    CONTINUE = True

    try:
        GIT_REPO_PATH: Path = git_ops.load_repopath()
    except FileNotFoundError as fnf:
        msg = FileNotFoundError("Did not find file 'repo_path'.")

        print(msg)

        CONTINUE = False

        raise NotImplementedError(
            "No repo_file detected. Loading repository path from environment/CLI arg not yet supported."
        )

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception loading repository from file. Details: {exc}"
        )

        raise msg

    if not CONTINUE:
        exit(1)

    REPO: GitController = GitController(
        local_path=GIT_REPO_PATH, exclude_branches=exclude_branches
    )
    # print(f"Git repository: {REPO}")
    STARTING_BRANCH: git.Head = REPO._repo.head.ref

    welcome_msg_data: WelcomeMsgData = WelcomeMsgData(
        repo_name=REPO.repo_name,
        current_branch=STARTING_BRANCH,
        local_path=GIT_REPO_PATH,
    )
    welcome_msg(welcome_msg_data)

    with benchmark(name="git_puller.pull()", description="Pulling with git_puller()"):
        with console.status(
            f"Running automated git branch pulls for repo '{welcome_msg_data.repo_name}'",
        ):
            try:

                git_puller.pull(REPO, exclude_branches=exclude_branches)

            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception running auto puller. Details: {exc}"
                )

                STARTING_BRANCH.checkout()

                raise msg

    STARTING_BRANCH.checkout()


if __name__ == "__main__":

    main(exclude_branches=["archive/old-apps"])
