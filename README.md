# Formation-EDC-BIM

Projet de formation BP Maçon (Étude de la Construction, Lecture de Plan & BIM) - Bâtiment CFA Bretagne, Campus de Vannes.

## 🚀 Aide & Automatisation Transfert Uptale VR

Pour automatiser et organiser le transfert des scénarios et plannings VR depuis votre application de conception vers **Uptale Studio** :

- 📖 **Guide Complet Markdown** : [`UPTALE_GUIDE_AUTOMATISATION.md`](UPTALE_GUIDE_AUTOMATISATION.md)
- 🌐 **Interface Web Interactive** : [`uptale_guide.html`](uptale_guide.html)
- 📐 **Schéma de données Pivot JSON** : [`uptale_schema.json`](uptale_schema.json)
- 🛠️ **Outil Python de Conversion & Automatisation** : [`tools/uptale_converter.py`](tools/uptale_converter.py)

### Utilisation rapide de l'outil de conversion :
```bash
python3 tools/uptale_converter.py <votre_script.json> <dossier_de_sortie>
```
Il génère les fichiers d'import CSV (quizz, voix-off), l'inventaire des médias et la charge utiles pour l'injection automatisée via RPA (Playwright).
