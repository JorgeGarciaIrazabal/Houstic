from datetime import datetime

from mongoengine import *


class House(Document):
    ip = StringField(max_length=16)
    name = StringField(max_length=50, required=True)
    connection_id = StringField(required=True)
    created_date = DateTimeField(default=datetime.utcnow)
