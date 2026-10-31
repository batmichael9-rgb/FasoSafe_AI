# train.py — FasoSafe_AI — Détection Helmet / NoHelmet (version CPU)
from ultralytics import YOLO
from pathlib import Path
import torch

DATA_YAML = Path("Helmet-Detection-4/data.yaml").resolve()
RUNS_DIR  = Path("runs").resolve()

def main():
    print("=== FasoSafe_AI — Entraînement (CPU) ===")
    print(f"CUDA : {torch.cuda.is_available()}")
    print(f"data.yaml : {DATA_YAML}")

    model = YOLO("yolov8n.pt")

    results = model.train(
        data=str(DATA_YAML),
        epochs=20,
        imgsz=512,
        batch=8,
        patience=10,
        project=str(RUNS_DIR),
        name="helmet_v1",
        exist_ok=False,
        pretrained=True,
        optimizer="auto",
        device="cpu",
        workers=2,
        plots=True,
        save=True,
        save_period=5,
    )

    print("\n=== Validation finale ===")
    metrics = model.val()
    print(f"mAP@0.5      : {metrics.box.map50:.4f}")
    print(f"mAP@0.5:0.95 : {metrics.box.map:.4f}")
    print(f"Precision    : {metrics.box.mp:.4f}")
    print(f"Recall       : {metrics.box.mr:.4f}")

    best = RUNS_DIR / "helmet_v1" / "weights" / "best.pt"
    print(f"\n✅ Meilleur modèle : {best}")

if __name__ == "__main__":
    main()