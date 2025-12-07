#!/usr/bin/env python3
"""
Script de test pour les nouveaux effets (mouvements continus).

Ce script teste:
1. Les effets de pan (panoramique)
2. Les effets de zoom continu
3. Les effets de rotation
4. La combinaison effets + transitions

Usage:
    python test_effects.py
"""

import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.video_generator_service import VideoGeneratorService
from app.services.effects.registry import EffectRegistry
from app.models.video_models import ImageTimestamp


def get_test_images(image_dir: str = "./resources/test_images") -> list[str]:
    """Get test images from directory.
    
    Args:
        image_dir: Directory containing test images
        
    Returns:
        List of image paths
    """
    print(f"📸 Récupération des images de test depuis: {image_dir}")
    image_paths = []
    valid_extensions = {".png", ".jpg", ".jpeg"}
    
    for root, _, files in os.walk(image_dir):
        for file in files:
            if Path(file).suffix.lower() in valid_extensions:
                filepath = os.path.join(root, file)
                image_paths.append(filepath)
    
    image_paths.sort()
    print(f"   ✓ {len(image_paths)} images trouvées")
    return image_paths


def test_pan_effects():
    """Test pan effects."""
    print("\n" + "="*60)
    print("TEST 1: Pan Effects (Panoramique)")
    print("="*60)
    
    images = get_test_images()
    if len(images) < 3:
        print("⚠️  Besoin d'au moins 3 images pour ce test")
        return
    
    # Take first 3 images
    test_images = images[:3]
    
    # Create video with different pan effects
    video_images = [
        ImageTimestamp(
            timestamp=0.0,
            image_path=test_images[0],
            effect="pan_right",
            effect_intensity=1.0
        ),
        ImageTimestamp(
            timestamp=3.0,
            image_path=test_images[1],
            effect="pan_down",
            effect_intensity=1.0
        ),
        ImageTimestamp(
            timestamp=6.0,
            image_path=test_images[2],
            effect="pan_diagonal_br",
            effect_intensity=1.0
        ),
    ]
    
    output_path = "./resources/test_videos/test_pan_effects.mp4"
    
    print(f"\n📹 Génération vidéo avec effets de pan...")
    print(f"   • Image 1: pan_right")
    print(f"   • Image 2: pan_down")
    print(f"   • Image 3: pan_diagonal_br")
    
    service = VideoGeneratorService(fps=30, resolution=(1280, 720))
    result = service.generate_video(
        images=video_images,
        output_path=output_path,
        transition_type="fade"
    )
    
    print(f"\n✅ Vidéo générée: {result['output_path']}")
    print(f"   • Durée: {result['duration']:.2f}s")
    print(f"   • Résolution: {result['resolution']}")


def test_zoom_effects():
    """Test continuous zoom effects."""
    print("\n" + "="*60)
    print("TEST 2: Zoom Continu")
    print("="*60)
    
    images = get_test_images()
    if len(images) < 3:
        print("⚠️  Besoin d'au moins 3 images pour ce test")
        return
    
    test_images = images[:3]
    
    video_images = [
        ImageTimestamp(
            timestamp=0.0,
            image_path=test_images[0],
            effect="zoom_in_continuous",
            effect_intensity=1.0
        ),
        ImageTimestamp(
            timestamp=3.0,
            image_path=test_images[1],
            effect="zoom_out_continuous",
            effect_intensity=1.0
        ),
        ImageTimestamp(
            timestamp=6.0,
            image_path=test_images[2],
            effect="zoom_in_out",
            effect_intensity=1.0
        ),
    ]
    
    output_path = "./resources/test_videos/test_zoom_effects.mp4"
    
    print(f"\n📹 Génération vidéo avec effets de zoom...")
    print(f"   • Image 1: zoom_in_continuous")
    print(f"   • Image 2: zoom_out_continuous")
    print(f"   • Image 3: zoom_in_out (breathing)")
    
    service = VideoGeneratorService(fps=30, resolution=(1280, 720))
    result = service.generate_video(
        images=video_images,
        output_path=output_path,
        transition_type="cross_dissolve"
    )
    
    print(f"\n✅ Vidéo générée: {result['output_path']}")
    print(f"   • Durée: {result['duration']:.2f}s")


def test_rotation_effects():
    """Test rotation effects."""
    print("\n" + "="*60)
    print("TEST 3: Effets de Rotation")
    print("="*60)
    
    images = get_test_images()
    if len(images) < 2:
        print("⚠️  Besoin d'au moins 2 images pour ce test")
        return
    
    test_images = images[:2]
    
    video_images = [
        ImageTimestamp(
            timestamp=0.0,
            image_path=test_images[0],
            effect="rotate_cw",
            effect_intensity=0.5  # Demi-rotation (180°)
        ),
        ImageTimestamp(
            timestamp=4.0,
            image_path=test_images[1],
            effect="rotate_slow",
            effect_intensity=1.0
        ),
    ]
    
    output_path = "./resources/test_videos/test_rotation_effects.mp4"
    
    print(f"\n📹 Génération vidéo avec effets de rotation...")
    print(f"   • Image 1: rotate_cw (intensité 0.5)")
    print(f"   • Image 2: rotate_slow")
    
    service = VideoGeneratorService(fps=30, resolution=(1280, 720))
    result = service.generate_video(
        images=video_images,
        output_path=output_path,
        transition_type="flash_white"
    )
    
    print(f"\n✅ Vidéo générée: {result['output_path']}")
    print(f"   • Durée: {result['duration']:.2f}s")


