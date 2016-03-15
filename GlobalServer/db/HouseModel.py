from datetime import datetime

from mongoengine import *


class House(Document):
    ip = StringField(max_length=16)
    name = StringField(max_length=50, required=True)
    connectionID = StringField(required=True)
    createdDate = DateTimeField(default=datetime.utcnow)