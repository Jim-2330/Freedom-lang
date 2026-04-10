class FreedonError(Exception):
    """Base error for Freedon Lang."""


class ParseError(FreedonError):
    """Raised when source code cannot be parsed."""


class EvalError(FreedonError):
    """Raised when evaluation fails."""

