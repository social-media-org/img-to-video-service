"""Rotation effects."""

import numpy as np
import cv2
from typing import Tuple
from app.services.effects.base import EffectBase
from app.services.effects.registry import EffectRegistry


class RotateClockwiseEffect(EffectBase):
    """Continuous clockwise rotation effect.
    
    Rotates the image smoothly in a clockwise direction during
    the entire display duration.
    """
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply clockwise rotation effect.
        
        Args:
            frame: Original frame
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Rotated and cropped frame
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # Apply smooth easing
        eased_progress = self.ease_in_out(progress)
        
        # Calculate rotation angle (0 to 360 degrees based on intensity)
        # Default intensity of 1.0 gives full 360° rotation
        max_angle = 360 * self.intensity
        angle = eased_progress * max_angle
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        # Resize frame to cover (with extra space for rotation)
        # We need to scale up a bit to avoid black corners after rotation
        scale_factor = 1.5  # Extra space for rotation
        
        if frame_ratio > target_ratio:
            new_h = int(target_h * scale_factor)
            new_w = int(new_h * frame_ratio)
        else:
            new_w = int(target_w * scale_factor)
            new_h = int(new_w / frame_ratio)
        
        # Resize frame
        resized = cv2.resize(frame, (new_w, new_h))
        
        # Get rotation matrix
        center = (new_w // 2, new_h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
        
        # Apply rotation
        rotated = cv2.warpAffine(
            resized, 
            rotation_matrix, 
            (new_w, new_h),
            borderMode=cv2.BORDER_REPLICATE
        )
        
        # Crop to target size from center
        x_start = (new_w - target_w) // 2
        y_start = (new_h - target_h) // 2
        
        cropped = rotated[y_start:y_start+target_h, x_start:x_start+target_w]
        
        return cropped


class RotateCounterClockwiseEffect(EffectBase):
    """Continuous counter-clockwise rotation effect.
    
    Rotates the image smoothly in a counter-clockwise direction during
    the entire display duration.
    """
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply counter-clockwise rotation effect.
        
        Args:
            frame: Original frame
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Rotated and cropped frame
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # Apply smooth easing
        eased_progress = self.ease_in_out(progress)
        
        # Calculate rotation angle (0 to 360 degrees based on intensity)
        max_angle = 360 * self.intensity
        angle = eased_progress * max_angle
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        # Resize frame to cover (with extra space for rotation)
        scale_factor = 1.5
        
        if frame_ratio > target_ratio:
            new_h = int(target_h * scale_factor)
            new_w = int(new_h * frame_ratio)
        else:
            new_w = int(target_w * scale_factor)
            new_h = int(new_w / frame_ratio)
        
        # Resize frame
        resized = cv2.resize(frame, (new_w, new_h))
        
        # Get rotation matrix (positive angle for counter-clockwise)
        center = (new_w // 2, new_h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Apply rotation
        rotated = cv2.warpAffine(
            resized, 
            rotation_matrix, 
            (new_w, new_h),
            borderMode=cv2.BORDER_REPLICATE
        )
        
        # Crop to target size from center
        x_start = (new_w - target_w) // 2
        y_start = (new_h - target_h) // 2
        
        cropped = rotated[y_start:y_start+target_h, x_start:x_start+target_w]
        
        return cropped


class RotateSlowEffect(EffectBase):
    """Slow rotation effect (subtle clockwise rotation).
    
    A very subtle rotation that adds just a hint of movement
    without being too distracting. Good for professional videos.
    """
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply slow rotation effect.
        
        Args:
            frame: Original frame
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Rotated and cropped frame
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # Apply smooth easing
        eased_progress = self.ease_in_out(progress)
        
        # Calculate rotation angle (very subtle: max 15 degrees)
        max_angle = 15 * self.intensity
        angle = eased_progress * max_angle
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        # Resize frame to cover (with extra space for rotation)
        scale_factor = 1.3
        
        if frame_ratio > target_ratio:
            new_h = int(target_h * scale_factor)
            new_w = int(new_h * frame_ratio)
        else:
            new_w = int(target_w * scale_factor)
            new_h = int(new_w / frame_ratio)
        
        # Resize frame
        resized = cv2.resize(frame, (new_w, new_h))
        
        # Get rotation matrix
        center = (new_w // 2, new_h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
        
        # Apply rotation
        rotated = cv2.warpAffine(
            resized, 
            rotation_matrix, 
            (new_w, new_h),
            borderMode=cv2.BORDER_REPLICATE
        )
        
        # Crop to target size from center
        x_start = (new_w - target_w) // 2
        y_start = (new_h - target_h) // 2
        
        cropped = rotated[y_start:y_start+target_h, x_start:x_start+target_w]
        
        return cropped


# Register rotation effects
EffectRegistry.register('rotate_cw', RotateClockwiseEffect)
EffectRegistry.register('rotate_ccw', RotateCounterClockwiseEffect)
EffectRegistry.register('rotate_slow', RotateSlowEffect)
