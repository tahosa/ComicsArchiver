import sqlite3
import MySQLdb
import sys
import logging

class Database:
    def __init__(self, config):
        self._type = config['type']
        logging.info("Opening connection to database '%s' on %s (%s)", config['database'], config['server'], config['type'])

        if self._type == 'sqlite':
            self._dbh = sqlite3.connect(config['server'])
        elif self._type == 'mysql' or self._type == 'mariadb':
            self._dbh = MySQLdb.connect(
                host=config['server'],
                db=config['database'],
                user=config['user'],
                passwd=config['password']
            )
        else:
            raise Exception("Unknown database type {0}".format(config['type']))

        if config['reset']:
            self._create_tables(True)
        elif not self._tables_exist():
            self._create_tables()

    def _tables_exist(self):
        logging.debug("Checking if tables exist")
        c = self._dbh.cursor()

        try:
            c.execute('SELECT * FROM comics')
            return True

        except:
            logging.exception("Unknown error: %s", sys.exc_info()[0])
            return False

    def _create_tables(self, drop=False):
        logging.debug("Creating database tables")
        c = self._dbh.cursor()

        try:
            if drop == True:
                c.execute('DROP TABLE comics')
                c.execute('DROP TABLE files')

            c.execute('''CREATE TABLE IF NOT EXISTS comics
                        (
                            name TEXT PRIMARY KEY,
                            description TEXT,
                            folder TEXT,
                            next_regex TEXT,
                            comic_regex TEXT,
                            notes_regex TEXT,
                            alt_text INT DEFAULT 0,
                            base_url TEXT,
                            start_url TEXT,
                            last_url TEXT,
                            active INT DEFAULT 1
                        )'''
            )

            c.execute('''CREATE TABLE IF NOT EXISTS files
                        (
                            comic INT NOT NULL,
                            num INT NOT NULL,
                            filename TEXT NOT NULL,
                            alt_text TEXT,
                            annotation TEXT,
                            CONSTRAINT pk_files PRIMARY KEY(comic, num)
                            CONSTRAINT uq_comic UNIQUE(comic, filename)
                        )'''
            )
            self._dbh.commit()

        except (sqlite3.ProgrammingError, MySQLdb.ProgrammingError) as ex:
            self._dbh.rollback()
            logging.Exception("Database error: %s", ex)

    def comic_exists(self, name):
        logging.debug("Checking if comic %s exists in database", name)
        c = self._dbh.cursor()

        try:
            c.execute('SELECT name FROM comics WHERE name=?', (name,))
            row = c.fetchone()
            return row != None
        except (sqlite3.ProgrammingError, MySQLdb.ProgrammingError) as ex:
            logging.exception("Database error: %s", ex)

        return False

    def insert_comic(self, name, desc, folder, nxt, comic, notes, alt, base, start):
        logging.debug("Inserting new comic into database")
        c = self._dbh.cursor()

        try:
            c.execute("INSERT INTO comics VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, '', 1)",
                (name, desc, folder, nxt, comic, notes, alt, base, start)
            )
            self._dbh.commit()

        except (sqlite3.ProgrammingError, MySQLdb.ProgrammingError) as ex:
            self._dbh.rollback()
            logging.exception("Database error: %s", ex)

    def insert_file(self, comic, filename, alt, annotation):
        logging.debug("Adding file to database")
        c = self._dbh.cursor()

        try:
            c.execute('SELECT max(num) FROM files WHERE comic = ?', (comic,))
            row = c.fetchone()
            num = 1

            if row[0] != None:
                num = row[0] + 1

            c.execute('INSERT INTO files VALUES(?, ?, ?, ?, ?)',
                (comic, num, filename, alt, annotation)
            )
            self._dbh.commit()

        except (sqlite3.ProgrammingError, MySQLdb.ProgrammingError) as ex:
            self._dbh.rollback();
            logging.exception("Database error: %s", ex)
            return False
        except (sqlite3.IntegrityError) as ex:
            logging.warning("%s already exists for %s", filename, comic)

        return True

    def set_last(self, comic, url):
        logging.debug("Setting last page for %s to '%s'", comic, url)
        c = self._dbh.cursor()

        try:
            c.execute('UPDATE comics SET last_url = ? WHERE name = ?', (url, comic))
            self._dbh.commit()

        except (sqlite3.ProgrammingError, MySQLdb.ProgrammingError) as ex:
            self._dbh.rollback()
            logging.exception("Database error: %s", ex)
