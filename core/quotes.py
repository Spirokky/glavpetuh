import sqlite3
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Quote(object):

    def __init__(self, db):
        try:
            self.connect = sqlite3.connect(db)
            self.cursor = self.connect.cursor()
        except Exception as e:
            logger.warning("Cannot connect to '%s' cause '%s'" % (db, e))

        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, text TEXT);")
        except Exception as e:
            logger.warning("Cannot create table - '%s'" % (e))
            self.connect.rollback()

        self.connect.commit()

    def get(self, id):
        if not id:
            raise ValueError('id must be integer')
        else:
            try:
                id = int(id)
            except ValueError as e:
                raise e

        data = None

        try:
            with self.connect:
                self.cursor.execute("SELECT id, text FROM quotes WHERE Id = (?);", (id,))
                data = self.cursor.fetchone()
        except Exception as e:
            logger.warning("Trying to get quote caused an '%s'" % (e))
            self.connect.rollback()

        return data

    def getrandom(self):
        data = None

        try:
            with self.connect:
                self.cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;")
                data = self.cursor.fetchone()
        except Exception as e:
            logger.warning("Trying to get random quote caused an '%s'" % (e))
            self.connect.rollback()

        return data

    def add(self, quote):
        new_quote = None

        try:
            with self.connect:
                self.cursor.execute("INSERT INTO quotes(text) VALUES (?);", (quote,))
                lid = self.cursor.lastrowid
                new_quote = self.cursor.execute("SELECT id, text FROM quotes WHERE Id = (?);", (lid,))
        except Exception as e:
            logger.warning("Trying to add quote caused an '%s'" % (e))
            self.connect.rollback()

        return new_quote

    def remove(self, id):
        if not id:
            raise ValueError('id must be integer')
        else:
            try:
                id = int(id)
            except ValueError as e:
                raise e

        target = None

        try:
            with self.connect:
                self.cursor.execute("SELECT Id, text FROM quotes WHERE Id = (?);", (id,))
                target = self.cursor.fetchone()
                self.cursor.execute("DELETE FROM quotes WHERE Id = (SELECT MAX(Id) FROM quotes);")
        except Exception as e:
            logger.warning("Cannot remove quote '%s' cause '%s'" % (id, e))
            self.connect.rollback()

        return target


if __name__ == '__main__':
    q = Quote('testing_database.db')
