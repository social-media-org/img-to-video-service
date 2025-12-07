"""Registry for managing available transitions."""

from typing import Dict, Type
from app.services.transitions.base import TransitionBase


class TransitionRegistry:
    """Registry to store and retrieve transition classes.
    
    This allows easy extension by registering new transition types
    without modifying existing code.
    """
    
    _transitions: Dict[str, Type[TransitionBase]] = {}
    
    @classmethod
    def register(cls, name: str, transition_class: Type[TransitionBase]) -> None:
        """Register a new transition type.
        
        Args:
            name: Unique name for the transition
            transition_class: Transition class to register
        """
        cls._transitions[name] = transition_class
    
    @classmethod
    def get(cls, name: str, duration: float = 0.5) -> TransitionBase:
        """Get a transition instance by name.
        
        Args:
            name: Name of the transition
            duration: Duration for the transition
            
        Returns:
            Instance of the transition
            
        Raises:
            ValueError: If transition name is not registered
        """
        if name not in cls._transitions:
            raise ValueError(
                f"Unknown transition '{name}'. Available: {list(cls._transitions.keys())}"
            )
        return cls._transitions[name](duration=duration)
    
    @classmethod
    def list_available(cls) -> list[str]:
        """List all available transition names.
        
        Returns:
            List of registered transition names
        """
        return list(cls._transitions.keys())
