userDataIndex = "userdataindex"

userDataMapping = {
    "properties": {
        "id": {"type": "keyword"},
        "ipAddress": {"type":"object", "enabled":False},
        "browserData": {"type":"object", "enabled":False},
        "searchTerms": {"type":"object", "enabled":False},
        "interactedAds": {"type":"object", "enabled":False},
        "interests":{"type":"object", "enabled":False},
    }
}


class User:
    def __init__(self,id,ipAddress="",browserData=[],searchTerms=[],interactedAds=[],interests=[]):
        self.id = id
        self.ipAddress = ipAddress
        self.browserData = browserData
        self.searchTerms = searchTerms
        self.interactedAds = interactedAds
        self.interests = interests

    # Getter and setter for id
    def getId(self):
        return self.id

    def setId(self, newId):
        self.id = newId

    # Getter and setter for ipAddress
    def getIpAddress(self):
        return self.ipAddress

    def setIpAddress(self, newIpAddress):
        self.ipAddress = newIpAddress

    # Getter and setter for browserData
    def getBrowserData(self):
        return self.browserData

    def setBrowserData(self, newBrowserData):
        self.browserData = newBrowserData

    # Getter and setter for searchTerms
    def getSearchTerms(self):
        return self.searchTerms

    def setSearchTerms(self, newSearchTerms):
        self.searchTerms = newSearchTerms

    # Getter and setter for interactedAds
    def getInteractedAds(self):
        return self.interactedAds

    def setInteractedAds(self, newInteractedAds):
        self.interactedAds = newInteractedAds

    # Getter and setter for interests
    def getInterests(self):
        return self.interests

    def setInterests(self, newInterests):
        self.interests = newInterests


    