"""Effects package for video generation."""

from app.services.effects.registry import EffectRegistry

# Import all effect modules to register them
from app.services.effects import static
from app.services.effects import pan
from app.services.effects import zoom
from app.services.effects import rotate

__all__ = ['EffectRegistry']
