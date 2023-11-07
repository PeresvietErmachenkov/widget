import customtkinter as ctk
import requests
import json
import geocoder

main_api = "d33e5646fac935017206d42d2c1c275b"
backup_api = "0348c6f6495900e17f3037be6867e600"

def get_api_data():
    global backup_api, main_api
    
    city = geocoder.ip('me')
    city = str(city)
    city = city.split()
    if city[0] != '<[ERROR':
        city = city[4][:-1]
        city = city[1:]
        print(city)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={main_api}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # print(json.dumps(data, indent = 4))
            # print(data["main"]["temp"])
            return data
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={backup_api}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # print(json.dumps(data, indent = 4))
                return data
            else:
                print("eror")
                return "error city name"
    else:
        return "error internet connection"
get_api_data()
