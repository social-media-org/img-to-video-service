"""Base class for all transitions."""

from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple


class TransitionBase(ABC):
    """Abstract base class for video transitions.
    
    All transition effects must inherit from this class and implement
    the apply() method.
    """
    
    def __init__(self, duration: float = 0.5):
        """Initialize transition.
        
        Args:
            duration: Duration of the transition in seconds
        """
        self.duration = duration
    
    @abstractmethod
    def apply(self, 
              frame1: np.ndarray, 
              frame2: np.ndarray, 
              progress: float) -> np.ndarray:
        """Apply transition effect between two frames.
        
        Args:
            frame1: First frame (numpy array)
            frame2: Second frame (numpy array)
            progress: Transition progress from 0.0 to 1.0
            
        Returns:
            Blended frame as numpy array
        """
        pass
    
    @staticmethod
    def ensure_same_size(frame1: np.ndarray, 
                         frame2: np.ndarray,
                         target_size: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray]:
        """Ensure both frames have the same size.
        
        Args:
            frame1: First frame
            frame2: Second frame
            target_size: Target size (width, height)
            
        Returns:
            Tuple of resized frames
        """
        import cv2
        
        if frame1.shape[:2] != target_size[::-1]:
            frame1 = cv2.resize(frame1, target_size)
        if frame2.shape[:2] != target_size[::-1]:
            frame2 = cv2.resize(frame2, target_size)
            
        return frame1, frame2
    
    @staticmethod
    def blend_frames(frame1: np.ndarray, 
                     frame2: np.ndarray, 
                     alpha: float) -> np.ndarray:
        """Simple alpha blending between two frames.
        
        Args:
            frame1: First frame
            frame2: Second frame
            alpha: Blend factor (0.0 = frame1, 1.0 = frame2)
            
        Returns:
            Blended frame
        """
        return (frame1 * (1 - alpha) + frame2 * alpha).astype(np.uint8)
