import requests
import base64

import logging

### TODO:
### Setup logging

class NextcloudNewsApi:

    baseurl = None
    header = None

    logger = None

    def __init__(self,appName, nextcloudUrl=None, username=None, password=None, logger=None) -> None:

        # if logger == None:
        #     logging.basicConfig(filename="newsApi.log", format = '%(asctime)s %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p',force=True)
        #     self.logger = logging.getLogger()
        #     print("ran")
        # else:
        #     self.logger = logger

        #self.logger = logging.getLogger()

        self.appName = appName

        if  nextcloudUrl == None and username == None and password == None:
            logging.info(self.appName + "No url,username,password inputed, skipping authentication")
            pass
        else:
            self.auth(nextcloudUrl=nextcloudUrl, username=username, password=password)

    def auth(self, nextcloudUrl, username, password):
        self.baseurl = nextcloudUrl + "/index.php/apps/news/api/v1-2/"

        #auth = "base64(" + username + ":" + password + ")"
        auth = username + ":" + password 
        print(base64.b64encode(bytes(auth, "utf-8")))
        self.header = {
            "Authorization": "Basic " + base64.b64encode(bytes(auth, "utf-8")).decode()
        }

        logging.info(self.appName + ": Generated auth tokens")

        try:
            self.getFolders()
        except Exception:
            return False
        
        return True

    def getFolders(self):
        route = "folders"

        params = {

        }
    
        r = self.get(route=route, params=params)

        #self.logger.info("Route:" + route + " \n Status code:" + str(r.status_code))

        logging.info(self.appName +": Route:" + route + " \n Status code:" + str(r.status_code))

        self.errorHandeler(status_code=r.status_code)

        return r.json()

    def getFeeds(self):
        route = "feeds"

        params = {

        }

        r = self.get(route=route, params=params)

        logging.info(self.appName +": Route:" + route + " \n Status code:" + str(r.status_code))

        self.errorHandeler(status_code=r.status_code)

        return r.json()

    def getUnread(self,batchSize=-1,offset=None,type=3,id=None,getRead='false',oldestFirst='false'):
        route = "items"

        params = {
            "batchSize": batchSize, #  the number of items that should be returned, defaults to -1, new in 5.2.3: -1 returns all items
            "offset": offset, # only return older (lower than equal that id) items than the one with id 30
            "type": type, # the type of the query (Feed: 0, Folder: 1, Starred: 2, All: 3)
            "id": id, # the id of the folder or feed, Use 0 for Starred and All
            "getRead": getRead, # if true it returns all items, false returns only unread items
            "oldestFirst": oldestFirst  # implemented in 3.002, if true it reverse the sort order
        }

        r = self.get(route=route, params=params)

        logging.info("Route:" + route + " \n Status code:" + str(r.status_code))

        self.errorHandeler(status_code=r.status_code)

        print(r.status_code)

        return r

    def get(self, route, params):

        print(self.baseurl + route)

        return requests.get(url=self.baseurl + route, headers=self.header, verify=False, params=params)

    def errorHandeler(self, status_code):
        if status_code == 404:
            logging.info(self.appName + ": Unable to connect url=" + self.baseurl)
            raise Exception("Unable to connect")
        
        if status_code == 401:
            logging.info(self.appName + ": Username or password is incoreect")
            raise Exception("Username or password is incorrect")

def main():
    logging.basicConfig(filename="newsApi.log",filemode="a", format = '%(asctime)s %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p',force=True)
    newsApi = NextcloudNewsApi(appName="News")

    login = False

    while login == False:
        url = input("Enter url: ")
        username = input("Enter username: ")
        password = input("Enter Password")

        if newsApi.auth(nextcloudUrl=url, username=username, password=password):
            login = True
        else:
            print("Username or password is incorrect")
            
        
    print(newsApi.header)

    unread = newsApi.getUnread().json()
    print(unread['items'])

    for item in unread['items']:
        print("-"*50)
        print("Title:" + item['title'])
        print("Read:" + str(item['unread']))
        print("Feedid:" + str(item['feedId']))
        print("-"*50)

    folders = newsApi.getFolders()

    for item in folders['folders']:
        print("-"*50)
        print("id: " + str(item['id']))
        print("name: " + str(item['name']))

if __name__ == "__main__":
    main()