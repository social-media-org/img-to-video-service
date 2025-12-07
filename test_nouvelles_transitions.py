"""Script de test pour les 3 nouvelles transitions modernes.

Ce script démontre l'utilisation des nouvelles transitions:
- smooth_spin: Rotation avec zoom (style TikTok)
- glitch: Effet de glitch digital moderne
- blur_zoom: Zoom avec flou de mouvement (style CapCut)
"""

import numpy as np
import cv2
from pathlib import Path
from app.services.transitions.registry import TransitionRegistry


def create_test_images():
    """Créer deux images de test colorées."""
    # Image 1: Gradient bleu
    img1 = np.zeros((720, 1280, 3), dtype=np.uint8)
    for i in range(720):
        img1[i, :] = [255 - int(i * 255 / 720), int(i * 200 / 720), 200]
    
    # Ajouter du texte
    cv2.putText(img1, "IMAGE 1", (450, 360), cv2.FONT_HERSHEY_BOLD, 3, (255, 255, 255), 5)
    
    # Image 2: Gradient rouge
    img2 = np.zeros((720, 1280, 3), dtype=np.uint8)
    for i in range(720):
        img2[i, :] = [int(i * 150 / 720), int(i * 100 / 720), 255 - int(i * 255 / 720)]
    
    # Ajouter du texte
    cv2.putText(img2, "IMAGE 2", (450, 360), cv2.FONT_HERSHEY_BOLD, 3, (255, 255, 255), 5)
    
    return img1, img2


def test_transition(transition_name, frame1, frame2, output_dir):
    """Tester une transition et générer des frames à différents moments."""
    print(f"\n🎬 Test de la transition: {transition_name}")
    
    # Créer le dossier de sortie
    trans_dir = output_dir / transition_name
    trans_dir.mkdir(parents=True, exist_ok=True)
    
    # Obtenir la transition
    transition = TransitionRegistry.get(transition_name, duration=0.5)
    
    # Générer des frames à différents moments de la transition
    progress_points = [0.0, 0.25, 0.5, 0.75, 1.0]
    
    for progress in progress_points:
        result = transition.apply(frame1, frame2, progress)
        
        # Convertir BGR en RGB pour sauvegarde
        result_rgb = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        
        # Sauvegarder
        filename = trans_dir / f"frame_{int(progress * 100):03d}.jpg"
        cv2.imwrite(str(filename), result_rgb)
        print(f"  ✅ Frame {int(progress * 100)}% → {filename}")
    
    print(f"  ✨ Test de {transition_name} terminé!")


def main():
    """Fonction principale de test."""
    print("=" * 60)
    print("🚀 TEST DES NOUVELLES TRANSITIONS MODERNES")
    print("=" * 60)
    
    # Créer le dossier de sortie
    output_dir = Path("/app/test_output_transitions")
    output_dir.mkdir(exist_ok=True)
    
    # Créer les images de test
    print("\n📸 Création des images de test...")
    frame1, frame2 = create_test_images()
    
    # Sauvegarder les images sources
    cv2.imwrite(str(output_dir / "source_image1.jpg"), cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR))
    cv2.imwrite(str(output_dir / "source_image2.jpg"), cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR))
    print(f"  ✅ Images sources créées dans {output_dir}")
    
    # Tester les 3 nouvelles transitions
    transitions_to_test = [
        ('smooth_spin', 'Rotation avec zoom (TikTok style)'),
        ('glitch', 'Effet de glitch digital moderne'),
        ('blur_zoom', 'Zoom avec flou de mouvement (CapCut style)')
    ]
    
    for trans_name, description in transitions_to_test:
        print(f"\n{'=' * 60}")
        print(f"📌 {trans_name.upper()}: {description}")
        print('=' * 60)
        test_transition(trans_name, frame1, frame2, output_dir)
    
    print("\n" + "=" * 60)
    print("🎉 TOUS LES TESTS TERMINÉS !")
    print("=" * 60)
    print(f"\n📁 Résultats disponibles dans: {output_dir}")
    print("\nStructure des dossiers:")
    print(f"  {output_dir}/")
    print("  ├── source_image1.jpg         (Image source 1)")
    print("  ├── source_image2.jpg         (Image source 2)")
    print("  ├── smooth_spin/")
    print("  │   ├── frame_000.jpg         (0% - début)")
    print("  │   ├── frame_025.jpg         (25%)")
    print("  │   ├── frame_050.jpg         (50% - milieu)")
    print("  │   ├── frame_075.jpg         (75%)")
    print("  │   └── frame_100.jpg         (100% - fin)")
    print("  ├── glitch/")
    print("  │   └── ... (même structure)")
    print("  └── blur_zoom/")
    print("      └── ... (même structure)")
    print("\n✨ Vous pouvez maintenant visualiser les transitions frame par frame!")


if __name__ == "__main__":
    main()
