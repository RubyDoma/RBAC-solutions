import os
import subprocess

print(
    "trigger_terraform_if_change_in_permissions executed"
)  # visible in the periodic run

from flask import Flask, request

app = Flask(__name__)


@app.route("/okta-webhook", methods=["POST"])
def okta_webhook():
    data = request.get_json()

    # Check if the event is related to role permission changes
    if is_role_permission_change(data):
        # Execute Terraform commands
        terraform_dir = os.environ("TERRAFORM_PATH")
        os.chdir(terraform_dir)
        subprocess.run(["terraform", "init"])
        subprocess.run(["terraform", "apply", "-auto-approve"])

    return "OK", 200


def is_role_permission_change(data):  # example
    if "eventType" in data and data["eventType"] == "user.authentication.succeeded":
        user_id = data.get("actor", {}).get("id")
        client_id = data.get("client", {}).get("id")

        if user_id == "desired_user_id" and client_id == "desired_client_id":
            return True

    return False


if __name__ == "__main__":
    app.run(port=5000)
