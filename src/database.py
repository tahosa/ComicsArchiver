import sys
import logging
import pprint

db = None

class Database:
    def __init__(self, config):
        global db
        self._type = config['type']
        logging.info("Opening connection to database '%s' on %s (%s)", config['database'], config['server'], config['type'])

        if self._type == 'sqlite':
            db = __import__("sqlite3")
            self._dbh = db.connect(config['server'])
            pprint.pprint(db)
        elif self._type == 'mysql' or self._type == 'mariadb':
            db = __import__("MySQLdb")
            self._dbh = db.connect(
                host=config['server'],
                db=config['database'],
                user=config['user'],
                passwd=config['password']
            )
        else:
            raise Exception("Unknown database type {0}".format(config['type']))

        pprint.pprint(db)

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
        pprint.pprint(db)
        logging.debug("Creating database tables")
        c = self._dbh.cursor()

        if drop == True:
            try:
                c.execute('DROP TABLE comics')
                c.execute('DROP TABLE files')
            except db.OperationalError as ex:
                logging.warning("Not dropping tables since they already don't exists")
            except db.ProgrammingError as ex:
                self._dbh.rollback()
                logging.exception("Database error: %s", ex)

        try:
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

        except db.ProgrammingError as ex:
            self._dbh.rollback()
            logging.exception("Database error: %s", ex)



    def get_comic_config(self, name):
        logging.debug("Fetching config data for %s", name)
        c = self._dbh.cursor()

        try:
            c.execute("SELECT * FROM comics WHERE name=?", (name,))
            row = c.fetchone()
            if row == None:
                return None
            else:
                config = {
                    "name": row[0],
                    "description": row[1],
                    "folder": row[2],
                    "nextRegex": row[3],
                    "comicRegex": row[4],
                    "notesRegex": row[5],
                    "altText": True if row[6] > 0 else False,
                    "baseUrl": row[7],
                    "startUrl": row[8],
                    "lastUrl": row[9],
                    "active": True if row[10] > 0 else False
                }
                return config

        except db.ProgrammingError as ex:
            self._dbh.rollback()
            logging.exception("Database error: %s", ex)

        return None

    def comic_exists(self, name):
        logging.debug("Checking if comic %s exists in database", name)
        c = self._dbh.cursor()

        try:
            c.execute('SELECT name FROM comics WHERE name=?', (name,))
            row = c.fetchone()
            return row != None
        except db.ProgrammingError as ex:
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

        except db.ProgrammingError as ex:
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

        except db.ProgrammingError as ex:
            self._dbh.rollback();
            logging.exception("Database error: %s", ex)
            return False
        except db.IntegrityError as ex:
            logging.warning("%s already exists for %s", filename, comic)

        return True

    def set_last(self, comic, url):
        logging.debug("Setting last page for %s to '%s'", comic, url)
        c = self._dbh.cursor()

        try:
            c.execute('UPDATE comics SET last_url = ? WHERE name = ?', (url, comic))
            self._dbh.commit()

        except db.ProgrammingError as ex:
            self._dbh.rollback()
            logging.exception("Database error: %s", ex)
