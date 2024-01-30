#!/usr/bin/env python

# Converted to python3, stripped out the smtp and twillo for a simple ntfy.sh notification

import argparse
# import subprocess
import json
import logging
import sys
import os
# import glob
import requests
import apprise
# import hashlib

from datetime import datetime
from os import path
# from subprocess import check_output
# from distutils.spawn import find_executable
# from math import log

GOES_URL_FORMAT = 'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=3&locationId={0}&minimum=1'

def notify_sms(settings, dates):
    for avail_apt in dates:

        location_id = settings.get("enrollment_location_id")
        location_name = settings.get("enrollment_location_name")
        if not location_name:
            location_name = location_id

        apobj = apprise.Apprise()
        apobj.add(settings['apprise_url'])
        logging.info('Sending notification.')
        apobj.notify(
            body='New GOES appointment available at %s on %s' % (
            location_name, avail_apt)
        )


def main(settings):
    try:
        # obtain the json from the web url
        data = requests.get(GOES_URL_FORMAT.format(
            settings['enrollment_location_id'])).json()

        # parse the json
        if not data:
            logging.info('No tests available.')
            return

        current_apt = datetime.strptime(
            settings['current_interview_date_str'], '%B %d, %Y')
        dates = []
        for o in data:
            if o['active']:
                dt = o['startTimestamp']  # 2017-12-22T15:15
                dtp = datetime.strptime(dt, '%Y-%m-%dT%H:%M')
                if current_apt > dtp:
                    dates.append(dtp.strftime('%A, %B %d @ %I:%M%p'))

        if not dates:
            return

        # hash = hashlib.md5(
        #     ''.join(dates) + current_apt.strftime('%B %d, %Y @ %I:%M%p')).hexdigest()
        # fn = "goes-notify_{0}.txt".format(hash)
        # if settings.get('no_spamming') and os.path.exists(fn):
        #     return
        # else:
        #     for f in glob.glob("goes-notify_*.txt"):
        #         os.remove(f)
        #     f = open(fn, "w")
        #     f.close()

    except OSError:
        logging.critical(
            "Something went wrong when trying to obtain the openings")
        return

    location_id = settings.get("enrollment_location_id")
    location_name = settings.get("enrollment_location_name")
    if not location_name:
        location_name = location_id
    msg = 'Found new appointment(s) in location %s on %s (current is on %s)!' % (
        location_name, dates[0], current_apt.strftime('%B %d, %Y @ %I:%M%p'))
    notify_sms(settings, dates)


def _check_settings(config):
    required_settings = (
        'current_interview_date_str',
        'enrollment_location_id'
    )

    for setting in required_settings:
        if not config.get(setting):
            raise ValueError(
                'Missing setting %s in config.json file.' % setting)


if __name__ == '__main__':

    # Configure Basic Logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: %(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        stream=sys.stdout,
    )

    pwd = path.dirname(sys.argv[0])

    # Parse Arguments
    parser = argparse.ArgumentParser(
        description="Command line script to check for goes openings.")
    parser.add_argument('--config', dest='configfile', default='%s/config.json' %
                        pwd, help='Config file to use (default is config.json)')
    arguments = vars(parser.parse_args())
    logging.info("config file is:" + arguments['configfile'])
    # Load Settings
    try:
        with open(arguments['configfile']) as json_file:
            settings = json.load(json_file)

            # merge args into settings IF they're True
            for key, val in list(arguments.items()):
                if not arguments.get(key):
                    continue
                settings[key] = val

            settings['configfile'] = arguments['configfile']
            _check_settings(settings)
    except Exception as e:
        logging.error('Error loading settings from config.json file: %s' % e)
        sys.exit()

    # Configure File Logging
    if settings.get('logfile'):
        handler = logging.FileHandler('%s/%s' % (pwd, settings.get('logfile')))
        handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(asctime)s %(message)s'))
        handler.setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(handler)

    logging.debug('Running cron with arguments: %s' % arguments)

    main(settings)
