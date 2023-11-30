import os

import requests

OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
OKTA_DOMAIN = os.environ("OKTA_DOMAIN")
USER_ID = ""
ROLE_NAME = ""

user_groups_endpoint = f"https://{OKTA_DOMAIN}/api/v1/users/{USER_ID}/groups"

headers = {
    "Authorization": f"SSWS {OKTA_API_TOKEN}",
    "Content-Type": "application/json",
}


def remove_role_from_user():
    try:
        # Get the current groups (roles) of the user
        response = requests.get(user_groups_endpoint, headers=headers)
        response.raise_for_status()

        user_groups = response.json()

        # Find the group (role) to remove
        group_to_remove = next(
            (group for group in user_groups if group["profile"]["name"] == ROLE_NAME),
            None,
        )

        if group_to_remove:
            # Remove the group (role) from the user
            group_id = group_to_remove["id"]
            remove_group_url = (
                f"https://{OKTA_DOMAIN}/api/v1/groups/{group_id}/users/{USER_ID}"
            )
            requests.delete(remove_group_url, headers=headers)
            print(f"Role '{ROLE_NAME}' removed from user with ID: {USER_ID}")
        else:
            print(f"Role '{ROLE_NAME}' not found for user with ID: {USER_ID}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


remove_role_from_user()
