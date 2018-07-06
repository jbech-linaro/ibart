# -*- coding: utf-8 -*-
import logging as log
import json
import os
import sqlite3

# Local imports
import github
import settings


DB_RUN_FILE = os.path.join(os.path.dirname(__file__), settings.db_file())


def db_connect(db_file=DB_RUN_FILE):
    con = sqlite3.connect(db_file)
    return con


def initialize():
    if not os.path.isfile(DB_RUN_FILE):
        con = db_connect()
        cur = con.cursor()
        sql = '''
                CREATE TABLE job (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pr_id text NOT NULL,
                    pr_number text NOT NULL,
                    full_name text NOT_NULL,
                    sha1 text NOT_NULL,
                    date text NOT NULL,
                    run_time text DEFAULT "N/A",
                    status text DEFAULT Pending,
                    payload text NOT NULL)
              '''
        cur.execute(sql)
        con.commit()
        con.close()


def add_build_record(payload):
    pr_id = github.pr_id(payload)
    pr_sha1 = github.pr_sha1(payload)

    log.debug("Adding record for {}/{}".format(pr_id, pr_sha1))
    if pr_id == 0 or pr_sha1 == 0:
        log.error("Trying to add s record with no pr_id or pr_sha1!")
        return

    con = db_connect()
    cur = con.cursor()
    sql = ("SELECT pr_id FROM job WHERE pr_id = '{}' AND "
           "sha1 = '{}'".format(pr_id, pr_sha1))
    cur.execute(sql)
    r = cur.fetchall()
    if len(r) >= 1:
        log.debug("Record for pr_id/sha1 {}/{} is already in the "
                  "database".format(pr_id, pr_sha1))
        con.commit()
        con.close()
        return

    pr_number = github.pr_number(payload)
    pr_full_name = github.pr_full_name(payload)
    sql = ("INSERT INTO job (pr_id, pr_number, full_name, sha1, date, payload)"
           " VALUES('{}','{}','{}', '{}', datetime('now'), '{}')".format(
            pr_id, pr_number, pr_full_name, pr_sha1, json.dumps(payload)))
    cur.execute(sql)
    con.commit()
    con.close()


def update_job(pr_id, pr_sha1, status, running_time):
    log.debug("Update status to {} for {}/{}".format(status, pr_id, pr_sha1))
    con = db_connect()
    cur = con.cursor()
    sql = ("UPDATE job SET status = '{}', run_time = '{}', "
           "date = datetime('now') WHERE pr_id = '{}' AND sha1 = '{}'".format(
            status, running_time, pr_id, pr_sha1))
    cur.execute(sql)
    con.commit()
    con.close()


def get_payload_from_pr_id(pr_id, pr_sha1):
    con = db_connect()
    cur = con.cursor()
    sql = ("SELECT payload FROM job WHERE pr_id = '{}' AND "
           "sha1 = '{}'".format(pr_id, pr_sha1))
    cur.execute(sql)
    r = cur.fetchall()
    if len(r) > 1:
        log.error("Found duplicated pr_id/pr_sha1 in the database")
        return -1
    con.commit()
    con.close()
    return json.loads("".join(r[0]))


def get_html_row(page):
    con = db_connect()
    cur = con.cursor()
    sql = ("SELECT id, pr_id, sha1, full_name, pr_number, date, run_time, "
           "status "
           "FROM job "
           "ORDER BY id DESC LIMIT {}".format(page * 15))
    cur.execute(sql)
    r = cur.fetchall()
    con.commit()
    con.close()
    return r


def get_pr(pr_number):
    con = db_connect()
    cur = con.cursor()
    sql = ("SELECT id, pr_id, sha1, full_name, pr_number, date, run_time, "
           "status "
           "FROM job "
           "WHERE pr_number = '{}' "
           "ORDER BY date DESC".format(pr_number))
    cur.execute(sql)
    r = cur.fetchall()
    con.commit()
    con.close()
    return r


def get_unique_pr(pr_full_name, pr_number):
    if pr_full_name is None or pr_number is None:
        log.error("Missing parameters!")
    con = db_connect()
    cur = con.cursor()
    sql = ("SELECT id, pr_id, sha1, full_name, pr_number, date, run_time, "
           "status "
           "FROM job "
           "WHERE full_name = '{}' AND pr_number = '{}' "
           "ORDER BY date DESC".format(pr_full_name, pr_number))
    cur.execute(sql)
    r = cur.fetchall()
    con.commit()
    con.close()
    return r


def get_pr_full_name(pr_full_name):
    if pr_full_name is None:
        log.error("Missing parameters!")
    con = db_connect()
    cur = con.cursor()
    sql = ("SELECT id, pr_id, sha1, full_name, pr_number, date, run_time, "
           "status "
           "FROM job "
           "WHERE full_name = '{}' "
           "ORDER BY date DESC".format(pr_full_name))
    cur.execute(sql)
    r = cur.fetchall()
    con.commit()
    con.close()
    return r


def get_job_info(pr_id, pr_sha1):
    con = db_connect()
    cur = con.cursor()
    sql = ("SELECT id, pr_id, sha1, full_name, pr_number, date, run_time, "
           "status "
           "FROM job "
           "WHERE pr_id = '{}' AND sha1 = '{}' ".format(
               pr_id, pr_sha1))
    cur.execute(sql)
    r = cur.fetchall()
    if len(r) > 1:
        log.error("Found duplicated pr_id/pr_sha1 in the database")
        return -1
    con.commit()
    con.close()
    return r[0]
