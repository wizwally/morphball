#include <LSM6DS3.h>
#include <Wire.h>

// Pin definitions
#define PIN_ALIVE       D5   // ← segnale dallo ESP32 (HIGH = attivo)
#define PIN_MOTION_OUT  D4   // → va a GPIO13 ESP32 per wake/reset timeout

// Oggetto IMU
LSM6DS3 IMU(I2C_MODE, 0x6A);  // I2C device address 0x6A

// Variabili lettura IMU
float aX, aY, aZ;
const float accelerationThreshold = 2.5;  // soglia in G per "movimento"
int ESP_alive = 0;

void setup() {
  pinMode(PIN_ALIVE, INPUT);
  pinMode(PIN_MOTION_OUT, OUTPUT);
  digitalWrite(PIN_MOTION_OUT, LOW);

  Serial.begin(115200);
  while (!Serial);

  if (IMU.begin() != 0) {
    Serial.println("⚠️ IMU non trovata o errore inizializzazione");
  } else {
    Serial.println("✅ IMU pronta — lettura accelerazioni");
    Serial.println("aX,aY,aZ");
  }
}

void loop() {
  // Lettura stato attuale del pin alive da ESP32
  int _ESP_alive = digitalRead(PIN_ALIVE);
  if (_ESP_alive != ESP_alive) {
    ESP_alive = _ESP_alive;
    Serial.print("🔄 ESP Animation state: ");
    Serial.println(ESP_alive ? "ON" : "OFF");
  }

  // Lettura accelerometro
  aX = IMU.readFloatAccelX();
  aY = IMU.readFloatAccelY();
  aZ = IMU.readFloatAccelZ();

  float aSum = fabs(aX) + fabs(aY) + fabs(aZ);

  static unsigned long lastMove = 0;
  if (aSum >= accelerationThreshold) {
    if (millis() - lastMove > 200) {
      Serial.println("📡 Movimento → alza PIN su ESP32");
      digitalWrite(PIN_MOTION_OUT, HIGH);
      lastMove = millis();
    }
  } else {
    digitalWrite(PIN_MOTION_OUT, LOW);
  }

  delay(50);  // frequenza di aggiornamento IMU
}