from Fetch import Fetch

class gitDataHead(Fetch):

    def __init__(self, path, authToken):
        super()
        self.path = path
        self.authToken = authToken

    def initHead(self):
        return Fetch.fetchDataHead(self, self.path, self.authToken)
