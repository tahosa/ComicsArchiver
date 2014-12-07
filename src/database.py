import sqlite3
import MySQLdb

class Database:
    def __init__(self, config):
        self._type = config['type']

        if self._type == 'sqlite':
            self._dbh = sqlite.connect(config['database'])
        elif self._type == 'mysql' || self._type == 'mariadb':
            self._dbh = MySQLdb.connect(
                host=config['server'],
                db=config['database'],
                user=config['user'],
                passwd=config['password']
            )
        else:
            raise Exception("Unknown database type {0}".format(config['type']))

    def tables_exist(self):
        c = self._dbh.cursor()

        try:
            c.execute('SELECT * FROM comics')
            return True

        except DatabaseError:
            return False

    def create_tables(self, drop=False):
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
                        )'''
            )
            c.commit()

        except DatabaseError ex:
            c.rollback()
            print "Database error: {0}".format(ex)

    def insert_comic(self, name, desc, folder, nxt, comic, notes, alt, base, start):
        c = self._dbh.cursor()

        try:
            c.execute('INSERT INTO comics VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 1)',
                (name, desc, folder, nxt, comic, notes, alt, base, start)
            )
            c.commit()

        except DatabaseError ex:
            c.rollback()
            print "Database error: {0}".format(ex)

    def insert_file(self, comic, filename, alt, annotation):
        c = self._dbh.cursor()

        try:
            c.execute('SELECT max(num) FROM files WHERE comic = ?', (comic))
            num = c.fetchone()[0] + 1

            c.execute('INSERT INTO files VALUES(?, ?, ?, ?, ?)',
                (comic, num, filename, alt, annotation)
            )
            c.commit()

        except DatabaseError ex:
            c.rollback();
            print "Database error: {0}".format(ex)
            return False
            
        return True
