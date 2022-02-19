
from flask_restful import Api, Resource, reqparse

class VideoToAudio(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'message': "video to audio Api Handler"
      }