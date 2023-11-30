import os

import requests

OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
OKTA_DOMAIN = os.environ("OKTA_DOMAIN")

events_api_url = f"https://{OKTA_DOMAIN}/api/v1/logs"

headers = {
    "Authorization": f"SSWS {OKTA_API_TOKEN}",
    "Accept": "application/json",
}

response = requests.get(events_api_url, headers=headers)

if response.status_code == 200:
    logs = response.json()
    # Process logs as needed
else:
    print(f"Error fetching logs. Status code: {response.status_code}")
