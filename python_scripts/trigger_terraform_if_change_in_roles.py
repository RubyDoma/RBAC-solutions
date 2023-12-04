import json
import os
import subprocess

import requests

print("trigger_terraform_if_change_in_roles executed")  # visible in the periodic run

OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
OKTA_DOMAIN = os.environ("OKTA_DOMAIN")
USER_ID = ""

TERRAFORM_EXECUTABLE = os.environ("TERRAFORM_PATH")
TERRAFORM_PROJECT = os.environ("TERRAFORM_PROJECT")

# File to store the previous state
STATE_FILE = "okta_state.json"

user_roles_endpoint = f"https://{OKTA_DOMAIN}/api/v1/users/{USER_ID}/roles"

headers = {
    "Authorization": f"SSWS {OKTA_API_TOKEN}",
    "Accept": "application/json",
}


def get_current_user_roles():
    try:
        response = requests.get(user_roles_endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        user_roles = response.json()
        return user_roles
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


current_roles = get_current_user_roles()

# Compare current roles with desired roles
desired_roles = [
    "ReadOnlyUser",
]


# Save the current state to a file
def save_current_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


if set(current_roles) != set(desired_roles):
    print("Role change detected. Triggering update.")

    # Trigger Terraform deployment
    terraform_cmd = [TERRAFORM_EXECUTABLE, "apply", "-auto-approve"]
    terraform_dir = TERRAFORM_PROJECT
    subprocess.run(terraform_cmd, cwd=terraform_dir)

    # Save the current state for future comparisons
    save_current_state(current_roles)

else:
    print("No role change detected.")
