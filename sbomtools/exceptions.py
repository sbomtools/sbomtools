"""
A set of exceptions that will be raised for these utilities.
"""

class PackageNotFound(Exception):
    """
    Raised when a required package is not found
    """

class DependencyNotMet(Exception):
    """
    Raised when a change would cause a dependency error.
    """

class AlreadyExists(Exception):
    """
    Returned when an update would overwrite an entry when not allowed.
    """

class FileFormatError(Exception):
    """
    Raised when there is a problem with the SBOM format.
    """

class UnknownError(Exception):
    """
    Something went wrong but we don't know what.
    """
