import click

from domain import GitRepository

import git
import rich


@click.group()
@click.command()
def main():
    pass


# @click.option(
#     "-p",
#     "--local-path",
#     type=click.Path(exists=True),
#     required=True,
#     help="Location of git repository to auto-pull",
# )

if __name__ == "__main__":
    GitRepository()
