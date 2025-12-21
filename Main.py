from flask import Flask, render_template, jsonify
import time
import random
import logging  


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

#trail inputs
pump = {
    "running": False,
    "start_time": None,
    "temperature": 30,
    "climate": "Normal",
    "motor": "OFF",
    "soil": 45,
    "air": 55,
    "humidity": 60
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
    return render_template(
        "index.html",
        pump_data={
            "running": pump["running"]
        }
    )

@app.route("/start", methods=["POST"])
def start_pump():
    if not pump["running"]:
        pump["running"] = True
        pump["start_time"] = time.time()
        pump["motor"] = "ON"
    return jsonify(success=True)

@app.route("/stop", methods=["POST"])
def stop_pump():
    pump["running"] = False
    pump["motor"] = "OFF"
    return jsonify(success=True)

@app.route("/status")
def status():
    update_sensors()
    return jsonify({
        "running": pump["running"],
        "motor": pump["motor"],
        "temperature": pump["temperature"],
        "climate": pump["climate"],
        "soil": pump["soil"],
        "air": pump["air"],
        "humidity": pump["humidity"],
        "time": get_running_time()
    })


if __name__ == "__main__":
    app.run(debug=True)
