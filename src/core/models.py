from datetime import datetime
from peewee import *
from playhouse.migrate import migrate, SqliteMigrator


db = SqliteDatabase('data.db', timeout=10)


class Quote(Model):
    text = TextField()
    created_date = DateTimeField(default=datetime.now)
    last_access = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class Tweet(Model):
    tweet_id = BigIntegerField(unique=True)
    text = TextField()
    created_date = DateTimeField()
    known_at = DateTimeField(default=datetime.now)
    photo_url = TextField(default='')

    class Meta:
        database = db


for t in (Quote, Tweet):
    t.create_table(fail_silently=True)


migrator = SqliteMigrator(db)

operations = [
    migrator.add_column('quote', 'last_access', Quote.last_access),
]

for op in operations:
    try:
        migrate(op)
    except OperationalError:
        pass
