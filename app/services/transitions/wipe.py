"""Wipe transitions (directional wipes)."""

import numpy as np
from app.services.transitions.base import TransitionBase
from app.services.transitions.registry import TransitionRegistry


class WipeLeftTransition(TransitionBase):
    """Wipe from right to left."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Calculate wipe position
        wipe_pos = int(w * progress)
        
        # Create result frame
        result = frame1.copy()
        
        # Replace left portion with frame2
        if wipe_pos > 0:
            result[:, :wipe_pos] = frame2[:, :wipe_pos]
        
        return result


class WipeRightTransition(TransitionBase):
    """Wipe from left to right."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Calculate wipe position
        wipe_pos = int(w * (1 - progress))
        
        # Create result frame
        result = frame1.copy()
        
        # Replace right portion with frame2
        if wipe_pos < w:
            result[:, wipe_pos:] = frame2[:, wipe_pos:]
        
        return result


class WipeUpTransition(TransitionBase):
    """Wipe from bottom to top."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Calculate wipe position
        wipe_pos = int(h * progress)
        
        # Create result frame
        result = frame1.copy()
        
        # Replace top portion with frame2
        if wipe_pos > 0:
            result[:wipe_pos, :] = frame2[:wipe_pos, :]
        
        return result


class WipeDownTransition(TransitionBase):
    """Wipe from top to bottom."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Calculate wipe position
        wipe_pos = int(h * (1 - progress))
        
        # Create result frame
        result = frame1.copy()
        
        # Replace bottom portion with frame2
        if wipe_pos < h:
            result[wipe_pos:, :] = frame2[wipe_pos:, :]
        
        return result


# Register transitions
TransitionRegistry.register('wipe_left', WipeLeftTransition)
TransitionRegistry.register('wipe_right', WipeRightTransition)
TransitionRegistry.register('wipe_up', WipeUpTransition)
TransitionRegistry.register('wipe_down', WipeDownTransition)
