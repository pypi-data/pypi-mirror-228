'''
Genie Harness Related Errors
'''


class GenieTgnError(Exception):
    '''
    GenieTgnError
    Raised when an error is seen while executing TGN methods
    '''

    def __init__(self, message):
        super().__init__("TGN-ERROR: {}".format(message))

class GenieConfigReplaceWarning(Exception):
    '''
    GenieConfigReplaceWarning
    Warning raised when execution of configure-replace will require a reload
    '''
    pass

# vim: ft=python et sw=4