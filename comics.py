#!/usr/bin/python

import sys
import os
import json
import pprint
import logging
from optparse import OptionParser

sys.path.append("src")
from download import Download

parser = OptionParser()
parser.add_option("-c", "--config-file", dest="configFile", help="Read config data from FILE", metavar="FILE")
parser.add_option("-s", "--static", action="store_true", dest="static", help="Create a static HTML site")
parser.add_option("-r", "--reset", action="store_true", dest="resetDatabase", help="Reset the database")
parser.add_option("-d", "--debug", action="store", type="int", default=100, dest="debug", help="Enable debug messages")

parser.set_defaults(configFile="config.json")

(opts, args) = parser.parse_args()
logging.basicConfig(level=opts.debug)

try:
    with open(opts.configFile, "r") as fh:
        config = json.loads(fh.read())

except IOError, e:
    logging.exception("Could not read from config file %s: %s", opts.configFile, e.strerror)
    sys.exit(1)
except ValueError, e:
    logging.exception("Could not parse JSON in %s: %s", opts.configFile, e.strerror)
    sys.exit(1)

logging.info("Successfully read config file %s", opts.configFile)

config['database']['reset'] = opts.resetDatabase

for file in os.listdir(config['directories']['config']):
    file = os.path.join(config['directories']['config'], file)
    logging.debug("Trying to parse %s", file)

    if not os.path.isfile(file):
        logging.warning("%s is not a file", file)
        continue

    try:
        with open(file) as fh:
            comicConfig = json.loads(fh.read())

            logging.info("Successfully read config for %s", comicConfig['name'])

            comicConfig['folder'] = os.path.join(config['directories']['comics'], comicConfig['folder'])
            if not os.path.exists(comicConfig['folder']):
                logging.info("Creating folder %s", comicConfig['folder'])
                os.makedirs(comicConfig['folder'])

            if opts.static:
                logging.debug("Doing a static download")
                dl = Download(comicConfig, config['database'], True)
                dl.create_static(config['directories']['html'])
            else:
                logging.debug("Adding files to database")
                dl = Download(comicConfig, config['database'])
                dl.crawl_comic()

    except IOError as e:
        logging.exception("Could not read from config file %s: %s. Skipping.", file, e.strerror)
        continue
    except ValueError as e:
        logging.exception("Could not parse JSON in %s: %s. Skipping.", file, e.strerror)
        continue
