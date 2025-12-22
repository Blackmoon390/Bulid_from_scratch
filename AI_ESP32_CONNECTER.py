import socket



with open("configurations.txt","r") as file:
    for line in file:
        if line.startswith("ip="):
            ip=line.split("=")[1]



ESP_IP = ip
ESP_PORT = 80

def initialize_model_esp32():
    import json
    # Load model JSON first
    with open("model.json") as f:
        model_json = json.load(f)



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