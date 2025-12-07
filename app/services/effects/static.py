"""Static effect (no movement)."""

import numpy as np
import cv2
from typing import Tuple
from app.services.effects.base import EffectBase
from app.services.effects.registry import EffectRegistry


class StaticEffect(EffectBase):
    """Static effect - no movement, image stays centered.
    
    This is the default effect when no effect is specified.
    """
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply static effect (no movement).
        
        Args:
            frame: Original frame
            progress: Effect progress (unused for static)
            frame_size: Target frame size (width, height)
            
        Returns:
            Frame resized to frame_size
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # If frame is already the right size, return as is
        if w == target_w and h == target_h:
            return frame
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        if frame_ratio > target_ratio:
            # Frame is wider - fit to height
            new_h = target_h
            new_w = int(new_h * frame_ratio)
        else:
            # Frame is taller - fit to width
            new_w = target_w
            new_h = int(new_w / frame_ratio)
        
        # Resize frame
        resized = cv2.resize(frame, (new_w, new_h))
        
        # Crop to center
        y_start = (new_h - target_h) // 2
        x_start = (new_w - target_w) // 2
        
        cropped = resized[y_start:y_start+target_h, x_start:x_start+target_w]
        
        return cropped


# Register effect
EffectRegistry.register('static', StaticEffect)
EffectRegistry.register('none', StaticEffect)  # Alias
