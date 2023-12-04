import os

from okta import UsersClient

OKTA_API_TOKEN = os.environ("OKTA_API_TOKEN")
OKTA_DOMAIN = os.environ("OKTA_DOMAIN")
USER_ID = ""
ROLE_NAME = ""

# Initialize Okta client
okta_client = UsersClient(f"https://{OKTA_DOMAIN}/", OKTA_API_TOKEN)


def add_role_to_user(user_id, role_name):
    try:
        user = okta_client.get_user(user_id)
        user.add_to_group(role_name)
        print(f"Role '{role_name}' added to user with ID: {user.id}")
    except Exception as e:
        print(f"Error: {e}")


add_role_to_user(USER_ID, ROLE_NAME)
