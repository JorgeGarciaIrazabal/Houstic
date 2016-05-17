from datetime import datetime
from mongoengine import *

from db.house_model import House


class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(max_length=50)
    password = StringField(max_length=50, required=True)
    houses = ListField(ReferenceField(House), default=[], reverse_delete_rule=CASCADE)
    created_date = DateTimeField(default=datetime.utcnow)

    @classmethod
    def get_user_houses(cls, user_id):
        return cls.objects(id=user_id).only("houses").get().houses


if __name__ == '__main__':
    connect("houstic")
    print(User.objects.only("houses").first())
    print("end")