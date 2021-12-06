import json
import requests
from datetime import datetime, timezone, timedelta
from dateutil import parser
import logging

def get_jupyter_kernels(resource_url, user_token):
    """extracting information for each kernel on a Jupyter server"""
    sessions_url = f"{resource_url}api/sessions"
    headers = {"Authorization": f"token {user_token}"}
    response = requests.get(sessions_url, headers=headers)
    result = response.json()
    return result


def check_jupyter_needs_shutoff(kernels, idle_time_delta):
    """Given a Jupyter session check if any of the kernel's activity is more recent than idle limit.
    Return True if the server needs to be shut off. In the event there are no kernels, do not shut
    off the server, instead leave it to Saturn Cloud's built in logic to handle.
    """
    # getting time window to keep the server on
    min_time = datetime.now(timezone.utc) - idle_time_delta

    if len(kernels) == 0:
        return False  # There are no kernels at all so do not act

    for k in kernels:
        if parser.parse(k["kernel"]["last_activity"]) >= min_time or k["kernel"]["execution_state"] != "idle":
            return False

    return True


def shutoff_resource(resource_id, base_url, user_token):
    """Turn off a Saturn Cloud resource for a user"""
    headers = {"Authorization": f"token {user_token}"}
    requests.post(
        f"{base_url}api/workspaces/{resource_id}/stop",
        headers=headers,
    )


time_delta_mapping = {
    "1 hour": timedelta(hours=1), # hack for testing
    "6 hours": timedelta(hours=6),
    "24 hours": timedelta(hours=24),
    "3 days": timedelta(hours=24 * 3),
    "7 days": timedelta(hours=24 * 7),
}


def close_user_resources(base_url, username, user_token):
    """Given a user access token, close their idle resources
    idle_limit is the limit in hours before shutting down the resource.
    """

    # get all of their workspace resources
    workspaces = requests.get(
        f"{base_url}api/workspaces",
        headers={"Authorization": f"token {user_token}"},
        ).json()["workspaces"]

    # filter to only Jupyter servers (to exclude RStudio servers)
    jupyter_servers = list(filter(lambda w: w["resource_type"] == "Jupyter Workspace", workspaces))

    # for each resource check last activity of the Jupyter kernels
    for resource in jupyter_servers:
        if resource["url"] is not None:  # this means there is an actively running JupyterLab server we can query
            time_delta = time_delta_mapping.get(resource["auto_shutoff"], None)
            if time_delta is None:
                continue
            kernels = get_jupyter_kernels(resource["url"], user_token)
            needs_shutoff = check_jupyter_needs_shutoff(kernels, time_delta)
            if needs_shutoff:
                logging.warning(f"Shutting down resource: {username}/{resource['name']}")
                shutoff_resource(resource, base_url, user_token)
