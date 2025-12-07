# 🎨 Guide des Transitions

Ce guide décrit toutes les transitions implémentées avec leurs caractéristiques et cas d'usage recommandés.

## 📋 Vue d'Ensemble

**17 transitions professionnelles** réparties en 4 catégories:

| Catégorie | Nombre | Description |
|-----------|--------|-------------|
| **Fade** | 3 | Fondus et flashes |
| **Zoom** | 3 | Effets de zoom |
| **Wipe** | 4 | Balayages directionnels |
| **Smooth** | 7 | Transitions fluides style TikTok/CapCut |

---

## 🌅 Catégorie: Fade (Fondu)

### 1. `cross_dissolve` (alias: `fade`)

**Description:** Fondu enchaîné classique et doux.

**Caractéristiques:**
- Transition linéaire simple
- Très naturelle et professionnelle
- La plus utilisée dans le cinéma

**Cas d'usage:**
- Vidéos professionnelles
- Présentations corporate
- Documentaires
- Transitions douces entre scènes

**Durée recommandée:** 0.5 - 1.0 seconde

```python
"transition_type": "cross_dissolve"
```

---

### 2. `flash_white` (alias: `flash`)

**Description:** Flash blanc rapide très populaire sur TikTok.

**Caractéristiques:**
- Fade rapide vers le blanc puis retour
- Effet dynamique et énergique
- Attire l'attention

**Cas d'usage:**
- Vidéos TikTok/Instagram/YouTube Shorts
- Changements de scène dramatiques
- Révélations de produits
- Contenu marketing jeune

**Durée recommandée:** 0.3 - 0.5 seconde

```python
"transition_type": "flash_white"
```

---

### 3. `fade_to_black`

**Description:** Fondu au noir puis retour (cinématique).

**Caractéristiques:**
- Transition classique du cinéma
- Indique un changement de temps ou de lieu
- Plus dramatique que le cross dissolve

**Cas d'usage:**
- Films et courts-métrages
- Vidéos storytelling
- Changements de chapitres
- Transitions temporelles

**Durée recommandée:** 0.8 - 1.5 secondes

```python
"transition_type": "fade_to_black"
```

---

## 🔍 Catégorie: Zoom

### 4. `zoom_in`

**Description:** Zoom progressif vers l'avant avec fondu.

**Caractéristiques:**
- L'image source zoom vers l'avant
- Effet cinématique et immersif
- Crée un sentiment d'approche

**Cas d'usage:**
- Focalisation sur un détail
- Transition vers une scène plus intime
- Effet dramatique
- Vidéos de voyage

**Durée recommandée:** 0.5 - 0.8 seconde

```python
"transition_type": "zoom_in"
```

**Paramètres techniques:**
- Zoom factor: 1.0 → 1.5
- Combine zoom + fade

---

### 5. `zoom_out`

**Description:** Zoom arrière progressif avec fondu.

**Caractéristiques:**
- L'image source s'éloigne
- Effet de révélation
- Sentiment d'ouverture

**Cas d'usage:**
- Révélation d'un contexte plus large
- Transition vers une vue d'ensemble
- Fin de séquence
- Transitions de départ

**Durée recommandée:** 0.5 - 0.8 seconde

```python
"transition_type": "zoom_out"
```

**Paramètres techniques:**
- Zoom factor: 1.5 → 1.0
- Combine zoom + fade

---

### 6. `smooth_zoom`

**Description:** Zoom fluide avec easing (style TikTok).

**Caractéristiques:**
- Courbe d'accélération smooth (ease-in-out)
- Mouvement très naturel
- Zoom subtil (1.0 → 1.3)
- Effet moderne et professionnel

**Cas d'usage:**
- Vidéos TikTok/Instagram
- Contenu lifestyle
- Vlogs
- Transitions douces modernes

**Durée recommandée:** 0.4 - 0.7 seconde

```python
"transition_type": "smooth_zoom"
```

**Fonction d'easing:**
```
ease-in-out: début lent → milieu rapide → fin lente
```

---

## 👉 Catégorie: Wipe (Balayage)

### 7. `wipe_left`

**Description:** Balayage de droite à gauche.

**Caractéristiques:**
- Transition directionnelle claire
- Effet de remplacement progressif
- Dynamique et moderne

**Cas d'usage:**
- Comparaisons avant/après
- Transitions entre lieux
- Slides de présentation
- Effet "tourner la page"

**Durée recommandée:** 0.4 - 0.6 seconde

```python
"transition_type": "wipe_left"
```

---

### 8. `wipe_right`

**Description:** Balayage de gauche à droite.

**Caractéristiques:**
- Opposé du wipe_left
- Sensation de progression
- Mouvement naturel (lecture occidentale)

**Cas d'usage:**
- Navigation vers l'avant
- Progression temporelle
- Défilement de contenu
- Présentation séquentielle

