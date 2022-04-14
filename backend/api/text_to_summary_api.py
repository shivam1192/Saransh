import os
import requests
from flask_restful import Api, Resource, reqparse
from flask import request
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
import numpy as np
import pyrebase
from api.helpers import helper
from nltk.tokenize import word_tokenize
import math

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

def clean_text(filename):
    file = open(filename, 'r')
    filedata = file.readlines()
    article = filedata
    sentences = []
    for sentence in article:
      print(sentence)
      sentence = re.sub('[^a-zA-Z]', ' ', str(sentence))
      sentence = re.sub('[\s+]', ' ', sentence)
      sentences.append(sentence)
    sentences.pop()
    display = " ".join(sentences)
    # print('Initial Text: ')
    # print(display)
    # print('\n')
    return sentences


def cnt_words(sent):
    cnt = 0
    words = word_tokenize(sent)
    for word in words:
        cnt += 1
    return cnt


def cnt_in_sent(sentences):
    txt_data = []
    i = 0
    for sent in sentences:
        i += 1
        cnt = cnt_words(sent)
        temp = {'id' : i, 'word_cnt': cnt}
        txt_data.append(temp)
    return txt_data


def freq_dict(sentences):
    i = 0
    freq_list = []
    for sent in sentences:
        i += 1
        freq_dict = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            if word in freq_dict:
                freq_dict[word] = freq_dict[word] + 1
            else:
                freq_dict[word] = 1
            temp = {'id':i, 'freq_dict': freq_dict}
        freq_list.append(temp)
    return freq_list


def calc_TF(text_data, freq_list):
    tf_scores = []
    for item in freq_list:
        ID = item['id']
        for k in item['freq_dict']:
            temp = {
                'id' : item['id'],
                'tf_score' : item['freq_dict'][k]/text_data[ID-1]['word_cnt'],
                'key' : k
            }
            tf_scores.append(temp)
    return tf_scores


def calc_IDF(text_data, freq_list):
    idf_scores = []
    cnt = 0
    for item in freq_list:
        cnt += 1
        for k in item['freq_dict']:
            val = sum([k in it['freq_dict'] for it in freq_list])
            temp = {
                'id' : cnt,
                'idf_score' : math.log(len(text_data)/(val+1)),
                'key': k
            }
            idf_scores.append(temp)
    return idf_scores


def calc_TFIDF(tf_scores, idf_scores):
    tfidf_scores = []
    for j in idf_scores:
        for i in tf_scores:
            if j['key'] == i['key'] and j['id'] == i['id']:
                temp = {
                    'id' : j['id'],
                    'tfidf_score' : j['idf_score'] * i['tf_score'],
                    'key' : j['key']
                    }
                tfidf_scores.append(temp)
    return tfidf_scores


def sent_scores(tfidf_scores, sentences, text_data):
    sent_data = []
    for txt in text_data:
        score = 0
        for i in range(0, len(tfidf_scores)):
            t_dict = tfidf_scores[i]
            if txt['id'] == t_dict['id']:
                score = score + t_dict['tfidf_score']
        temp = {
            'id' : txt['id'],
            'score' : score,
            'sentence' : sentences[txt['id'] - 1]}
        sent_data.append(temp)
    return sent_data


def summary(sent_data):
    cnt = 0
    summary =[]
    for t_dict in sent_data:
        cnt = cnt + t_dict['score']
    avg =  cnt / len(sent_data)
    for sent in sent_data:
        if sent['score'] >= (avg*0.95):
            summary.append(sent['sentence'])
    summary = ". ".join(summary)
    return summary


def summarize(data):
    # sentences =  clean_text('/content/text.txt')
    article = data.strip(' ').split('\n')

    sentences = []
    for sentence in article:
      sentence = re.sub('[^a-zA-Z]', ' ', str(sentence))
      sentence = re.sub('[\s+]', ' ', sentence)
      sentence = sentence.strip(' ')
      sentences.append(sentence)
    sentences.pop()
    sentences.pop()
    text_data = cnt_in_sent(sentences)

    freq_list = freq_dict(sentences)
    tf_scores = calc_TF(text_data, freq_list)
    idf_scores = calc_IDF(text_data, freq_list)

    tfidf_scores = calc_TFIDF(tf_scores, idf_scores)

    sent_data = sent_scores(tfidf_scores, sentences, text_data)
    result = summary(sent_data)
    return result


class TextToSummary(Resource):
  def get(self):
    textLink = request.args.get('textlink', default = None, type = str)
    token = request.args.get('token', default = None, type = str)

    if textLink is not None:
      text = 'text'
      textParsingIndex = textLink.find(text)
      generate_link = ''
      if token != None:
        generate_link = textLink[0:textParsingIndex+4] + '%2F' + textLink[textParsingIndex+5:] + '&token='+token 
      else:
        generate_link = textLink[0:textParsingIndex+4] + '%2F' + textLink[textParsingIndex+5:]

      print(generate_link)

      response = requests.get(generate_link)
      data = response.text

      summary = summarizer(text = data, tokenizer=nlp,max_sent_in_summary=4)

      with open("summary.txt", 'w') as f:
            f.write(summary)

      storage.child("summary/new.txt").put("summary.txt")
      summary_link = storage.child("summary/new.txt").get_url(None)
      os.remove("summary.txt")

      return {
        'resultStatus': 'SUCCESS',
        'status': 200,
        'data_link' : summary_link,
        'message': "video to audio Api Handler"
        }
    else:
      return {
        'resultStatus': 'Failed',
        'status' : 400,
        'message': "Something went Wrong"
        }
