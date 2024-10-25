#!/usr/bin/env python3
"""
This module retrieves information about the upcoming SpaceX launch.
"""
import requests
from datetime import datetime, timezone


def get_launch_details(launch_data):
    """
    Retrieves and formats the launch details.
    """
    launch_name = launch_data['name']
    launch_date_local = launch_data['date_local']
    rocket_id = launch_data['rocket']

    rocket_url = 'https://api.spacexdata.com/v4/rockets/{}'.format(rocket_id)
    rocket_response = requests.get(rocket_url)
    rocket_name = rocket_response.json().get('name', 'Unknown rocket')

    launchpad_id = launch_data['launchpad']
    launchpad_url = 'https://api.spacexdata.com/v4/launchpads/{}'.format(
        launchpad_id
    )
    launchpad_response = requests.get(launchpad_url)
    launchpad_data = launchpad_response.json()
    launchpad_name = launchpad_data.get('name', 'Unknown launchpad')
    launch_local = launchpad_data.get('locality', 'Unknown locality')

    return '{} ({}) {} - {} ({})'.format(
        launch_name,
        launch_date_local,
        rocket_name,
        launchpad_name,
        launch_local
    )


def get_upcoming_launch():
    """
    Retrieves information about the upcoming SpaceX launch.
    """
    try:
        url = 'https://api.spacexdata.com/v4/launches/upcoming'
        response = requests.get(url)
        if response.status_code == 200:
            launches = response.json()
            upcoming_launch = sorted(launches, key=lambda x: x['date_unix'])[0]
            print(get_launch_details(upcoming_launch))
        else:
            print('Error: {}'.format(response.status_code))
    except requests.exceptions.RequestException as e:
        print('Request failed: {}'.format(e))


if __name__ == '__main__':
    get_upcoming_launch()
