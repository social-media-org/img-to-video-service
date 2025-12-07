"""Zoom transitions (Zoom In, Zoom Out, Smooth Zoom)."""

import numpy as np
import cv2
from app.services.transitions.base import TransitionBase
from app.services.transitions.registry import TransitionRegistry


class ZoomInTransition(TransitionBase):
    """Zoom in transition - zooms into the first image while fading to second.
    
    Creates a dynamic effect where the first image zooms in as the
    second image fades in.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Zoom factor (1.0 to 1.5)
        zoom = 1.0 + progress * 0.5
        
        # Calculate crop region for zoom effect
        new_h, new_w = int(h / zoom), int(w / zoom)
        y1 = (h - new_h) // 2
        x1 = (w - new_w) // 2
        
        # Crop and resize frame1 to create zoom effect
        cropped = frame1[y1:y1+new_h, x1:x1+new_w]
        zoomed_frame1 = cv2.resize(cropped, (w, h))
        
        # Blend with frame2
        return self.blend_frames(zoomed_frame1, frame2, progress)


class ZoomOutTransition(TransitionBase):
    """Zoom out transition - zooms out from first image while fading to second."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Zoom factor (1.5 to 1.0)
        zoom = 1.5 - progress * 0.5
        
        # Calculate crop region
        new_h, new_w = int(h / zoom), int(w / zoom)
        y1 = (h - new_h) // 2
        x1 = (w - new_w) // 2
        
        # Crop and resize
        cropped = frame1[y1:y1+new_h, x1:x1+new_w]
        zoomed_frame1 = cv2.resize(cropped, (w, h))
        
        # Blend
        return self.blend_frames(zoomed_frame1, frame2, progress)


class SmoothZoomTransition(TransitionBase):
    """Smooth zoom transition (TikTok style).
    
    Combines zoom with smooth easing for a more natural feel.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        # Smooth easing function (ease-in-out)
        eased_progress = self._ease_in_out(progress)
        
        h, w = frame1.shape[:2]
        
        # Zoom factor with easing
        zoom = 1.0 + eased_progress * 0.3
        
        # Zoom frame1
        new_h, new_w = int(h / zoom), int(w / zoom)
        y1 = (h - new_h) // 2
        x1 = (w - new_w) // 2
        cropped = frame1[y1:y1+new_h, x1:x1+new_w]
        zoomed_frame1 = cv2.resize(cropped, (w, h))
        
        # Blend with smooth alpha
        return self.blend_frames(zoomed_frame1, frame2, eased_progress)
    
    @staticmethod
    def _ease_in_out(t: float) -> float:
        """Smooth easing function."""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2


# Register transitions
TransitionRegistry.register('zoom_in', ZoomInTransition)
TransitionRegistry.register('zoom_out', ZoomOutTransition)
TransitionRegistry.register('smooth_zoom', SmoothZoomTransition)
