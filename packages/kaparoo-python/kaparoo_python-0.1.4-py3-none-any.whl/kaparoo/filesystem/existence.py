# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = (
    # single
    "path_exists",
    "file_exists",
    "dir_exists",
    "check_if_path_exists",
    "check_if_file_exists",
    "check_if_dir_exists",
    # multiple
    "paths_exist",
    "files_exist",
    "dirs_exist",
    "check_if_paths_exist",
    "check_if_files_exist",
    "check_if_dirs_exist",
)

import os
from pathlib import Path
from typing import TYPE_CHECKING, overload

from kaparoo.filesystem.exceptions import DirectoryNotFoundError, NotAFileError
from kaparoo.filesystem.utils import join_prefix, stringify_path, stringify_paths

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Literal

    from kaparoo.filesystem.types import StrPath


# ========================== #
#           Single           #
# ========================== #


def path_exists(path: StrPath) -> bool:
    "Test whether a given path exists."
    return os.path.exists(path)


def file_exists(path: StrPath) -> bool:
    "Test whether a given path exists and is a file."
    return os.path.isfile(path)


def dir_exists(path: StrPath) -> bool:
    "Test whether a given path exists and is a directory."
    return os.path.isdir(path)


@overload
def check_if_path_exists(path: StrPath, *, stringify: Literal[False] = False) -> Path:
    ...


@overload
def check_if_path_exists(path: StrPath, *, stringify: Literal[True]) -> str:
    ...


@overload
def check_if_path_exists(path: StrPath, *, stringify: bool) -> Path | str:
    ...


def check_if_path_exists(path: StrPath, *, stringify: bool = False) -> Path | str:
    """Check if a given path exists and return it as a Path object.

    Args:
        path: The path to check for existence.
        stringify: Whether to return the path as a string. Defaults to False.

    Returns:
        The path as a Path object or a string, depending on the value of `stringify`.

    Raises:
        FileNotFoundError: If the path does not exist.
    """

    if not (path := Path(path)).exists():
        raise FileNotFoundError(f"no such path: {path}")

    return stringify_path(path) if stringify else path


@overload
def check_if_file_exists(path: StrPath, *, stringify: Literal[False] = False) -> Path:
    ...


@overload
def check_if_file_exists(path: StrPath, *, stringify: Literal[True]) -> str:
    ...


@overload
def check_if_file_exists(path: StrPath, *, stringify: bool) -> Path | str:
    ...


def check_if_file_exists(path: StrPath, *, stringify: bool = False) -> Path | str:
    """Check if a given path exists and is a file, and return it as a Path object.

    Args:
        path: The file path to check for existence.
        stringify: Whether to return the path as a string. Defaults to False.

    Returns:
        The path as a Path object or a string, depending on the value of `stringify`.

    Raises:
        FileNotFoundError: If the path does not exist.
        NotAFileError: If the path exists but is not a file.
    """

    if not (path := Path(path)).exists():
        raise FileNotFoundError(f"no such file: {path}")
    elif not path.is_file():
        raise NotAFileError(f"not a file: {path}")

    return stringify_path(path) if stringify else path


@overload
def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: Literal[False] = False
) -> Path:
    ...


@overload
def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: Literal[True]
) -> str:
    ...


@overload
def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: bool
) -> Path | str:
    ...


def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: bool = False
) -> Path | str:
    """Check if a given path exists and is a directory, and return it as a Path object.

    Args:
        path: The directory path to check for existence.
        make: Whether to create the directory with mode `0o777` if it does not exist.
            If an integer is provided, use it as the octal mode. Defaults to False.
        stringify: Whether to return the path as a string. Defaults to False.

    Returns:
        The path as a Path object or a string, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If the path does not exist and `make` is False.
        NotADirectoryError: If the path exists but is not a directory.
    """  # noqa: E501

    if not (path := Path(path)).exists():
        if make is False:
            raise DirectoryNotFoundError(f"no such directory: {path}")
        path.mkdir(mode=0o777 if make is True else make, parents=True)
    elif not path.is_dir():
        raise NotADirectoryError(f"not a directory: {path}")

    return stringify_path(path) if stringify else path


# ========================== #
#          Multiple          #
# ========================== #


