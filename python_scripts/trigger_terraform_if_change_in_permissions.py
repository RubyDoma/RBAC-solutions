import os
import requests
import json
import subprocess

OKTA_BASE_URL = os.environ("OKTA_DOMAIN")
OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
ROLE_IDS_TO_MONITOR = ["roleId1", "roleId2"]
STORED_PERMISSIONS_FILE = "stored_permissions.json"

def fetch_role_permissions(role_id):
    url = f"{OKTA_BASE_URL}/api/v1/roles/{role_id}"
    headers = {
        "Authorization": f"SSWS {OKTA_API_TOKEN}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("permissions", [])
    else:
        print(f"Error fetching role permissions for {role_id}: {response.status_code}")
        return None

def load_stored_permissions():
    try:
        with open(STORED_PERMISSIONS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_permissions(permissions):
    with open(STORED_PERMISSIONS_FILE, "w") as file:
        json.dump(permissions, file, indent=2)

def trigger_terraform():
    terraform_project_path = os.environ("TERRAFORM_PROJECT")

    subprocess.run(["cd", terraform_project_path], check=True, shell=True)

    subprocess.run(["terraform", "init"], check=True, shell=True)
    subprocess.run(["terraform", "apply", "-auto-approve"], check=True, shell=True)

if __name__ == "__main__":
    stored_permissions = load_stored_permissions()

    for role_id in ROLE_IDS_TO_MONITOR:
        current_permissions = fetch_role_permissions(role_id)

        if current_permissions is not None and current_permissions != stored_permissions.get(role_id):
            print(f"Role permissions for {role_id} have changed. Triggering Terraform.")
            trigger_terraform()
            # Update stored permissions
            stored_permissions[role_id] = current_permissions
            save_permissions(stored_permissions)
        else:
            print(f"Role permissions for {role_id} are unchanged.")
