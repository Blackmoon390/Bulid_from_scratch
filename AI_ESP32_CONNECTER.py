import socket
import json
import time
import Weather


with open("configurations.txt") as file:
    for line in file:
        if line.startswith("ip="):
            ESP_IP = line.split("=")[1].strip().strip('"')

ESP_PORT = 80


def extract_json(http_response):
    if "\r\n\r\n" in http_response:
        return http_response.split("\r\n\r\n", 1)[1]
    return http_response

def send_json(data):
    body = json.dumps(data)

    request = (
        "POST / HTTP/1.1\r\n"
        f"Host: {ESP_IP}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + body
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(20)
    sock.connect((ESP_IP, ESP_PORT))
    sock.sendall(request.encode())

    response = b""
    while True:
        part = sock.recv(1024)
        if not part:
            break
        response += part

    sock.close()
    return response.decode()



ESP_MOTOR_STATUS = 0
motor_start_time = None


Soil_Moisture = 0

def initialize_model_esp32():
    global ESP_MOTOR_STATUS, Soil_Moisture, motor_start_time

    with open("model.json") as f:
        model_json = json.load(f)

    response = send_json(model_json)
    data = json.loads(extract_json(response))

    print("MODEL LOAD RESPONSE:", data)

    ESP_MOTOR_STATUS = data["motor_status"]
    if ESP_MOTOR_STATUS == 1:
        motor_start_time = time.time()


def update_sensor_input():
    with open("configurations.txt") as file:
        for line in file:
            if line.startswith("crop_stage="):
                crop_stage = int(line.split("=")[1])
            if line.startswith("soil_type="):
                soil_type = int(line.split("=")[1])
            if line.startswith("tank_capacity="):
                tank_capacity = int(line.split("=")[1])
    return tank_capacity, crop_stage, soil_type

Weatherdata = Weather.get_weather_data()

model_input_data = {
    "type": "data",
    "input": [
        97,                              # Soil Moisture (sensor later)
        Weatherdata["weather"],
        update_sensor_input()[0],
        Weatherdata["humidity"],
        Weatherdata["temperature"],
        Weatherdata["rain_forecast"],
        Weatherdata["time_of_day"],
        update_sensor_input()[1],
        update_sensor_input()[2]
    ]
}


def monitor_system():
    """
    Continuously checks motor status from the model and updates motor_start_time.
    Sends data at different intervals:
    - Motor OFF: every 30 minutes
    - Motor ON: every 5 minutes
    """
    global motor_start_time, ESP_MOTOR_STATUS

    while True:
        response = send_json(model_input_data)  # use your global model_input_data
        try:
            data = json.loads(extract_json(response))
        except json.JSONDecodeError:
            print("Invalid JSON:", response)
            time.sleep(60)  # retry sooner
            continue

        print("AUTO RESPONSE:", data)

        motor_status = data.get("motor_status", 0)

        # Motor turned ON
        if motor_status == 1 and ESP_MOTOR_STATUS == 0:
            motor_start_time = time.time()
            print("Motor started at:", motor_start_time)

        # Motor turned OFF
        if motor_status == 0 and ESP_MOTOR_STATUS == 1:
            print("Motor stopped. Last start time:", motor_start_time)
            motor_start_time = None

        ESP_MOTOR_STATUS = motor_status  # update global motor status

        # Sleep depending on motor status
        if ESP_MOTOR_STATUS == 0:
            time.sleep(30 * 60)  # 30 minutes if motor OFF
        else:
            time.sleep(5 * 60)   # 5 minutes if motor ON

