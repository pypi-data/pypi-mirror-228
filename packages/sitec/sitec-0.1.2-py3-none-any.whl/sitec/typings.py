# coding=utf-8
"""
.dotfiles Typings Module
"""
__all__ = (
    "ExcType",
    "StrOrBytesPath",
)

import os
from typing import Type
from typing import TypeAlias

ExcType: TypeAlias = Type[Exception] | tuple[Type[Exception], ...]
StrOrBytesPath = str | bytes | os.PathLike[str] | os.PathLike[bytes]
