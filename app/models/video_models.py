"""Pydantic models for video generation."""

from pydantic import BaseModel, Field, field_validator
from typing import List


class ImageTimestamp(BaseModel):
    """Model for an image with its timestamp."""
    
    timestamp: float = Field(..., description="Timestamp in seconds")
    image_path: str = Field(..., description="Local path to the image file")
    
    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Timestamp must be non-negative")
        return v


class VideoRequest(BaseModel):
    """Request model for video generation."""
    
    images: List[ImageTimestamp] = Field(
        ..., 
        min_length=2,
        description="List of images with timestamps (minimum 2 images)"
    )
    output_path: str = Field(
        ...,
        description="Local path where the video will be saved"
    )
    transition_type: str = Field(
        default="cross_dissolve",
        description="Type of transition to use between images"
    )
    fps: int = Field(
        default=30,
        ge=15,
        le=60,
        description="Frames per second for the output video"
    )
    resolution: tuple[int, int] = Field(
        default=(1280, 720),
        description="Output video resolution (width, height)"
    )
    
    @field_validator('images')
    @classmethod
    def validate_images_order(cls, v: List[ImageTimestamp]) -> List[ImageTimestamp]:
        """Ensure images are sorted by timestamp."""
        sorted_images = sorted(v, key=lambda x: x.timestamp)
        return sorted_images


class VideoResponse(BaseModel):
    """Response model for video generation."""
    
    success: bool
    output_path: str
    duration: float = Field(description="Duration of the generated video in seconds")
    message: str
    details: dict | None = None
