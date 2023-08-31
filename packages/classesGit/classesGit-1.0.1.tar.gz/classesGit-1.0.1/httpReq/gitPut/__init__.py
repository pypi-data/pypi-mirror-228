from classes.httpReq.Fetch.__init__ import Fetch

class gitDataPut(Fetch):

    def __init__(self, path, data, authToken):
        super()
        self.path = path
        self.data = data
        self.authToken = authToken

    def initPut(self):
        return Fetch.fetchDataPut(self, self.path, self.data, self.authToken)
