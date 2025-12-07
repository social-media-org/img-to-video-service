"""Pan effects (panoramic movements)."""

import numpy as np
import cv2
from typing import Tuple
from app.services.effects.base import EffectBase
from app.services.effects.registry import EffectRegistry


class PanEffect(EffectBase):
    """Base pan effect with configurable direction.
    
    Pan effects smoothly move across an image, revealing parts that
    would otherwise be cropped out. Perfect for images larger than
    the video resolution.
    """
    
    def __init__(self, intensity: float = 1.0, direction: str = 'right'):
        """Initialize pan effect.
        
        Args:
            intensity: Pan intensity (0.0 to 1.0+)
            direction: Pan direction ('right', 'left', 'up', 'down', 
                      'diagonal_tr', 'diagonal_tl', 'diagonal_br', 'diagonal_bl')
        """
        super().__init__(intensity)
        self.direction = direction
    
    def apply(self, 
              frame: np.ndarray, 
              progress: float,
              frame_size: Tuple[int, int]) -> np.ndarray:
        """Apply pan effect.
        
        Args:
            frame: Original frame (can be larger than frame_size)
            progress: Effect progress from 0.0 to 1.0
            frame_size: Target frame size (width, height)
            
        Returns:
            Cropped frame with pan effect applied
        """
        h, w = frame.shape[:2]
        target_w, target_h = frame_size
        
        # Apply smooth easing for natural movement
        eased_progress = self.ease_in_out(progress)
        
        # Calculate aspect ratios
        frame_ratio = w / h
        target_ratio = target_w / target_h
        
        # Resize frame to cover the target size (maintaining aspect ratio)
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
        
        # Calculate maximum movement range
        max_x_movement = max(0, new_w - target_w)
        max_y_movement = max(0, new_h - target_h)
        
        # Calculate pan offset based on direction and progress
        x_offset, y_offset = self._calculate_offset(
            eased_progress,
            max_x_movement,
            max_y_movement
        )
        
        # Crop the frame at the calculated offset
        cropped = resized[y_offset:y_offset+target_h, x_offset:x_offset+target_w]
        
        return cropped
    
    def _calculate_offset(self, 
                         progress: float, 
                         max_x: int, 
                         max_y: int) -> Tuple[int, int]:
        """Calculate pan offset based on direction.
        
        Args:
            progress: Eased progress (0.0 to 1.0)
            max_x: Maximum horizontal movement
            max_y: Maximum vertical movement
            
        Returns:
            Tuple of (x_offset, y_offset)
        """
        # Apply intensity to movement range
        max_x = int(max_x * self.intensity)
        max_y = int(max_y * self.intensity)
        
        if self.direction == 'right':
            # Pan from left to right
            x_offset = int(progress * max_x)
            y_offset = max_y // 2
            
        elif self.direction == 'left':
            # Pan from right to left
            x_offset = int((1 - progress) * max_x)
            y_offset = max_y // 2
            
        elif self.direction == 'down':
            # Pan from top to bottom
            x_offset = max_x // 2
            y_offset = int(progress * max_y)
            
        elif self.direction == 'up':
            # Pan from bottom to top
            x_offset = max_x // 2
            y_offset = int((1 - progress) * max_y)
            
        elif self.direction == 'diagonal_br':
            # Pan from top-left to bottom-right
            x_offset = int(progress * max_x)
            y_offset = int(progress * max_y)
            
        elif self.direction == 'diagonal_bl':
            # Pan from top-right to bottom-left
            x_offset = int((1 - progress) * max_x)
            y_offset = int(progress * max_y)
            
        elif self.direction == 'diagonal_tr':
            # Pan from bottom-left to top-right
            x_offset = int(progress * max_x)
            y_offset = int((1 - progress) * max_y)
            
        elif self.direction == 'diagonal_tl':
            # Pan from bottom-right to top-left
            x_offset = int((1 - progress) * max_x)
            y_offset = int((1 - progress) * max_y)
            
        else:
            # Default: center
            x_offset = max_x // 2
            y_offset = max_y // 2
        
        return x_offset, y_offset


# Create specific pan effect classes
class PanRightEffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='right')


class PanLeftEffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='left')


class PanUpEffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='up')


class PanDownEffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='down')


class PanDiagonalTREffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='diagonal_tr')


class PanDiagonalTLEffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='diagonal_tl')


class PanDiagonalBREffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='diagonal_br')


class PanDiagonalBLEffect(PanEffect):
    def __init__(self, intensity: float = 1.0):
        super().__init__(intensity, direction='diagonal_bl')


# Register all pan effects
EffectRegistry.register('pan_right', PanRightEffect)
EffectRegistry.register('pan_left', PanLeftEffect)
EffectRegistry.register('pan_up', PanUpEffect)
EffectRegistry.register('pan_down', PanDownEffect)
EffectRegistry.register('pan_diagonal_tr', PanDiagonalTREffect)
EffectRegistry.register('pan_diagonal_tl', PanDiagonalTLEffect)
EffectRegistry.register('pan_diagonal_br', PanDiagonalBREffect)
EffectRegistry.register('pan_diagonal_bl', PanDiagonalBLEffect)
