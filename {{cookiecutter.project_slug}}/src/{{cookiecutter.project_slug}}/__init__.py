"""This module contains the main namespace of {{ cookiecutter.project_slug }}."""
# Import the version from _version.py which is dynamically created by setuptools-scm
# when the project is installed. Do not add it to version control!
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"


__all__ = ["__version__"]