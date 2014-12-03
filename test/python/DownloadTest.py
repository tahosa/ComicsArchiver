import sys
import unittest
import json

sys.path.append("../../src")
from download import Download

class DownloadTest(unittest.TestCase):
    def test_init(self):
        config = json.loads('{"key":"value"}')
        db = json.loads('{"db":"name"}')

        dl = Download(config, db)

        self.assertEquals(dl.config['key'], 'value')
        self.assertEquals(dl.config['database']['db'], 'name')

if __name__ == '__main__':
    unittest.main()
