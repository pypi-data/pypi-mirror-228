# -*- coding: utf-8 -*-

__all__ = ("AbsolutePathError", "DirectoryNotFoundError", "NotAFileError")


class AbsolutePathError(OSError):
    """Exception to raise when a path is an absolute path."""


class DirectoryNotFoundError(FileNotFoundError):
    """Exception to raise when a directory does not exist.

    Note:
        Since this exception inherits from `FileNotFoundError`,
        it should be handled before handling `FileNotFoundError`
        in the exception handling block.
    """


class NotAFileError(OSError):
    """Exception to raise when a path exists but is not a file."""