def test_mixed_effects_and_transitions():
    """Test mixing different effects with different transitions."""
    print("\n" + "="*60)
    print("TEST 4: Effets Mixtes + Transitions Variées")
    print("="*60)
    
    images = get_test_images()
    if len(images) < 4:
        print("⚠️  Besoin d'au moins 4 images pour ce test")
        return
    
    test_images = images[:4]
    
    # Mix different effects and transitions
    video_images = [
        ImageTimestamp(
            timestamp=0.0,
            image_path=test_images[0],
            effect="pan_right",
            effect_intensity=1.0,
            transition_type="zoom_in"  # Transition spécifique
        ),
        ImageTimestamp(
            timestamp=3.0,
            image_path=test_images[1],
            effect="zoom_in_continuous",
            effect_intensity=1.0,
            transition_type="smooth_slide_left"
        ),
        ImageTimestamp(
            timestamp=6.0,
            image_path=test_images[2],
            effect="rotate_slow",
            effect_intensity=1.0,
            transition_type="flash_white"
        ),
        ImageTimestamp(
            timestamp=9.0,
            image_path=test_images[3],
            effect="pan_diagonal_br",
            effect_intensity=0.8
            # No transition_type specified - will use global
        ),
    ]
    
    output_path = "./resources/test_videos/test_mixed_effects.mp4"
    
    print(f"\n📹 Génération vidéo avec effets et transitions variés...")
    print(f"   • Image 1: pan_right → zoom_in transition")
    print(f"   • Image 2: zoom_in_continuous → smooth_slide_left transition")
    print(f"   • Image 3: rotate_slow → flash_white transition")
    print(f"   • Image 4: pan_diagonal_br (intensity=0.8)")
    
    service = VideoGeneratorService(fps=30, resolution=(1280, 720))
    result = service.generate_video(
        images=video_images,
        output_path=output_path,
        transition_type="fade"  # Global transition (used for last image)
    )
    
    print(f"\n✅ Vidéo générée: {result['output_path']}")
    print(f"   • Durée: {result['duration']:.2f}s")


def test_static_vs_dynamic():
    """Test comparison between static and dynamic effects."""
    print("\n" + "="*60)
    print("TEST 5: Comparaison Static vs Dynamique")
    print("="*60)
    
    images = get_test_images()
    if len(images) < 2:
        print("⚠️  Besoin d'au moins 2 images pour ce test")
        return
    
    test_images = images[:2]
    
    # Static effect (old behavior)
    video_images_static = [
        ImageTimestamp(
            timestamp=0.0,
            image_path=test_images[0],
            effect="static"  # Pas de mouvement
        ),
        ImageTimestamp(
            timestamp=3.0,
            image_path=test_images[1],
            effect="static"
        ),
    ]
    
    output_static = "./resources/test_videos/test_static.mp4"
    
    print(f"\n📹 Génération vidéo STATIQUE (ancien comportement)...")
    service = VideoGeneratorService(fps=30, resolution=(1280, 720))
    result = service.generate_video(
        images=video_images_static,
        output_path=output_static,
        transition_type="fade"
    )
    print(f"   ✓ Vidéo statique générée: {result['output_path']}")
    
    # Dynamic effect
    video_images_dynamic = [
        ImageTimestamp(
            timestamp=0.0,
            image_path=test_images[0],
            effect="pan_right"
        ),
        ImageTimestamp(
            timestamp=3.0,
            image_path=test_images[1],
            effect="zoom_in_continuous"
        ),
    ]
    
    output_dynamic = "./resources/test_videos/test_dynamic.mp4"
    
    print(f"\n📹 Génération vidéo DYNAMIQUE (nouveau comportement)...")
    result = service.generate_video(
        images=video_images_dynamic,
        output_path=output_dynamic,
        transition_type="fade"
    )
    print(f"   ✓ Vidéo dynamique générée: {result['output_path']}")
    
    print(f"\n💡 Comparez les deux vidéos pour voir la différence:")
    print(f"   • Static: {output_static}")
    print(f"   • Dynamic: {output_dynamic}")


def list_available_effects():
    """List all available effects."""
    print("\n" + "="*60)
    print("EFFETS DISPONIBLES")
    print("="*60)
    
    effects = EffectRegistry.list_available()
    effects.sort()
    
    print(f"\nTotal: {len(effects)} effets\n")
    
    # Group by category
    pan_effects = [e for e in effects if 'pan' in e]
    zoom_effects = [e for e in effects if 'zoom' in e or 'breathing' in e]
    rotate_effects = [e for e in effects if 'rotate' in e]
    other_effects = [e for e in effects if e not in pan_effects + zoom_effects + rotate_effects]
    
    if pan_effects:
        print("📐 Pan (Panoramique):")
        for effect in pan_effects:
            print(f"   • {effect}")
    
    if zoom_effects:
        print("\n🔍 Zoom:")
        for effect in zoom_effects:
            print(f"   • {effect}")
    
    if rotate_effects:
        print("\n🔄 Rotation:")
        for effect in rotate_effects:
            print(f"   • {effect}")
    
    if other_effects:
        print("\n⚡ Autres:")
        for effect in other_effects:
            print(f"   • {effect}")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🎬 TEST DES NOUVEAUX EFFETS VIDÉO")
    print("="*60)
    
    # Ensure output directory exists
    os.makedirs("./resources/test_videos", exist_ok=True)
    
    # List available effects
    list_available_effects()
    
    # Run tests
    try:
        test_pan_effects()
        test_zoom_effects()
        test_rotation_effects()
        test_mixed_effects_and_transitions()
        test_static_vs_dynamic()
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS SONT RÉUSSIS!")
        print("="*60)
        print("\n📂 Vidéos générées dans: ./resources/test_videos/")
        print("\n💡 Vous pouvez maintenant:")
        print("   1. Visualiser les vidéos générées")
        print("   2. Tester via l'API: POST /api/v1/videos/generate")
        print("   3. Lister les effets via: GET /api/v1/videos/effects")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
