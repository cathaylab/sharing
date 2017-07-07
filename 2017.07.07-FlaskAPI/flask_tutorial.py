#!/usr/local/bin/python
from flask import Flask, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

#Mongo connection
MONGO_HOST = 'localhost' #88.8.141.118
MONGO_DB = 'mydb'
client = MongoClient(MONGO_HOST)
db = client[MONGO_DB]
#success = client[MONGO_DB].authenticate(MONGO_USER, MONGO_PWD, mechanism="SCRAM-SHA-1")

@app.route('/helloworld')
def hello_world():
    '''
    Say hello to the world
    '''
    

    '''
    hi it's me
    '''

    return 'Hello, World!'

@app.route('/userinterest')
def interest():
    '''
    Type username and return all interest for this user
    '''
    username = request.args.get('username')
    collect = db.interest.find({'name':username},{ '_id': 0})
    collect_decode = [repr(col).decode('unicode-escape') for col in collect]
    return jsonify(collect_decode)


@app.route('/userscore', methods = ['POST'])
def score():
    '''
    Type username and interest then return the score of the interest
    '''
    json_data = request.get_json(force=True)
    username = json_data['username']
    interest = json_data['interest']    
    collect = db.interest.find({'$and':[{'name':username},{'interest':interest}]},{ '_id': 0})
    return jsonify(collect[0]['score'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
