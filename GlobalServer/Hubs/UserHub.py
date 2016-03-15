from mongoengine import DoesNotExist
from wshubsapi.Hub import Hub

from db.HouseModel import House
from db.UserModel import User


# not tested
class UserHub(Hub):
    def loggin(self, userJson):
        try:
            user = User.objects.get(email=userJson["email"])
            user.update(**userJson)  # not sure if update works with just one object
        except DoesNotExist:
            user = User.from_json(userJson)
        user.save()
        return user.id

    def getMyHouses(self, _sender):
        # sender.ID has to be the user id
        return User.getUserHouses(_sender.ID)

    def addHouse(self, house, _sender):
        house = House.from_json(house)
        house.save()
        user = self.__getUser(_sender)
        user.houses.append(house)
        return house.id

    def removeHouse(self, houseId):
        House(id=houseId).delete()
        return True

    def __getUser(self, sender):
        """
        :rtype: User
        """
        return User.objects.get(id=sender.ID)