**Durée recommandée:** 0.4 - 0.6 seconde

```python
"transition_type": "wipe_right"
```

---

### 9. `wipe_up`

**Description:** Balayage de bas en haut.

**Caractéristiques:**
- Mouvement vertical
- Sentiment d'élévation
- Effet de révélation

**Cas d'usage:**
- Révélations dramatiques
- Transitions vers le haut (ciel, sommets)
- Effet "lever de rideau"
- Contenu aspirationnel

**Durée recommandée:** 0.4 - 0.6 seconde

```python
"transition_type": "wipe_up"
```

---

### 10. `wipe_down`

**Description:** Balayage de haut en bas.

**Caractéristiques:**
- Mouvement vertical descendant
- Effet de fermeture/conclusion
- Sentiment de descente

**Cas d'usage:**
- Transitions vers le bas
- Conclusions
- Effet "fermeture de rideau"
- Changements de tempo

**Durée recommandée:** 0.4 - 0.6 seconde

```python
"transition_type": "wipe_down"
```

---

## ✨ Catégorie: Smooth (Style TikTok/CapCut)

### 11. `smooth_slide_left`

**Description:** Glissement fluide vers la gauche avec easing.

**Caractéristiques:**
- Mouvement de glissement complet
- Easing cubic pour mouvement naturel
- Les deux images glissent ensemble

**Cas d'usage:**
- Carrousels de produits
- Transitions de stories Instagram
- Effet "swipe"
- Navigation mobile

**Durée recommandée:** 0.5 - 0.8 seconde

```python
"transition_type": "smooth_slide_left"
```

**Fonction d'easing:**
```
ease-in-out-cubic: accélération/décélération cubique
```

---

### 12. `smooth_slide_right`

**Description:** Glissement fluide vers la droite avec easing.

**Caractéristiques:**
- Identique à smooth_slide_left mais direction opposée
- Mouvement naturel et fluide
- Easing cubic

**Cas d'usage:**
- Retour en arrière dans navigation
- Transitions inverses
- Effet "retour"
- Annulation d'action

**Durée recommandée:** 0.5 - 0.8 seconde

```python
"transition_type": "smooth_slide_right"
```

---

### 13. `smooth_flip`

**Description:** Retournement fluide (flip horizontal).

**Caractéristiques:**
- Effet de rotation sur l'axe vertical
- Scale horizontal de 1.0 → 0 → 1.0
- Blend au milieu de la transition
- Effet 3D simulé

**Cas d'usage:**
- Révélations surprenantes
- Changements de perspective
- Effet "carte qui se retourne"
- Transitions ludiques

**Durée recommandée:** 0.6 - 1.0 seconde

```python
"transition_type": "smooth_flip"
```

---

### 14. `smooth_stretch`

**Description:** Étirement fluide avec effet de rebond.

**Caractéristiques:**
- Easing "back" avec overshoot (rebond)
- Effet élastique et dynamique
- Scale progressif
- Très moderne et tendance

**Cas d'usage:**
- Vidéos énergiques et fun
- Contenu jeune/moderne
- Transitions ludiques
- Révélations produits

**Durée recommandée:** 0.5 - 0.8 seconde

```python
"transition_type": "smooth_stretch"
```

**Fonction d'easing:**
```
ease-out-back: overshoot puis retour (effet rebond)
```

### 15. `smooth_spin` (alias: `spin`)

**Description:** Rotation fluide avec zoom (très populaire sur TikTok).

**Caractéristiques:**
- Combine rotation 360° et zoom progressif
- Easing quadratique pour mouvement naturel
- Effet dynamique et accrocheur
- Très tendance sur les réseaux sociaux

**Cas d'usage:**
- Vidéos TikTok/Instagram Reels
- Révélations de produits
- Transitions dynamiques
- Contenu viral/fun

**Durée recommandée:** 0.5 - 0.8 seconde

```python
"transition_type": "smooth_spin"
```

**Paramètres techniques:**
- Rotation : 0° → 360°
- Zoom : 1.0 → 1.3
- Easing : ease-in-out quadratic

---

### 16. `glitch`

**Description:** Effet de glitch digital moderne avec séparation RGB.

**Caractéristiques:**
- Séparation et décalage des canaux RGB
- Intensité maximale au milieu de la transition
- Effet très moderne et technologique
- Easing sinusoïdal pour fluidité

**Cas d'usage:**
- Vidéos tech et gaming
- Contenu futuriste/cyberpunk
- Transitions stylées modernes
- Contenu digital/startup

**Durée recommandée:** 0.4 - 0.6 seconde

```python
"transition_type": "glitch"
```

**Paramètres techniques:**
- Décalage RGB : ±2% de la largeur
- Intensité glitch : 0 → 1 → 0 (pic au milieu)
- Easing : ease-in-out sine

