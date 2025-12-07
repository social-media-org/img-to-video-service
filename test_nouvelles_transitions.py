"""Script de test pour les 3 nouvelles transitions modernes."""

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
    
    cv2.putText(img1, "IMAGE 1", (450, 360), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
    
    # Image 2: Gradient rouge
    img2 = np.zeros((720, 1280, 3), dtype=np.uint8)
    for i in range(720):
        img2[i, :] = [int(i * 150 / 720), int(i * 100 / 720), 255 - int(i * 255 / 720)]
    
    cv2.putText(img2, "IMAGE 2", (450, 360), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
    
    return img1, img2


def test_transition(transition_name, frame1, frame2, output_dir):
    """Tester une transition."""
    print(f"\n🎬 Test: {transition_name}")
    trans_dir = output_dir / transition_name
    trans_dir.mkdir(parents=True, exist_ok=True)
    transition = TransitionRegistry.get(transition_name, duration=0.5)
    
    for progress in [0.0, 0.25, 0.5, 0.75, 1.0]:
        result = transition.apply(frame1, frame2, progress)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        filename = trans_dir / f"frame_{int(progress * 100):03d}.jpg"
        cv2.imwrite(str(filename), result_rgb)
        print(f"  ✅ Frame {int(progress * 100)}%")
    print(f"  ✨ {transition_name} OK!")


def main():
    print("=" * 60)
    print("🚀 TEST DES NOUVELLES TRANSITIONS MODERNES")
    print("=" * 60)
    
    output_dir = Path("./test_output_transitions")
    output_dir.mkdir(exist_ok=True)
    
    print("\n📸 Création des images de test...")
    frame1, frame2 = create_test_images()
    
    cv2.imwrite(str(output_dir / "source_image1.jpg"), cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR))
    cv2.imwrite(str(output_dir / "source_image2.jpg"), cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR))
    print("  ✅ Images sources créées")
    
    transitions = [
        ('smooth_spin', 'Rotation avec zoom'),
        ('glitch', 'Effet de glitch digital'),
        ('blur_zoom', 'Zoom avec flou de mouvement')
    ]
    
    for trans_name, desc in transitions:
        print(f"\n{'=' * 60}")
        print(f"📌 {trans_name}: {desc}")
        test_transition(trans_name, frame1, frame2, output_dir)
    
    print("\n" + "=" * 60)
    print("🎉 TOUS LES TESTS TERMINÉS!")
    print("=" * 60)
    print(f"\n📁 Résultats dans: {output_dir}")
    print("\n✨ Visualisez les transitions frame par frame!")


if __name__ == "__main__":
    main()
