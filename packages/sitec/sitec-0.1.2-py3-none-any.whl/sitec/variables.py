# coding=utf-8
"""
Sitec Variables Module
"""

__all__ = (
    "LINUX",
    "MACOS"
)

import sys

"""
    is a tty?, not jupyter, not FORCE_COLOR set and not idlelib
"""
LINUX = sys.platform == "linux"
"""
    Is Linux? sys.platform == 'linux'
"""
MACOS = sys.platform == "darwin"
