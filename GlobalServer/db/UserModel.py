from datetime import datetime
from mongoengine import *

from db.HouseModel import House


class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(max_length=50)
    password = StringField(max_length=50, required=True)
    houses = ListField(ReferenceField(House), default=[], reverse_delete_rule=CASCADE)
    createdDate = DateTimeField(default=datetime.utcnow)

    @classmethod
    def getUserHouses(cls, userId):
        return cls.objects(id=userId).only("houses").get().houses


if __name__ == '__main__':
    connect("houstic")
    print User.objects.only("houses").first()
    print "end"