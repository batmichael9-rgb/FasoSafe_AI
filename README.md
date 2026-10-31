# 🛡️ FasoSafe AI - Détection de Casque (Circulation Routière)

Projet Deep Learning (YOLOv8) capable de détecter si un motard porte un casque ou non, avec alerte matérielle via Arduino (LED + Buzzer).

## 📁 Structure du projet
- `train.py` : Script d'entraînement du modèle YOLOv8.
- `predict.py` : Script de détection en temps réel (webcam/vidéo/image) avec envoi d'alerte série à l'Arduino.
- `app_web.py` : Interface web locale (Gradio) pour tester le modèle.
- `arduino/alert_system.ino` : Code C++ pour la carte Arduino (LED verte/rouge + Buzzer).
- `requirements.txt` : Liste des dépendances Python.

## 🚀 Comment lancer le projet chez soi

### 1. Prérequis
- Python 3.10 ou 3.11
- Une carte Arduino (Uno, Nano, etc.) avec LED et Buzzer

### 2. Installation
Ouvrez un terminal dans le dossier du projet et tapez :
```bash
pip install -r requirements.txt