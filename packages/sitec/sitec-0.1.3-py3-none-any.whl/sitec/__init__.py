# coding=utf-8
"""
sitec Module
"""

__all__ = (
    "CalledProcessError",
    "TempDir",
    "Top",

    "PYTHON_FTP",

    "PathIs",
    "PathSuffix",
    "FileName",

    "chdir",
    "command",
    "dependencies",
    "distribution",
    "findup",
    "getpths",
    "getsitedir",
    "getstdout",
    "parent",
    "python_latest",
    "python_version",
    "python_versions",
    "requirements",
    "superproject",
    "supertop",
    "suppress",
    "toiter",
    "top",
    "version",

    "ExcType",
    "StrOrBytesPath",

    "LINUX",
    "MACOS"
)

from sitec import classes
from sitec import constants
from sitec import enums
from sitec import exceptions
from sitec import functions
from sitec import typings
from sitec import variables

from sitec.__version__ import __version__

from sitec.classes import CalledProcessError as CalledProcessError
from sitec.classes import TempDir as TempDir
from sitec.classes import Top as Top

from sitec.constants import PYTHON_FTP as PYTHON_FTP

from sitec.enums import PathIs as PathIs
from sitec.enums import PathSuffix as PathSuffix
from sitec.enums import FileName as FileName

from sitec.functions import chdir as chdir
from sitec.functions import command as command
from sitec.functions import dependencies as dependencies
from sitec.functions import distribution as distribution
from sitec.functions import findup as findup
from sitec.functions import getpths as getpths
from sitec.functions import getsitedir as getsitedir
from sitec.functions import getstdout as getstdout
from sitec.functions import parent as parent
from sitec.functions import python_latest as python_latest
from sitec.functions import python_version as python_version
from sitec.functions import python_versions as python_versions
from sitec.functions import requirements as requirements
from sitec.functions import superproject as superproject
from sitec.functions import supertop as supertop
from sitec.functions import suppress as suppress
from sitec.functions import toiter as toiter
from sitec.functions import top as top
from sitec.functions import version as version

from sitec.typings import ExcType as ExcType
from sitec.typings import StrOrBytesPath as StrOrBytesPath

from sitec.variables import LINUX as LINUX
from sitec.variables import MACOS as MACOS
