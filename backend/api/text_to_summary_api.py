
from flask_restful import Api, Resource, reqparse

class TextToSummary(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'message':"text to summary Api Handler"
      }