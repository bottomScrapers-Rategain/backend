from flask import Flask, jsonify,request
from flask_cors import CORS
from UserData import userDataIndex,UserService,User
from Utils import getRecord,getAllRecords

app = Flask(__name__)
CORS(app)


@app.route('/getRecord',methods=['GET'])
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

    return jsonify(UserService,getAllValue(body['userId']))



if __name__ == '__main__':
    app.run(debug=True)