# Guide Complet : Automatisation & Organisation du Transfert vers Uptale VR

> **Auteur** : Pascal AMET / Bâtiment CFA Bretagne
> **Objectif** : Passer d'une application de conception / scénarisation VR (planning + script) à un module interactif sur la plateforme **Uptale Studio** de manière automatisée, rapide et sans erreurs.

---

## 1. Comprendre l'Architecture d'un Module Uptale VR

Uptale Studio structure un module de formation en Réalité Virtuelle selon la hiérarchie suivante :

```
[ MODULE VR ]
  ├── Méta-données (Titre, Description, Langue, Mode de suivi SCORM/xAPI)
  ├── Médias 360° (Photos equirectangulaires 2:1 ou Vidéos 360°)
  ├── [ SCÈNE 1 ]
  │     ├── Arrière-plan (Photo/Vidéo 360)
  │     ├── Voix-off / Sous-titre (TTS ou Audio .mp3)
  │     ├── Orientation initiale (Yaw, Pitch)
  │     └── Tags / Hotspots (Ancre visuelle 3D)
  │           ├── Tag Information (Texte, Image, Vidéo 2D)
  │           ├── Tag Question / Quizz (QCM, QCU, Vrai/Faux, Zone à cliquer)
  │           ├── Tag Liens / Transition Scène
  │           └── Tag Déclencheur / Score
  └── [ SCÈNE 2 ... N ]
```

---

## 2. Le Défi du Transfert Manuel & La Solution d'Automatisation

### Pourquoi le transfert manuel est long & complexe :
1. Repositionnement manuel de chaque hotspot et recopie individuelle du texte des questions/réponses.
2. Saisie manuelle des voix-off et des feedbacks d'erreur/réussite.
3. Risque élevé d'erreurs de frappe ou d'incohérences de nommage entre la phase d'ingénierie pédagogique et l'édition sur Uptale Studio.

### La Solution : Les 3 Voies d'Automatisation

1. **Voie 1 : L'Import CSV / Excel Batch (Prise en charge native Uptale)**
   - Exporter l'ensemble des quizz, questions, choix et textes de voix-off depuis votre application dans des CSV structurés.
   - Utiliser la fonction d'import en masse ("Bulk Import") d'Uptale Studio pour créer toutes les questions en un clic.

2. **Voie 2 : Injection via Payload RPA / Extension Navigateur (Playwright / Puppeteer)**
   - Un script d'automatisation lit le fichier de structure JSON (`uptale_rpa_payload.json`) généré par l'outil de conversion et interagit automatiquement avec l'interface Web d'Uptale Studio pour :
     - Créer l'arborescence des scènes.
     - Associer les médias 360 correspondants.
     - Positionner précisément les hotspots selon les coordonnées angulaires `(yaw, pitch)`.

3. **Voie 3 : Intégration API REST / Studio SDK (Espace Entreprise / API Premium)**
   - Si votre abonnement Uptale inclut l'accès aux API Studio : poussée directe du JSON pivot via requête HTTP POST vers l'endpoint de l'organisation.

---

## 3. Modèle de Données Pivot (JSON Schema)

Pour connecter votre application de planning/script à Uptale, votre application doit générer un fichier JSON respectant la structure pivot `uptale_schema.json` :

### Exemple de fichier JSON (`script_module.json`)
```json
{
  "module_info": {
    "title": "Module VR - Sécurité Chantier BP Maçon",
    "description": "Scénario d'évaluation des EPI et de la lecture de plan sur chantier réel",
    "author": "Pascal AMET",
    "language": "fr"
  },
  "scenes": [
    {
      "scene_id": "scene_01_accueil",
      "title": "Zone d'accueil et briefing",
      "media_type": "photo_360",
      "media_file": "360_accueil_chantier.jpg",
      "initial_view": { "yaw": 0, "pitch": 0 },
      "voiceover": {
        "text": "Bienvenue sur le chantier. Vérifiez vos équipements.",
        "audio_file": "voiceover_scene1.mp3",
        "auto_play": true
      },
      "hotspots": [
        {
          "hotspot_id": "hs_01_quiz_epi",
          "title": "Quiz EPI",
          "type": "quiz_question",
          "position": { "yaw": 45, "pitch": 0 },
          "content": {
            "quiz": {
              "question": "Quel équipement est obligatoire dès l'accès au chantier ?",
              "question_type": "single_choice",
              "options": [
                { "id": "opt1", "text": "Casque de chantier à jugulaire", "is_correct": true },
                { "id": "opt2", "text": "Casquette simple", "is_correct": false }
              ],
              "points": 10,
              "explanation": "Le casque est obligatoire."
            }
          }
        }
      ]
    }
  ]
}
```

