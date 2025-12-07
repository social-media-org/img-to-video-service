"""Smooth transitions (TikTok/CapCut style)."""

import numpy as np
import cv2
from app.services.transitions.base import TransitionBase
from app.services.transitions.registry import TransitionRegistry


class SmoothSlideTransition(TransitionBase):
    """Smooth slide transition with easing."""
    
    def __init__(self, duration: float = 0.5, direction: str = 'left'):
        super().__init__(duration)
        self.direction = direction
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Ease-in-out function for smooth movement
        eased = self._ease_in_out_cubic(progress)
        
        if self.direction == 'left':
            offset = int(w * eased)
            result = np.zeros_like(frame1)
            
            # Slide frame1 to the left
            if offset < w:
                result[:, :w-offset] = frame1[:, offset:]
            
            # Slide frame2 from the right
            result[:, w-offset:] = frame2[:, :offset]
            
        elif self.direction == 'right':
            offset = int(w * eased)
            result = np.zeros_like(frame1)
            
            # Slide frame1 to the right
            if offset < w:
                result[:, offset:] = frame1[:, :w-offset]
            
            # Slide frame2 from the left
            result[:, :offset] = frame2[:, w-offset:]
            
        else:
            result = frame1
        
        return result
    
    @staticmethod
    def _ease_in_out_cubic(t: float) -> float:
        """Cubic easing function for smooth acceleration/deceleration."""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2


class SmoothFlipTransition(TransitionBase):
    """Smooth flip/rotation transition."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Ease the progress
        eased = self._ease_in_out(progress)
        
        # Calculate scale factor for flip effect
        if eased < 0.5:
            # First half: scale down frame1
            scale = 1.0 - (eased * 2)
            current_frame = frame1
        else:
            # Second half: scale up frame2
            scale = (eased - 0.5) * 2
            current_frame = frame2
        
        # Apply horizontal flip effect
        new_w = max(1, int(w * scale))
        resized = cv2.resize(current_frame, (new_w, h))
        
        # Center the resized frame
        result = np.zeros_like(frame1)
        x_offset = (w - new_w) // 2
        
        if new_w > 0:
            result[:, x_offset:x_offset+new_w] = resized
        
        # Blend edges for smooth transition
        if 0.4 < eased < 0.6:
            alpha = abs(eased - 0.5) * 2
            result = self.blend_frames(frame1, frame2, alpha)
        
        return result
    
    @staticmethod
    def _ease_in_out(t: float) -> float:
        """Quadratic easing."""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2


class SmoothStretchTransition(TransitionBase):
    """Smooth stretch transition (scale effect)."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Ease progress
        eased = self._ease_out_back(progress)
        
        # Scale frame1 down while frame2 scales up
        scale1 = 1.0 - eased * 0.5
        scale2 = eased
        
        # Resize frames
        new_h1, new_w1 = max(1, int(h * scale1)), max(1, int(w * scale1))
        new_h2, new_w2 = max(1, int(h * scale2)), max(1, int(w * scale2))
        
        resized1 = cv2.resize(frame1, (new_w1, new_h1))
        resized2 = cv2.resize(frame2, (new_w2, new_h2))
        
        # Create result and center frames
        result = np.zeros_like(frame1)
        
        # Place frame1
        y1, x1 = (h - new_h1) // 2, (w - new_w1) // 2
        result[y1:y1+new_h1, x1:x1+new_w1] = resized1
        
        # Blend frame2 on top
        y2, x2 = (h - new_h2) // 2, (w - new_w2) // 2
        if new_h2 > 0 and new_w2 > 0:
            # Alpha blend the overlapping region
            alpha = eased
            result[y2:y2+new_h2, x2:x2+new_w2] = self.blend_frames(
                result[y2:y2+new_h2, x2:x2+new_w2],
                resized2,
                alpha
            )
        
        return result
    
    @staticmethod
    def _ease_out_back(t: float) -> float:
        """Ease out with overshoot for bouncy effect."""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


class SmoothLeftSlideTransition(SmoothSlideTransition):
    def __init__(self, duration: float = 0.5):
        super().__init__(duration, direction='left')


class SmoothRightSlideTransition(SmoothSlideTransition):
    def __init__(self, duration: float = 0.5):
        super().__init__(duration, direction='right')


# Register transitions
TransitionRegistry.register('smooth_slide_left', SmoothLeftSlideTransition)
TransitionRegistry.register('smooth_slide_right', SmoothRightSlideTransition)
TransitionRegistry.register('smooth_flip', SmoothFlipTransition)
TransitionRegistry.register('smooth_stretch', SmoothStretchTransition)
