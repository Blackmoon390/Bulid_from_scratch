from flask import Flask, render_template, jsonify
import time
import random

app = Flask(__name__)

pump = {
    "running": False,
    "start_time": 0,
    "temperature": 30,
    "climate": "Normal",
    "motor": "OFF",
    "soil": 40,
    "air": 55,
    "humidity": 60
}

def update_sensors():
    pump["temperature"] = random.randint(25, 40)
    pump["soil"] = random.randint(20, 80)
    pump["air"] = random.randint(30, 70)
    pump["humidity"] = random.randint(40, 90)
    pump["climate"] = "Hot" if pump["temperature"] > 35 else "Normal"

def running_time():
    if pump["running"]:
        return int(time.time() - pump["start_time"])
    return 0


