import gradio as gr
import cv2
from ultralytics import YOLO

model = YOLO("runs/helmet_v1/weights/best.pt")

def detecter(image):
    if image is None:
        return None
    
    # L'image de la webcam arrive en RGB, on la passe en BGR pour YOLO
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    results = model.predict(image_bgr, conf=0.45)
    annotated_img = results[0].plot()
    annotated_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    return annotated_rgb

# Créer l'interface avec accès à la WEBCAM
demo = gr.Interface(
    fn=detecter,
    inputs=gr.Image(sources=["webcam", "upload"], label="Prenez une photo ou importez-en une"),
    outputs=gr.Image(label="Résultat de FasoSafe AI"),
    title="🛡️ FasoSafe AI - Surveillance en direct",
    description="Prenez une photo avec votre webcam ou importez une image pour analyser le port du casque."
)

if __name__ == "__main__":
    demo.launch()