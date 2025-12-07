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


class SmoothSpinTransition(TransitionBase):
    """Smooth spin transition with rotation and zoom (TikTok style).
    
    Combines rotation and zoom with smooth easing for a dynamic effect.
    Very popular on TikTok and Instagram Reels.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Smooth easing
        eased = self._ease_in_out_quad(progress)
        
        # Rotation angle (0 to 360 degrees)
        angle = eased * 360
        
        # Zoom factor (1.0 to 1.3)
        zoom = 1.0 + eased * 0.3
        
        # Get rotation matrix
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, zoom)
        
        # Apply rotation and zoom to frame1
        rotated_frame1 = cv2.warpAffine(frame1, rotation_matrix, (w, h), 
                                        borderMode=cv2.BORDER_CONSTANT,
                                        borderValue=(0, 0, 0))
        
        # Blend with frame2 using eased alpha
        return self.blend_frames(rotated_frame1, frame2, eased)
    
    @staticmethod
    def _ease_in_out_quad(t: float) -> float:
        """Quadratic easing for smooth acceleration/deceleration."""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2


class GlitchTransition(TransitionBase):
    """Glitch transition with RGB channel separation (modern digital style).
    
    Creates a digital glitch effect by separating and shifting RGB channels.
    Very trendy for tech, gaming, and modern content.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Use ease-in-out for smooth glitch intensity
        eased = self._ease_in_out_sine(progress)
        
        # Glitch is strongest in the middle of the transition
        glitch_intensity = 1.0 - abs(eased - 0.5) * 2  # 0 -> 1 -> 0
        
        # Base blend between frames
        blended = self.blend_frames(frame1, frame2, eased)
        
        # Apply glitch effect if intensity is significant
        if glitch_intensity > 0.1:
            # Separate RGB channels
            b, g, r = cv2.split(blended)
            
            # Calculate shift amounts based on intensity
            shift = int(w * 0.02 * glitch_intensity)  # Max 2% of width
            
            # Shift red channel right
            r_shifted = np.zeros_like(r)
            if shift < w:
                r_shifted[:, shift:] = r[:, :w-shift]
            
            # Shift blue channel left
            b_shifted = np.zeros_like(b)
            if shift < w:
                b_shifted[:, :w-shift] = b[:, shift:]
            
            # Keep green channel as is
            g_shifted = g
            
            # Merge channels back
            glitched = cv2.merge([b_shifted, g_shifted, r_shifted])
            
            # Blend glitched effect with original based on intensity
            result = self.blend_frames(blended, glitched, glitch_intensity * 0.6)
            
            return result
        else:
            return blended
    
    @staticmethod
    def _ease_in_out_sine(t: float) -> float:
        """Sine easing for very smooth transitions."""
        return -(np.cos(np.pi * t) - 1) / 2


class BlurZoomTransition(TransitionBase):
    """Blur zoom transition with motion blur effect (CapCut style).
    
    Combines zoom with directional blur for a professional motion effect.
    Creates smooth, cinematic transitions.
    """
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Smooth easing
        eased = self._ease_in_out_cubic(progress)
        
        # Zoom factor
        zoom = 1.0 + eased * 0.4
        
        # Calculate crop for zoom
        new_h, new_w = int(h / zoom), int(w / zoom)
        y1 = (h - new_h) // 2
        x1 = (w - new_w) // 2
        
        # Crop and resize frame1
        cropped = frame1[y1:y1+new_h, x1:x1+new_w]
        zoomed_frame1 = cv2.resize(cropped, (w, h))
        
        # Apply radial blur effect based on progress
        # Blur is strongest in the middle of transition
        blur_intensity = 1.0 - abs(eased - 0.5) * 2  # 0 -> 1 -> 0
        
        if blur_intensity > 0.2:
            # Calculate blur kernel size (must be odd)
            kernel_size = int(15 * blur_intensity)
            if kernel_size % 2 == 0:
                kernel_size += 1
            kernel_size = max(3, kernel_size)
            
            # Apply motion blur
            zoomed_frame1 = cv2.GaussianBlur(zoomed_frame1, (kernel_size, kernel_size), 0)
        
        # Blend with frame2
        return self.blend_frames(zoomed_frame1, frame2, eased)
    
    @staticmethod
    def _ease_in_out_cubic(t: float) -> float:
        """Cubic easing for smooth motion."""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2


# Register transitions
TransitionRegistry.register('smooth_slide_left', SmoothLeftSlideTransition)
TransitionRegistry.register('smooth_slide_right', SmoothRightSlideTransition)
TransitionRegistry.register('smooth_flip', SmoothFlipTransition)
TransitionRegistry.register('smooth_stretch', SmoothStretchTransition)
TransitionRegistry.register('smooth_spin', SmoothSpinTransition)
TransitionRegistry.register('spin', SmoothSpinTransition)  # Alias
TransitionRegistry.register('glitch', GlitchTransition)
TransitionRegistry.register('blur_zoom', BlurZoomTransition)
