import urllib.parse
import requests

from colorama import Fore, Style, init

init(autoreset=True)


MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
API_KEY = "EGVIJZBu6OlzjazQolRueK1VFVfoi30D"


def get_route(origin, destination):
    url = MAIN_API + urllib.parse.urlencode({
        "key": API_KEY,
        "from": origin,
        "to": destination
    })

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("\nError: The MapQuest request timed out.")
        return None

    except requests.exceptions.RequestException as error:
        print("\nError connecting to MapQuest.")
        print(error)
        return None

    except ValueError:
        print("\nError: MapQuest returned invalid JSON.")
        return None


def display_route(data, origin, destination):
    status_code = data["info"]["statuscode"]

    if status_code == 402:
        print("\nError 402: One or both locations are invalid.")
        return

    elif status_code == 611:
        print("\nError 611: Missing entry.")
        return

    elif status_code != 0:
        print(f"\nError: MapQuest returned status code {status_code}.")
        return

    route = data["route"]

    miles = route["distance"]
    kilometers = miles * 1.61

    print(Fore.GREEN + "\n========================================")
    print(Fore.GREEN + "        FOLKOPS ROUTE SUMMARY")
    print(Fore.GREEN + "========================================")
    print(f"From        : {origin}")
    print(f"To          : {destination}")
    print(f"Travel Time : {route['formattedTime']}")
    print(f"Distance    : {miles:.2f} miles")
    print(f"Distance    : {kilometers:.2f} km")
    calculate_fuel_cost(kilometers)
    print("========================================")

    print("\nTURN-BY-TURN DIRECTIONS")
    print("----------------------------------------")

    for number, maneuver in enumerate(
        route["legs"][0]["maneuvers"], start=1
    ):
        narrative = maneuver["narrative"]
        miles = maneuver["distance"]
        kilometers = miles * 1.61

        print(f"{number}. {narrative}")
        print(f"   Distance: {kilometers:.2f} km")
        print()


def main():
    print(Fore.CYAN + "========================================")
    print(Fore.CYAN + "       FOLKOPS MAPQUEST ROUTER")
    print(Fore.CYAN + "========================================")

    while True:
        origin = input("\nStarting Location (q to quit): ").strip()

        if origin.lower() == "q":
            print("Goodbye!")
            break

        if not origin:
            print(Fore.RED + "\nError: Starting location cannot be empty.")
            continue

        destination = input("Destination (q to quit): ").strip()

        if destination.lower() == "q":
            print("Goodbye!")
            break

        if not destination:
            print("Error: Destination cannot be empty.")
            continue

        data = get_route(origin, destination)

        if data is not None:
            display_route(data, origin, destination)

def calculate_fuel_cost(distance_km):
    print(Fore.YELLOW + "\nFUEL COST ESTIMATE")
    print(Fore.YELLOW + "----------------------------------------")

    while True:
        try:
            efficiency = float(
                input("Vehicle fuel efficiency (km/L): ")
            )

            if efficiency <= 0:
                print("Please enter a value greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            fuel_price = float(
                input("Fuel price (PHP/L): ")
            )

            if fuel_price <= 0:
                print("Please enter a value greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    fuel_needed = distance_km / efficiency
    estimated_cost = fuel_needed * fuel_price

    print(f"\nEstimated fuel needed : {fuel_needed:.2f} L")
    print(f"Estimated fuel cost   : PHP {estimated_cost:,.2f}")

    return estimated_cost
if __name__ == "__main__":
    main()