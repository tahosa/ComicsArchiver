import unittest
import json
import os
import sys
import sqlite3

sys.path.append("../../src")
from database import Database

class DatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        json_raw = open("config.json")
        cls._config = json.loads(json_raw.read())
        cls._config['database']['reset'] = True
        cls.db = Database(cls._config['database'])

    @classmethod
    def tearDownClass(cls):
        os.remove("comics.db")

    def testInit(self):
        self.assertIsInstance(self.db._dbh, sqlite3.Connection)

    def testGetComicConfig(self):
        if not self.db.comic_exists("test"):
            self.db.insert_comic("test", "test", "test", "test", "test", 0, 0, "test", "test")

        result = self.db.get_comic_config("test")
        self.assertEquals(result['name'], "test")
        result2 = self.db.get_comic_config("bad")
        self.assertIsNone(result2)

    def testComicInsert(self):
        self.db = Database(self._config['database'])
        self.assertFalse(self.db.comic_exists("bad"))
        self.db.insert_comic("test", "test", "test", "test", "test", 0, 0, "test", "test")
        self.assertTrue(self.db.comic_exists("test"))

    def testFileInsert(self):
        if not self.db.comic_exists("test"):
            self.db.insert_comic("test", "test", "test", "test", "test", 0, 0, "test", "test")

        self.db.insert_file("test", "test", "test", "test")

        result = self.db._dbh.execute("select * from files where comic='test'").fetchall()
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0][0], 'test')

    def testSetLast(self):
        if not self.db.comic_exists("test"):
            self.db.insert_comic("test", "test", "test", "test", "test", 0, 0, "test", "test")

        self.db.set_last("test", "lasturl")
        result = self.db._dbh.execute("select * from comics").fetchall()
        self.assertEquals(result[0][9], "lasturl")

if __name__ == '__main__':
    unittest.main()
