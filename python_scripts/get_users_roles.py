import os

import requests

OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
OKTA_DOMAIN = os.environ("OKTA_DOMAIN")
USER_ID = ""

user_roles_endpoint = f"https://{OKTA_DOMAIN}/api/v1/users/{USER_ID}/roles"

headers = {
    "Authorization": f"SSWS {OKTA_API_TOKEN}",
    "Accept": "application/json",
}


def get_user_roles():
    try:
        response = requests.get(user_roles_endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        user_roles = response.json()
        return user_roles
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


user_roles = get_user_roles()
print(f"User Roles: {user_roles}")
