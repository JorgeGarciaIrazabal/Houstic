from mongoengine import DoesNotExist

from hubs.middle_ware_hub import MiddleWareHub
from db.house_model import House
from db.user_model import User
import json


# not tested
class UserHub(MiddleWareHub):
    def login(self, user_json):
        return User.objects.get(email=user_json["email"])

    def register(self, user_json):
        user = User.from_json(json.dumps(user_json, ensure_ascii=False))
        user.save()
        return user

    def get_my_houses(self, _sender):
        # sender.ID has to be the user id
        return User.get_user_houses(_sender.ID)

    def add_house(self, house, _sender):
        house = House.from_json(house)
        house.save()
        user = self.__get_user(_sender)
        user.houses.append(house)
        return house.id

    def remove_house(self, house_id):
        House(id=house_id).delete()
        return True

    def __get_user(self, sender):
        """
        :rtype: User
        """
        return User.objects.get(id=sender.ID)
