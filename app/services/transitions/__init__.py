"""Transitions package for video generation."""

from app.services.transitions.registry import TransitionRegistry

# Import all transition modules to register them
from app.services.transitions import fade
from app.services.transitions import zoom
from app.services.transitions import wipe
from app.services.transitions import smooth

__all__ = ['TransitionRegistry']