---

### 17. `blur_zoom`

**Description:** Zoom avec flou de mouvement (style CapCut professionnel).

**Caractéristiques:**
- Combine zoom progressif et flou gaussien
- Flou maximal au milieu de la transition
- Effet cinématique et fluide
- Easing cubique pour accélération naturelle

**Cas d'usage:**
- Vidéos professionnelles
- Montages CapCut/Premiere Pro
- Transitions cinématiques
- Vlogs et contenus lifestyle

**Durée recommandée:** 0.6 - 1.0 seconde

```python
"transition_type": "blur_zoom"
```

**Paramètres techniques:**
- Zoom : 1.0 → 1.4
- Flou : kernel adaptatif (3 à 15px)
- Easing : ease-in-out cubic

---

## 🎯 Guide de Sélection Rapide

### Par Style de Contenu

| Style | Transitions Recommandées |
|-------|--------------------------|
| **Professionnel/Corporate** | `cross_dissolve`, `fade_to_black`, `blur_zoom` |
| **TikTok/Instagram** | `flash_white`, `smooth_zoom`, `smooth_slide_left`, `smooth_stretch`, `smooth_spin`, `glitch` |
| **Cinématique** | `fade_to_black`, `zoom_in`, `zoom_out`, `blur_zoom` |
| **Moderne/Dynamique** | `flash_white`, `smooth_flip`, `wipe_left`, `smooth_spin`, `glitch` |
| **Présentation** | `cross_dissolve`, `wipe_right`, `wipe_left` |

### Par Durée Souhaitée

| Durée | Transitions |
|-------|-------------|
| **Rapide (0.3-0.4s)** | `flash_white`, `wipe_*` |
| **Moyenne (0.5-0.7s)** | `cross_dissolve`, `zoom_in`, `smooth_zoom`, `smooth_slide_*` |
| **Lente (0.8-1.5s)** | `fade_to_black`, `smooth_flip` |

### Par Énergie

| Énergie | Transitions |
|---------|-------------|
| **Calme** | `cross_dissolve`, `fade_to_black` |
| **Modérée** | `zoom_*`, `smooth_zoom`, `wipe_*` |
| **Énergique** | `flash_white`, `smooth_stretch`, `smooth_flip` |

---

## 🔧 Paramètres Techniques

### Structure d'une Transition

Toutes les transitions héritent de `TransitionBase` et implémentent:

```python
def apply(self, 
          frame1: np.ndarray,      # Image source
          frame2: np.ndarray,      # Image destination
          progress: float          # 0.0 à 1.0
         ) -> np.ndarray:          # Image résultante
```

### Fonctions d'Easing Utilisées

1. **Linear** - Aucun easing
   - Utilisé par: `cross_dissolve`, `wipe_*`

2. **Ease-in-out Quadratic**
   - Formule: `2t²` si `t < 0.5`, sinon `1 - (-2t + 2)²/2`
   - Utilisé par: `smooth_zoom`, `smooth_flip`

3. **Ease-in-out Cubic**
   - Formule: `4t³` si `t < 0.5`, sinon `1 - (-2t + 2)³/2`
   - Utilisé par: `smooth_slide_*`

4. **Ease-out Back**
   - Formule: `1 + c3(t-1)³ + c1(t-1)²` avec `c1 = 1.70158`
   - Utilisé par: `smooth_stretch`
   - Effet: Overshoot (dépasse puis revient)

---

## 💡 Conseils d'Utilisation

### 1. Cohérence
- Utilisez le **même type de transition** dans une vidéo pour cohérence
- Ou alternez entre 2-3 transitions complémentaires

### 2. Durée
- **Trop court** (< 0.3s): peut sembler brusque
- **Trop long** (> 1.5s): peut ennuyer
- **Optimal**: 0.4 - 0.8 secondes pour la plupart des cas

### 3. Contexte
- **Business**: Privilégier `cross_dissolve`, `fade_to_black`
- **Créatif**: Expérimenter avec `smooth_*`, `flash_white`
- **Storytelling**: `fade_to_black`, `zoom_*`

### 4. Performance
- Les transitions simples (`fade`, `wipe`) sont plus rapides à calculer
- Les transitions avec easing (`smooth_*`) nécessitent plus de calcul

---

## 🚀 Exemples d'Usage Combiné

### Vidéo Marketing Moderne
```json
{
  "transition_type": "flash_white",
  "duration": 0.4
}
```

### Présentation Corporate
```json
{
  "transition_type": "cross_dissolve",
  "duration": 0.7
}
```

### Story Instagram
```json
{
  "transition_type": "smooth_slide_left",
  "duration": 0.5
}
```

### Court-métrage
```json
{
  "transition_type": "fade_to_black",
  "duration": 1.2
}
```

---

**Créé avec ❤️ pour des transitions vidéo professionnelles**
