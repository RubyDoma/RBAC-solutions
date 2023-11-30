import json
import os

import requests

OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
OKTA_DOMAIN = os.environ("OKTA_DOMAIN")
ROLE_ID = ""

role_endpoint = f"https://{OKTA_DOMAIN}/api/v1/roles/{ROLE_ID}"

headers = {
    "Authorization": f"SSWS {OKTA_API_TOKEN}",
    "Content-Type": "application/json",
}


def modify_role_permissions():
    try:
        # Get current role details
        response = requests.get(role_endpoint, headers=headers)
        response.raise_for_status()

        role_details = response.json()

        # Modify role permissions (example)
        role_details["appLinks"] = [
            {"appName": "app_name", "appInstanceUrl": "https://example.com"}
        ]

        # Update role details
        update_role_url = f"https://{OKTA_DOMAIN}/api/v1/roles/{ROLE_ID}"
        requests.put(update_role_url, headers=headers, data=json.dumps(role_details))
        print(f"Role permissions modified for role with ID: {ROLE_ID}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Modify role permissions
modify_role_permissions()
