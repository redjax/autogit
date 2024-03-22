from __future__ import annotations

import time
import json
from pathlib import Path
import typing as t

from core import PLATFORM
from domain import GitRepository
import git
from modules import git_ops
from packages import git_puller
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from contextlib import contextmanager


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

    print(msg)


class WelcomeMsgData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    repo_name: str = Field(default=None)
    current_branch: git.Head = Field(default=None)


def welcome_msg(msg_data: WelcomeMsgData = None) -> None:
    if not msg_data:
        print(
            f"<Welcome message skipping, no message data detected. Continuing script execution.>"
        )
        return

    print(
        f"| Autogit |\n{'-' * 32}\n| Repository Name: {msg_data.repo_name}\n| Current branch: {msg_data.current_branch}\n{'=' * 32}"
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

    REPO: GitRepository = GitRepository(
        local_path=GIT_REPO_PATH, exclude_branches=exclude_branches
    )
    # print(f"Git repository: {REPO}")
    STARTING_BRANCH: git.Head = REPO._repo.head.ref

    welcome_msg_data: WelcomeMsgData = WelcomeMsgData(
        repo_name=REPO.repo_name, current_branch=STARTING_BRANCH
    )
    welcome_msg(welcome_msg_data)

    try:
        with benchmark(
            name="git_puller.pull()", description="Pulling with git_puller()"
        ):
            git_puller.pull(REPO, exclude_branches=exclude_branches)

    except Exception as exc:
        msg = Exception(f"Unhandled exception running auto puller. Details: {exc}")

        STARTING_BRANCH.checkout()

        raise msg

    STARTING_BRANCH.checkout()


if __name__ == "__main__":

    main(exclude_branches=["archive/old-apps"])
