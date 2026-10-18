import requests

name = input("Enter your firts name: ")

url = "https://jiza-mae-gubac.onrender.com/hello"
params = {"name": name}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data["message"])
else:
    print("Request failed.")
    print("Status Code:", response.status_code)