---

## 4. Outil de Conversion Automatique (`uptale_converter.py`)

Un outil en ligne de commande dédié a été développé dans le répertoire de votre projet :
`tools/uptale_converter.py`

### Utilisation :
```bash
python3 tools/uptale_converter.py <votre_script.json> <dossier_de_sortie>
```

### Fichiers générés automatiquement :
1. **`uptale_quizzes_import.csv`** : Fichier CSV au format de séparation `;` et encodage UTF-8 BOM, prêt pour l'import de quizz dans Uptale Studio.
2. **`uptale_voiceovers_subtitles.csv`** : Fichier récapitulatif des scripts audio et sous-titres pour la génération Voix-off TTS.
3. **`uptale_media_manifest.json`** : Inventaire exhaustif des médias requis (images 360, sons mp3, illustrations) pour vérifier que rien ne manque avant le transfert.
4. **`uptale_rpa_payload.json`** : Données structurées par scène et hotspots avec coordonnées spatiales précises pour l'injecteur RPA Playwright.

---

## 5. Procédure & Checklist d'Organisation Étape par Étape

### Phase 1 : Préparation & Convention de Nommage
- [ ] Nommer tous vos médias 360° selon l'ID de la scène (ex: `S01_Accueil_360.jpg`, `S02_Banches_360.jpg`).
- [ ] Préparer vos voix-off au format `.mp3` ou utiliser la voix de synthèse intégrée d'Uptale.
- [ ] Vérifier que votre script dans l'application contient toutes les questions/réponses et les bonnes annotations.

### Phase 2 : Export & Conversion
- [ ] Exporter le fichier JSON de votre application.
- [ ] Lancer la commande de conversion avec `uptale_converter.py`.
- [ ] Consulter le fichier `uptale_media_manifest.json` pour confirmer la présence de tous les fichiers médias.

### Phase 3 : Transfert sur Uptale Studio
1. **Création du Module** : Dans Uptale Studio, créer un nouveau module et renseigner le titre.
2. **Batch Upload Médias 360** : Glisser-déposer l'ensemble des photos/vidéos 360° identifiées dans le manifest.
3. **Import des Quizz** : Cliquer sur **Importer les Quizz / Questions** et sélectionner `uptale_quizzes_import.csv`.
4. **Vérification / Placement Spatial** : Utiliser les coordonnées `yaw` / `pitch` figurant dans le rapport pour positionner visuellement les hotspots dans chaque scène.

---

## 6. Automatisation Complète par Script RPA (Playwright Node.js/Python)

Pour zéro clic manuel, vous pouvez utiliser un script Playwright qui se connecte à votre compte Uptale Studio et exécute automatiquement les opérations de création de scènes et de hotspots en bouclant sur `uptale_rpa_payload.json`.

Exemple de fragment de code Playwright :
```javascript
const { chromium } = require('playwright');
const rpaData = require('./uptale_export/uptale_rpa_payload.json');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  // 1. Connexion à Uptale Studio
  await page.goto('https://studio.uptale.io/login');
  await page.fill('#email', process.env.UPTALE_EMAIL);
  await page.fill('#password', process.env.UPTALE_PASSWORD);
  await page.click('button[type="submit"]');

  // 2. Boucle sur les scènes à injecter
  for (const scene of rpaData.actions) {
    console.log(`Création automatique de la scène : ${scene.title}`);
    // Interaction avec l'éditeur 3D Uptale...
  }

  await browser.close();
})();
```

---

*Ce guide et les outils associés permettent de réduire le temps de transfert de plusieurs heures à seulement quelques minutes par module VR !*
