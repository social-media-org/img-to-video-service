"""API routes for video generation."""

from fastapi import APIRouter, HTTPException, status
from app.models.video_models import VideoRequest, VideoResponse
from app.services.video_generator_service import VideoGeneratorService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("/generate", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def generate_video(request: VideoRequest) -> VideoResponse:
    """Generate a video from images with transitions.
    
    Args:
        request: Video generation request with images and settings
        
    Returns:
        VideoResponse with generation details
        
    Raises:
        HTTPException: If video generation fails
    """
    logger.info(f"Received video generation request: {len(request.images)} images")
    
    try:
        # Create video generator service
        service = VideoGeneratorService(
            fps=request.fps,
            resolution=request.resolution,
            transition_duration=0.5  # Default transition duration
        )
        
        # Generate video
        result = service.generate_video(
            images=request.images,
            output_path=request.output_path,
            transition_type=request.transition_type
        )
        
        logger.info(f"Video generated successfully: {result['output_path']}")
        
        return VideoResponse(
            success=True,
            output_path=result['output_path'],
            duration=result['duration'],
            message="Video generated successfully",
            details={
                "num_images": result['num_images'],
                "transition_type": result['transition_type'],
                "resolution": result['resolution'],
                "fps": result['fps']
            }
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/transitions", response_model=dict)
async def list_transitions() -> dict:
    """List all available transition types.
    
    Returns:
        Dictionary with available transitions
    """
    transitions = VideoGeneratorService.list_available_transitions()
    
    return {
        "transitions": transitions,
        "count": len(transitions)
    }


@router.get("/effects", response_model=dict)
async def list_effects() -> dict:
    """List all available effect types.
    
    Returns:
        Dictionary with available effects
    """
    effects = VideoGeneratorService.list_available_effects()
    
    return {
        "effects": effects,
        "count": len(effects)
    }
