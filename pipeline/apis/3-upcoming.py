#!/usr/bin/env python3
"""Pipeline Api"""
import requests
from datetime import datetime

if __name__ == '__main__':
    """Pipeline Api"""
    url = "https://api.spacexdata.com/v4/launches/upcoming"
    try:
        response = requests.get(url)
        response.raise_for_status()
        launches = response.json()

        # Find the nearest upcoming launch
        recent = None
        for launch in launches:
            launch_time = int(launch["date_unix"])
            if recent is None or launch_time < recent["date_unix"]:
                recent = launch

        if recent:
            launch_name = recent["name"]
            date = recent["date_local"]
            rocket_id = recent["rocket"]
            launchpad_id = recent["launchpad"]

            # Get Rocket Name
            rocket_response = requests.get(f"https://api.spacexdata.com/v4/rockets/{rocket_id}")
            rocket_name = rocket_response.json().get("name", "Unknown Rocket")

            # Get Launchpad Information
            launchpad_response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}")
            launchpad_data = launchpad_response.json()
            launchpad_name = launchpad_data.get("name", "Unknown Launchpad")
            launchpad_location = launchpad_data.get("locality", "Unknown Location")

            # Format and Print Result
            print(f"{launch_name} ({date}) {rocket_name} - {launchpad_name} ({launchpad_location})")
        else:
            print("No upcoming launches found.")

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

