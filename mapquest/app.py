from flask import Flask, render_template, request
import urllib.parse
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

MAPQUEST_API_KEY = os.getenv("MAPQUEST_API_KEY")

MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"


@app.route("/", methods=["GET", "POST"])
def index():

    route_data = None
    error = None

    origin = ""
    destination = ""
    fuel_efficiency = ""
    fuel_price = ""
    cargo_weight = ""
    trip_cost = ""

    if request.method == "POST":

        origin = request.form.get("origin", "").strip()
        destination = request.form.get("destination", "").strip()

        fuel_efficiency = request.form.get(
            "fuel_efficiency", ""
        ).strip()

        fuel_price = request.form.get(
            "fuel_price", ""
        ).strip()

        cargo_weight = request.form.get(
            "cargo_weight", ""
        ).strip()

        trip_cost = request.form.get(
            "trip_cost", ""
        ).strip()


        # -----------------------------
        # Validate required inputs
        # -----------------------------

        if not origin or not destination:

            error = (
                "Please enter both an origin "
                "and destination."
            )

        else:

            try:

                fuel_efficiency_value = float(
                    fuel_efficiency
                )

                fuel_price_value = float(
                    fuel_price
                )

                cargo_weight_value = float(
                    cargo_weight
                )

                trip_cost_value = float(
                    trip_cost
                )


                # -----------------------------
                # Validate numeric inputs
                # -----------------------------

                if (
                    fuel_efficiency_value <= 0
                    or fuel_price_value <= 0
                    or cargo_weight_value <= 0
                    or trip_cost_value <= 0
                ):

                    raise ValueError


                # -----------------------------
                # Build MapQuest request
                # -----------------------------

                params = {
                    "key": MAPQUEST_API_KEY,
                    "from": origin,
                    "to": destination
                }

                url = (
                    MAIN_API
                    + urllib.parse.urlencode(params)
                )


                response = requests.get(
                    url,
                    timeout=15
                )

                response.raise_for_status()

                data = response.json()


                # -----------------------------
                # Check MapQuest status
                # -----------------------------

                status_code = data.get(
                    "info", {}
                ).get(
                    "statuscode"
                )


                if status_code == 0:

                    route = data["route"]


                    # -----------------------------
                    # Distance calculations
                    # -----------------------------

                    distance_miles = route.get(
                        "distance",
                        0
                    )

                    distance_km = (
                        distance_miles * 1.61
                    )


                    # -----------------------------
                    # Fuel calculations
                    # -----------------------------

                    fuel_needed = (
                        distance_km
                        / fuel_efficiency_value
                    )

                    fuel_cost = (
                        fuel_needed
                        * fuel_price_value
                    )


                    # -----------------------------
                    # Shipment calculations
                    # -----------------------------

                    cost_per_ton = (
                        trip_cost_value
                        / cargo_weight_value
                    )

                    cost_per_kg = (
                        cost_per_ton
                        / 1000
                    )


                    fuel_cost_percentage = (
                        fuel_cost
                        / trip_cost_value
                    ) * 100


                    remaining_trip_cost = (
                        trip_cost_value
                        - fuel_cost
                    )


                    # -----------------------------
                    # Turn-by-turn directions
                    # -----------------------------

                    maneuvers = route.get(
                        "legs",
                        [{}]
                    )[0].get(
                        "maneuvers",
                        []
                    )


                    for maneuver in maneuvers:

                        maneuver["kilometers"] = (
                            maneuver.get(
                                "distance",
                                0
                            ) * 1.61
                        )


                    # -----------------------------
                    # Send results to webpage
                    # -----------------------------

                    route_data = {

                        "time": route.get(
                            "formattedTime",
                            "N/A"
                        ),

                        "miles": distance_miles,

                        "kilometers": distance_km,

                        "fuel_needed": fuel_needed,

                        "fuel_cost": fuel_cost,

                        "cargo_weight": (
                            cargo_weight_value
                        ),

                        "trip_cost": (
                            trip_cost_value
                        ),

                        "cost_per_ton": (
                            cost_per_ton
                        ),

                        "cost_per_kg": (
                            cost_per_kg
                        ),

                        "fuel_cost_percentage": (
                            fuel_cost_percentage
                        ),

                        "remaining_trip_cost": (
                            remaining_trip_cost
                        ),

                        "maneuvers": maneuvers
                    }


                elif status_code == 402:

                    error = (
                        "MapQuest could not process "
                        "one or both locations. "
                        "Please check your input."
                    )


                elif status_code == 611:

                    error = (
                        "A required location entry "
                        "is missing. Please enter "
                        "both locations."
                    )


                else:

                    error = (
                        f"MapQuest returned "
                        f"status code {status_code}."
                    )


            except ValueError:

                error = (
                    "Fuel efficiency, fuel price, "
                    "cargo weight, and trip cost "
                    "must be valid numbers greater "
                    "than zero."
                )


            except requests.exceptions.Timeout:

                error = (
                    "The MapQuest request timed out. "
                    "Please try again."
                )


            except requests.exceptions.RequestException:

                error = (
                    "Unable to connect to the "
                    "MapQuest service. Please check "
                    "your internet connection."
                )


    return render_template(
        "index.html",

        route=route_data,

        error=error,

        origin=origin,

        destination=destination,

        fuel_efficiency=fuel_efficiency,

        fuel_price=fuel_price,

        cargo_weight=cargo_weight,

        trip_cost=trip_cost
    )


if __name__ == "__main__":
    app.run(debug=True)