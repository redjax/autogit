from __future__ import annotations

from pathlib import Path
import typing as t

import git
from modules import git_ops
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
)


class GitController(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, exclude=["_repo"])

    local_path: t.Union[str, Path] = Field(
        default=None, description="Path to repository on local machine"
    )
    exclude_branches: list[str] | None = Field(
        default_factory=[],
        description="A list of branch names (as strings) to ignore when running automated git actions.",
    )

    @field_validator("local_path")
    def validate_local_path(cls, v) -> Path:
        if isinstance(v, Path):
            if "~" in f"{Path}":
                return v.expanduser()
            else:
                return v

        if isinstance(v, str):
            return Path(v)

        raise ValidationError

    @property
    def exists(self) -> bool:
        return self.local_path.exists()

    @computed_field
    @property
    def _repo(self) -> git.Repo:
        if not self.exists:
            raise FileNotFoundError(f"Could not find path '{self.local_path}'")

        try:
            repo: git.Repo = git_ops.load_git_repo(self.local_path)

            repo = git_ops.validate_git_repo(repo)

            return repo

        except Exception as exc:
            msg = Exception(
                f"Couldn't initialize git repository at path '{self.local_path}'. Details: {exc}"
            )

            raise msg

    @computed_field
    @property
    def repo_name(self) -> str:
        return self._repo.working_tree_dir.split("/")[-1]

    @computed_field
    @property
    def branches(self) -> list[git.Head]:
        try:
            branches: list[git.Head] = git_ops.get_branchnames(repo=self._repo)

            return branches

        except Exception as exc:
            msg = Exception(f"Unhandled exception getting branch names. Details: {exc}")

            raise msg

    @computed_field
    @property
    def remotes(self) -> list[git.Remote]:
        try:
            remotes: list[git.Remote] = git_ops.get_remotes(repo=self._repo)

            return remotes

        except Exception as exc:
            msg = Exception(f"Unhandled exception getting git remotes. Details: {exc}")

            raise msg

    @computed_field
    @property
    def untracked_files(self) -> list[str]:
        try:
            untracked: list[str] = git_ops.get_untracked(repo=self._repo)

            return untracked

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting untracked branches. Details: {exc}"
            )

            raise msg

    def pull(self, exclude_branches: list[str] | None = None) -> bool:

        if exclude_branches is None or len(exclude_branches) == 0:
            exclude_branches = self.exclude_branches

        origin: git.RemoteReference = self._repo.remotes.origin
        ## Store branch before synch operations
        STARTING_BRANCH: git.Head = self._repo.head.ref

        def reset_branch(branch: git.Head = STARTING_BRANCH):
            branch.checkout()

        print(f"\nStarting branch auto-pull\n")

        try:
            for b in self.branches:
                if exclude_branches:
                    if f"{b}" in exclude_branches:
                        print(f"Skipping excluded branch '{b}'.")
                        continue

                head = self._repo.heads[f"{b}"]

                ## Checkout branch
                head.checkout()
                print(f"Fetching changes for branch '{b}'")
                origin.fetch()

                print(f"Pulling changes for branch '{b}'")
                try:
                    origin.pull()
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception pulling changes for branch '{b}'. Details: {exc}"
                    )

                    reset_branch()

                    raise msg

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception running branch puller. Details: {exc}"
            )
            reset_branch()

            raise msg
