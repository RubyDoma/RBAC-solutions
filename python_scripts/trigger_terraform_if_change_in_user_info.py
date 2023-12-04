import json
import os
import subprocess

from okta import UsersClient
from okta.models.user import User

from python_scripts.get_user_info import get_all_users

print(
    "trigger_terraform_if_change_in_user_info executed."
)  # visible in the periodic run

OKTA_BASE_URL = os.environ("OKTA_DOMAIN")
API_TOKEN = os.environ("OKTA_API_TOKEN")

TERRAFORM_EXECUTABLE = os.environ("TERRAFORM_PATH")

# File to store the previous state
STATE_FILE = "okta_state.json"

# Initialize Okta client
okta_client = UsersClient(f"{OKTA_BASE_URL}/", API_TOKEN)

get_all_users()


# Load the previous state from a file
def load_previous_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


# Save the current state to a file
def save_current_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    # Get the current users from Okta
    current_users = get_all_users()
    print("Current Users:")
    for user in current_users:
        if isinstance(user, User):
            print(f"- {user.profile.login}")

    # Load the previous state from the file
    previous_users = load_previous_state()

    # Compare current and previous states
    if current_users != previous_users:
        print("Changes detected in Okta users. Triggering Terraform deployment...")

        # Trigger Terraform deployment
        terraform_cmd = [TERRAFORM_EXECUTABLE, "apply", "-auto-approve"]
        subprocess.run(terraform_cmd, cwd=TERRAFORM_EXECUTABLE)

        # Save the current state for future comparisons
        save_current_state(current_users)
    else:
        print("No changes in Okta users.")
