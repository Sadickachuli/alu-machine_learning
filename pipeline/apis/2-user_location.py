#!/usr/bin/env python3

""" Return location of a GitHub user"""

import requests
import sys
import time

def get_github_user_location(url):
    try:
        res = requests.get(url)
        
        if res.status_code == 403:
            rate_limit = res.headers.get('X-Ratelimit-Reset')
            if rate_limit:
                rate_limit = int(rate_limit)
                current_time = int(time.time())
                diff = (rate_limit - current_time) // 60
                print(f"Reset in {diff} min")
            else:
                print("Rate limit exceeded. Try again later.")
                
        elif res.status_code == 404:
            print("Not found")
        elif res.status_code == 200:
            user_info = res.json()
            location = user_info.get('location', 'Location not specified')
            print(location)
        else:
            print(f"Unexpected error: {res.status_code}")
    except requests.RequestException as e:
        print(f"Failed to retrieve data: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./2-user_location.py <GitHub API user URL>")
    else:
        get_github_user_location(sys.argv[1])
