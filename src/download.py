import urllib
import urllib2
import re
import database

class Download:
    def __init__(self, config, database, static=False):
        self.config = config
        self._dbh = Database(database)

    def create_static(self):
        return True

    def crawl_comic(self):
        return True

    def _get_next(self, url, page):
        linkSearch = re.search(
            r"<a[^>]+href\s*=\s*[\'\"]([^\'\"]*)[\'\"].*?" + self.config['nextSearch'] + r".*?<\/a>",
            page,
            re.IGNORECASE | re.DOTALL
        )

        if linkSearch:
            link = linksearch.group(1)

            absSearch = re.match(r"http:", link)
            rootSearch = re.match(r"\/", link)

            if absSearch:
                return link
            elif rootSearch:
                stripped = re.match(r"(http:\/\/[^\/]*?)\/", url)
                return stripped.groups(1) + link
            else:
                stripped = re.match(r"(http:\/\/.*\/)[^\/]*", url)
                return stripped.groups(1) + link

        else:
            return None

    def _download(self, url, page, static=False):
        comics = set(re.findall(self.config['comicSearch'], page, re.MULTILINE))
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
                dlUrl = stripped.groups(1) + rootSearch.groups(1)
            else:
                stripped = re.match(r"(http://.*\/)[^\/]*", url)
                dlUrl = stripped.groups(1) + rootSearch.groups(1)

            fileMatch = re.search(r"\/?([^\/]+)$", c)
            filename = self.config['folder'] + "/" + fileMatch.groups(1)

            urllib.urlretrieve(dlUrl, filename)

            # Last two params are for alt text and notes on the file
            if not static and not self._dbh.insert_file(self.config['name'], filename, None, None):
                raise Exception("Unable to continue due to a database error.")

            files.append(filename)

        return files
