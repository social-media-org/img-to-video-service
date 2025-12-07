#!/usr/bin/env python3
"""
Script de test autonome pour la génération de vidéos.

Ce script:
1. Utilise des images existantes dans ./resources/test_images
2. Détermine la résolution minimale des images pour éviter la déformation.
3. Teste toutes les transitions disponibles.
4. Crée des vidéos de démonstration.
5. Peut être exécuté sans lancer l'API.

Usage:
    python test_video_generation.py
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.video_generator_service import VideoGeneratorService
from app.models.video_models import ImageTimestamp

def get_test_images_with_dimensions(image_dir: str = "./resources/test_images") -> list[tuple[str, int, int]]:
    """Récupère les chemins et dimensions des images de test depuis le répertoire spécifié.

    Args:
        image_dir: Répertoire contenant les images de test.

    Returns:
        Liste de tuples (chemin_image, largeur, hauteur) des images trouvées.
    """
    print(f"📸 Récupération des images de test depuis: {image_dir}")
    image_data = []
    valid_extensions = {".png", ".jpg", ".jpeg"}
    for root, _, files in os.walk(image_dir):
        for file in files:
            if Path(file).suffix.lower() in valid_extensions:
                filepath = os.path.join(root, file)
                try:
                    with Image.open(filepath) as img:
                        width, height = img.size
                        image_data.append((filepath, width, height))
                except Exception as e:
                    print(f"  ✗ Erreur lors de la lecture de l'image {filepath}: {e}")
    image_data.sort(key=lambda x: x[0]) # Ensure a consistent order based on path
    print(f"  ✓ {len(image_data)} images trouvées avec dimensions.")
    return image_data


def test_transition(transition_name: str, image_paths: list[str], resolution: tuple[int, int], output_dir: str = "./resources/test_videos"):
    """Tester une transition spécifique.
    
    Args:
        transition_name: Nom de la transition à tester
        image_paths: Liste des chemins vers les images
        resolution: Résolution (largeur, hauteur) de la vidéo à générer.
        output_dir: Répertoire de sortie pour les vidéos
    """
    print(f"\n🎬 Test de la transition: {transition_name} avec résolution {resolution}")
    
    # Créer le répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Créer les timestamps (chaque image dure 3 secondes)
    timestamps = [
        ImageTimestamp(timestamp=float(i * 3), image_path=path)
        for i, path in enumerate(image_paths)
    ]
    
    # Chemin de sortie
    output_path = os.path.join(output_dir, f"video_{transition_name}.mp4")
    
    # Créer le service et générer la vidéo
    try:
        start_time = time.time()
        service = VideoGeneratorService(fps=30, resolution=resolution)
        result = service.generate_video(
            images=timestamps,
            output_path=output_path,
            transition_type=transition_name
        )
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"  ✓ Vidéo générée: {result["output_path"]}")
        print(f"  ✓ Durée de génération: {duration:.2f}s")
        print(f"  ✓ Durée vidéo: {result["duration"]:.2f}s")
        print(f"  ✓ Résolution: {result["resolution"]}")
        print(f"  ✓ FPS: {result["fps"]}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale du script de test."""
    print("=" * 60)
    print("🎥 TEST DE GÉNÉRATION DE VIDÉOS AVEC TRANSITIONS")
    print("=" * 60)
    
    total_start_time = time.time()

    # Étape 1: Récupérer les images de test avec leurs dimensions
    image_data = get_test_images_with_dimensions()
    if not image_data:
        print("❌ Aucune image de test trouvée. Veuillez placer des images dans ./resources/test_images/")
        sys.exit(1)

    # Déterminer la résolution minimale
    min_width = min(data[1] for data in image_data)
    min_height = min(data[2] for data in image_data)
    target_resolution = (min_width, min_height)
    print(f"🎯 Résolution cible de la vidéo (plus petite image): {target_resolution}")
    
    # Extraire seulement les chemins d'image pour les passer à test_transition
    image_paths = [data[0] for data in image_data]

    # Étape 2: Lister les transitions disponibles
    print("\n📋 Transitions disponibles:")
    available_transitions = VideoGeneratorService.list_available_transitions()
    for i, transition in enumerate(available_transitions, 1):
        print(f"  {i}. {transition}")
    
    # Étape 3: Tester toutes les transitions disponibles
    transitions_to_test = available_transitions
    
    print(f"\n🧪 Test de {len(transitions_to_test)} transitions...")
    
    results = {}
    for transition in transitions_to_test:
        if transition in available_transitions:
            success = test_transition(transition, image_paths, target_resolution)
            results[transition] = success
        else:
            print(f"\n⚠️  Transition \'{transition}\' non disponible")
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
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    print(f"\n⏱️ Durée totale des tests: {total_duration:.2f}s")
    
    print("\n💾 Les vidéos générées sont dans: ./resources/test_videos/")
    print("=" * 60)


if __name__ == "__main__":
    main()
