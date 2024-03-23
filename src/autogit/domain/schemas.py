from __future__ import annotations

from pathlib import Path
import typing as t

import git

# from modules import git_ops
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
)


class GitController(BaseModel):
    """Custom class to store git repository details & handle git operations.

    Params:
        repo_url (str | None): A URL to a remote git repository. If no URL is passed, the repository must already exist locally.
        local_path (str | Path): A path to the local git repository.
        exclude_branches (optional, list[str]): An optional list of string values representing branches to skip git operations on.

    """

    model_config = ConfigDict(arbitrary_types_allowed=True, exclude=["_repo"])

    repo_url: str | None = Field(default=None, description="Remote repository's URL.")
    local_path: t.Union[str, Path] = Field(
        default=None, description="Path to repository on local machine"
    )
    exclude_branches: list[str] | None = Field(
        default=None,
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
        """Check if local git repository path exists.

        Returns:
            (bool): `True` if self.local_path exists.
            (bool): `False` if self.local_path does not exist.

        """
        return self.local_path.exists()

    @computed_field
    @property
    def _repo(self) -> git.Repo:
        """Initialize a git.Repo object from class params. Attempts to clone repository if `not self.local_path.exists`.

        Returns:
            (git.Repo): An initialized git.Repo object, where the repository has been cloned to a local path.

        Raises:
            (Exception): When an unhandled/unexpected exception occurs.

        """
        if not self.exists:
            print(
                f"[WARNING] Repository does not exist at {self.local_path}. Attempting to clone."
            )
            try:
                try:
                    clone_repo: git.Repo = git.Repo.clone_from(
                        url=self.repo_url, to_path=self.local_path
                    )
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception cloning git repo from url '{self.repo_url}' to local path '{self.local_path}'. Details: {exc}"
                    )

                    raise msg

            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception cloning repository from URL '{self.repo_url}'. Details: {exc}"
                )

                raise msg
        try:
            _repo: git.Repo = git.Repo(path=self.local_path)

            return _repo

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception loading git repository at path '{self.local_path}'. Details: {exc}"
            )

            raise msg

    @computed_field
    @property
    def repo_name(self) -> str:
        """Get repository name from directory path."""
        return self._repo.working_tree_dir.split("/")[-1]

    @computed_field
    @property
    def branches(self) -> list[git.Head]:
        try:
            branches: list[git.Head] = self._repo.heads

            return branches

        except Exception as exc:
            msg = Exception(f"Unhandled exception getting branch names. Details: {exc}")

            raise msg

    @computed_field
    @property
    def remotes(self) -> list[git.Remote]:
        """Return a list of remotes for the local repository."""
        try:
            remotes: list[git.Remote] = self._repo.remotes

            return remotes

        except Exception as exc:
            msg = Exception(f"Unhandled exception getting git remotes. Details: {exc}")

            raise msg

    @computed_field
    @property
    def untracked_files(self) -> list[str]:
        """Return a list of string values representing untracked local files."""
        try:
            untracked: list[str] = self._repo.untracked_files

            return untracked

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting untracked branches. Details: {exc}"
            )

            raise msg

    def autopull(self, exclude_branches: list[str] | None = None) -> None:
        """Automate pulling git branches.

        Params:
            (list[str] | None): An optional list of strings representing git branch names
                that should be skipped during git operations.

        Raises:
            (Exception): When an unhandled/unexpected exception occurs.

        """
        if exclude_branches is None or len(exclude_branches) == 0:
            exclude_branches = self.exclude_branches

        origin: git.Remote = self._repo.remotes.origin
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
