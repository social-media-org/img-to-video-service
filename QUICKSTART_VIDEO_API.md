# 🚀 Quick Start - API de Génération de Vidéos

Guide de démarrage rapide pour utiliser l'API de génération de vidéos avec transitions.

## ⚡ Installation (30 secondes)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Démarrer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ L'API est maintenant disponible sur **http://localhost:8000**

---

## 🧪 Test Rapide (1 minute)

### Option 1: Script de Test Autonome

```bash
python test_video_generation.py
```

Ce script:
- Génère 3 images de test automatiquement
- Teste 5 transitions différentes
- Crée les vidéos dans `/tmp/test_videos/`

### Option 2: Test Manuel avec Curl

```bash
# 1. Créer des images de test (ou utiliser vos propres images)
# Les images doivent exister localement

# 2. Envoyer une requête
curl -X POST http://localhost:8000/api/v1/videos/generate \
  -H "Content-Type: application/json" \
  -d '{
    "images": [
      {"timestamp": 0.0, "image_path": "/chemin/vers/image1.jpg"},
      {"timestamp": 3.0, "image_path": "/chemin/vers/image2.jpg"},
      {"timestamp": 6.0, "image_path": "/chemin/vers/image3.jpg"}
    ],
    "output_path": "/tmp/ma_video.mp4",
    "transition_type": "smooth_zoom"
  }'
```

---

## 📡 API Endpoints

### 1. Health Check
```bash
GET /health
```

### 2. Lister les Transitions
```bash
GET /api/v1/videos/transitions

# Retourne:
{
  "transitions": [
    "cross_dissolve", "flash_white", "zoom_in",
    "wipe_left", "smooth_zoom", ...
  ],
  "count": 16
}
```

### 3. Générer une Vidéo
```bash
POST /api/v1/videos/generate
```

**Paramètres minimum:**
```json
{
  "images": [
    {"timestamp": 0.0, "image_path": "/path/img1.jpg"},
    {"timestamp": 3.0, "image_path": "/path/img2.jpg"}
  ],
  "output_path": "/path/output.mp4"
}
```

**Paramètres complets:**
```json
{
  "images": [...],
  "output_path": "/path/output.mp4",
  "transition_type": "smooth_zoom",    // défaut: "cross_dissolve"
  "fps": 30,                           // défaut: 30 (min: 15, max: 60)
  "resolution": [1280, 720]            // défaut: [1280, 720]
}
```

---

## 🎨 Transitions Disponibles (Choix Rapide)

### Pour Vidéos Professionnelles
- `cross_dissolve` - Fondu classique ⭐
- `fade_to_black` - Cinématique

### Pour TikTok/Instagram
- `flash_white` - Flash blanc dynamique ⭐
- `smooth_zoom` - Zoom fluide ⭐
- `smooth_slide_left` - Glissement fluide

### Pour Effets Dynamiques
- `zoom_in` - Zoom avant
- `wipe_left` - Balayage gauche
- `smooth_flip` - Retournement

**⭐ = Les plus populaires**

[Voir le guide complet des transitions →](TRANSITIONS_GUIDE.md)

---

## 💻 Utilisation en Python

### Avec l'API (Requêtes HTTP)

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/videos/generate",
    json={
        "images": [
            {"timestamp": 0.0, "image_path": "/path/img1.jpg"},
            {"timestamp": 3.0, "image_path": "/path/img2.jpg"},
            {"timestamp": 6.0, "image_path": "/path/img3.jpg"}
        ],
        "output_path": "/tmp/video.mp4",
        "transition_type": "smooth_zoom"
    }
)

result = response.json()
print(f"Vidéo créée: {result['output_path']}")
```

### Directement avec le Service (Sans API)

```python
from app.services.video_generator_service import VideoGeneratorService
from app.models.video_models import ImageTimestamp

# Créer le service
service = VideoGeneratorService(fps=30, resolution=(1280, 720))

