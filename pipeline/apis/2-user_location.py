#!/usr/bin/env python3

import sys
import requests
import time

def get_user_location(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        
        if status_code == 200:
            data = response.json()
            location = data.get('location')
            if location:
                print(location)
            else:
                print("Location not specified")
        elif status_code == 404:
            print("Not found")
        elif status_code == 403:
            reset_timestamp = int(response.headers.get('X-RateLimit-Reset', 0))
            reset_time = (reset_timestamp - time.time()) / 60
            print(f"Reset in {int(reset_time)} min")
        else:
            print("An error occurred:", status_code)
    except requests.RequestException as e:
        print("Failed to retrieve data:", e)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./2-user_location.py <GitHub API user URL>")
    else:
        get_user_location(sys.argv[1])

