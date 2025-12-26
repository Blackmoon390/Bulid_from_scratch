#include <WiFi.h>
#include <ArduinoJson.h>
#include <math.h>

/* ================= WIFI ================= */
const char* ssid = "your iot wifi or home server wifi or system wifi to connect esp";
const char* password = "your wifi password";

WiFiServer server(80);
WiFiClient client;

/* ================= NN SHAPE ================= */
#define NN_INPUT 9

/* ================= HARDWARE ================= */
#define MOTOR_PIN 26
#define SOIL_PIN 34

/* ================= ADC ================= */
#define ADC_MAX 4095.0
#define SOIL_DISCONNECTED_THRESHOLD 4000   // > this = sensor not connected

/* ================= MODEL STORAGE ================= */
float mean[NN_INPUT], stdv[NN_INPUT];
float w1[NN_INPUT], b1;
bool modelReady = false;

/* ================= ACTIVATION ================= */
float sigmoid(float x) {
  return 1.0 / (1.0 + exp(-x));
}

/* ================= SOIL SENSOR ================= */
float readSoilMoisture() {
  int raw = analogRead(SOIL_PIN);

  // Sensor not connected or floating
  if (raw > SOIL_DISCONNECTED_THRESHOLD) {
    return -1;   // invalid
  }

  // Map ADC → %
  float moisture = map(raw, 4095, 1500, 0, 100);

  if (moisture < 0) moisture = 0;
  if (moisture > 100) moisture = 100;

  return moisture;
}

/* ================= HTTP JSON RESPONSE ================= */
void sendJson(WiFiClient &client, JsonDocument &res) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.println();
  serializeJson(res, client);
  client.println();
  client.stop();
}

/* ================= DEFAULT MODEL ================= */
void loadDefaultModel() {

  float default_mean[NN_INPUT] = {
    4.3365773, 2.0724838, 6.5155836,
    6.9384437, 7.0219887, 2.0105541,
    2.4799751, 2.5793617, 2.3739966
  };

  float default_std[NN_INPUT] = {1,1,1,1,1,1,1,1,1};

  float default_w1[NN_INPUT] = {
   -4.4337863, 0.20415738, 0.86087825,
    0.70885146, 0.65811204, -4.54027617,
    0.26513432, 0.29909167, 0.06024213
  };

  for (int i = 0; i < NN_INPUT; i++) {
    mean[i] = default_mean[i];
    stdv[i] = default_std[i];
    w1[i]   = default_w1[i];
  }

  b1 = 5.5392888;
  modelReady = true;

  Serial.println(" Default AI model loaded");
}

/* ================= LOAD MODEL FROM JSON ================= */
void loadModel(JsonDocument &doc, WiFiClient &client) {

  for (int i = 0; i < NN_INPUT; i++) {
    mean[i] = doc["mean"][i];
    stdv[i] = doc["std"][i];
    if (stdv[i] == 0) stdv[i] = 1;
    w1[i]   = doc["w1"][i][0];
  }

  b1 = doc["b1"];
  modelReady = true;

  StaticJsonDocument<128> res;
  res["status"] = "model_loaded";
  res["motor_status"] = digitalRead(MOTOR_PIN);

  sendJson(client, res);
}

/* ================= NN PREDICT ================= */
int predict(float raw[], float &prob) {

  float out = 0;
  for (int i = 0; i < NN_INPUT; i++) {
    float x = (raw[i] - mean[i]) / stdv[i];
    out += x * w1[i];
  }

  out += b1;
  prob = sigmoid(out);

  return (prob >= 0.5) ? HIGH : LOW;
}

/* ================= AUTO MODE ================= */
void handleAuto(JsonDocument &doc, WiFiClient &client) {

  StaticJsonDocument<256> res;

  if (!modelReady) {
    res["error"] = "model_not_loaded";
    sendJson(client, res);
    return;
  }

  float input[NN_INPUT];

  /* 🔹 Soil moisture priority logic */
  float sensorMoisture = readSoilMoisture();

  if (sensorMoisture >= 0) {
    input[0] = sensorMoisture;              // SENSOR wins
  } else if (!doc["input"][0].isNull()) {
    input[0] = doc["input"][0];             // Python fallback
  } else {
    input[0] = 50;                          // safe default
  }

  /* Remaining inputs from Python */
  for (int i = 1; i < NN_INPUT; i++) {
    input[i] = doc["input"][i] | 0;
  }

  float prob;
  int motor = predict(input, prob);

  digitalWrite(MOTOR_PIN, motor);

  res["soil_moisture"] = input[0];
  res["motor_status"]  = motor;
  res["probability"]   = prob;
  res["control"]       = "ai";

  sendJson(client, res);
}

/* ================= MANUAL MODE ================= */
void handleManual(JsonDocument &doc, WiFiClient &client) {

  int motor = doc["motor"];
  digitalWrite(MOTOR_PIN, motor);

  StaticJsonDocument<128> res;
  res["motor_status"] = motor;
  res["control"] = "manual";

  sendJson(client, res);
}

/* ================= SETUP ================= */
void setup() {

  Serial.begin(115200);

  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(SOIL_PIN, INPUT);
  digitalWrite(MOTOR_PIN, LOW);

  loadDefaultModel();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");
  Serial.println(WiFi.localIP());

  server.begin();
}

/* ================= LOOP ================= */
void loop() {

  client = server.available();
  if (!client) return;

  String payload = "";
  unsigned long start = millis();

  while (client.connected() && millis() - start < 10000) {
    while (client.available()) {
      payload += (char)client.read();
      start = millis();
    }
    delay(1);
  }

  if (payload.length() == 0) {
    client.stop();
    return;
  }

  int jsonStart = payload.indexOf("\r\n\r\n");
  if (jsonStart == -1) {
    client.stop();
    return;
  }

  payload = payload.substring(jsonStart + 4);

  StaticJsonDocument<25000> doc;
  if (deserializeJson(doc, payload)) {
    StaticJsonDocument<64> res;
    res["error"] = "invalid_json";
    sendJson(client, res);
    return;
  }

  const char* type = doc["type"];

  if (strcmp(type, "model") == 0) {
    loadModel(doc, client);
  }
  else if (strcmp(type, "data") == 0) {
    handleAuto(doc, client);
  }
  else if (strcmp(type, "manual") == 0) {
    handleManual(doc, client);
  }
  else {
    StaticJsonDocument<64> res;
    res["error"] = "unknown_type";
    sendJson(client, res);
  }
}