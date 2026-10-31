// alert_system.ino — FasoSafe AI
// LED verte = OK / LED rouge + buzzer = ALERTE
// Protocole série : recevoir "ALERTE\n" ou "OK\n" depuis Python

const int LED_VERTE = 8;
const int LED_ROUGE = 9;
const int BUZZER    = 10;

void setup() {
  pinMode(LED_VERTE, OUTPUT);
  pinMode(LED_ROUGE, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(LED_VERTE, HIGH);   // état initial : normal
  digitalWrite(LED_ROUGE, LOW);
  noTone(BUZZER);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == "ALERTE") {
      digitalWrite(LED_VERTE, LOW);
      digitalWrite(LED_ROUGE, HIGH);
      tone(BUZZER, 1000);           // 1 kHz
    }
    else if (msg == "OK") {
      digitalWrite(LED_ROUGE, LOW);
      digitalWrite(LED_VERTE, HIGH);
      noTone(BUZZER);
    }
  }
}