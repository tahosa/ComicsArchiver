import sys
import unittest
import json
import pprint
import shutil
import os

sys.path.append("../../src")
from download import Download
from database import Database

class DownloadTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        json_raw = open("example.json")
        cls._config = json.loads(json_raw.read())

        config_raw = open("config.json")
        cls._db = json.loads(config_raw.read())['database']
        cls._db['reset'] = True

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("example")
        os.remove("comics.db")

    def test_init(self):
        dl = Download(self._config, self._db)

        self.assertEquals(dl.config['nextRegex'], 'nav-next')
        self.assertIsInstance(dl._dbh, Database)

    def test_get_next(self):
        dl = Download(self._config, self._db)

        result = dl._get_next("http://example.com/", "<a href='http://example.com/next' class='nav-next'>Next Comic</a>")
        self.assertEquals(result, "http://example.com/next")

        result = dl._get_next("http://example.com/", "<a href='/next' class='nav-next'>Next Comic</a>")
        self.assertEquals(result, "http://example.com/next")

        result = dl._get_next("http://example.com/", "<a href='next' class='nav-next'>Next Comic</a>")
        self.assertEquals(result, "http://example.com/next")

if __name__ == '__main__':
    unittest.main()
