
from curses import noecho
from email import header
from email.policy import default
from urllib import request
from xml.dom.minidom import Document, DocumentFragment

from importlib_metadata import re
from flask_restful import Api, Resource, reqparse
import requests


class AudioToText(Resource):
  def get(self):
    request_data = request.get_json()   

    if(request_data['status']==200):
        audioLink = request_data['data-link']

    if audioLink is not None:
        endpoint = "https://api.assembly.com/v2/transcript"
        audio = {"audioLink" : audioLink}
        headers = {
            "authorization": key,
            "content-type": "application/json"
        }
        apiResponse = requests.post(endpoint, json = audio, headers = headers)
        id = apiResponse.json()['id']
        textResponse = requests.get(endpoint +"/"+ id, headers)
        if(textResponse.json()['status'] != "completed"):
            return {
                'resultStatus': 'Failed',
                'status' : 400,
                'message': "Something went Wrong"
            }
        with open(id + '.txt', 'w') as f:
            f.write(textResponse.json()['text'])
      
        return {
        'resultStatus': 'SUCCESS',
        'message': "audio to text Api Handler"
        }
    else:
        return {
        'resultStatus': 'Failed',
        'status' : 400,
        'message': "Something went Wrong"
        }