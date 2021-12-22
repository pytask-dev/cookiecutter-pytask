"""This module contains hooks which are executed after the template is rendered."""
import shutil
import subprocess
import warnings
from pathlib import Path


def remove_file(*filepath):
    """Remove a file."""
    try:
        Path(*filepath).unlink()
    except FileNotFoundError:
        pass


def remove_directory(*filepath):
    """Remove a directory."""
    try:
        path = Path(*filepath)
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def main():
    """Apply post generation hooks."""
    project_path = Path.cwd()

    if "{{ cookiecutter.create_changelog }}" == "no":
        remove_file(project_path, "CHANGES.rst")

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_file(project_path, "LICENSE")

    if "{{ cookiecutter.add_tox }}" == "no":
        remove_directory(project_path, ".github", "workflows")
        remove_file("tox.ini")

    if "{{ cookiecutter.add_github_actions }}" == "no":
        remove_directory(project_path, ".github", "workflows")

    if "{{ cookiecutter.add_readthedocs }}" == "no":
        remove_file(project_path, ".readthedocs.yaml")

    if "{{ cookiecutter.make_initial_commit }}" == "yes":
        subprocess.run(
            ("git", "config", "--global", "init.defaultBranch", "main"), check=True
        )
        subprocess.run(("git", "init"), check=True)
        subprocess.run(("git", "add", "."), check=True)
        subprocess.run(("git", "commit", "-am", "Initial commit."), check=True)

    if "{{ cookiecutter.create_conda_environment_at_finish }}" == "yes":
        if shutil.which("mamba") is not None:
            conda_exe = shutil.which("mamba")
        else:
            conda_exe = shutil.which("conda")

        if conda_exe is None:
            warnings.warn(
                "conda environment could not be created since no conda or mamba "
                "executable was found."
            )
        else:
            subprocess.run(("conda", "env", "create"), check=True)


if __name__ == "__main__":
    main()
