import html
import json
import logging
import sqlite3
import tweepy

from config import secrets

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

db = 'core/database.db'
db_test = 'core/testing_database.db'


class TweetsListener(tweepy.StreamListener):

    def __init__(self):
        try:
            self.connect = sqlite3.connect(db)
            self.cursor = self.connect
        except Exception as e:
            logger.error("Cannot connect to '%s' cause '%s'" % (db, e))

        super(tweepy.StreamListener, self).__init__()

        with self.connect:
            try:
                self.cursor.execute(
                    "CREATE TABLE IF NOT EXISTS tweets (status INTEGER, tweet TEXT);"
                )
            except:
                pass

    def on_data(self, raw_data):
        try:
            data = json.loads(raw_data)

            text = html.unescape(data["text"])
            userid = data["user"]["id"]

            if userid in [2849516458, 781306838]:
                res = (0, text)
            else:
                res = None

            if res:
                with self.connect:
                    self.cursor.execute("INSERT INTO tweets VALUES (?, ?);", res)

        except Exception as e:
            logger.warning(e)

    def on_status(self, status):
        try:
            logger.info(status)

        except Exception as e:
            logger.warning(e)

    def on_error(self, status_code):
        logger.error(status_code)
        return True  # keep stream alive

    def on_timeout(self):
        logger.info("Timeout")


def main():
    consumer_key = secrets.consumer_key
    consumer_secret = secrets.consumer_secret
    access_token = secrets.access_token
    access_secret = secrets.access_token_secret

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = tweepy.Stream(auth, TweetsListener(), timeout=None)

    stream.filter(follow=['2849516458', '781306838'])


if __name__ == '__main__':
    try:
        db = db_test
        main(False, False)

    except Exception as e:
        logger.warning(e)
