#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import serial
import subprocess
import time
import yaml
import sys
from argparse import ArgumentParser

import logging

################################################################################
# Relay logic
################################################################################
RELAY_BINARY = "{}/{}".format(os.path.dirname(os.path.realpath(__file__)),
                              './hidusb-relay-cmd')

class Relay():
    """ Represents an single relay """
    def __init__(self, name, relay_number):
        self.name = name
        self.relay_number = relay_number

    def info(self):
        return "type: %s, number: %d" % (self.name, self.relay_number)

    def turn_on(self):
        logging.debug("Turning on %s-relay (r: %d)" % (self.name, self.relay_number))
        # logging.debug("cmd: %s on %d" % (RELAY_BINARY, self.relay_number))
        subprocess.call([RELAY_BINARY, "on", str(self.relay_number)])

    def turn_off(self):
        logging.debug("Turning off %s-relay (r: %d)" % (self.name, self.relay_number))
        # logging.debug("cmd: %s off %d" % (RELAY_BINARY, self.relay_number))
        subprocess.call([RELAY_BINARY, "off", str(self.relay_number)])


class PowerRelay(Relay):
    def __init__(self):
        Relay.__init__(self, "power", 1)

    def __str__(self):
        return self.info()

    def enable(self):
        self.turn_on()

    def disable(self):
        self.turn_off()


class RecoveryRelay(Relay):
    def __init__(self):
        Relay.__init__(self, "recovery", 2)

    def __str__(self):
        return self.info()

    def enable(self):
        self.turn_on()

    def disable(self):
        self.turn_off()


class HiKeyAutoBoard():
    def __init__(self, root=None):
        self.pr = PowerRelay()
        self.rr = RecoveryRelay()
        self.root = root

    def __str__(self):
        return "%s\n%s" % (self.pr, self.rr)

    def power_off(self):
        # They relay is Normally Closed, so we need to turn on the relay to
        # power off the device.
        self.pr.turn_on()

    def power_on(self):
        # They relay is Normally Closed, so we need to turn off the relay to
        # power on the device.
        self.pr.turn_off()

    def power_cycle(self):
        self.power_off()
        time.sleep(0.8)
        self.power_on()

    def enable_recovery_mode(self):
        """ This will power cycle the device and go into recovery mode. """
        self.power_off()
        self.rr.enable()
        time.sleep(1.0)
        self.power_on()

    def disable_recovery_mode(self):
        """ This will turn off the device go back to normal mode. """
        self.power_off()
        self.rr.disable()

    def flash(self, yaml_file):
        self.enable_recovery_mode()
        time.sleep(5)

        # Open the yaml file containing all the flash commands etc.
        with open(yaml_file, 'r') as yml:
            yml_config = yaml.load(yml)
        yml_iter = yml_config['flash_cmds']

        child = pexpect.spawn("/bin/bash")
        f = open('flash.log', 'w')
        child.logfile = f

        logging.debug("Flashing the device")

        for i in yml_iter:
            if cfg.args.v:
                logging.debug("cmd: %s, exp: %s (timeout %d)" % (i['cmd'], i['exp'], i['timeout']))
            child.sendline(i['cmd'])
            child.expect(i['exp'], timeout=i['timeout'])

        logging.debug("Done flashing!")

        self.disable_recovery_mode()

    def run_test(self, yaml_file):
        # Open the yaml file containing all the flash commands etc.
        with open(yaml_file, 'r') as yml:
            yml_config = yaml.load(yml)
        yml_iter = yml_config['xtest_cmds']

        child = pexpect.spawn("/bin/bash")
        f = open('xtest.log', 'w')
        child.logfile = f

        child.sendline("picocom -b 115200 /dev/ttyUSB0")
        child.expect("Terminal ready", timeout=3)

        logging.debug("Start running tests")
        self.power_cycle()

        for i in yml_iter:
            if cfg.args.v:
                logging.debug("cmd: %s, exp: %s (timeout %d)" % (i['cmd'], i['exp'], i['timeout']))
            if i['cmd'] is not None:
                child.sendline(i['cmd'])
            child.expect(i['exp'], timeout=i['timeout'])

        logging.debug("xtest done!")
        self.power_off()


def power_on():
    relay = PowerRelay()
    relay.disable()
    return

def power_off():
    relay = PowerRelay()
    relay.enable()
    return

def normal_boot():
    power_off()

    # Make sure that it's not still in recovery mode.
    relay = RecoveryRelay()
    relay.disable()

    time.sleep(1)
    power_on()

def recovery_boot():
    power_off()
    time.sleep(1)

    # Enable recovery pin
    relay = RecoveryRelay()
    relay.enable()

    time.sleep(1)
    power_on()

################################################################################
# Argument parser
################################################################################
def get_parser():
    """ Takes care of script argument parsing. """
    parser = ArgumentParser(description='Script used to flash HiKey 6220 \
            automatically')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--boot', required=False, action="store_true", \
            default=False, \
            help='Reboot HiKey into boot mode (turns off/on)')

    group.add_argument('--recovery', required=False, action="store_true", \
            default=False, \
            help='Reboot HiKey into recovery mode (turns off/on)')

    group.add_argument('--on', required=False, action="store_true", \
            default=False, \
            help='Power on HiKey')

    group.add_argument('--off', required=False, action="store_true", \
            default=False, \
            help='Power off HiKey')

    parser.add_argument('-v', required=False, action="store_true", \
            default=False, \
            help='Output some verbose debugging info')

    return parser


def initialize_logging():
    LOG_FMT = ("[%(levelname)s] %(funcName)s():%(lineno)d   %(message)s")
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FMT)


def main(argv):
    initialize_logging()
    parser = get_parser()
    args = parser.parse_args()

    if args.boot:
        print("Booting up HiKey")
        normal_boot()
    elif args.recovery:
        print("Booting up in recovery mode")
        recovery_boot()
    elif args.on:
        print("Power on HiKey")
        power_on()
    elif args.off:
        print("Power off HiKey")
        power_off()

if __name__ == "__main__":
    main(sys.argv)
