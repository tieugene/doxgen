"""Exceptions"""

class DGExc(RuntimeError):
    """Basic error"""

    def __str__(self):
        """Make string representation of exception."""
        if uplink := super().__str__():
            return f"{self.__class__.__name__}: {uplink}"
        return self.__class__.__name__


class DGWarn(RuntimeWarning):
    """Basic warrning"""

class DGRenderExc(DGExc):
    """Plugin template rendering error."""
