import os
from urllib.parse import urlencode

import requests


# this should be populated by the secrets manager
EMAILS_FOR_ACCOUNTS = os.getenv("EMAILS_FOR_ACCOUNTS")

# this should be populated by Saturn. This script will only work if
# run from an account that has admin access
BASE_URL = os.getenv("BASE_URL")
SATURN_TOKEN = os.getenv("SATURN_TOKEN")
saturn_headers = {"Authorization": f"token {SATURN_TOKEN}"}

def check_for_account_by_email(email: str) -> bool:
    url = f"{BASE_URL}/api/users"
    query_string = urlencode(dict(q=f"email:{email}", page=1, size=1))
    url = url + "?" + query_string
    response = requests.get(url, headers=saturn_headers)
    results = response.json()['users']
    if results:
        return True
    return False


def check_for_account_by_username(username: str) -> bool:
    url = f"{BASE_URL}/api/users"
    query_string = urlencode(dict(q=f"username:{username}", page=1, size=1))
    url = url + "?" + query_string
    response = requests.get(url, headers=saturn_headers)
    results = response.json()['users']

    if results:
        return True
    return False


def make_unique_username(email: str) -> str:
    candidate_username = email.split('@')[0]
    candidate_username = "".join(c for c in candidate_username if c.isalnum())

    # we'll try 100 integers until we get a unique name
    for c in range(100):
        to_try = candidate_username
        if c:
            to_try = candidate_username + str(c)
        if not check_for_account_by_username(to_try):
            return to_try
    raise ValueError(f'unable to find username for {candidate_username}')


def make_account(username: str, email: str):
    url = f"{BASE_URL}/api/users"
    body = dict(
        username=username,
        email=email,
        admin=False,
        locked=False,
        send_reset_email=False,
        prevent_duplicate_emails=True,
    )
    response = requests.post(url, json=body, headers=saturn_headers)
    print(response.json())


def ensure_account_exists(email: str) -> None:
    if check_for_account_by_email(email):
        return
    username = make_unique_username(email)
    make_account(username, email)


def run():
    for email in EMAILS_FOR_ACCOUNTS.split('\n'):
        if email:
            ensure_account_exists(email)


if __name__ == "__main__":
    run()
