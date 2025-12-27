Intelligent Irrigation Monitoring System (NN + IoT)

This repository contains an edge-based intelligent irrigation system that uses an ESP32, a soil moisture sensor, and a neural network trained in Python to automatically control a water pump.

The system runs locally over Wi-Fi, performs AI inference on the ESP32, and provides a web interface for monitoring and manual control.

Overview

The system automates irrigation using real soil and environmental conditions instead of fixed schedules.
It supports AI-based automatic control, manual override, and fallback logic for sensor failures.

Features

Neural network–based irrigation decision

AI inference running on ESP32

Soil moisture sensing via ESP32 ADC

Automatic and manual motor control

REST API communication

Web dashboard for monitoring

Sensor disconnection detection and fallback

Local Wi-Fi operation (no cloud dependency)

Project Structure
.
├── esp32/
│   └── irrigation_esp32.ino
├── python/
│   ├── intialzer.py
│   ├── Scratch_model_training.py
│   ├── main.py
│   └── model.json
├── web/
│   ├── app.py
│   ├── templates/
│   └── static/
├── README.md

How It Works (Brief)

System configuration and parameters are initialized.

Neural network is trained from scratch.

Trained model is used for real-time inference and ESP32 communication.

ESP32 controls the irrigation motor based on AI decisions.

Web dashboard displays live status and allows manual control.

How to Run
1. Prerequisites

Python 3.9+

ESP32 board support installed in Arduino IDE

ESP32 and PC connected to the same Wi-Fi network

Hardware connections completed

2. Run Python Scripts (Important Order)

Navigate to the Python directory:

cd python


Run the scripts in the following order:

Step 1: Initialize system parameters
python intialzer.py

Step 2: Train neural network from scratch
python Scratch_model_training.py


This generates the trained model parameters and saves them as model.json.

Step 3: Start the main system
python main.py


This script:

Sends the model and input data to ESP32

Receives sensor values and motor status

Syncs data with the web dashboard

3. Flash the ESP32

Open esp32/irrigation_esp32.ino in Arduino IDE

Update Wi-Fi credentials:

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";


Select ESP32 Dev Module and correct COM port

Upload the code to ESP32

4. Start the Web Dashboard

From the web directory:

cd web
python app.py


Open a browser and visit:

http://localhost:5000

Fallback Logic

Soil sensor connected → ESP32 ADC value is used

Sensor disconnected → Python-provided moisture is used

Both unavailable → safe default irrigation behavior

Limitations

Single-layer neural network

Local network operation only

Designed for small-scale deployments

Future Improvements

Multi-layer neural networks

Cloud integration

Long-range communication (LoRaWAN)

Solar-powered ESP32 nodes

Historical data analytics

Mobile application support
