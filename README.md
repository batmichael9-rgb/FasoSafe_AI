
# 🛡️ FasoSafe AI - Helmet Detection (Road Traffic)

A deep learning project (YOLOv8) capable of detecting whether a motorcyclist is wearing a helmet or not, with a hardware alert via Arduino (LED + buzzer).

## 📁 Project Structure
- `train.py`: Script for training the YOLOv8 model.
- `predict.py`: Script for real-time detection (webcam/video/image) that sends a serial alert to the Arduino.
- `app_web.py`: Local web interface (Gradio) for testing the model.
- `arduino/alert_system.ino`: C++ code for the Arduino board (green/red LED + buzzer).
- `requirements.txt`: List of Python dependencies.

## 🚀 How to get the project running at home

### 1. Prerequisites
- Python 3.10 or 3.11
- An Arduino board (Uno, Nano, etc.) with an LED and buzzer

### 2. Installation
Open a terminal in the project folder and type:
```bash
pip install -r requirements.txt



 