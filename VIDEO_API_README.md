# 🎬 API de Génération de Vidéos avec Transitions

API FastAPI pour créer des vidéos à partir d'images avec de magnifiques transitions professionnelles (style Canva/CapCut).

## ✨ Fonctionnalités

- ✅ **16 transitions professionnelles** implémentées
- ✅ **Architecture extensible** pour ajouter facilement de nouvelles transitions
- ✅ **Service testable indépendamment** (sans lancer l'API)
- ✅ **API REST** pour intégration facile
- ✅ **Images locales** (pas de téléchargement nécessaire)
- ✅ **Contrôle total** sur la durée, résolution et FPS
- ✅ **Clean Architecture** avec séparation des responsabilités

## 🎨 Transitions Disponibles

### Transitions Fade
- `cross_dissolve` / `fade` - Fondu enchaîné classique
- `flash_white` / `flash` - Flash blanc rapide (style TikTok)
- `fade_to_black` - Fondu au noir (cinématique)

### Transitions Zoom
- `zoom_in` - Zoom avant progressif
- `zoom_out` - Zoom arrière progressif
- `smooth_zoom` - Zoom fluide avec easing (style TikTok)

### Transitions Wipe (Balayage)
- `wipe_left` - Balayage de droite à gauche
- `wipe_right` - Balayage de gauche à droite
- `wipe_up` - Balayage de bas en haut
- `wipe_down` - Balayage de haut en bas

### Transitions Smooth (Style TikTok/CapCut)
- `smooth_slide_left` - Glissement fluide vers la gauche
- `smooth_slide_right` - Glissement fluide vers la droite
- `smooth_flip` - Retournement fluide
- `smooth_stretch` - Étirement fluide

## 🚀 Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Ou utiliser le Makefile
make install
```

## 📋 Structure du Projet

```
app/
├── models/
│   └── video_models.py          # Modèles Pydantic (VideoRequest, VideoResponse)
├── services/
│   ├── video_generator_service.py  # Service principal de génération
│   └── transitions/                # Système de transitions
│       ├── base.py                 # Classe abstraite TransitionBase
│       ├── registry.py             # Registry pour enregistrer les transitions
│       ├── fade.py                 # Transitions de fondu
│       ├── zoom.py                 # Transitions de zoom
│       ├── wipe.py                 # Transitions de balayage
│       └── smooth.py               # Transitions smooth (TikTok style)
├── routes/
│   └── video_routes.py          # Routes API
└── main.py                      # Application FastAPI

test_video_generation.py         # Script de test autonome
```

## 🧪 Test Autonome (Sans API)

Le service peut être testé **sans lancer l'API** grâce au script de test:

```bash
python test_video_generation.py
```

Ce script:
1. Génère 3 images colorées de test
2. Teste 5 transitions différentes
3. Crée des vidéos de démonstration dans `/tmp/test_videos/`

### Sortie Attendue

```
============================================================
🎥 TEST DE GÉNÉRATION DE VIDÉOS AVEC TRANSITIONS
============================================================
📸 Génération des images de test...
  ✓ Créé: /tmp/test_images/image_1.png
  ✓ Créé: /tmp/test_images/image_2.png
  ✓ Créé: /tmp/test_images/image_3.png

📋 Transitions disponibles:
  1. cross_dissolve
  2. fade
  ... (16 transitions)

🧪 Test de 5 transitions...

🎬 Test de la transition: cross_dissolve
  ✓ Vidéo générée: /tmp/test_videos/video_cross_dissolve.mp4
  ✓ Durée: 8.50s
  ✓ Résolution: (1280, 720)
  ✓ FPS: 30

✨ Tests réussis: 5/5
🎉 TOUS LES TESTS SONT PASSÉS!
```

## 🌐 Utilisation de l'API

### Démarrer le Serveur

```bash
# Avec Make
make run

# Ou directement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible sur: **http://localhost:8000**

### Documentation Interactive

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints API

### 1. Health Check

```bash
GET /health
```

**Réponse:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Lister les Transitions Disponibles

```bash
GET /api/v1/videos/transitions
```

**Réponse:**
```json
{
  "transitions": [
    "cross_dissolve",
    "flash_white",
    "zoom_in",
    "wipe_left",
    "smooth_zoom",
    ...
  ],
  "count": 16
}
```

### 3. Générer une Vidéo

```bash
POST /api/v1/videos/generate
Content-Type: application/json
```

**Corps de la Requête:**
```json
{
  "images": [
    {
      "timestamp": 0.0,
      "image_path": "/path/to/image1.png"
    },
    {
      "timestamp": 3.0,
      "image_path": "/path/to/image2.png"
    },
    {
      "timestamp": 6.0,
      "image_path": "/path/to/image3.png"
    }
  ],
  "output_path": "/path/to/output.mp4",
  "transition_type": "smooth_zoom",
  "fps": 30,
  "resolution": [1280, 720]
}
```

**Paramètres:**
- `images` (obligatoire): Liste d'images avec timestamps
  - `timestamp`: Position temporelle en secondes
  - `image_path`: Chemin local vers l'image
- `output_path` (obligatoire): Chemin de sortie pour la vidéo
- `transition_type` (optionnel): Type de transition (défaut: "cross_dissolve")
- `fps` (optionnel): Images par seconde (défaut: 30, min: 15, max: 60)
- `resolution` (optionnel): Résolution [largeur, hauteur] (défaut: [1280, 720])

**Réponse:**
```json
{
  "success": true,
  "output_path": "/path/to/output.mp4",
  "duration": 8.5,
  "message": "Video generated successfully",
  "details": {
    "num_images": 3,
    "transition_type": "smooth_zoom",
    "resolution": [1280, 720],
    "fps": 30
  }
}
```

## 💻 Exemples d'Utilisation

### Exemple avec curl

```bash
# Créer le fichier de requête
cat > request.json << EOF
{
  "images": [
    {"timestamp": 0.0, "image_path": "/tmp/image1.jpg"},
    {"timestamp": 2.5, "image_path": "/tmp/image2.jpg"},
    {"timestamp": 5.0, "image_path": "/tmp/image3.jpg"}
  ],
  "output_path": "/tmp/output.mp4",
  "transition_type": "flash_white",
  "fps": 30,
  "resolution": [1920, 1080]
}
EOF

# Envoyer la requête
curl -X POST http://localhost:8000/api/v1/videos/generate \
  -H "Content-Type: application/json" \
  -d @request.json
```

### Exemple avec Python

```python
import requests

payload = {
    "images": [
        {"timestamp": 0.0, "image_path": "/tmp/image1.jpg"},
        {"timestamp": 3.0, "image_path": "/tmp/image2.jpg"},
        {"timestamp": 6.0, "image_path": "/tmp/image3.jpg"}
    ],
    "output_path": "/tmp/my_video.mp4",
    "transition_type": "zoom_in",
    "fps": 30,
    "resolution": [1280, 720]
}

response = requests.post(
    "http://localhost:8000/api/v1/videos/generate",
    json=payload
)

print(response.json())
```

### Exemple avec le Service Directement (Sans API)

```python
from app.services.video_generator_service import VideoGeneratorService
from app.models.video_models import ImageTimestamp

# Créer le service
service = VideoGeneratorService(
    fps=30,
    resolution=(1280, 720)
)

# Préparer les images
images = [
    ImageTimestamp(timestamp=0.0, image_path="/tmp/image1.jpg"),
    ImageTimestamp(timestamp=3.0, image_path="/tmp/image2.jpg"),
    ImageTimestamp(timestamp=6.0, image_path="/tmp/image3.jpg")
]

# Générer la vidéo
result = service.generate_video(
    images=images,
    output_path="/tmp/output.mp4",
    transition_type="smooth_zoom"
)

print(f"Vidéo générée: {result['output_path']}")
print(f"Durée: {result['duration']}s")
```

## 🔧 Ajouter une Nouvelle Transition

L'architecture est conçue pour être facilement extensible:

### 1. Créer une Nouvelle Classe de Transition

```python
# app/services/transitions/my_transition.py

from app.services.transitions.base import TransitionBase
from app.services.transitions.registry import TransitionRegistry
import numpy as np

class MyCustomTransition(TransitionBase):
    """Ma transition personnalisée."""
    
    def apply(self, frame1: np.ndarray, frame2: np.ndarray, progress: float) -> np.ndarray:
        # Implémenter l'effet de transition
        # progress va de 0.0 (frame1) à 1.0 (frame2)
        
        # Exemple simple: blend avec une courbe personnalisée
        eased_progress = progress * progress  # Easing quadratique
        return self.blend_frames(frame1, frame2, eased_progress)

# Enregistrer la transition
TransitionRegistry.register('my_custom', MyCustomTransition)
```

### 2. Importer dans `__init__.py`

```python
# app/services/transitions/__init__.py

from app.services.transitions import my_transition  # Ajouter cette ligne
```

### 3. Utiliser la Nouvelle Transition

```json
{
  "transition_type": "my_custom",
  ...
}
```

C'est tout! Aucune modification du code existant n'est nécessaire.

## 📊 Calcul de la Durée

La durée de chaque image est **calculée automatiquement** à partir des timestamps:

```
Durée de l'image N = timestamp[N+1] - timestamp[N]
```

**Exemple:**
```json
{
  "images": [
    {"timestamp": 0.0, ...},   // Durée: 3.0s (3.0 - 0.0)
    {"timestamp": 3.0, ...},   // Durée: 2.5s (5.5 - 3.0)
    {"timestamp": 5.5, ...}    // Durée: 2.5s (même durée que précédente)
  ]
}
```

## ⚙️ Configuration

Le fichier `.env` contient la configuration de l'application:

```env
# Application
APP_NAME="FastAPI Clean Architecture"
APP_VERSION="1.0.0"
APP_PORT=8000

# API
API_V1_PREFIX=/api/v1

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 🐛 Gestion des Erreurs

L'API retourne des codes HTTP standard:

- **200 OK** - Requête réussie
- **201 Created** - Vidéo générée avec succès
- **400 Bad Request** - Erreur de validation (images invalides, chemins inexistants, etc.)
- **500 Internal Server Error** - Erreur serveur

**Exemple de réponse d'erreur:**
```json
{
  "error": "BadRequestException",
  "message": "Image file not found: /tmp/nonexistent.jpg",
  "details": null
}
```

## 📝 Technologies Utilisées

- **FastAPI** - Framework web moderne et rapide
- **MoviePy** - Manipulation de vidéos
- **OpenCV** - Traitement d'images
- **Pillow** - Manipulation d'images
- **NumPy** - Calculs numériques
- **Pydantic** - Validation de données
- **Uvicorn** - Serveur ASGI

## 🎯 Cas d'Usage

- Création de slideshows dynamiques
- Génération automatique de vidéos marketing
- Montage vidéo automatisé
- Création de stories pour réseaux sociaux
- Présentation de produits
- Tutoriels vidéo automatisés

## 🤝 Contribution

Pour ajouter de nouvelles transitions:
1. Créer une classe héritant de `TransitionBase`
2. Implémenter la méthode `apply()`
3. Enregistrer dans le `TransitionRegistry`
4. Importer dans `__init__.py`

## 📄 License

MIT

---

**Créé avec ❤️ pour des transitions vidéo professionnelles**
