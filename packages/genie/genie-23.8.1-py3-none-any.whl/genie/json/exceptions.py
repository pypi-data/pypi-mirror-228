"""Errors related to json classes"""


class ApiImportError(Exception):
    """ApiImportError

    Raised when an API fails to import correctly
    """
    def __init__(self):
        super().__init__("Unable to successfully import API extension modules")
