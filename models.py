from peewee import *
import datetime
import os
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ: # later we will manually add this env var
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this
                                                     # env var for you
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('trips.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE

#or DecimalField() FloatField() DoubleField()
class Trip(Model):
    name = CharField()
    center_lat = DoubleField()
    center_long = DoubleField()
    pin1_title = CharField()
    pin1_subtitle = CharField()
    pin1_text = CharField()
    pin1_color = CharField()
    pin1_lat = DoubleField()
    pin1_long = DoubleField()
    pin2_title = CharField()
    pin2_subtitle = CharField()
    pin2_text = CharField()
    pin2_color = CharField()
    pin2_lat = DoubleField()
    pin2_long = DoubleField()
    #create a relationship between an trip and a user:
    uploader = ForeignKeyField(User, backref='trips')
    date = DateField()
    time = TimeField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    # Creating table when we're initializing
    DATABASE.create_tables([User, Trip], safe=True)
    print("TABLES Created")
    DATABASE.close()
