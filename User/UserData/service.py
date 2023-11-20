from UserData.mapping import User,userDataIndex
from Utils import *
from GraphDb import connector as graphClient
import json
from collections import Counter
import spacy

# Load spaCy with medium-sized English word vectors
nlp = spacy.load("en_core_web_md")

# nltk.download('punkt')

def semanticSimilarity(query1, query2):
    query1 = query1.lower()
    query2 = query2.lower()

    if query1=="" or query2=="":
        return 0
    doc1 = nlp(query1)
    doc2 = nlp(query2)
    similarity = doc1.similarity(doc2)
    return similarity

def topNFrequentValues(data, key, n=5):
    # Use Counter to count occurrences of values at key k across all dictionaries
    counts = Counter(value for d in data for value in d.get(key, []))

    # Get the top n most frequent values
    topNValues = [value for value, _ in counts.most_common(n)]

    return topNValues

def findExactMatches(list1, list2):
    # Convert lists to sets for efficient comparison
    set1 = set(list1)
    set2 = set(list2)

    # Check for exact matches
    return 1 if set1 == set2 else 0


def jaccardSimilarity(list1, list2,multiplier=1):
    set1 = set(list1)
    set2 = set(list2)

    intersectionSize = len(set1.intersection(set2))
    unionSize = len(set1.union(set2))

    # Jaccard similarity is the size of the intersection divided by the size of the union
    similarity = intersectionSize / unionSize if unionSize != 0 else 0

    return similarity*multiplier

def fuzzySimilarity(list1, list2,multiplier=1):
    totalSimilarity = 0.0
    totalPairs = 0

    for query1 in list1:
        for query2 in list2:
            similarity = semanticSimilarity(query1, query2)
            totalSimilarity += similarity
            totalPairs += 1

    overallSimilarity = totalSimilarity / totalPairs if totalPairs != 0 else 0.0

    return overallSimilarity

class UserService:
    @staticmethod
    def saveUser(user: User):
        userJson = user.__dict__

        if not checkIfExists(userDataIndex,userJson['id']):
            insertRecord(userDataIndex,userJson)
        
        else:
            pass


    @staticmethod
    def getUserById(userId)->User:
        record = getRecord(userDataIndex,userId)
        
        if len(record)==0:
            return User(-1)

        return User(**record["_source"])

    @staticmethod
    def _updateUser(userId, newUser: User):
        newUserJson = newUser.__dict__

        if not checkIfExists(userDataIndex,userId):
            insertRecord(userDataIndex,newUserJson)

        else:
            updateRecord(userDataIndex,userId,newUserJson)

    
    @staticmethod
    def deleteUser(userId):
        deleteRecord(userDataIndex,userId)

    
    @staticmethod
    def updateUser(userId,key,addValue)->User:
        user: User = UserService.getUserById(userId)


        if(user.getId()==-1):
            saveDict = User(-1).__dict__
            saveDict['id'] = userId

            if key!='ipaddress':
                saveDict[key] = [addValue]
            else:
                saveDict[key]=addValue

            UserService.saveUser(User(**saveDict))
            return User(**saveDict)
        
        user = user.__dict__

        if key!='ipAddress':
            user[key].append(addValue)
        else:
            user[key] = addValue

        user = User(**user)

        UserService._updateUser(userId,user)
        return user
    
    @staticmethod
    def getSimilarUser(user: User)->User:
        user = user.__dict__
        query = {
            "query": {
                "bool": {
                "must_not": [
                    {
                    "term": {
                        "_id": user['id']
                    }
                    }
                ]
                }
            }
            }
        

        def getScore(x):
            score = (x['ipAddress']==user['ipAddress'])*50 + findExactMatches(x['browserData'],user['browserData']) + jaccardSimilarity(x['interests'],user['interests'],3) + fuzzySimilarity(x['searchTerms'],user['searchTerms'],2) + jaccardSimilarity(x['interactedAds'],user['interactedAds'],1)
            print(score)
            return score
        
        
        res = runQuery(userDataIndex,query)
        data = [d["_source"] for d in res['hits']['hits']]

        if len(data)==0:
            return User(id=-1)
        
        data = list(filter(lambda x:getScore(x)>4.0,data))

        if len(data)==0:
            return User(id=-1)
        
        data.sort(key = lambda x: getScore(x),reverse=True)

        return User(**data[0])
    
    @staticmethod
    def mergeSimilarSessions(userId):

        if type(userId) != User:
            if not checkIfExists(userDataIndex,userId):
                return
            
            user: User = UserService.getUserById(userId)

        elif type(userId) == User:
            user = userId
            userId = userId.getId()
            print(userId)

        graphClient.addNode(userId)
        graphClient.deleteEdgesForNode(userId)

        similarUser = UserService.getSimilarUser(user)
        print(similarUser.__dict__)
        if similarUser.getId()==-1:
            return

        graphClient.addNode(similarUser.getId())
        graphClient.addEdge(userId,similarUser.getId())
        return
    
    @staticmethod
    def getUserData(userId,key):
        if not checkIfExists(userDataIndex,userId):
            return
        
        connectedUserIds = graphClient.getConnectedComponent(userId)

        query = {
            "query":{
                "ids":{
                    "values":connectedUserIds
                }
            }
        }

        res = runQuery(userDataIndex,query)

        res = [d["_source"] for d in res['hits']['hits']]

        if len(res)==0:
            return []
        
        return topNFrequentValues(res,key)





    

