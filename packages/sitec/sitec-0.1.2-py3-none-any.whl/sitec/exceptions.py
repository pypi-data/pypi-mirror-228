# -*- coding: utf-8 -*-
"""Custom Errors
"""


class SitecBaseError(Exception):
    """
    Base Exception from which all other custom Exceptions defined in semantic_release
    inherit
    """


class InvalidArgument(SitecBaseError):
    """
    Raised when function is called with invalid argument
    """
