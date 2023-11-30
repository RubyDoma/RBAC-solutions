import os

from okta import GroupsClient, UsersClient
from okta.models.group import Group
from okta.models.user import User

OKTA_BASE_URL = os.environ("OKTA_DOMAIN")
API_TOKEN = os.environ("OKTA_API_TOKEN")

# Initialize Okta clients
users_client = UsersClient(f"{OKTA_BASE_URL}/", API_TOKEN)
groups_client = GroupsClient(f"{OKTA_BASE_URL}/", API_TOKEN)


def get_all_users():
    users = users_client.get_list()
    return users


def get_all_groups():
    groups = groups_client.get_list()
    return groups


if __name__ == "__main__":
    users = get_all_users()
    print("Users:")
    for user in users:
        if isinstance(user, User):
            print(f"- {user.profile.login}")

    groups = get_all_groups()
    print("\nGroups:")
    for group in groups:
        if isinstance(group, Group):
            print(f"- {group.profile.name}")
