import geocoder

g = geocoder.ip('me')

print("City       :", g.city)
print("Latitude   :", g.lat)
print("Longitude  :", g.lng)

datas=[]

with open("configurations.txt","r") as file:
    for line in file:
        if line.strip().startswith("City="):
            line=f'City="{g.city}"\n'
        datas.append(line)

with open("configurations.txt","w") as file:
    file.writelines(datas)

