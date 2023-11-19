from es import esclient
import pandas as pd
from elasticsearch import helpers
import json
client = esclient.getClient()

def createIndex(indexName):
    res=client.indices.create(index=indexName)
    print(res)
    return res

def getRecord(indexName,id=id):
    return client.get(index=indexName, doc_type="_doc", id=id)

def getAllIndex():
    res=client.indices.get_alias("*")
    print(res)

def deleteAllIndex():
    indices=client.indices.get_alias().keys()
    for name in indices:
        print(f"Deleted {name}")
        client.indices.delete(index=name)

def deleteIndex(indexName):
    client.indices.delete(index=indexName)


def createMapping(indexName,params):
    res = client.indices.put_mapping(index = indexName,body=params)
    return res

def createSetting(indexName,params):
    res = client.indices.put_settings(index=indexName,body=params)

def closeIndex(indexName):
    res = client.indices.close(index=indexName)

def openIndex(indexName):
    res = client.indices.open(index=indexName)

def getMapping(indexName):
    res = client.indices.get_mapping(index = indexName)
    return res

def getAllRecords(indexName, size=1):
    dataQuery={
      "size":size,
        "query" : {
            "match_all" : {}
        }
    }
    res = client.search(index=indexName, body=dataQuery, ignore=400)
    return res

def deleteAllRecords(indexName):
  data={
        "query": {
            "match_all": {}
        }
    }
  res=client.delete_by_query(index=indexName,doc_type="_doc",body=data)
  return res

def insertRecord(indexName, record):
    if "id" in record:
        return client.index(index=indexName, doc_type="_doc", id = record["id"],body = record)
    else:
        return client.index(index=indexName, doc_type="_doc",body = record)

def updateRecord(indexName, id, record):
    return client.update(index = indexName, id=id, body={"doc": record})

#data is a pd dataframe
def bulkUpload(indexName, data, saveSize=50):

    actions = []

    for index,row in data.iterrows():
        # print(len(json.loads(row['feature'])))

        try:
            row['feature'] = json.loads(row['feature'])
        except Exception:
            pass

        dataDict = dict()

        for key in row.keys():
            dataDict[key]=row[key]
        source = {
                    **dataDict
                    }
        
                    
        action = {
                    '_index': indexName,
                    '_op_type': 'index',
                    '_id': row['id'],
                    '_source': source
                    }
        
        actions.append(action)

        if len(actions) >= saveSize:
            helpers.bulk(client, actions)
            del actions[0:len(actions)]

    if len(actions) > 0:
        helpers.bulk(client, actions)