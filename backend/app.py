
from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.audio_to_text_api import AudioToText
from api.video_to_audio_api import VideoToAudio
from api.text_to_summary_api import TextToSummary


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(VideoToAudio, '/flask/videotoaudio')
api.add_resource(AudioToText, '/flask/audiototext')
api.add_resource(TextToSummary, '/flask/texttosummary')
