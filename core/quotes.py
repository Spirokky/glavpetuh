import sqlite3
import logging
import inspect

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

connect = sqlite3.connect('database.db')
cursor = connect.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS quotes (Id INTEGER PRIMARY KEY, text TEXT);")
connect.commit()


def quote_get(id=None):
    data = None
    try:
        with connect:
            if id:
                cursor.execute("SELECT Id, text FROM quotes WHERE Id = (?);", (id,))
                data = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;")
                data = cursor.fetchone()
    except Exception as error:
        logger.warning("quote_get('%s') caused an '%s" % (id, error))
    return data


def quote_add(quote):
    with connect:
        cursor.execute("INSERT INTO quotes(text) VALUES (?);", (quote,))
        lid = cursor.lastrowid


def quote_remove(id=None):
    with connect:
        if id:
            cursor.execute("SELECT Id, text FROM quotes WHERE Id = (?);", (id,))
            target = cursor.fetchone()
            cursor.execute("DELETE FROM quotes WHERE Id = (SELECT MAX(Id) FROM quotes);")
            return target
        else:
            cursor.execute("SELECT Id, text FROM quotes WHERE Id = (SELECT MAX(Id) FROM quotes);")
            target = cursor.fetchone()
            cursor.execute("DELETE FROM quotes WHERE Id = (SELECT MAX(Id) FROM quotes);")
            return target


if __name__ == '__main__':
    data = quote_get(1)
    print(data)
    print(type(data))
# for x in range(25):
#     time.sleep(1.5)
#     q.quote_get()
