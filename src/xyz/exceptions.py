"""
    xyz.exceptions
    ~~~~~~~~~~~~~~
"""


class XYZException(Exception):
    def __init__(self, msg, *args):
        self.msg = msg
        super().__init__(msg, *args)


class PostError(XYZException):
    "Generic Post Exception"
    pass
