# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("join_prefix", "stringify_path", "stringify_paths")

import os
import platform
from pathlib import Path
from typing import TYPE_CHECKING, overload

from kaparoo.filesystem.exceptions import AbsolutePathError

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Literal

    from kaparoo.filesystem.types import StrPath


def stringify_path(path: StrPath, after: StrPath | None = None) -> str:
    """Convert a path to a string and optionally make it relative.

    Args:
        path: The path to be converted to a string.
        after: The base path to make `path` relative to. If provided, the function
            returns only the string in `path` after `after`. Defaults to None.

    Returns:
        The string representation of the `path`.
            In Windows environment, all `\\` will be replaced to `/`.

    Raises:
        ValueError: If `after` is given and the `path` is not a subpath of `after`.
    """
    if after is not None:
        path = Path(path).relative_to(after)  # may raise ValueError
    path = os.fspath(path)
    return path.replace("\\", "/") if platform.system() == "Windows" else path


def stringify_paths(*paths: StrPath, after: StrPath | None = None) -> Sequence[str]:
    """Convert multiple paths to strings and optionally make them relative.

    Args:
        *paths: Multiple paths to be converted to strings.
        after: The base path to make all of the `paths` relative to. If provided,
            the function returns only the string in each of `paths` after `after`.
            Defaults to None.

    Returns:
        A seqeunce of string representations of the `paths`.
            In Windows environment, all `\\` will be replace to `/`.

    Raises:
        ValueError: If `after` is given and any of `paths` is not a subpath of `after`.
    """
    return [stringify_path(path, after) for path in paths]


@overload
def join_prefix(
    prefix: StrPath, *relpaths: StrPath, stringify: Literal[False] = False
) -> Sequence[Path]:
    ...


@overload
def join_prefix(
    prefix: StrPath, *relpaths: StrPath, stringify: Literal[True]
) -> Sequence[str]:
    ...


@overload
def join_prefix(
    prefix: StrPath, *relpaths: StrPath, stringify: bool
) -> Sequence[Path] | Sequence[str]:
    ...


def join_prefix(
    prefix: StrPath, *relpaths: StrPath, stringify: bool = False
) -> Sequence[Path] | Sequence[str]:
    """Join prefix with relative paths and return as a sequence of Path objects.

    Args:
        prefix: The prefix path to be joined with `relpaths`.
        *relpaths: Relative paths to be joined with `prefix`.
        stringify: Whether to return a sequence of strings. Defaults to False.

    Returns:
        The modified paths as a sequence of Path object or a sequence of strings,
            depending on the value of `stringify`.

    Raises:
        AbsolutePathError: If any of `relpaths` is an absolute path.
    """

    prefix, newpaths = Path(prefix), []

    for relpath in relpaths:
        # \path\to\file is RELATIVE PATH in Windows (DOS)
        # see https://learn.microsoft.com/en-us/dotnet/standard/io/file-path-formats
        if Path(relpath).is_absolute():
            raise AbsolutePathError(f"absolute path is not allowed: {relpath}")
        newpaths.append(prefix / relpath)

    return stringify_paths(*newpaths) if stringify else newpaths
