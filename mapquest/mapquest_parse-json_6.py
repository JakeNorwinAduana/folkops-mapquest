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

        route = json_data["route"]

        print("\n==============================")
        print("       ROUTE INFORMATION")
        print("==============================")

        print("From:", orig)
        print("To:", dest)
        print("Travel Time:", route["formattedTime"])
        print("Distance:", format(route["distance"], ".2f"), "miles")
        #print("Fuel Used:", format(route["fuelUsed"], ".2f"), "gallons")

        kilometers = route["distance"] * 1.61
        #liters = route["fuelUsed"] * 3.78

        print("Distance:", format(kilometers, ".2f"), "km")
        #print("Fuel Used:", format(liters, ".2f"), "liters")

        print("\nTURN-BY-TURN DIRECTIONS")
        print("------------------------------")

        for maneuver in route["legs"][0]["maneuvers"]:
            narrative = maneuver["narrative"]
            distance = maneuver["distance"]
            distance_km = distance * 1.61

            print(narrative)
            print("Distance:", format(distance_km, ".2f"), "km")
            print("------------------------------")