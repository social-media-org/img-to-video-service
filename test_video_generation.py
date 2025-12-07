#!/usr/bin/env python3
"""
Script de test autonome pour la génération de vidéos.

Ce script:
1. Génère 3 images colorées avec Pillow
2. Teste plusieurs transitions différentes
3. Crée des vidéos de démonstration
4. Peut être exécuté sans lancer l'API

Usage:
    python test_video_generation.py
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.video_generator_service import VideoGeneratorService
from app.models.video_models import ImageTimestamp


def create_test_images(output_dir: str = "/tmp/test_images") -> list[str]:
    """Créer 3 images de test colorées avec du texte.
    
    Args:
        output_dir: Répertoire où sauvegarder les images
        
    Returns:
        Liste des chemins vers les images créées
    """
    print("📸 Génération des images de test...")
    
    # Créer le répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Dimensions des images
    width, height = 1280, 720
    
    # Définir les couleurs et les textes
    images_config = [
        {
            "color": (255, 100, 100),  # Rouge
            "text": "Image 1 - RED",
            "filename": "image_1.png"
        },
        {
            "color": (100, 255, 100),  # Vert
            "text": "Image 2 - GREEN",
            "filename": "image_2.png"
        },
        {
            "color": (100, 100, 255),  # Bleu
            "text": "Image 3 - BLUE",
            "filename": "image_3.png"
        }
    ]
    
    image_paths = []
    
    for config in images_config:
        # Créer une image avec couleur de fond
        img = Image.new('RGB', (width, height), config["color"])
        draw = ImageDraw.Draw(img)
        
        # Ajouter du texte au centre
        text = config["text"]
        
        # Utiliser une police par défaut (size pour la taille)
        try:
            # Essayer d'utiliser une police système
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            # Utiliser la police par défaut si la police système n'est pas disponible
            font = ImageFont.load_default()
        
        # Calculer la position pour centrer le texte
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Dessiner le texte avec bordure noire
        # Bordure noire
        border_width = 3
        for adj_x in range(-border_width, border_width + 1):
            for adj_y in range(-border_width, border_width + 1):
                draw.text((position[0] + adj_x, position[1] + adj_y), text, font=font, fill=(0, 0, 0))
        
        # Texte blanc
        draw.text(position, text, font=font, fill=(255, 255, 255))
        
        # Sauvegarder l'image
        filepath = os.path.join(output_dir, config["filename"])
        img.save(filepath)
        image_paths.append(filepath)
        print(f"  ✓ Créé: {filepath}")
    
    return image_paths


def test_transition(transition_name: str, image_paths: list[str], output_dir: str = "/tmp/test_videos"):
    """Tester une transition spécifique.
    
    Args:
        transition_name: Nom de la transition à tester
        image_paths: Liste des chemins vers les images
        output_dir: Répertoire de sortie pour les vidéos
    """
    print(f"\n🎬 Test de la transition: {transition_name}")
    
    # Créer le répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Créer les timestamps (chaque image dure 3 secondes)
    timestamps = [
        ImageTimestamp(timestamp=0.0, image_path=image_paths[0]),
        ImageTimestamp(timestamp=3.0, image_path=image_paths[1]),
        ImageTimestamp(timestamp=6.0, image_path=image_paths[2])
    ]
    
    # Chemin de sortie
    output_path = os.path.join(output_dir, f"video_{transition_name}.mp4")
    
    # Créer le service et générer la vidéo
    try:
        service = VideoGeneratorService(fps=30, resolution=(1280, 720))
        result = service.generate_video(
            images=timestamps,
            output_path=output_path,
            transition_type=transition_name
        )
        
        print(f"  ✓ Vidéo générée: {result['output_path']}")
        print(f"  ✓ Durée: {result['duration']:.2f}s")
        print(f"  ✓ Résolution: {result['resolution']}")
        print(f"  ✓ FPS: {result['fps']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erreur: {str(e)}")
        return False


def main():
    """Fonction principale du script de test."""
    print("=" * 60)
    print("🎥 TEST DE GÉNÉRATION DE VIDÉOS AVEC TRANSITIONS")
    print("=" * 60)
    
    # Étape 1: Générer les images de test
    image_paths = create_test_images()
    
    # Étape 2: Lister les transitions disponibles
    print("\n📋 Transitions disponibles:")
    available_transitions = VideoGeneratorService.list_available_transitions()
    for i, transition in enumerate(available_transitions, 1):
        print(f"  {i}. {transition}")
    
    # Étape 3: Tester quelques transitions
    transitions_to_test = [
        "cross_dissolve",
        "flash_white",
        "zoom_in",
        "wipe_left",
        "smooth_zoom"
    ]
    
    print(f"\n🧪 Test de {len(transitions_to_test)} transitions...")
    
    results = {}
    for transition in transitions_to_test:
        if transition in available_transitions:
            success = test_transition(transition, image_paths)
            results[transition] = success
        else:
            print(f"\n⚠️  Transition '{transition}' non disponible")
            results[transition] = False
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    for transition, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {transition}")
    
    print(f"\n✨ Tests réussis: {successful}/{total}")
    
    if successful == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
    else:
        print(f"\n⚠️  {total - successful} test(s) ont échoué")
    
    print("\n💾 Les vidéos générées sont dans: /tmp/test_videos/")
    print("=" * 60)


if __name__ == "__main__":
    main()
