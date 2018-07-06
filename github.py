import logging as log
import os
import requests


def pr_id(payload):
    """Returns the ID of the GitHub job."""
    return payload['pull_request']['id']


def pr_number(payload):
    """Returns the pull request number."""
    return payload['number']


def pr_sha1(payload):
    """Returns the commit hash (the SHA-1)."""
    return payload['pull_request']['head']['sha']


def pr_clone_url(payload):
    """Returns full URL to the committers own project."""
    return payload['pull_request']['head']['repo']['clone_url']


def pr_name(payload):
    """Returns the name (ex. optee_os) of the Git project."""
    return payload['repository']['name']


def pr_full_name(payload):
    """Returns the full name (ex. OP-TEE/optee_os) of the Git project."""
    return payload['repository']['full_name']


def pr_statuses_url(payload):
    """Returns URL for sending status updates."""
    return payload['pull_request']['statuses_url']


def pr_branch(payload):
    """Returns the name of the commiers branch."""
    return payload['pull_request']['head']['ref']


def update_state(payload, state, description):
    if payload is None or state is None or description is None:
        log.error("Missing one or several parameters")
        return

    request = {'context': 'IBART'}
    request['state'] = state
    # TODO: This is something that could/should be added so settings.py instead
    # of just having it as an environment variable.
    try:
        server_url = os.environ['IBART_URL']
    except KeyError:
        log.error("Environment variable IBART_URL probably not set, no update"
                  "sent")
        return False

    _pr_full_name = pr_full_name(payload)
    _pr_number = pr_number(payload)
    _pr_id = pr_id(payload)
    _pr_sha1 = pr_sha1(payload)

    # See websrv.py : show_log()
    request['target_url'] = "{su}/logs/{fn}/{n}/{i}/{s}".format(
            su=server_url, fn=_pr_full_name, n=_pr_number, i=_pr_id,
            s=_pr_sha1)

    request['description'] = description
    # log.debug("request: {}".format(request))

    # Read the personal token (from GitHub)
    try:
        token = "token {}".format(os.environ['GITHUB_TOKEN'])
    except KeyError:
        log.error("Environment variable GITHUB_TOKEN probably not set, no"
                  "update sent")
        return False

    # Set the token
    headers = {'content-type': 'application/json',
               'Authorization': token}

    # Note that this will print sensitive information
    # log.debug("headers: {}".format(headers))

    statuses_url = pr_statuses_url(payload)
    # log.debug("statuses_url: {}".format(statuses_url))

    res = requests.post(statuses_url, json=request, headers=headers)
    # log.debug("response # from server: # {}".format(res.text))
