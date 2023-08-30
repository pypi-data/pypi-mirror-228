# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = (
    # create
    "make_dirs",
    # empty
    "dir_empty",
    "dirs_empty",
    # search
    "get_paths",
    "get_files",
    "get_dirs",
)

import os
import random
from pathlib import Path
from typing import TYPE_CHECKING, overload

from kaparoo.filesystem.existence import (
    _join_root_if_provided,
    check_if_dir_exists,
    check_if_dirs_exist,
)
from kaparoo.filesystem.utils import stringify_paths

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Literal

    from kaparoo.filesystem.types import StrPath, StrPaths


def make_dirs(
    *paths: StrPath,
    root: StrPath | None = None,
    mode: int = 0o777,
    exist_ok: bool = False,
) -> StrPaths:
    """Create directories specified by the provided paths.

    Args:
        *paths: Multiple directory paths to create.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.
        mode: The permission for the newly created directories. Defaults to 0o777.
        exist_ok: Whether to raise FileExistsError when trying to create an existing
            directory, Defaults to False.

    Return:
        The paths optionally resolved to the `root` directory.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the `root` directory does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        FileExistsError: If 'exist_ok' is False and a directory already exists.
        OSError: If there is an OS-level error while creating the directories.
    """
    paths = _join_root_if_provided(root, *paths)
    for path in paths:
        os.makedirs(path, mode, exist_ok)
    return paths


# ========================== #
#            Empty           #
# ========================== #


def dir_empty_unsafe(path: StrPath) -> bool:
    return not os.listdir(path)


def dirs_empty_unsafe(*paths: StrPath, root: StrPath | None = None) -> bool:
    if root is not None:
        paths = tuple(os.path.join(root, p) for p in paths)
    return all(dir_empty_unsafe(p) for p in paths)


def dir_empty(path: StrPath) -> bool:
    """Check if a given directory is empty.

    Args:
        path: The directory path to check for emptiness.

    Returns:
        True if the directory is empty, False otherwise.

    Raises:
        DirectoryNotFoundError: If the path does not exist.
        NotADirectoryError: If the path exists but is not a directory.
    """
    path = check_if_dir_exists(path)
    return dir_empty_unsafe(path)


def dirs_empty(*paths: StrPath, root: StrPath | None = None) -> bool:
    """Check if all the given directories are empty.

    Args:
        *paths: Multiple directory paths to check for emptiness.
        root: The root directory to resolve relative paths. If provided, all paths
            will be resolved relative to the `root` directory. Defaults to None.

    Returns:
        True if all the directories are empty, False otherwise.

    Raises:
        AbsolutePathError: If `root` is given and any of `paths` is an absolute path.
        DirectoryNotFoundError: If the root directory does not exist.
        DirectoryNotFoundError: If any of `paths` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        NotADirectoryError: If any of `paths` exists but is not a directory.
    """
    paths = check_if_dirs_exist(*paths, root=root)
    return all(dir_empty_unsafe(p) for p in paths)


# ========================== #
#           Search           #
# ========================== #


