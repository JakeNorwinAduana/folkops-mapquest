import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "EGVIJZBu6OlzjazQolRueK1VFVfoi30D"

while True:
    orig = input("Starting Location (q to quit): ")

    if orig.lower() == "q":
        break

    dest = input("Destination (q to quit): ")

    if dest.lower() == "q":
        break

    url = main_api + urllib.parse.urlencode({
        "key": key,
        "from": orig,
        "to": dest
    })

    json_data = requests.get(url).json()

    if json_data["info"]["statuscode"] == 0:

        print("\nRoute Information")
        print("------------------------------")

        print("Directions:", json_data["route"]["formattedTime"])
        print("Duration:", json_data["route"]["formattedTime"])
        print("Distance:", json_data["route"]["distance"], "miles")
        #print("Fuel Used:", json_data["route"]["fuelUsed"], "gallons")

        miles = json_data["route"]["distance"]
        kilometers = miles * 1.61

        #gallons = json_data["route"]["fuelUsed"]
        #liters = gallons * 3.78

        print("Distance:", format(kilometers, ".2f"), "km")
        #print("Fuel Used:", format(liters, ".2f"), "liters")

        print("------------------------------")