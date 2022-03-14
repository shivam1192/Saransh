import os
from flask_restful import Resource
from flask import request
import moviepy.editor as mp
import pyrebase
from api.helpers import helper

firebase = pyrebase.initialize_app(helper.config)
storage = firebase.storage()

class VideoToAudio(Resource):
  def get(self):
    videoLink = request.args.get('videolink', default = None, type = str)
    token = request.args.get('token', default = None, type = str)

    if videoLink is not None:
      videos = 'videos'
      videoParsingIndex = videoLink.find(videos)
      generate_link = videoLink[0:videoParsingIndex+6] + '%2F' + videoLink[videoParsingIndex+7:] + '&token='+token
      print(generate_link)
      my_clip = mp.VideoFileClip(generate_link)
      my_clip.audio.write_audiofile(r"my_result.mp3")
      storage.child("audio/new.mp3").put("my_result.mp3")
      audio_link = storage.child("audio/new.mp3").get_url(None)
      os.remove("my_result.mp3")
      return {
        'resultStatus': 'SUCCESS',
        'status': 200,
        'data-link' : audio_link,
        'message': "video to audio Api Handler"
        }
    else:
      return {
        'resultStatus': 'Failed',
        'status' : 400,
        'message': "Something went Wrong"
        }
