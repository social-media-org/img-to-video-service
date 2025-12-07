"""Service for generating videos from images with transitions.

This service is designed to be testable independently without launching the API.
"""

import os
from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np
from moviepy import VideoClip, concatenate_videoclips
from PIL import Image

from app.services.transitions.registry import TransitionRegistry
from app.models.video_models import ImageTimestamp
from app.core.logging import get_logger

logger = get_logger(__name__)


class VideoGeneratorService:
    """Service to generate videos from images with transitions."""
    
    def __init__(self, 
                 fps: int = 30,
                 resolution: Tuple[int, int] = (1280, 720),
                 transition_duration: float = 0.5):
        """Initialize the video generator service.
        
        Args:
            fps: Frames per second for output video
            resolution: Output resolution (width, height)
            transition_duration: Duration of transitions in seconds
        """
        self.fps = fps
        self.resolution = resolution
        self.transition_duration = transition_duration
        
    def generate_video(self,
                      images: List[ImageTimestamp],
                      output_path: str,
                      transition_type: str = "cross_dissolve") -> dict:
        """Generate a video from a list of images with transitions.
        
        Args:
            images: List of ImageTimestamp objects (must be sorted by timestamp)
            output_path: Path where the video will be saved
            transition_type: Type of transition to use
            
        Returns:
            Dictionary with generation details
            
        Raises:
            ValueError: If images list is invalid or paths don't exist
            RuntimeError: If video generation fails
        """
        logger.info(f"Starting video generation with {len(images)} images")
        
        # Validate inputs
        self._validate_inputs(images, output_path)
        
        try:
            # Load and prepare images
            frames_data = self._load_images(images)
            
            # Get transition instance
            transition = TransitionRegistry.get(transition_type, self.transition_duration)
            logger.info(f"Using transition: {transition_type}")
            
            # Create video clips
            clips = []
            total_duration = 0
            
            for i in range(len(frames_data)):
                frame_data = frames_data[i]
                
                # Calculate duration for this image
                if i < len(images) - 1:
                    # Duration until next timestamp
                    duration = images[i + 1].timestamp - images[i].timestamp
                else:
                    # Last image: use same duration as previous or default 3 seconds
                    if i > 0:
                        duration = images[i].timestamp - images[i - 1].timestamp
                    else:
                        duration = 3.0
                
                # Create clip for static image
                if duration > self.transition_duration:
                    static_duration = duration - self.transition_duration
                    static_clip = self._create_static_clip(
                        frame_data['frame'],
                        static_duration
                    )
                    clips.append(static_clip)
                    total_duration += static_duration
                
                # Create transition clip (except for last image)
                if i < len(frames_data) - 1:
                    transition_clip = self._create_transition_clip(
                        frame_data['frame'],
                        frames_data[i + 1]['frame'],
                        transition
                    )
                    clips.append(transition_clip)
                    total_duration += self.transition_duration
            
            # Concatenate all clips
            logger.info(f"Concatenating {len(clips)} clips")
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Write video file
            logger.info(f"Writing video to {output_path}")
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio=False,
                logger=None
            )
            
            logger.info(f"Video generated successfully: {output_path}")
            
            return {
                "success": True,
                "output_path": output_path,
                "duration": total_duration,
                "num_images": len(images),
                "transition_type": transition_type,
                "resolution": self.resolution,
                "fps": self.fps
            }
            
        except Exception as e:
            logger.error(f"Error generating video: {str(e)}")
            raise RuntimeError(f"Failed to generate video: {str(e)}")
    
    def _validate_inputs(self, images: List[ImageTimestamp], output_path: str) -> None:
        """Validate input parameters.
        
        Args:
            images: List of images to validate
            output_path: Output path to validate
            
        Raises:
            ValueError: If validation fails
        """
        if not images or len(images) < 2:
            raise ValueError("At least 2 images are required")
        
        # Check if all image files exist
        for img in images:
            if not os.path.exists(img.image_path):
                raise ValueError(f"Image file not found: {img.image_path}")
        
        # Check output path
        if not output_path:
            raise ValueError("Output path cannot be empty")
        
        # Check if output directory is writable
        output_dir = os.path.dirname(os.path.abspath(output_path))
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                raise ValueError(f"Cannot create output directory: {e}")
    
    def _load_images(self, images: List[ImageTimestamp]) -> List[dict]:
        """Load and prepare all images.
        
        Args:
            images: List of ImageTimestamp objects
            
        Returns:
            List of dictionaries with loaded frames
        """
        frames_data = []
        
        for img in images:
            logger.info(f"Loading image: {img.image_path}")
            
            # Load image with PIL then convert to numpy array
            pil_image = Image.open(img.image_path)
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert to numpy array
            frame = np.array(pil_image)
            
            # Resize to target resolution
            frame = cv2.resize(frame, self.resolution)
            
            frames_data.append({
                'frame': frame,
                'timestamp': img.timestamp,
                'path': img.image_path
            })
        
        return frames_data
    
    def _create_static_clip(self, frame: np.ndarray, duration: float) -> VideoClip:
        """Create a static video clip from a single frame.
        
        Args:
            frame: Frame as numpy array
            duration: Duration in seconds
            
        Returns:
            VideoClip instance
        """
        def make_frame(t):
            return frame
        
        return VideoClip(make_frame, duration=duration)
    
    def _create_transition_clip(self,
                               frame1: np.ndarray,
                               frame2: np.ndarray,
                               transition: 'TransitionBase') -> VideoClip:
        """Create a transition clip between two frames.
        
        Args:
            frame1: First frame
            frame2: Second frame
            transition: Transition instance to apply
            
        Returns:
            VideoClip with transition effect
        """
        duration = self.transition_duration
        
        def make_frame(t):
            progress = t / duration
            progress = max(0.0, min(1.0, progress))  # Clamp to [0, 1]
            return transition.apply(frame1, frame2, progress)
        
        return VideoClip(make_frame, duration=duration)
    
    @staticmethod
    def list_available_transitions() -> List[str]:
        """List all available transition types.
        
        Returns:
            List of transition names
        """
        return TransitionRegistry.list_available()
