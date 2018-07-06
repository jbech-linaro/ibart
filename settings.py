#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging as log
import yaml
import os


def get_settings_yml_file():
    yml_file = None
    config_file = "configs/settings.yaml"

    try:
        with open(config_file, 'r') as yml:
            yml_file = yaml.load(yml)
    except KeyError:
        log.error("Couldn't find {}", config_file)
        exit()

    return yml_file


def config_path():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['config']['path']
    except KeyError:
        log.error("No config path in settings file")
        return "Missing key!"


def repo_bin():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['repo']['bin']
    except KeyError:
        log.error("No repo bin in settings file")
        return "Missing key!"


def repo_reference():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['repo']['reference']
    except KeyError:
        log.error("No repo reference in settings file")
        return "Missing key!"


def aarch32_toolchain_path():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['toolchain']['aarch32_path']
    except KeyError:
        log.error("No aarch32 toolchain in settings file")
        return "Missing key!"


def aarch64_toolchain_path():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['toolchain']['aarch64_path']
    except KeyError:
        log.error("No aarch64 toolchain in settings file")
        return "Missing key!"


def aarch32_prefix():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['toolchain']['aarch32_prefix']
    except KeyError:
        log.error("No aarch32 prefix in settings file")
        return "Missing key!"


def aarch64_prefix():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['toolchain']['aarch64_prefix']
    except KeyError:
        log.error("No aarch64 prefix in settings file")
        return "Missing key!"


def workspace_path():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['workspace']['path']
    except KeyError:
        log.error("No workspace path in settings file")
        return "Missing key!"


def log_dir():
    try:
        if os.environ['IBART_LOG_DIR']:
            return os.environ['IBART_LOG_DIR']
    except KeyError:
        pass

    yml_file = get_settings_yml_file()
    try:
        return yml_file['log']['dir']
    except KeyError:
        log.error("No log dir in settings file")
        return "Missing key!"


def log_file():
    try:
        if os.environ['IBART_CORE_LOG']:
            return os.environ['IBART_CORE_LOG']
    except KeyError:
        pass

    yml_file = get_settings_yml_file()
    try:
        return yml_file['log']['file']
    except KeyError:
        log.error("No log file specified in settings file or env")
        return "Missing key!"


def db_file():
    try:
        if os.environ['IBART_DB_FILE']:
            return os.environ['IBART_DB_FILE']
    except KeyError:
        pass

    yml_file = get_settings_yml_file()
    try:
        return yml_file['db']['file']
    except KeyError:
        log.error("No db file specified in settings file or env")
        return "Missing key!"


def jobdefs_path():
    try:
        if os.environ['IBART_JOBDEFS']:
            return os.environ['IBART_JOBDEFS']
    except KeyError:
        pass

    yml_file = get_settings_yml_file()
    try:
        return yml_file['jobs']['path']
    except KeyError:
        log.error("No jobdefs folder specified in settings file or env")
        return "Missing key!"


def remote_jobs():
    yml_file = get_settings_yml_file()
    my_jobs = []
    try:
        yml_iter = yml_file['jobs']['remotedefs']
        for i in yml_iter:
            my_jobs.append("{}".format(i))
    except KeyError:
        log.error("No remote jobdefs in settings file")
        return "Missing key!"
    return my_jobs

###############################################################################
# Everything below this line is just for debugging this
###############################################################################


def foo():
    yml_file = get_settings_yml_file()
    try:
        return yml_file['foo']['aarch64_path']
    except KeyError:
        return "Missing key!"


def initialize():
    log.info("Configure settings")
    log.debug("config: {}".format(config_path()))
    log.debug("repo binary: {}".format(repo_bin()))
    log.debug("repo reference: {}".format(repo_reference()))
    log.debug("aarch32_toolchain_path: {}".format(aarch32_toolchain_path()))
    log.debug("aarch64_toolchain_path: {}".format(aarch64_toolchain_path()))
    log.debug("aarch32_prefix: {}".format(aarch32_prefix()))
    log.debug("aarch64_prefix: {}".format(aarch64_prefix()))
    log.debug("workspace_path: {}".format(workspace_path()))
    log.debug("log_dir: {}".format(log_dir()))
    log.debug("log_file: {}".format(log_file()))
    log.debug("db_file: {}".format(db_file()))
    log.debug("config_path: {}".format(config_path()))
    log.debug("remote_jobs: {}".format(remote_jobs()))


def initialize_logger():
    LOG_FMT = ("[%(levelname)s] %(funcName)s():%(lineno)d   %(message)s")
    log.basicConfig(
        # filename="core.log",
        level=log.DEBUG,
        format=LOG_FMT,
        filemode='w')


if __name__ == "__main__":
    initialize_logger()
    initialize()
    foo()
