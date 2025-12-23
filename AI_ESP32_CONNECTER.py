import socket
import json
import time
import Weather



with open("configurations.txt","r") as file:
    for line in file:
        if line.startswith("ip="):
            ip=line.split("=")[1].strip().strip('" ')

Weatherdata=Weather.get_weather_data()


datam=["soilmoisture",Weatherdata["weather"],"capacity",Weatherdata["humidity"],Weatherdata["temperature"],Weatherdata["rain_forecast"],Weatherdata["time_of_day"]]



ESP_IP = ip
ESP_PORT = 80

ESP_MOTOR_STATUS=1

def initialize_model_esp32():
    global ESP_MOTOR_STATUS
    # Load model JSON first
    with open("model.json") as f:
        model_json = json.load(f)
        response=send_json(model_json)
        data=json.loads(response)
        ESP_MOTOR_STATUS=data["motor_status"]




# resp = send_json(model_json)
# print("ESP32 Response:", resp)

def send_json(data):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(20)  # longer timeout for big JSON
    sock.connect((ESP_IP, ESP_PORT))
    sock.sendall(json.dumps(data).encode('utf-8'))

    # Read full response until connection closes
    response = b""
    try:
        while True:
            part = sock.recv(1024)
            if not part:
                break
            response += part
    except socket.timeout:
        pass
    sock.close()
    return response.decode('utf-8')

def monitor_system():
    while True:
        if ESP_MOTOR_STATUS == 1:
            # send_json(data)
            time.sleep(5*60)
        else:
            # send_json(data)
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

