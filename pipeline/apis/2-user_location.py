#!/usr/bin/env python3

""" Return location of a GitHub user or provide rate limit information """

import requests
import sys
import time

def get_github_user_location(url):
    """
    Fetch and display the location of a specified GitHub user.

    Parameters:
        url (str): The full API URL of the GitHub user.

    Behavior:
        - If the request status code is 403, prints the time until rate limit reset.
        - If the request status code is 404, prints "Not found".
        - If the request is successful (200), prints the user's location.
        - If the location is not specified, indicates that.
    """
    try:
        res = requests.get(url)
        
        if res.status_code == 403:
            rate_limit = res.headers.get('X-Ratelimit-Reset')
            if rate_limit:
                rate_limit = int(rate_limit)
                current_time = int(time.time())
                diff = (rate_limit - current_time) // 60
                print("Reset in {} min".format(diff))
            else:
                print("Rate limit exceeded. Try again later.")
                
        elif res.status_code == 404:
            print("Not found")
        elif res.status_code == 200:
            user_info = res.json()
            location = user_info.get('location')
            if location:
                print(location)
            else:
                print("Location not specified")
        else:
            print("Unexpected error: {}".format(res.status_code))
    except requests.RequestException as e:
        print("Failed to retrieve data: {}".format(e))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./2-user_location.py <GitHub API user URL>")
    else:
        get_github_user_location(sys.argv[1])

