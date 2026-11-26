"""File Organizer: sort files into folders by extension or category."""

from .organizer import Move, MoveError, OrganizeResult, organize

__version__ = "1.0.0"

__all__ = [
    "Move",
    "MoveError",
    "OrganizeResult",
    "__version__",
    "organize",
]
