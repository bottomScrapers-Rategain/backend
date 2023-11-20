from Utils import *
from UserData import User,UserService,userDataIndex,userDataMapping

#Do not run this file !!!
if __name__=="__main__":
    # deleteAllRecords(userDataIndex)
    # deleteIndex(userDataIndex)
    # createIndex(userDataIndex)
    # createMapping(userDataIndex,userDataMapping)
    # deleteAllRecords(userDataIndex)
    testUser1 = {
        'id':"abc12",
        'ipAddress':"192.168.1.1",
        'browserData':["Chrome",  "Version 95"],
        'searchTerms':["blog" ,"technology"],
        'interactedAds':["ad456"],
        'interests':["programming" ,"data science"]
    }

    user = User(**testUser1)
    # # UserService.saveUser(user)
    print(UserService.getSimilarUser(user).__dict__)
    # UserService.updateUser("abc123","interests","moonlighting")
    # UserService.updateUser("abc123","searchTerms","lightning")
    # print(getRecord(userDataIndex,"abc123"))