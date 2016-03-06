from wshubsapi.Hub import Hub


class LoggingHub(Hub):
    def loggin(self, user, password):
        return "necessary to implement"

    def getMyHouses(self, _sender):
        # query houses with _sender.ID
        return []
