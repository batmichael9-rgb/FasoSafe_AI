# predict.py — FasoSafe AI — Détection + alerte Arduino
from ultralytics import YOLO
import cv2
import serial
import time
from collections import deque

# ── PARAMÈTRES ──────────────────────────────────────
MODEL_PATH      = "runs/helmet_v1/weights/best.pt"

# ⚠️ CHOIX DE LA SOURCE :
# - Webcam : 0
# - Image : "sanscasque.jpg"
# - Vidéo : "videos/test.mp4"
SOURCE          =r"C:\Users\batmi\OneDrive\Documents\FasoSafe_AI\image test\Sécurité_routière___l’ONASER_sensibilise_sur_le_port_du_casque_à_Banfora(240p).mp4"
CONF            = 0.45
ARDUINO_PORT    = "COM8"  # ⚠️ Vérifiez que c'est bien le port de votre Arduino 
ARDUINO_BAUD    = 9600
CONFIRM_FRAMES  = 3                   
NAMES           = {0: "Helmet", 1: "NoHelmet"}
# ────────────────────────────────────────────────────

def open_arduino():
    if ARDUINO_PORT is None:
        print("[!] Mode démo sans Arduino")
        return None
    try:
        ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD, timeout=1)
        time.sleep(2)  # Reset Arduino
        print(f"[✓] Arduino connecté sur {ARDUINO_PORT}")
        return ser
    except Exception as e:
        print(f"[!] Arduino indisponible ({e})")
        return None

def send(ser, msg):
    if ser:
        try:
            ser.write((msg + "\n").encode())
        except Exception:
            pass

def main():
    model = YOLO(MODEL_PATH)
    ser   = open_arduino()
    
    is_image = isinstance(SOURCE, str) and SOURCE.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    cap = None

    try: # <--- DÉBUT DE LA SÉCURITÉ
        if is_image:
            print(f"\nAnalyse de l'image : {SOURCE}")
            frame = cv2.imread(SOURCE)
            if frame is None:
                print("❌ Impossible de lire l'image.")
                return
            
            results = model.predict(frame, conf=CONF, verbose=False)[0]
            n_helmet, n_nohelmet = 0, 0
            
            for box in results.boxes:
                cls_id = int(box.cls[0])
                conf_v = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = NAMES.get(cls_id, str(cls_id))
                color = (0, 255, 0) if label == "Helmet" else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} {conf_v:.2f}", (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                if label == "Helmet": n_helmet += 1
                else: n_nohelmet += 1

            if n_nohelmet > 0:
                send(ser, "ALERTE")
                print("🚨 ALERTE — personne sans casque détectée !")
                cv2.putText(frame, "!! ALERTE !!", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            else:
                send(ser, "OK")

            cv2.putText(frame, f"Helmet: {n_helmet}   NoHelmet: {n_nohelmet}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.imshow("FasoSafe AI - Image", frame)
            print("👉 Appuyez sur n'importe quelle touche pour fermer...")
            cv2.waitKey(0)

        else:
            print(f"\nOuverture du flux vidéo...")
            cap = cv2.VideoCapture(SOURCE)
            cv2.namedWindow("FasoSafe AI - Direct", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("FasoSafe AI - Direct", 1280, 720) 
            if not cap.isOpened():
                print("❌ Impossible d'ouvrir la source.")
                return

            history = deque(maxlen=CONFIRM_FRAMES)
            alert_active = False

            while True:
                ret, frame = cap.read()
                if not ret: break
                
                results = model.predict(frame, conf=CONF, verbose=False)[0]
                n_helmet, n_nohelmet = 0, 0
                for box in results.boxes:
                    cls_id = int(box.cls[0])
                    conf_v = float(box.conf[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = NAMES.get(cls_id, str(cls_id))
                    color = (0, 255, 0) if label == "Helmet" else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{label} {conf_v:.2f}", (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    if label == "Helmet": n_helmet += 1
                    else: n_nohelmet += 1

                history.append(n_nohelmet > 0)
                confirmed = len(history) == CONFIRM_FRAMES and all(history)

                if confirmed and not alert_active:
                    send(ser, "ALERTE")
                    alert_active = True
                    print("🚨 ALERTE — personne sans casque confirmée")
                elif not confirmed and alert_active:
                    send(ser, "OK")
                    alert_active = False
                    print("✅ Situation normale")

                cv2.putText(frame, f"Helmet: {n_helmet}   NoHelmet: {n_nohelmet}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                if alert_active:
                    cv2.putText(frame, "!! ALERTE !!", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

                cv2.imshow("FasoSafe AI - Direct", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break

    except KeyboardInterrupt:
        print("\n[!] Arrêt manuel demandé.")
    
    finally: # <--- CETTE PARTIE S'EXÉCUTE TOUJOURS À LA FIN
        print("Nettoyage et extinction de l'Arduino...")
        send(ser, "OK") # On force l'extinction du buzzer
        time.sleep(0.5) # On laisse le temps à l'Arduino de lire le message
        if ser: ser.close()
        if cap: cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()