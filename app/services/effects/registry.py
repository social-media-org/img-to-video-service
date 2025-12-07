"""Registry for managing available effects."""

from typing import Dict, Type
from app.services.effects.base import EffectBase


class EffectRegistry:
    """Registry to store and retrieve effect classes.
    
    This allows easy extension by registering new effect types
    without modifying existing code.
    """
    
    _effects: Dict[str, Type[EffectBase]] = {}
    
    @classmethod
    def register(cls, name: str, effect_class: Type[EffectBase]) -> None:
        """Register a new effect type.
        
        Args:
            name: Unique name for the effect
            effect_class: Effect class to register
        """
        cls._effects[name] = effect_class
    
    @classmethod
    def get(cls, name: str, intensity: float = 1.0) -> EffectBase:
        """Get an effect instance by name.
        
        Args:
            name: Name of the effect
            intensity: Intensity for the effect
            
        Returns:
            Instance of the effect
            
        Raises:
            ValueError: If effect name is not registered
        """
        if name not in cls._effects:
            raise ValueError(
                f"Unknown effect '{name}'. Available: {list(cls._effects.keys())}"
            )
        return cls._effects[name](intensity=intensity)
    
    @classmethod
    def list_available(cls) -> list[str]:
        """List all available effect names.
        
        Returns:
            List of registered effect names
        """
        return list(cls._effects.keys())