@overload
def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = False,
    num_samples: int | None = None,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Get paths of files or directories in a given directory.

    Args:
        root: The directory to search for paths.
        pattern: A glob pattern to match the paths against. Defaults to None and
            automatically uses "*" to list all paths included in the `root` directory.
        ignores: A sequence of paths to ignore. If any path in `ignores` does not start
            with `root`, it is treated as a relative path. For example, `any/path` is
            treated as `root/any/path`. Defaults to None.
        condition: A predicate that takes a Path object and decides whether to include
            the path in the results. Defaults to None.
        num_samples: A maximum number of paths to return. If given and its value is
            smaller than the total number of paths, only the `num_samples` paths of the
            total are randomly selected and returned. Hence, even using the same value
            of `num_samples`, may return a different result. Defaults to None.
        recursive: Whether to search for paths recursively in subdirectories of the
            `root` directory. Defaults to `False`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The paths that match the specified criteria as a sequence of Path objects or a
            sequence of strings, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If `root` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        ValueError: If `num_samples` is not a positive int.
    """

    root = check_if_dir_exists(root)

    if not isinstance(pattern, str):
        pattern = "*"

    paths = list(root.rglob(pattern) if recursive else root.glob(pattern))

    if root in paths:
        paths.remove(root)

    if not ignores:
        ignores = []

    for ignore in ignores:
        path_ignore = Path(ignore)
        if not path_ignore.is_relative_to(root):
            path_ignore = root / path_ignore

        if path_ignore in paths:
            paths.remove(path_ignore)

    if callable(condition):
        paths = [p for p in paths if condition(p)]

    if isinstance(num_samples, int) and num_samples < len(paths):
        if num_samples <= 0:
            raise ValueError("`num_samples` must be a positive int")
        paths = random.sample(paths, num_samples)

    return stringify_paths(*paths) if stringify else paths


@overload
def get_files(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def get_files(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def get_files(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def get_files(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Get paths of files in a given directory.

    Args:
        root: The directory to search for paths.
        pattern: A glob pattern to match the paths against. Defaults to None and
            automatically uses "*" to list all paths included in the `root` directory.
        ignores: A sequence of paths to ignore. If any path in `ignores` does not start
            with `root`, it is treated as a relative path. For example, `any/path` is
            treated as `root/any/path`. Defaults to None.
        condition: A predicate that takes a Path object and decides whether to include
            the path in the results. Defaults to None.
        num_samples: A maximum number of paths to return. If given and its value is
            smaller than the total number of paths, only the `num_samples` paths of the
            total are randomly selected and returned. Hence, even using the same value
            of `num_samples`, may return a different result. Defaults to None.
        recursive: Whether to search for paths recursively in subdirectories of the
            `root` directory. Defaults to `False`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The file paths that match the specified criteria as a sequence of Path objects
            or a sequence of strings, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If `root` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        ValueError: If `num_samples` is not a positive int.
    """

    if not callable(condition):
        file_condition = lambda p: p.is_file()  # noqa: E731
    else:
        file_condition = lambda p: p.is_file() and condition(p)  # type: ignore[misc] # noqa: E501, E731

    file_paths = get_paths(
        root,
        pattern=pattern,
        ignores=ignores,
        condition=file_condition,
        num_samples=num_samples,
        recursive=recursive,
        stringify=stringify,
    )

    return file_paths


@overload
def get_dirs(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def get_dirs(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def get_dirs(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def get_dirs(
    root: StrPath,
    *,
    pattern: str | None = None,
    ignores: StrPaths | None = None,
    condition: Callable[[Path], bool] | None = None,
    num_samples: int | None = None,
    recursive: bool = False,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Get paths of directories in a given directory.

    Args:
        root: The directory to search for paths.
        pattern: A glob pattern to match the paths against. Defaults to None and
            automatically uses "*" to list all paths included in the `root` directory.
        ignores: A sequence of paths to ignore. If any path in `ignores` does not start
            with `root`, it is treated as a relative path. For example, `any/path` is
            treated as `root/any/path`. Defaults to None.
        condition: A predicate that takes a Path object and decides whether to include
            the path in the results. Defaults to None.
        num_samples: A maximum number of paths to return. If given and its value is
            smaller than the total number of paths, only the `num_samples` paths of the
            total are randomly selected and returned. Hence, even using the same value
            of `num_samples`, may return a different result. Defaults to None.
        recursive: Whether to search for paths recursively in subdirectories of the
            `root` directory. Defaults to `False`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The directory paths that match the specified criteria as a sequence of Path
            objects or a sequence of strings, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If `root` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        ValueError: If `num_samples` is not a positive int.
    """

    if not callable(condition):
        dir_condition = lambda p: p.is_dir()  # noqa: E731
    else:
        dir_condition = lambda p: p.is_dir() and condition(p)  # type: ignore[misc] # noqa: E501, E731

    dir_paths = get_paths(
        root,
        pattern=pattern,
        ignores=ignores,
        condition=dir_condition,
        num_samples=num_samples,
        recursive=recursive,
        stringify=stringify,
    )

    return dir_paths
