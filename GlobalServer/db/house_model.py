from datetime import datetime

from mongoengine import *


class House(Document):
    name = StringField(max_length=50, default=None)
    created_date = DateTimeField(default=datetime.utcnow)
