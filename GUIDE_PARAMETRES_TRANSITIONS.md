# 🎛️ Guide des Paramètres de Transitions

## Guide pratique pour les développeurs

Ce guide vous explique comment **modifier les paramètres des transitions** pour personnaliser vos effets vidéo.

---

## 📖 Table des Matières

1. [Modifier la Durée des Transitions](#1-modifier-la-durée-des-transitions)
2. [Ajuster les Paramètres d'Easing](#2-ajuster-les-paramètres-deasing)
3. [Fonctions d'Easing Disponibles](#3-fonctions-deasing-disponibles)
4. [Exemples Pratiques](#4-exemples-pratiques)
5. [Créer vos Propres Paramètres](#5-créer-vos-propres-paramètres)

---

## 1. Modifier la Durée des Transitions

### 🎯 Principe de Base

La durée d'une transition contrôle combien de temps elle dure entre deux images. Plus la durée est longue, plus la transition est lente et fluide.

### 📝 Via l'API (Méthode Simple)

Lors de la génération de la vidéo, vous pouvez ajuster la durée dans le service :

```python
from app.services.video_generator_service import VideoGeneratorService

# Créer le service avec une durée personnalisée
service = VideoGeneratorService(
    fps=30,
    resolution=(1280, 720),
    transition_duration=0.8  # 👈 Modifier ici (en secondes)
)

# Générer la vidéo
result = service.generate_video(
    images=images,
    output_path="output.mp4",
    transition_type="smooth_spin"
)
```

**Durées recommandées :**
- **Rapide** : `0.3 - 0.4s` (dynamique, énergique)
- **Moyenne** : `0.5 - 0.7s` (standard, équilibré)
- **Lente** : `0.8 - 1.2s` (fluide, cinématique)

### 🔧 Via le Code de Transition (Méthode Avancée)

Vous pouvez aussi modifier directement dans la classe de transition :

```python
from app.services.transitions.registry import TransitionRegistry

# Obtenir une transition avec durée personnalisée
transition = TransitionRegistry.get('smooth_spin', duration=1.0)  # 1 seconde

# Utiliser dans votre code
result_frame = transition.apply(frame1, frame2, progress=0.5)
```

---

## 2. Ajuster les Paramètres d'Easing

### 🎯 Qu'est-ce que l'Easing ?

L'easing (ou courbe d'accélération) contrôle **comment la transition progresse dans le temps**. Au lieu d'une progression linéaire constante, l'easing crée des accélérations et décélérations naturelles.

**Exemple visuel :**
```
Linéaire :     ————————————  (vitesse constante)
Ease-in-out :  ╱‾‾‾‾‾‾‾‾╲  (lent → rapide → lent)
```

### 📝 Modifier l'Easing dans une Transition

Chaque transition possède sa propre fonction d'easing. Voici comment la modifier :

#### Exemple : Modifier l'easing de `smooth_spin`

**Fichier :** `/app/app/services/transitions/smooth.py`

```python
class SmoothSpinTransition(TransitionBase):
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # 👇 MODIFIER L'EASING ICI
        # Option 1 : Utiliser l'easing actuel (quadratique)
        eased = self._ease_in_out_quad(progress)
        
        # Option 2 : Utiliser un easing différent
        # eased = self._ease_in_out_cubic(progress)  # Plus rapide
        # eased = self._ease_in_out_sine(progress)   # Plus doux
        # eased = self._ease_out_back(progress)      # Avec rebond
        # eased = progress  # Linéaire (sans easing)
        
        # Le reste du code utilise 'eased' au lieu de 'progress'
        angle = eased * 360
        zoom = 1.0 + eased * 0.3
        # ...
```

### 🎛️ Paramètres Clés à Ajuster

#### A. Intensité du Zoom

```python
# Dans la méthode apply() de la transition
zoom = 1.0 + eased * 0.3  # 👈 Modifier le 0.3

# Exemples :
zoom = 1.0 + eased * 0.5  # Zoom plus fort
zoom = 1.0 + eased * 0.2  # Zoom plus subtil
zoom = 1.0 + eased * 0.8  # Zoom très prononcé
```

#### B. Angle de Rotation

```python
# Pour smooth_spin
angle = eased * 360  # 👈 Modifier le 360

# Exemples :
angle = eased * 180   # Demi-tour seulement
angle = eased * 720   # Deux tours complets
angle = eased * 90    # Quart de tour
```

#### C. Intensité du Glitch

```python
# Dans GlitchTransition
shift = int(w * 0.02 * glitch_intensity)  # 👈 Modifier le 0.02

# Exemples :
shift = int(w * 0.05 * glitch_intensity)  # Glitch plus fort (5%)
shift = int(w * 0.01 * glitch_intensity)  # Glitch subtil (1%)
```

#### D. Intensité du Flou

```python
# Dans BlurZoomTransition
kernel_size = int(15 * blur_intensity)  # 👈 Modifier le 15

# Exemples :
kernel_size = int(25 * blur_intensity)  # Flou plus fort
kernel_size = int(10 * blur_intensity)  # Flou plus léger
kernel_size = int(35 * blur_intensity)  # Flou très prononcé
```

---

## 3. Fonctions d'Easing Disponibles

Voici toutes les fonctions d'easing que vous pouvez utiliser :

### 📊 Linear (Linéaire)

**Formule :** `t`

**Utilisation :**
```python
eased = progress  # Aucune accélération
```

**Caractéristique :** Vitesse constante, robotique, sans variation.

---

### 📊 Ease-In-Out Quadratic

**Formule :**
```python
@staticmethod
def _ease_in_out_quad(t: float) -> float:
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - pow(-2 * t + 2, 2) / 2
```

**Utilisation :**
```python
eased = self._ease_in_out_quad(progress)
```

**Caractéristique :** Accélération douce, idéal pour la plupart des transitions.
**Transitions utilisant cela :** `smooth_zoom`, `smooth_flip`, `smooth_spin`

---

### 📊 Ease-In-Out Cubic

**Formule :**
```python
@staticmethod
def _ease_in_out_cubic(t: float) -> float:
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2
```

**Utilisation :**
```python
eased = self._ease_in_out_cubic(progress)
```

**Caractéristique :** Accélération plus rapide que quadratic, plus dynamique.
**Transitions utilisant cela :** `smooth_slide_left`, `smooth_slide_right`, `blur_zoom`

---

### 📊 Ease-Out-Back (Rebond)

**Formule :**
```python
@staticmethod
def _ease_out_back(t: float) -> float:
    c1 = 1.70158  # 👈 Modifier pour plus/moins de rebond
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)
```

**Utilisation :**
```python
eased = self._ease_out_back(progress)
```

**Caractéristique :** Dépasse légèrement la cible puis revient (effet rebond).
**Transitions utilisant cela :** `smooth_stretch`

**Ajuster le rebond :**
```python
c1 = 1.70158  # Standard
c1 = 2.5      # Rebond plus prononcé
c1 = 1.0      # Rebond subtil
```

---

### 📊 Ease-In-Out Sine

**Formule :**
```python
@staticmethod
def _ease_in_out_sine(t: float) -> float:
    return -(np.cos(np.pi * t) - 1) / 2
```

**Utilisation :**
```python
eased = self._ease_in_out_sine(progress)
```

**Caractéristique :** Très fluide et naturel, basé sur une sinusoïde.
**Transitions utilisant cela :** `glitch`

---

## 4. Exemples Pratiques

### 🎬 Exemple 1 : Créer un Spin Plus Rapide

**Objectif :** Faire tourner l'image plus vite avec un zoom plus prononcé.

**Fichier :** `/app/app/services/transitions/smooth.py`

```python
class SmoothSpinTransition(TransitionBase):
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        # Utiliser un easing cubic pour plus de vitesse
        eased = self._ease_in_out_cubic(progress)  # ✅ Changé de quad à cubic
        
        # Augmenter l'angle de rotation
        angle = eased * 720  # ✅ 720° au lieu de 360° (2 tours)
        
        # Augmenter le zoom
        zoom = 1.0 + eased * 0.6  # ✅ 0.6 au lieu de 0.3
        
        # ... reste du code inchangé
```

**Résultat :** Transition plus dynamique et énergique.

---

### 🎬 Exemple 2 : Glitch Subtil et Élégant

**Objectif :** Créer un effet glitch plus discret pour du contenu corporate.

**Fichier :** `/app/app/services/transitions/smooth.py`

```python
class GlitchTransition(TransitionBase):
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        
        eased = self._ease_in_out_sine(progress)
        glitch_intensity = 1.0 - abs(eased - 0.5) * 2
        blended = self.blend_frames(frame1, frame2, eased)
        
        # Rendre le glitch plus subtil
        if glitch_intensity > 0.3:  # ✅ Seuil plus élevé (0.3 au lieu de 0.1)
            b, g, r = cv2.split(blended)
            
            # Réduire le décalage
            shift = int(w * 0.005 * glitch_intensity)  # ✅ 0.5% au lieu de 2%
            
            # ... reste du code ...
            
            # Réduire l'intensité du blend final
            result = self.blend_frames(blended, glitched, glitch_intensity * 0.3)  # ✅ 0.3 au lieu de 0.6
            return result
        else:
            return blended
```

**Résultat :** Effet glitch professionnel et discret.

---

### 🎬 Exemple 3 : Blur Zoom Cinématique

**Objectif :** Créer un blur zoom lent et cinématique comme au cinéma.

**Étape 1 : Augmenter la durée via l'API**

```python
service = VideoGeneratorService(
    fps=30,
    resolution=(1920, 1080),  # Full HD
    transition_duration=1.2  # ✅ 1.2 secondes (lent)
)

result = service.generate_video(
    images=images,
    output_path="cinematic_video.mp4",
    transition_type="blur_zoom"
)
```

**Étape 2 : Ajuster le flou dans le code**

**Fichier :** `/app/app/services/transitions/smooth.py`

```python
class BlurZoomTransition(TransitionBase):
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        # ... code précédent ...
        
        # Zoom plus subtil
        zoom = 1.0 + eased * 0.2  # ✅ 0.2 au lieu de 0.4
        
        # Flou plus prononcé
        if blur_intensity > 0.1:  # ✅ Seuil plus bas
            kernel_size = int(25 * blur_intensity)  # ✅ 25 au lieu de 15
            if kernel_size % 2 == 0:
                kernel_size += 1
            kernel_size = max(3, kernel_size)
            
            zoomed_frame1 = cv2.GaussianBlur(zoomed_frame1, (kernel_size, kernel_size), 0)
        
        # ... reste du code ...
```

**Résultat :** Transition lente, floue et cinématographique.

---

## 5. Créer vos Propres Paramètres

### 🛠️ Méthode : Ajouter des Paramètres Configurables

Vous pouvez rendre les paramètres configurables via le constructeur :

```python
class CustomSpinTransition(TransitionBase):
    """Spin transition avec paramètres personnalisables."""
    
    def __init__(self, 
                 duration: float = 0.5,
                 rotation_angle: float = 360.0,  # 👈 Nouveau paramètre
                 zoom_intensity: float = 0.3):   # 👈 Nouveau paramètre
        super().__init__(duration)
        self.rotation_angle = rotation_angle
        self.zoom_intensity = zoom_intensity
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        h, w = frame1.shape[:2]
        eased = self._ease_in_out_quad(progress)
        
        # Utiliser les paramètres configurables
        angle = eased * self.rotation_angle  # ✅ Utilise le paramètre
        zoom = 1.0 + eased * self.zoom_intensity  # ✅ Utilise le paramètre
        
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, zoom)
        rotated_frame1 = cv2.warpAffine(frame1, rotation_matrix, (w, h))
        
        return self.blend_frames(rotated_frame1, frame2, eased)
    
    @staticmethod
    def _ease_in_out_quad(t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2
```

### 📝 Utilisation de la Transition Personnalisée

```python
# Enregistrer la transition
from app.services.transitions.registry import TransitionRegistry
TransitionRegistry.register('custom_spin', CustomSpinTransition)

# Utiliser avec des paramètres personnalisés
transition = CustomSpinTransition(
    duration=0.8,
    rotation_angle=720.0,  # 2 tours complets
    zoom_intensity=0.5     # Zoom prononcé
)

result_frame = transition.apply(frame1, frame2, progress=0.5)
```

---

## 📊 Tableau Récapitulatif des Paramètres

| Transition | Paramètre Principal | Valeur Par Défaut | Plage Recommandée |
|------------|---------------------|-------------------|-------------------|
| **smooth_spin** | `rotation_angle` | 360° | 180° - 720° |
| **smooth_spin** | `zoom_intensity` | 0.3 | 0.2 - 0.8 |
| **glitch** | `shift` (% largeur) | 2% | 0.5% - 5% |
| **glitch** | `blend_intensity` | 0.6 | 0.3 - 0.9 |
| **blur_zoom** | `zoom_intensity` | 0.4 | 0.2 - 0.6 |
| **blur_zoom** | `kernel_size` | 15 | 10 - 35 |
| **smooth_stretch** | `back_constant` (c1) | 1.70158 | 1.0 - 2.5 |

---

## 🎨 Conseils de Personnalisation

### ✅ Bonnes Pratiques

1. **Testez progressivement** : Changez un paramètre à la fois
2. **Gardez des valeurs réalistes** : Trop d'effet peut être désagréable
3. **Adaptez à votre contenu** :
   - Corporate → effets subtils
   - TikTok/Instagram → effets prononcés
   - Cinéma → effets lents et fluides

### ⚠️ Pièges à Éviter

1. **Valeurs trop extrêmes** :
   ```python
   zoom = 1.0 + eased * 5.0  # ❌ Trop fort, image déformée
   zoom = 1.0 + eased * 0.4  # ✅ Raisonnable
   ```

2. **Durées inadaptées** :
   ```python
   transition_duration = 0.1  # ❌ Trop rapide, effet saccadé
   transition_duration = 3.0  # ❌ Trop lent, ennuyeux
   transition_duration = 0.6  # ✅ Équilibré
   ```

3. **Easing incompatible** :
   - Pour des effets rebondissants → utiliser `ease_out_back`
   - Pour des effets fluides → utiliser `ease_in_out_sine`
   - Pour des effets dynamiques → utiliser `ease_in_out_cubic`

---

## 🧪 Testing et Ajustement

### Script de Test Rapide

Créez un fichier `/app/test_custom_transition.py` :

```python
"""Script pour tester rapidement les paramètres de transition."""

import numpy as np
import cv2
from app.services.transitions.smooth import SmoothSpinTransition

# Charger deux images de test
frame1 = cv2.imread('resources/test_images/image1.jpg')
frame2 = cv2.imread('resources/test_images/image2.jpg')

# Redimensionner
frame1 = cv2.resize(frame1, (1280, 720))
frame2 = cv2.resize(frame2, (1280, 720))

# Créer la transition avec paramètres personnalisés
transition = SmoothSpinTransition(duration=0.8)

# Tester à différents moments
for progress in [0.0, 0.25, 0.5, 0.75, 1.0]:
    result = transition.apply(frame1, frame2, progress)
    cv2.imwrite(f'test_output/frame_{int(progress*100)}.jpg', result)
    print(f"✅ Frame à {progress*100}% généré")

print("🎉 Test terminé ! Vérifiez les images dans test_output/")
```

**Exécuter :**
```bash
python test_custom_transition.py
```

---

## 📚 Ressources Supplémentaires

### Liens Utiles

- **Easing Functions Visualizer** : [easings.net](https://easings.net) - Visualisez toutes les fonctions d'easing
- **OpenCV Docs** : [docs.opencv.org](https://docs.opencv.org) - Documentation OpenCV
- **MoviePy Docs** : [zulko.github.io/moviepy](https://zulko.github.io/moviepy/) - Documentation MoviePy

### Fichiers Clés du Projet

- `/app/app/services/transitions/smooth.py` - Transitions modernes (TikTok/CapCut)
- `/app/app/services/transitions/base.py` - Classe de base
- `/app/app/services/transitions/registry.py` - Registre des transitions
- `/app/TRANSITIONS_GUIDE.md` - Guide complet des transitions

---

## ✨ Résumé Rapide

### Pour modifier la **durée** :
```python
service = VideoGeneratorService(transition_duration=0.8)  # En secondes
```

### Pour modifier l'**easing** :
```python
# Dans la méthode apply() de votre transition
eased = self._ease_in_out_cubic(progress)  # Choisir la fonction d'easing
```

### Pour modifier l'**intensité** :
```python
# Exemples de paramètres à ajuster :
zoom = 1.0 + eased * 0.5      # Intensité du zoom
angle = eased * 720           # Angle de rotation
shift = int(w * 0.03 * intensity)  # Décalage glitch
kernel_size = int(25 * intensity)  # Taille du flou
```

---

**🎬 Bon montage vidéo ! N'hésitez pas à expérimenter et créer vos propres effets !**
