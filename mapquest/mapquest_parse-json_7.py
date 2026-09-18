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

    status_code = json_data["info"]["statuscode"]

    if status_code == 0:

        route = json_data["route"]

        print("\n==============================")
        print("       ROUTE INFORMATION")
        print("==============================")

        print("From:", orig)
        print("To:", dest)
        print("Travel Time:", route["formattedTime"])

        miles = route["distance"]
        kilometers = miles * 1.61

        #gallons = route["fuelUsed"]
        #liters = gallons * 3.78

        print("Distance:", format(miles, ".2f"), "miles")
        print("Distance:", format(kilometers, ".2f"), "km")
        #print("Fuel Used:", format(gallons, ".2f"), "gallons")
        #print("Fuel Used:", format(liters, ".2f"), "liters")

        print("\nTURN-BY-TURN DIRECTIONS")
        print("------------------------------")

        for maneuver in route["legs"][0]["maneuvers"]:
            narrative = maneuver["narrative"]
            distance_km = maneuver["distance"] * 1.61

            print(narrative)
            print("Distance:", format(distance_km, ".2f"), "km")
            print("------------------------------")

    elif status_code == 402:
        print("\nError 402: One or both locations are invalid.")

    elif status_code == 611:
        print("\nError 611: Missing entry.")

    else:
        print("\nError:", status_code)