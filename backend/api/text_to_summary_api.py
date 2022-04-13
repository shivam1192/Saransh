import os
import requests
from flask_restful import Api, Resource, reqparse
from flask import request

from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
import numpy as np
import pyrebase
from api.helpers import helper


firebase = pyrebase.initialize_app(helper.config)
storage = firebase.storage()

nlp = English()
nlp.add_pipe('sentencizer')

def summarizer(text, tokenizer, max_sent_in_summary=3):
  document = nlp(text.replace("\n", ""))
  sentences = [sent.text.strip() for sent in document.sents]
  sentence_organizer = {k:v for v,k in enumerate(sentences)}
  tf_idf_vectorizer = TfidfVectorizer(min_df=2,  max_features=None, 
                                      strip_accents='unicode', 
                                      analyzer='word',
                                      token_pattern=r'\w{1,}',
                                      ngram_range=(1, 3), 
                                      use_idf=1,smooth_idf=1,
                                      sublinear_tf=1,
                                      stop_words = 'english')
  tf_idf_vectorizer.fit(sentences)
  sentence_vectors = tf_idf_vectorizer.transform(sentences)
  sentence_scores = np.array(sentence_vectors.sum(axis=1)).ravel()
  N = max_sent_in_summary
  top_n_sentences = [sentences[ind] for ind in np.argsort(sentence_scores, axis=0)[::-1][:N]]
  mapped_top_n_sentences = [(sentence,sentence_organizer[sentence]) for sentence in top_n_sentences]
  mapped_top_n_sentences = sorted(mapped_top_n_sentences, key = lambda x: x[1])
  ordered_scored_sentences = [element[0] for element in mapped_top_n_sentences]
  summary = " ".join(ordered_scored_sentences)
  return summary


class TextToSummary(Resource):
  def get(self):
    textLink = request.args.get('textlink', default = None, type = str)
    token = request.args.get('token', default = None, type = str)

    if textLink is not None:
      text = 'text'
      textParsingIndex = textLink.find(text)
      generate_link = textLink[0:textParsingIndex+4] + '%2F' + textLink[textParsingIndex+5:] + '&token='+token
      print(generate_link)

      response = requests.get(generate_link)
      data = response.text

      summary = summarizer(text=data, tokenizer=nlp, max_sent_in_summary=3)

      with open("summary.txt", 'w') as f:
            f.write(summary)

      storage.child("summary/new.txt").put("summary.txt")
      summary_link = storage.child("summary/new.txt").get_url(None)
      os.remove("summary.txt")

      return {
        'resultStatus': 'SUCCESS',
        'status': 200,
        'summary_link' : summary_link,
        'message': "video to audio Api Handler"
        }
    else:
      return {
        'resultStatus': 'Failed',
        'status' : 400,
        'message': "Something went Wrong"
        }
