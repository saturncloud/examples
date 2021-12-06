import requests
import os
import userautoshutoff


def get_user_list(base_url, admin_token):
    """As an admin, get a list of all users on the Saturn Cloud account"""
    headers = {"Authorization": f"token {admin_token}"}
    result = requests.get(f"{base_url}api/users", headers=headers)
    list_of_users = result.json()["users"]
    return list_of_users


def get_user_token(base_url, username, admin_token):
    """As an admin, create a login link for a user and extract their access token"""
    url = f"{base_url}auth/createloginlink/{username}"
    headers = {"Authorization": f"token {admin_token}"}
    result = requests.post(url, headers=headers).json()
    login_link = result["result"]["login_link"]
    s = requests.session()
    s.get(login_link)
    t = s.get(f"{base_url}api/user/token")
    return t.json()["token"]


def autoshutoff():
    """Get a list of users, get their tokens, then shutoff their idle Jupyter servers
    with it"""
    base_url = os.environ["SATURN_APP_URL"]
    admin_token = os.environ["ADMIN_ACCESS_TOKEN"]
    users = get_user_list(base_url, admin_token)
    for user in users:
        username = user["username"]
        user_token = get_user_token(base_url, username, admin_token)
        userautoshutoff.close_user_resources(base_url, username, user_token)


if __name__ == "__main__":
    autoshutoff()
