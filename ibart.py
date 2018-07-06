#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, jsonify
import hashlib
import hmac
import json
import logging as log
import os
import sys

# Local imports
import db
import github
import logger as ibl
import worker

app = Flask(__name__)


def verify_hmac_hash(data, signature):
    try:
        github_secret = bytearray(os.environ['GITHUB_SECRET'], 'utf-8')
    except KeyError:
        log.error("Environment variable GITHUB_SECRET probably not set")
        return False

    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)

    # Need to convert this to bytearray, since hmac.compare_digest expect
    # either a unicode string or a byte array
    hexdigest = bytearray("sha1=" + mac.hexdigest(), "utf-8")
    signature = bytearray(signature, "utf-8")
    return hmac.compare_digest(hexdigest, signature)


def dump_json_blob_to_file(request, filename="last_blob.json"):
    """ Debug function to dump the last json blob to file """
    with open(filename, 'w') as f:
        payload = request.get_json()
        json.dump(payload, f, indent=4)


@app.route('/')
def main_page(page=1):
    sql_data = db.get_html_row(page)
    return render_template('main.html', sd=sql_data, page=page)


@app.route('/<int:page>')
def main_paginate(page):
    sql_data = db.get_html_row(page)
    return render_template('main.html', sd=sql_data, page=page)


@app.route('/restart/<int:pr_id>/<pr_sha1>')
def restart_page(pr_id, pr_sha1):
    worker.user_add(pr_id, pr_sha1)
    # if request.is_secure:
    #    if request.referrer:
    #        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/stop/<int:pr_id>/<pr_sha1>')
def stop_page(pr_id, pr_sha1):
    worker.cancel(pr_id, pr_sha1)
    # if request.is_secure:
    #    if request.referrer:
    #        return redirect(request.referrer)
    return redirect(request.referrer)


# TODO: This will show PRs from all gits and not a unique git
@app.route('/pr/<int:pr_number>')
def show_pr(pr_number):
    sql_data = db.get_pr(pr_number)
    return render_template('pr.html', sd=sql_data, pr_number=pr_number)


# logs/jbech-linaro/
@app.route('/logs/<owner>/<project>')
def show_pr_full_name(owner, project):
    pr_full_name = "{}/{}".format(owner, project)
    sql_data = db.get_pr_full_name(pr_full_name)
    return render_template('pr_full_name.html', sd=sql_data, project=project)


# logs/jbech-linaro/optee_client/1/
@app.route('/logs/<owner>/<project>/<int:pr_number>')
def show_unique_pr(owner, project, pr_number):
    pr_full_name = "{}/{}".format(owner, project)
    sql_data = db.get_unique_pr(pr_full_name, pr_number)
    return render_template('unique_pr.html', sd=sql_data)


# logs/jbech-linaro/optee_os/2/149713049/2bcfbd494fd4ce795840697a4d10cdb26f39d6aa
@app.route('/logs/<owner>/<project>/<int:pr_number>/<int:pr_id>/<pr_sha1>')
def show_log(owner, project, pr_number, pr_id, pr_sha1):
    pr_full_name = "{}/{}".format(owner, project)
    logs = ibl.get_logs(pr_full_name, pr_number, pr_id, pr_sha1)
    sql_data = db.get_job_info(pr_id, pr_sha1)
    payload = db.get_payload_from_pr_id(pr_id, pr_sha1)
    commiter_branch = github.pr_branch(payload)
    return render_template('job.html', sd=sql_data, logs=logs,
                           commiter_branch=commiter_branch)


@app.route('/payload', methods=['POST'])
def payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    dump_json_blob_to_file(request)

    # Check the signature to ensure that the message comes from GitHub
    if verify_hmac_hash(data, signature) is not True:
        return jsonify({'msg': 'wrong signature'})

    if request.headers.get('X-GitHub-Event') == "pull_request":
        payload = request.get_json()

        # Only do real work when it working with an open pull request
        if (payload['action'] != "synchronize" and
                payload['action'] != "opened"):
            return 'OK'

        worker.add(payload)
    return 'OK'


@app.errorhandler(404)
def page_not_found(error):
        return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    worker.initialize()
    app.run(debug=True, host='0.0.0.0')
