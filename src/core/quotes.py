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

    def get(self, id=None, all=False):
        if all:
            with self.connect:
                self.cursor.execute("SELECT * FROM quotes ;")
                data = self.cursor.fetchall()
            return data
        else:
            if not id:
                with self.connect:
                    self.cursor.execute("SELECT id, text FROM quotes WHERE id = (SELECT MAX(id)  FROM quotes);")
                    data = self.cursor.fetchone()
                return data
            else:
                try:
                    id = (int(id))
                except ValueError as e:
                    raise e
                with self.connect:
                    self.cursor.execute("SELECT id, text FROM quotes WHERE Id = (?);", (id,))
                    data = self.cursor.fetchone()
                return data

    def getrandom(self):
        with self.connect:
            self.cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;")
            data = self.cursor.fetchone()

        return data

    def add(self, quote):
        with self.connect:
            self.cursor.execute("INSERT INTO quotes(text) VALUES (?);", (quote,))
            lid = self.cursor.lastrowid
            self.cursor.execute("SELECT id, text FROM quotes WHERE id = (?);", (lid,))
            new_quote = self.cursor.fetchone()

        return new_quote

    def remove(self, id=None):
        if not id:
            self.cursor.execute("SELECT id FROM quotes WHERE id = (SELECT MAX(id)  FROM quotes);")
            id = self.cursor.fetchone()
        else:
            try:
                id = (int(id),)
            except ValueError as e:
                raise e

        with self.connect:
            self.cursor.execute("SELECT id, text FROM quotes WHERE id = (?);", id)
            target = self.cursor.fetchone()
            self.cursor.execute("DELETE FROM quotes WHERE id = (?);", id)

        return target


if __name__ == '__main__':
    q = Quote('testing_database.db')
    print(q.get(all=True))
