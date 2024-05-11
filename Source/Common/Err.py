
class LSError(Exception):
    """Base class for all exceptions raised by the LS stack.
    """
    pass

class LSTypeError(TypeError):
    """Exception raised when an operation or function is applied to an
    object of inappropriate type. The associated value is a string
    giving details about the type mismatch.
    """

class LSUndoFlagError(LSError):
    """Exception raised when an operation is not allowed to be undo.
    """
    pass
