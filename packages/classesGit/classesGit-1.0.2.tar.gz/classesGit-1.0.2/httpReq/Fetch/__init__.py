import requests
import json

class Fetch:

    def fetchDataGet(self, path, authToken):

        res = requests.get(path, headers={
                "Authorization": f"Bearer {authToken}"
        })

        data = res.json()

        return data

    def fetchDataPut(self, path, data, authToken):

        res = requests.put(path, json.dumps(data, separators=(',', ':')), headers={
            "Authorization": f"Bearer {authToken}",
            "Content-Type": "application/json;charset=UTF-8"
        })
        print(res)

    def fetchDataHead(self, path, authToken):
        res = requests.head(path, headers={
            "Authorization": f"Bearer {authToken}",
            "Content-Type": "application/json;charset=UTF-8"
        })

        return res.headers
