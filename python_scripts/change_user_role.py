import os

import requests

OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
OKTA_DOMAIN = os.environ("OKTA_DOMAIN")
USER_ID = ""
NEW_ROLE_NAME = ""

user_groups_endpoint = f"https://{OKTA_DOMAIN}/api/v1/users/{USER_ID}/groups"

headers = {
    "Authorization": f"SSWS {OKTA_API_TOKEN}",
    "Content-Type": "application/json",
}


def change_user_role():
    try:
        # Get the current groups (roles) of the user
        response = requests.get(user_groups_endpoint, headers=headers)
        response.raise_for_status()

        user_groups = response.json()

        # Find the group (role) to add
        new_role = next(
            (
                group
                for group in user_groups
                if group["profile"]["name"] == NEW_ROLE_NAME
            ),
            None,
        )

        if new_role:
            # Update the user's roles with the new role
            new_role_id = new_role["id"]
            add_group_url = (
                f"https://{OKTA_DOMAIN}/api/v1/groups/{new_role_id}/users/{USER_ID}"
            )
            requests.put(add_group_url, headers=headers)
            print(f"User with ID: {USER_ID} assigned to the new role: {NEW_ROLE_NAME}")
        else:
            print(f"Role '{NEW_ROLE_NAME}' not found.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


change_user_role()
