#!/usr/bin/python

import sys
import os
import json
import urllib2
import pprint
from optparse import OptionParser

sys.path.append("src")
import download

parser = OptionParser()
parser.add_option("-c", "--config-file", dest="configFile", help="Read config data from FILE", metavar="FILE")
parser.add_option("-s", "--static", action="store_true", dest="static", help="Create a static HTML site")

parser.set_defaults(configFile="config.json")

(opts, args) = parser.parse_args()

try:
    with open(opts.configFile, "r") as fh:
        config = json.loads(fh.read())

except IOError as e:
    print "Could note read from config file {0}: {1}\n".format(opts.configFile, e.strerror)
    sys.exit(1)
except ValueError as e:
    print "Could not parse JSON in {0}: {1}\n".format(opts.configFile, e.strerror)
    sys.exit(1)

try:
    for file in os.listdir(config.directories.config):
        if not os.path.isfile(file):
            continue

        try:
            with open(file) as fh:
                comicConfig = json.loads(fh.read())
                dl = Download(comicConfig, config.database)
                if opts.static:
                    dl.create_static(config.directories.html)
                else:
                    dl.create_dynamic(config.directories.html)
                    
        except IOError as e:
            print "Could note read from config file {0}: {1}. Skipping.\n".format(file, e.strerror)
            continue
        except ValueError as e:
            print "Could not parse JSON in {0}: {1}. Skipping.\n".format(file, e.strerror)
            continue

except NameError:
    print "Config file directory was not defined in {0}\n".format(opts.configFile)
    sys.exit(1)
