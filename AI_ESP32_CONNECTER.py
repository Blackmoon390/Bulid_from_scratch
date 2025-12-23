import socket
import json
import time
import Weather



with open("configurations.txt","r") as file:
    for line in file:
        if line.startswith("ip="):
            ip=line.split("=")[1].strip().strip('" ')


def update_sensor_input():
    with open("configurations.txt","r") as file:
        for line in file:
            if line.startswith("crop_stage="):
                crop_stage=line.split("=")[1].strip()
                crop_stage=int(crop_stage)
            if line.startswith("soil_type="):
                soil_type=line.split("=")[1].strip()
                soil_type=int(soil_type)
            if line.startswith("tank_capacity="):
                tank_capacity=line.split("=")[1].strip()
                tank_capacity=int(tank_capacity)
    return tank_capacity,crop_stage,soil_type


Weatherdata=Weather.get_weather_data()






ESP_IP = ip
ESP_PORT = 80

ESP_MOTOR_STATUS=1
Soil_Moisture=0


model_input_data=[Soil_Moisture,Weatherdata["weather"],update_sensor_input()[0],Weatherdata["humidity"],Weatherdata["temperature"],Weatherdata["rain_forecast"],Weatherdata["time_of_day"],update_sensor_input()[1],update_sensor_input()[2]]


def initialize_model_esp32():
    global ESP_MOTOR_STATUS,Soil_Moisture
    # Load model JSON first
    with open("model.json") as f:
        model_json = json.load(f)
        response=send_json(model_json)
        data=json.loads(response)
        ESP_MOTOR_STATUS=data["motor_status"]
        Soil_Moisture=data["soil_moisture"]


# resp = send_json(model_json)
# print("ESP32 Response:", resp)

def send_json(data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(20)

        sock.connect((ESP_IP, ESP_PORT))
        sock.sendall(json.dumps(data).encode("utf-8"))

        response = b""
        while True:
            part = sock.recv(1024)
            if not part:
                break
            response += part

        sock.close()
        return response.decode("utf-8")

    except socket.timeout:
        return "ERROR: Connection timeout"

    except ConnectionRefusedError:
        return "ERROR: ESP32 refused connection"

    except socket.gaierror:
        return "ERROR: Invalid IP address"

    except json.JSONDecodeError:
        return "ERROR: JSON encoding failed"

    except Exception as e:
        return f"ERROR: {str(e)}"



def monitor_system():
    while True:
        if ESP_MOTOR_STATUS == 1:
            send_json(model_input_data)
            time.sleep(5*60)
        else:
            send_json(model_input_data)
            time.sleep(30*60)


    





# data_json = {
#     "type": "data",
#     "input": [68,0,38,47,18,0,0,3,0]  # example sensor values
# }

# resp = send_json(data_json)
# print("ESP32 Response:", resp)

# data_json = {
#     "type": "data",
#     "input": [27,1,55,57,31,0,2,1,1]  # example sensor values
# }

# resp = send_json(data_json)
# print("ESP32 Response:", resp)


# data_json = {
#   "type": "manual",
#   "motor": 1
# }


# resp = send_json(data_json)
# print("ESP32 Response:", resp)



# data={"soil_moisture":20,"weather":0,"tank_capacity":100,"humidity":100,"tempture":26,"rain_forecast":32,"timeofday":2}

print(update_sensor_input())