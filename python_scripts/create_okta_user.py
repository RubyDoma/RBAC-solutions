import json
import os

import requests

OKTA_BASE_URL = os.environ("OKTA_DOMAIN")
API_TOKEN = os.environ("OKTA_API_TOKEN")


def create_user(username, email, password, firstName, lastName):
    url = f"{OKTA_BASE_URL}/api/v1/users"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SSWS {API_TOKEN}",
    }
    data = {
        "profile": {
            "login": username,
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
        },
        "credentials": {"password": {"value": password}},
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
