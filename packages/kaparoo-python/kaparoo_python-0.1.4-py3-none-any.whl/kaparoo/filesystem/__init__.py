# -*- coding: utf-8 -*-

__all__ = (
    # exceptions
    "AbsolutePathError",
    "DirectoryNotFoundError",
    "NotAFileError",
    # types
    "StrPath",
    "StrPaths",
    # utils
    "join_prefix",
    "stringify_path",
    "stringify_paths",
    # existence
    "check_if_dir_exists",
    "check_if_dirs_exist",
    "check_if_file_exists",
    "check_if_files_exist",
    "check_if_path_exists",
    "check_if_paths_exist",
    "dir_exists",
    "dirs_exist",
    "file_exists",
    "files_exist",
    "path_exists",
    "paths_exist",
    # directory
    "dir_empty",
    "dirs_empty",
    "get_dirs",
    "get_files",
    "get_paths",
    "make_dirs",
)

from kaparoo.filesystem.directory import (
    dir_empty,
    dirs_empty,
    get_dirs,
    get_files,
    get_paths,
    make_dirs,
)
from kaparoo.filesystem.exceptions import (
    AbsolutePathError,
    DirectoryNotFoundError,
    NotAFileError,
)
from kaparoo.filesystem.existence import (
    check_if_dir_exists,
    check_if_dirs_exist,
    check_if_file_exists,
    check_if_files_exist,
    check_if_path_exists,
    check_if_paths_exist,
    dir_exists,
    dirs_exist,
    file_exists,
    files_exist,
    path_exists,
    paths_exist,
)
from kaparoo.filesystem.types import StrPath, StrPaths
from kaparoo.filesystem.utils import (
    join_prefix,
    stringify_path,
    stringify_paths,
)
