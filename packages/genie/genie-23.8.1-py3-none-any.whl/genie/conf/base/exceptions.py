"""Error Related to base classes"""


class UnknownLinkError(Exception):
    """UnknownLinkError

    Raised when a specified link is unknown
    """

    def __init__(self, link, testbed):
        super().__init__("There is no link {link} in this "
                         "testbed {testbed}".format(link=link,
                                                    testbed=testbed))


class UnknownInterfaceTypeError(Exception):
    """UnknownInterfaceTypeError"""

    def __init__(self):
        super().__init__("Unknown interface type")


class SingleLoopbackConnectionError(Exception):
    """SingleLoopbackConnectionError"""

    def __init__(self):
        super().__init__("LoopbackLink can only contains "
                         "one interface obj")


class LoopbackConnectionTypeError(Exception):
    """LoopbackConnectionTypeError"""

    def __init__(self):
        super().__init__("LoopbackLink can noly connect "
                         "'loopback' type interface")


class CountError(Exception):
    """Wrong Count for Find methods"""

    pass

# vim: ft=python et sw=4