# Définir les images
images = [
    ImageTimestamp(timestamp=0.0, image_path="/path/img1.jpg"),
    ImageTimestamp(timestamp=3.0, image_path="/path/img2.jpg"),
    ImageTimestamp(timestamp=6.0, image_path="/path/img3.jpg")
]

# Générer la vidéo
result = service.generate_video(
    images=images,
    output_path="/tmp/video.mp4",
    transition_type="smooth_zoom"
)

print(f"✓ Vidéo: {result['output_path']}")
print(f"✓ Durée: {result['duration']}s")
```

---

## ⚙️ Configuration Rapide

### Changer le Port
```bash
# Dans .env
APP_PORT=8080

# Puis redémarrer
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Changer la Résolution par Défaut
```python
service = VideoGeneratorService(
    fps=60,                    # Plus fluide
    resolution=(1920, 1080)    # Full HD
)
```

---

## 🎯 Exemples Rapides

### Slideshow Simple (3 images, 3 secondes chacune)
```python
images = [
    ImageTimestamp(timestamp=0.0, image_path="img1.jpg"),
    ImageTimestamp(timestamp=3.0, image_path="img2.jpg"),
    ImageTimestamp(timestamp=6.0, image_path="img3.jpg")
]
```
→ Durée totale: ~8.5s (incluant transitions)

### Durées Variables
```python
images = [
    ImageTimestamp(timestamp=0.0, image_path="img1.jpg"),    # 1 seconde
    ImageTimestamp(timestamp=1.0, image_path="img2.jpg"),    # 4 secondes
    ImageTimestamp(timestamp=5.0, image_path="img3.jpg")     # 4 secondes
]
```

### Vidéo Haute Qualité
```json
{
  "fps": 60,
  "resolution": [1920, 1080],
  "transition_type": "smooth_zoom"
}
```

---

## 🐛 Résolution Rapide de Problèmes

### Erreur: "Image file not found"
✅ Vérifiez que les chemins d'images sont corrects et que les fichiers existent

### Erreur: "Unknown transition"
✅ Listez les transitions disponibles:
```bash
curl http://localhost:8000/api/v1/videos/transitions
```

### Erreur: "At least 2 images are required"
✅ Fournissez au minimum 2 images

### Le serveur ne démarre pas
✅ Vérifiez que le port 8000 n'est pas déjà utilisé:
```bash
lsof -i :8000
```

---

## 📚 Documentation Complète

- **[VIDEO_API_README.md](VIDEO_API_README.md)** - Documentation API complète
- **[TRANSITIONS_GUIDE.md](TRANSITIONS_GUIDE.md)** - Guide détaillé des 16 transitions
- **[examples_usage.py](examples_usage.py)** - 7 exemples pratiques
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Récapitulatif technique

---

## 🚀 Prochaines Étapes

1. ✅ Tester avec vos propres images
2. ✅ Expérimenter avec différentes transitions
3. ✅ Ajuster FPS et résolution selon vos besoins
4. ✅ Intégrer dans votre application

### Ajouter une Nouvelle Transition

Créer un fichier `app/services/transitions/ma_transition.py`:

```python
from app.services.transitions.base import TransitionBase
from app.services.transitions.registry import TransitionRegistry
import numpy as np

class MaTransition(TransitionBase):
    def apply(self, frame1, frame2, progress):
        # Votre effet ici
        return self.blend_frames(frame1, frame2, progress)

TransitionRegistry.register('ma_transition', MaTransition)
```

Puis l'importer dans `app/services/transitions/__init__.py`. C'est tout! ✅

---

## 📞 Support

Pour des questions ou problèmes:
1. Consultez d'abord la documentation complète
2. Vérifiez les exemples dans `examples_usage.py`
3. Testez avec `test_video_generation.py`

---

**Prêt à créer des vidéos incroyables! 🎬**
