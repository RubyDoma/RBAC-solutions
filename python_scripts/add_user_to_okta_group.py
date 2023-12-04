import os

import requests

from python_scripts.create_okta_user import create_user

OKTA_BASE_URL = os.environ("OKTA_DOMAIN")
API_TOKEN = os.environ("OKTA_API_TOKEN")


# Add a user to an Okta group
def add_user_to_group(user_id, group_id):
    url = f"{OKTA_BASE_URL}/api/v1/groups/{group_id}/users/{user_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SSWS {API_TOKEN}",
    }
    response = requests.put(url, headers=headers)
    return response.status_code == 204  # success


if __name__ == "__main__":
    # Create a new user
    new_user = create_user("username", "email", "password", "firstname", "lastname")
    user_id = new_user["id"]
    group_id = ""

    # Add the user to a group
    if add_user_to_group(user_id, group_id):
        print("Successfully added user to the group")
    else:
        print("Failed to add user to the group")
