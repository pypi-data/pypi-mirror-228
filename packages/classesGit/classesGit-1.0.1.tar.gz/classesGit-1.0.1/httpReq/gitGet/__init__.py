from classes.httpReq.Fetch.__init__ import Fetch

class gitDataGet(Fetch):

    def __init__(self, path, authToken):
        super()
        self.path = path
        self.authToken = authToken

    def initGet(self):
        return Fetch.fetchDataGet(self, self.path, self.authToken)
