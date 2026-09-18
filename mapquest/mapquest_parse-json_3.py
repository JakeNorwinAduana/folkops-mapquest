import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "EGVIJZBu6OlzjazQolRueK1VFVfoi30D"

while True:
    orig = input("Starting Location: ")
    dest = input("Destination: ")

    url = main_api + urllib.parse.urlencode({
        "key": key,
        "from": orig,
        "to": dest
    })

    json_data = requests.get(url).json()

    if json_data["info"]["statuscode"] == 0:
        print("Successful Route Call")
        print(json_data)