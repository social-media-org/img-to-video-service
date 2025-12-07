"""Fade transitions (Cross Dissolve, Flash, etc.)."""

import numpy as np
from app.services.transitions.base import TransitionBase
from app.services.transitions.registry import TransitionRegistry


class CrossDissolveTransition(TransitionBase):
    """Classic cross dissolve / fade transition.
    
    Smoothly fades from one image to another using alpha blending.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        # Simple linear alpha blend
        return self.blend_frames(frame1, frame2, progress)


class FlashWhiteTransition(TransitionBase):
    """Flash white transition popular on TikTok.
    
    Quickly flashes to white before showing the next image.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        # Create white frame
        white_frame = np.ones_like(frame1) * 255
        
        if progress < 0.5:
            # First half: fade to white
            alpha = progress * 2  # 0 to 1
            return self.blend_frames(frame1, white_frame, alpha)
        else:
            # Second half: fade from white to frame2
            alpha = (progress - 0.5) * 2  # 0 to 1
            return self.blend_frames(white_frame, frame2, alpha)


class FadeToBlackTransition(TransitionBase):
    """Fade to black transition (cinematic).
    
    Fades to black then fades in the next image.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        # Create black frame
        black_frame = np.zeros_like(frame1)
        
        if progress < 0.5:
            # First half: fade to black
            alpha = progress * 2
            return self.blend_frames(frame1, black_frame, alpha)
        else:
            # Second half: fade from black
            alpha = (progress - 0.5) * 2
            return self.blend_frames(black_frame, frame2, alpha)


# Register transitions
TransitionRegistry.register('cross_dissolve', CrossDissolveTransition)
TransitionRegistry.register('fade', CrossDissolveTransition)  # Alias
TransitionRegistry.register('flash_white', FlashWhiteTransition)
TransitionRegistry.register('flash', FlashWhiteTransition)  # Alias
TransitionRegistry.register('fade_to_black', FadeToBlackTransition)
