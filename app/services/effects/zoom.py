"""Continuous zoom effects."""

import numpy as np
import cv2
from typing import Tuple
from app.services.effects.base import EffectBase
from app.services.effects.registry import EffectRegistry


class ZoomInContinuousEffect(EffectBase):
    """Continuous zoom in effect - zooms into the image during its entire display duration.
    
    Creates a smooth, continuous zoom effect that makes the video more dynamic.
    The image gradually zooms in from normal size to a larger view.
    """
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply continuous zoom in effect.
        
        Args:
            frame: Original frame
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Zoomed and cropped frame
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # Apply smooth easing
        eased_progress = self.ease_in_out(progress)
        
        # Zoom factor: starts at 1.0, increases based on intensity
        # Default intensity of 1.0 gives max zoom of 1.3x
        max_zoom = 1.0 + (0.3 * self.intensity)
        zoom = 1.0 + eased_progress * (max_zoom - 1.0)
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        # First, resize frame to cover the target size
        if frame_ratio > target_ratio:
            new_h = target_h
            new_w = int(new_h * frame_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / frame_ratio)
        
        # Apply additional zoom
        zoom_w = int(new_w * zoom)
        zoom_h = int(new_h * zoom)
        
        # Resize with zoom
        resized = cv2.resize(frame, (zoom_w, zoom_h))
        
        # Crop from center
        x_start = (zoom_w - target_w) // 2
        y_start = (zoom_h - target_h) // 2
        
        cropped = resized[y_start:y_start+target_h, x_start:x_start+target_w]
        
        return cropped


class ZoomOutContinuousEffect(EffectBase):
    """Continuous zoom out effect - zooms out from the image during its entire display duration.
    
    Creates a smooth, continuous zoom out effect. The image starts zoomed in
    and gradually zooms out to normal size.
    """
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply continuous zoom out effect.
        
        Args:
            frame: Original frame
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Zoomed and cropped frame
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # Apply smooth easing
        eased_progress = self.ease_in_out(progress)
        
        # Zoom factor: starts high, decreases to 1.0
        max_zoom = 1.0 + (0.3 * self.intensity)
        zoom = max_zoom - eased_progress * (max_zoom - 1.0)
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        # First, resize frame to cover the target size
        if frame_ratio > target_ratio:
            new_h = target_h
            new_w = int(new_h * frame_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / frame_ratio)
        
        # Apply zoom
        zoom_w = int(new_w * zoom)
        zoom_h = int(new_h * zoom)
        
        # Resize with zoom
        resized = cv2.resize(frame, (zoom_w, zoom_h))
        
        # Crop from center
        x_start = (zoom_w - target_w) // 2
        y_start = (zoom_h - target_h) // 2
        
        cropped = resized[y_start:y_start+target_h, x_start:x_start+target_w]
        
        return cropped


class ZoomInOutEffect(EffectBase):
    """Zoom in then out effect - creates a breathing effect.
    
    The image zooms in during the first half, then zooms back out during
    the second half, creating a dynamic "breathing" motion.
    """
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply zoom in/out effect.
        
        Args:
            frame: Original frame
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Zoomed and cropped frame
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # Apply smooth easing
        eased_progress = self.ease_in_out(progress)
        
        # Calculate zoom factor (in at first half, out at second half)
        max_zoom = 1.0 + (0.2 * self.intensity)
        if eased_progress < 0.5:
            # First half: zoom in
            zoom = 1.0 + (eased_progress * 2) * (max_zoom - 1.0)
        else:
            # Second half: zoom out
            zoom = max_zoom - ((eased_progress - 0.5) * 2) * (max_zoom - 1.0)
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        # Resize frame to cover the target size
        if frame_ratio > target_ratio:
            new_h = target_h
            new_w = int(new_h * frame_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / frame_ratio)
        
        # Apply zoom
        zoom_w = int(new_w * zoom)
        zoom_h = int(new_h * zoom)
        
        # Resize with zoom
        resized = cv2.resize(frame, (zoom_w, zoom_h))
        
        # Crop from center
        x_start = (zoom_w - target_w) // 2
        y_start = (zoom_h - target_h) // 2
        
        cropped = resized[y_start:y_start+target_h, x_start:x_start+target_w]
        
        return cropped


# Register zoom effects
EffectRegistry.register('zoom_in_continuous', ZoomInContinuousEffect)
EffectRegistry.register('zoom_out_continuous', ZoomOutContinuousEffect)
EffectRegistry.register('zoom_in_out', ZoomInOutEffect)
EffectRegistry.register('breathing', ZoomInOutEffect)  # Alias
