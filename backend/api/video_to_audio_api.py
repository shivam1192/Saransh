import pyrebase

config  = {
  "projectId": "saransh-36252",
  "appId": "1:810027509020:web:c38d4b4ce5ea82a202c6d9",
  "databaseURL": "https://saransh-36252-default-rtdb.firebaseio.com",
  "storageBucket": "saransh-36252.appspot.com",
  "locationId": "us-central",
  "apiKey": "AIzaSyAYkvtXrRtT2V6WVtR3vBP4IL7xDVBs2BE",
  "authDomain": "saransh-36252.firebaseapp.com",
  "messagingSenderId": "810027509020",
  "measurementId": "G-B0JCFZ62LK"
};

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


import os
from flask_restful import Api, Resource, reqparse
from flask import request
import moviepy.editor as mp

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