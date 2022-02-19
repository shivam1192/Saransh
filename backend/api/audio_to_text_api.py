
from flask_restful import Api, Resource, reqparse

class AudioToText(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'message': "audio to text Api Handler"
      }