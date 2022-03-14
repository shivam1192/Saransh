from api.helpers import helper
from flask_restful import Resource
import requests
import pyrebase
from flask import request
import pprint
from time import sleep
import os

firebase = pyrebase.initialize_app(helper.config)
storage = firebase.storage()

class AudioToText(Resource):
  def get(self):
    audioLink = request.args.get('audiolink', default = None, type = str)
    token = request.args.get('token', default = None, type = str)
    
    if audioLink is not None:

        audioParsingIndex = audioLink.find('audio')
        audioLink = audioLink[0:audioParsingIndex+5] + '%2F' + audioLink[audioParsingIndex+6:] + '&token=' + token
        endpoint = "https://api.assemblyai.com/v2/transcript"
        audio = {"audio_url" : audioLink}
        headers = {
            "authorization": helper.assembly['key'],
            "content-type": "application/json"
        }
        apiResponse = requests.post(endpoint, json = audio, headers = headers)
        print("*"*10 + "\nTranscription request send\n" + "*"*10)
        pprint.pprint(apiResponse.json())

        id = apiResponse.json()['id']
        apiend = endpoint+"/"+id
        textResponse = requests.get(apiend, headers = headers)
        print("*"*10 + "Called for text ouput" + "*"*10)
        pprint.pprint(textResponse.json())

        filename = textResponse.json()['id'] + '.txt'

        while textResponse.json()['status'] != 'completed':
            sleep(30)
            textResponse = requests.get(apiend, headers = headers)
            print("file is " + textResponse.json()['status'])
        with open(filename, 'w') as f:
            f.write(textResponse.json()['text'])
      
        text_link = storage.child("text/" + id).put(id + ".txt")
        text_link = storage.child("text/" + id).get_url(None)
        os.remove(filename)

        return {
        'resultStatus': 'SUCCESS',
        'text-link': text_link,
        'message': "audio to text Api Handler"
        }
    else:
        return {
        'resultStatus': 'Failed',
        'status' : 400,
        'message': "Something went Wrong"
        }
