import urllib
import urllib2
import re
import os
import sys
import logging
import pprint
from database import Database
from orderedset import OrderedSet

class Download:
    def __init__(self, config, database, static=False):
        self.config = config
        self._dbh = Database(database)

    def create_static(self):
        return True

    def crawl_comic(self):
        if not os.path.exists(self.config['folder']):
            logging.info("Creating folder '%s'", self.config['folder'])
            os.makedirs(self.config['folder'])
        elif not os.path.isdir(self.config['folder']):
            raise Exception("Comic folder {0} is not a directory".format(self.config['folder']))

        if not self._dbh.comic_exists(self.config['name']):
            self._dbh.insert_comic(
                self.config['name'],
                self.config['description'],
                self.config['folder'],
                self.config['nextRegex'],
                self.config['comicRegex'],
                self.config['notesRegex'],
                self.config['altText'],
                self.config['baseUrl'],
                self.config['startUrl']
            )

        current = self.config['startUrl']
        last = ""

        while True:
            logging.info("Searching '%s' for files", current)
            resp = urllib2.urlopen(current)
            page = resp.read()

            files = self._download(current, page)
            logging.debug("Downloaded %d images", len(files))

            nxt = self._get_next(current, page)
            logging.debug("Found next page '%s'", nxt)

            last = current
            current = nxt
            self._dbh.set_last(self.config['name'], last)

            if last == self.config['baseUrl'] or last == current or current == '' or current == None or re.search("#$", current):
                logging.debug("Ending crawl_comic: last: %s, current: %s, nxt: %s", last, current, nxt)
                break;


    def _get_next(self, url, page):
        linkSearch = re.search(
            r"<a[^>]+?href\s*=\s*[\'\"](.+?)[\'\"].*?" + self.config['nextRegex'] + r".*?<\/a>",
            page,
            re.IGNORECASE
        )

        logging.debug("_get_next searching for %s", linkSearch.re.pattern)
        #logging.debug("_get_next searching through:\n %s", linkSearch.string)
        logging.debug("_get_next matched whole string '%s'", linkSearch.group(0))

        if linkSearch != None:
            logging.debug("_get_next found: %s", pprint.pformat(linkSearch.groups()))
            link = linkSearch.group(1)

            absSearch = re.match(r"http:", link)
            rootSearch = re.match(r"\/", link)

            if absSearch:
                return link
            elif rootSearch:
                stripped = re.match(r"(http:\/\/[^\/]*?)\/", url)
                return stripped.group(1) + link
            else:
                stripped = re.match(r"(http:\/\/.*\/)[^\/]*", url)
                return stripped.group(1) + link

        else:
            return None

    def _download(self, url, page, static=False):
        comics = OrderedSet(re.findall(self.config['comicRegex'], page, re.MULTILINE))
        files = []

        for c in comics:
            if re.search(r"\.ico$", c):
                continue

            dlUrl = ""

            absSearch = re.match("http:", c)
            rootSearch = re.match(r"\/([^/]*?)", c)

            if absSearch:
                dlUrl = c
            elif rootSearch:
                stripped = re.match(r"(http:\/\/[^\/]+?)", url)
                dlUrl = stripped.group(1) + rootSearch.group(1)
            else:
                stripped = re.match(r"(http://.*\/)[^\/]*", url)
                dlUrl = stripped.group(1) + rootSearch.group(1)

            fileMatch = re.search(r".*\/([^\/?]+)", c)
            filename = os.path.join(self.config['folder'], fileMatch.group(1))

            logging.info("Downloading '%s' as '%s'", dlUrl, filename)
            urllib.urlretrieve(dlUrl, filename)

            # Last two params are for alt text and notes on the file
            if not static and not self._dbh.insert_file(self.config['name'], filename, None, None):
                raise Exception("Unable to continue due to a database error")

            files.append(filename)

        return files
