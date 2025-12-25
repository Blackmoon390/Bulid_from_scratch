from flask import Flask, render_template, jsonify, request
import time
import random
import logging  
import AI_ESP32_CONNECTER as ai
import Weather
import threading
import os


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

ai.initialize_model_esp32()

data=Weather.get_weather_data()

app = Flask(__name__)


pump = {
    "running": False if ai.ESP_MOTOR_STATUS == 0 else True,
    "start_time": ai.motor_start_time,
    "temperature": data["temperature"],
    "climate": "Normal",
    "motor": "OFF" if ai.ESP_MOTOR_STATUS == 0 else "ON",
    "soil": "Not Connected" if ai.Soil_Moisture == 0 else ai.Soil_Moisture,
    "air": 45,
    "pippe":56,
    "humidity": data["humidity"],
    "last_action": "NONE"
}

motor_on= {
  "type": "manual",
  "motor": 1
}

motor_off= {
  "type": "manual",
  "motor": 0
}

settings = {
    "tank_capacity": 100,
    "crop_stage": 1,     #1:seeding 2:growth 3:flowering
    "soil_type": 0        #0:sandy 1:loamy 2:clay
}


def update_sensors():
    pump["temperature"] = random.randint(25, 40)
    pump["soil"] = random.randint(20, 80)
    pump["air"] = random.randint(30, 70)
    pump["humidity"] = random.randint(40, 90)
    pump["climate"] = "Hot" if pump["temperature"] > 35 else "Normal"

def get_running_time():
    if pump["running"] and pump["start_time"]:
        return int(time.time() - pump["start_time"])
    return 0

  

@app.route("/")
def index():
    return render_template("index.html", pump_data=pump)

@app.route("/settings")
def settings_page():
    return render_template("settings.html", settings=settings)

@app.route("/save_settings", methods=["POST"])
def save_settings():
    data = request.json

    settings["tank_capacity"] = int(data["tank_capacity"])
    settings["crop_stage"] = int(data["crop_stage"])
    settings["soil_type"] = int(data["soil_type"])

    
    print("⚙️ SETTINGS SAVED")

    return jsonify(success=True)

@app.route("/start", methods=["POST"])
def start_pump():

    ai.send_json(motor_on)

    if not pump["running"]:
        pump["running"] = True
        pump["start_time"] = time.time()
        pump["motor"] = "ON"
        pump["last_action"] = "START"
    return jsonify(success=True)

@app.route("/stop", methods=["POST"])
def stop_pump():

    ai.send_json(motor_off)
    
    print("🔴 STOP button pressed")
    pump["running"] = False
    pump["motor"] = "OFF"
    pump["last_action"] = "STOP"
    return jsonify(success=True)

@app.route("/status")
def status():
    # update_sensors()
    return jsonify({
        "running": pump["running"],
        "motor": pump["motor"],
        "temperature": pump["temperature"],
        "climate": pump["climate"],
        "soil": pump["soil"],
        "air": pump["air"],
        "humidity": pump["humidity"],
        "time": get_running_time(),
        "last_action": pump["last_action"],
        "settings": settings
    })


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        t = threading.Thread(target=ai.monitor_system)
        t.daemon = True
        t.start()

    app.run(host="0.0.0.0",debug=True)
