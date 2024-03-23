from modules.repofile import load_repos_file, load_controllers

from domain import GitController

if __name__ == "__main__":
    repos_data = load_repos_file()

    print(f"Repos: {repos_data}")

    controllers: list[GitController] = load_controllers(repos=repos_data)

    for c in controllers:
        print(f"Controller: {c}")
