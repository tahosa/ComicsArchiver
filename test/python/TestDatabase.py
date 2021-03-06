import unittest
import json
import os
import sys
import sqlite3

sys.path.append("../../src")
from database import Database

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        json_raw = open(os.path.dirname(os.path.realpath(__file__)) + "/config.json")
        cls._config = json.loads(json_raw.read())
        cls._config['database']['reset'] = True
        cls.db = Database(cls._config['database'])

    @classmethod
    def tearDownClass(cls):
        os.remove("test.db")

    def testInit(self):
        self.assertIsInstance(self.db, Database)
        self.assertIsInstance(self.db._dbh, sqlite3.Connection)
        self.assertTrue(self.db._tables_exist())

        cfg2 = self._config['database']
        cfg2['server'] = "test2.db"
        cfg2['reset'] = False

        with Database(cfg2) as db2:
            self.assertIsInstance(db2, Database)
            self.assertTrue(db2._tables_exist())

        cfg2['type'] = 'badtype'
        self.assertRaises(Exception, Database, cfg2)

        os.remove('test2.db')

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
