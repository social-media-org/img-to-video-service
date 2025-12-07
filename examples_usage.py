#!/usr/bin/env python3
"""
Exemples d'utilisation du service de génération de vidéos.

Ce fichier montre différentes façons d'utiliser le service,
que ce soit via l'API ou directement via le service.
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.video_generator_service import VideoGeneratorService
from app.models.video_models import ImageTimestamp


# =============================================================================
# EXEMPLE 1: Utilisation Basique du Service
# =============================================================================

def example_basic_usage():
    """Exemple basique: créer une vidéo avec 3 images."""
    print("=" * 60)
    print("EXEMPLE 1: Utilisation Basique")
    print("=" * 60)
    
    # Créer le service
    service = VideoGeneratorService(
        fps=30,
        resolution=(1280, 720)
    )
    
    # Définir les images (timestamps en secondes)
    images = [
        ImageTimestamp(timestamp=0.0, image_path="/tmp/test_images/image_1.png"),
        ImageTimestamp(timestamp=3.0, image_path="/tmp/test_images/image_2.png"),
        ImageTimestamp(timestamp=6.0, image_path="/tmp/test_images/image_3.png")
    ]
    
    # Générer la vidéo
    result = service.generate_video(
        images=images,
        output_path="/tmp/example_basic.mp4",
        transition_type="cross_dissolve"
    )
    
    print(f"✓ Vidéo générée: {result['output_path']}")
    print(f"✓ Durée: {result['duration']:.2f}s")
    print()


# =============================================================================
# EXEMPLE 2: Utiliser Différentes Transitions
# =============================================================================

def example_multiple_transitions():
    """Créer plusieurs vidéos avec différentes transitions."""
    print("=" * 60)
    print("EXEMPLE 2: Différentes Transitions")
    print("=" * 60)
    
    service = VideoGeneratorService(fps=30, resolution=(1280, 720))
    
    images = [
        ImageTimestamp(timestamp=0.0, image_path="/tmp/test_images/image_1.png"),
        ImageTimestamp(timestamp=2.0, image_path="/tmp/test_images/image_2.png"),
        ImageTimestamp(timestamp=4.0, image_path="/tmp/test_images/image_3.png")
    ]
    
    # Tester plusieurs transitions
    transitions = ["flash_white", "zoom_in", "smooth_slide_left"]
    
    for transition in transitions:
        output_path = f"/tmp/example_{transition}.mp4"
        
        result = service.generate_video(
            images=images,
            output_path=output_path,
            transition_type=transition
        )
        
        print(f"✓ {transition:20s} -> {output_path}")
    
    print()


# =============================================================================
# EXEMPLE 3: Vidéo Haute Résolution
# =============================================================================

def example_high_resolution():
    """Créer une vidéo en Full HD."""
    print("=" * 60)
    print("EXEMPLE 3: Vidéo Haute Résolution (1920x1080)")
    print("=" * 60)
    
    service = VideoGeneratorService(
        fps=60,  # 60 FPS pour plus de fluidité
        resolution=(1920, 1080)  # Full HD
    )
    
    images = [
        ImageTimestamp(timestamp=0.0, image_path="/tmp/test_images/image_1.png"),
        ImageTimestamp(timestamp=4.0, image_path="/tmp/test_images/image_2.png"),
        ImageTimestamp(timestamp=8.0, image_path="/tmp/test_images/image_3.png")
    ]
    
    result = service.generate_video(
        images=images,
        output_path="/tmp/example_hd.mp4",
        transition_type="smooth_zoom"
    )
    
    print(f"✓ Résolution: {result['resolution']}")
    print(f"✓ FPS: {result['fps']}")
    print(f"✓ Fichier: {result['output_path']}")
    print()


# =============================================================================
# EXEMPLE 4: Timestamps Non-Uniformes
# =============================================================================

def example_variable_duration():
    """Images avec durées variables."""
    print("=" * 60)
    print("EXEMPLE 4: Durées Variables")
    print("=" * 60)
    
    service = VideoGeneratorService()
    
    # Durées différentes pour chaque image
    images = [
        ImageTimestamp(timestamp=0.0, image_path="/tmp/test_images/image_1.png"),   # Dure 1.5s
        ImageTimestamp(timestamp=1.5, image_path="/tmp/test_images/image_2.png"),   # Dure 4.0s
        ImageTimestamp(timestamp=5.5, image_path="/tmp/test_images/image_3.png")    # Dure 4.0s (même que précédente)
    ]
    
    result = service.generate_video(
        images=images,
        output_path="/tmp/example_variable.mp4",
        transition_type="wipe_left"
    )
    
    print(f"✓ Image 1: 1.5s")
    print(f"✓ Image 2: 4.0s")
    print(f"✓ Image 3: 4.0s")
    print(f"✓ Durée totale: {result['duration']:.2f}s")
    print()


# =============================================================================
# EXEMPLE 5: Lister les Transitions Disponibles
# =============================================================================

def example_list_transitions():
    """Afficher toutes les transitions disponibles."""
    print("=" * 60)
    print("EXEMPLE 5: Transitions Disponibles")
    print("=" * 60)
    
    transitions = VideoGeneratorService.list_available_transitions()
    
    print(f"Total: {len(transitions)} transitions\n")
    
    # Grouper par catégorie (basé sur le préfixe)
    categories = {
        "Fade": [t for t in transitions if 'fade' in t or 'flash' in t or 'cross' in t],
        "Zoom": [t for t in transitions if 'zoom' in t],
        "Wipe": [t for t in transitions if 'wipe' in t],
        "Smooth": [t for t in transitions if 'smooth' in t]
    }
    
    for category, trans_list in categories.items():
        print(f"\n{category}:")
        for t in trans_list:
            print(f"  - {t}")
    
    print()


# =============================================================================
# EXEMPLE 6: Utilisation avec l'API (Requête HTTP)
# =============================================================================

def example_api_usage():
    """Exemple d'appel à l'API REST."""
    print("=" * 60)
    print("EXEMPLE 6: Utilisation de l'API REST")
    print("=" * 60)
    
    import requests
    import json
    
    # Préparer la requête
    payload = {
        "images": [
            {"timestamp": 0.0, "image_path": "/tmp/test_images/image_1.png"},
            {"timestamp": 3.0, "image_path": "/tmp/test_images/image_2.png"},
            {"timestamp": 6.0, "image_path": "/tmp/test_images/image_3.png"}
        ],
        "output_path": "/tmp/example_api.mp4",
        "transition_type": "flash_white",
        "fps": 30,
        "resolution": [1280, 720]
    }
    
    print("Requête:")
    print(json.dumps(payload, indent=2))
    print()
    
    try:
        # Envoyer la requête
        response = requests.post(
            "http://localhost:8000/api/v1/videos/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✓ Succès!")
            print(f"  Output: {result['output_path']}")
            print(f"  Duration: {result['duration']}s")
        else:
            print(f"✗ Erreur: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("⚠️  Le serveur n'est pas accessible.")
        print("   Démarrez-le avec: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    print()


# =============================================================================
# EXEMPLE 7: Gestion d'Erreurs
# =============================================================================

def example_error_handling():
    """Exemples de gestion d'erreurs."""
    print("=" * 60)
    print("EXEMPLE 7: Gestion d'Erreurs")
    print("=" * 60)
    
    service = VideoGeneratorService()
    
    # Erreur 1: Fichier image inexistant
    print("\n1. Test avec fichier inexistant:")
    try:
        images = [
            ImageTimestamp(timestamp=0.0, image_path="/tmp/nonexistent.png"),
            ImageTimestamp(timestamp=3.0, image_path="/tmp/test_images/image_2.png")
        ]
        service.generate_video(images, "/tmp/test.mp4", "fade")
    except ValueError as e:
        print(f"   ✓ Erreur capturée: {e}")
    
    # Erreur 2: Transition invalide
    print("\n2. Test avec transition invalide:")
    try:
        from app.services.transitions.registry import TransitionRegistry
        TransitionRegistry.get("invalid_transition")
    except ValueError as e:
        print(f"   ✓ Erreur capturée: {e}")
    
    # Erreur 3: Moins de 2 images
    print("\n3. Test avec une seule image:")
    try:
        images = [
            ImageTimestamp(timestamp=0.0, image_path="/tmp/test_images/image_1.png")
        ]
        service.generate_video(images, "/tmp/test.mp4", "fade")
    except ValueError as e:
        print(f"   ✓ Erreur capturée: {e}")
    
    print()


# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def main():
    """Exécuter tous les exemples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "EXEMPLES D'UTILISATION - API VIDÉO" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Liste des exemples
    examples = [
        ("Utilisation Basique", example_basic_usage),
        ("Différentes Transitions", example_multiple_transitions),
        ("Haute Résolution", example_high_resolution),
        ("Durées Variables", example_variable_duration),
        ("Lister les Transitions", example_list_transitions),
        ("API REST", example_api_usage),
        ("Gestion d'Erreurs", example_error_handling)
    ]
    
    print("Exemples disponibles:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nExécution de tous les exemples...\n")
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"✗ Erreur dans {name}: {e}")
            print()
    
    print("=" * 60)
    print("✓ Tous les exemples ont été exécutés!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
