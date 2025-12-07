"""Base class for all effects (continuous movements)."""

from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple


class EffectBase(ABC):
    """Abstract base class for video effects (continuous movements).
    
    Effects are applied during the entire duration of an image display,
    unlike transitions which occur between images.
    
    Examples: pan, continuous zoom, rotation
    """
    
    def __init__(self, intensity: float = 1.0):
        """Initialize effect.
        
        Args:
            intensity: Effect intensity (0.0 to 1.0+)
        """
        self.intensity = intensity
    
    @abstractmethod
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply effect to a frame at a given progress.
        
        Args:
            frame: Original frame (numpy array) - can be larger than frame_size
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Modified frame as numpy array with size = frame_size
        """
        pass
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """Smooth easing function for natural movement.
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Eased progress
        """
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear easing (no easing).
        
        Args:
            t: Progress from 0.0 to 1.0
            
        Returns:
            Same progress (linear)
        """
        return t
