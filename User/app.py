from flask import Flask, jsonify,request
from flask_cors import CORS
from UserData import userDataIndex,UserService,User
from Utils import getRecord,getAllRecords
import random

app = Flask(__name__)
CORS(app)
baseAdUrl = "https://rategain2023.s3.ap-south-1.amazonaws.com/Ads"

lengthDict = {
    "clothing":16,
    "baby":15,
    "cars":15,
    "electronics":15,
    "grocery":15,
    "hardware":15,
    "health":15,
    "media":15,
    "outdoor":15,
    "video games":15,
    "home":15,
    "betting":15,
    "dating":15,
    "instruments":15,
    "jewellery":15,
    "pet":15,
    "software":15,
    "sports":15,
    "stationary":15,
    "toys":15
}

numAds = 4



@app.route('/getrecord',methods=['GET'])
def getRecords():
    return jsonify(getAllRecords(userDataIndex,size=10))


@app.route('/update',methods=['POST'])
def updateRecord():
    body = request.get_json()
    ipAddress = request.remote_addr
    if 'userId' not in body or 'key' not in body or 'value' not in body:
        return

    try:
        userId = body['userId']
        key = body['key']
        value = body['value']

        user: User = UserService.updateUser(userId,key,value)
        user: User = UserService.updateUser(userId,"ipAddress",ipAddress)
        UserService.mergeSimilarSessions(user)

        return "Success",200
    
    except Exception as e:
        print(e)
        return "Internal Server Error",500
    

@app.route('/getvalue',methods=["POST"])
def getValue():
    body = request.get_json()

    return UserService.getUserData(body['userId'],body['key'])


@app.route('/getallvalue',methods=["POST"])
def getAllValue():
    body = request.get_json()
    print(body)
    return jsonify(UserService.getAllUserData(body['userId']))
    # return jsonify({"a":"b"})


@app.route('/getads',methods=['POST'])
def getAds():
    body = request.get_json()

    if 'interestList' not in body:
        return "error",400
    
    adList = []

    for interest in body['interestList']:
        if interest not in lengthDict:
            continue

        limit = lengthDict[interest]
        indexes = random.sample(list(range(1,limit+1)),numAds)

        for index in indexes:
            url = f"{baseAdUrl}/{interest}/{index}.png"
            adList.append(url)

    if len(adList)>=numAds:
        adList = random.sample(adList,numAds)

    return jsonify({'adList':adList}),200

if __name__ == '__main__':
    app.run(debug=True)