import requests
import base64


class NextcloudNewsApi:

    baseurl = None

    header = None

    def __init__(self, nextcloudUrl, username, password) -> None:
        self.baseurl = nextcloudUrl + "/index.php/apps/news/api/v1-2/"

        auth = "base64(" + username + ":" + password + ")"
        print(base64.b64encode(bytes(auth, "ascii")))
        self.header = {
            "Authorization": "Basic " + base64.b64encode(bytes(auth, "utf-8")).decode()
        }

    
    def getUnread(self,batchSize=None,offset=None,type=None,id=None,getRead=None,oldestFirst=None):
        route = "items"

        params = {
            "batchSize": batchSize, #  the number of items that should be returned, defaults to -1, new in 5.2.3: -1 returns all items
            "offset": offset, # only return older (lower than equal that id) items than the one with id 30
            "type": type, # the type of the query (Feed: 0, Folder: 1, Starred: 2, All: 3)
            "id": id, # the id of the folder or feed, Use 0 for Starred and All
            "getRead": getRead, # if true it returns all items, false returns only unread items
            "oldestFirst": oldestFirst  # implemented in 3.002, if true it reverse the sort order
        }

        return self.get(route=route, params=params)

    def get(self, route, params):

        print(self.baseurl + route)

        return requests.get(url=self.baseurl + route, headers=self.header, verify=False, params=params)

def main():
    newsApi = NextcloudNewsApi(nextcloudUrl="https://nextcloud.tail", username="ncp", password="")

    print(newsApi.getUnread(type=3,getRead=False,batchSize=-1))

if __name__ == "__main__":
    main()