def _join_root_if_provided(
    root: StrPath | None, *paths: StrPath
) -> tuple[StrPath, ...]:
    if root is not None:
        root = check_if_dir_exists(root)
        paths = tuple(join_prefix(root, *paths))
    return paths


def paths_exist(*paths: StrPath, root: StrPath | None = None) -> bool:
    """Test whether multiple paths exist.

    Args:
        *paths: Multiple paths to check for existence.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.

    Returns:
        True if all paths exist, False otherwise.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the `root` directory does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
    """
    paths = _join_root_if_provided(root, *paths)
    return all(path_exists(path) for path in paths)


def files_exist(*paths: StrPath, root: StrPath | None = None) -> bool:
    """Test whether multiple files exist.

    Args:
        *paths: Multiple file paths to check for existence.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.

    Returns:
        True if all file paths exist, False otherwise.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the `root` directory does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
    """
    paths = _join_root_if_provided(root, *paths)
    return all(file_exists(path) for path in paths)


def dirs_exist(*paths: StrPath, root: StrPath | None = None) -> bool:
    """Test whether multiple directories exist.

    Args:
        *paths: Multiple directory paths to check for existence.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.

    Returns:
        True if all directory paths exist, False otherwise.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the `root` directory does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
    """
    paths = _join_root_if_provided(root, *paths)
    return all(dir_exists(path) for path in paths)


@overload
def check_if_paths_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: Literal[False] = False
) -> Sequence[Path]:
    ...


@overload
def check_if_paths_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: Literal[True]
) -> Sequence[str]:
    ...


@overload
def check_if_paths_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: bool
) -> Sequence[Path] | Sequence[str]:
    ...


def check_if_paths_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: bool = False
) -> Sequence[Path] | Sequence[str]:
    """Check if multiple paths exist and return them as a sequence of Path objects.

    Args:
        *paths: Multiple paths to check for existence.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.
        stringify: Whether to return a sequence of strings. Defaults to False.

    Returns:
        The paths as a sequence of Path objects or a sequence of strings,
            depending on the value of stringify.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the `root` directory does not exist.
        FileNotFoundError: If any of `paths` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
    """
    paths = _join_root_if_provided(root, *paths)
    paths = [check_if_path_exists(path) for path in paths]
    return stringify_paths(*paths) if stringify else paths


@overload
def check_if_files_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: Literal[False] = False
) -> Sequence[Path]:
    ...


@overload
def check_if_files_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: Literal[True]
) -> Sequence[str]:
    ...


@overload
def check_if_files_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: bool
) -> Sequence[Path] | Sequence[str]:
    ...


def check_if_files_exist(
    *paths: StrPath, root: StrPath | None = None, stringify: bool = False
) -> Sequence[Path] | Sequence[str]:
    """Check if multiple files exist and return them as a sequence of Path objects.

    Args:
        *paths: Multiple file paths to check for existence.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.
        stringify: Whether to return a sequence of strings. Defaults to False.

    Returns:
        The file paths as a sequence of Path objects or a sequence of strings,
            depending on the value of `stringify`.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the `root` directory does not exist.
        FileNotFoundError: If any of `paths` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        NotAFileError: If any of `paths` exists but is not a file.
    """
    paths = _join_root_if_provided(root, *paths)
    paths = [check_if_file_exists(path) for path in paths]
    return stringify_paths(*paths) if stringify else paths


@overload
def check_if_dirs_exist(
    *paths: StrPath,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def check_if_dirs_exist(
    *paths: StrPath,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def check_if_dirs_exist(
    *paths: StrPath,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def check_if_dirs_exist(
    *paths: StrPath,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Check if multiple directories exist and return them as a sequence of Path objects.

    Args:
        *paths: Multiple directory paths to check for existence.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.
        make: Whether to create the directories with mode `0o777` if they do not exist.
            If an integer is provided, use it as the octal mode. Defaults to False.
        stringify: Whether to return a sequence of strings. Defaults to False.

    Returns:
        The directory paths as a sequence of Path objects or a sequence of strings,
            depending on the value of `stringify`.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the `root` directory does not exist.
        DirectoryNotFoundError: If any of `paths` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        NotADirectoryError: If any of `paths` exists but is not a directory.
    """  # noqa: E501
    paths = _join_root_if_provided(root, *paths)
    paths = [check_if_dir_exists(path, make=make) for path in paths]
    return stringify_paths(*paths) if stringify else paths
