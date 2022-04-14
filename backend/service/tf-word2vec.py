import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

stopwords = list(STOP_WORDS)
doc = spacy.load('en_core_web_sm')
doc = doc(text_corpus)




word_frequencies = {}

for word in tokens:
    if word not in word_frequencies.keys():
        word_frequencies[word] = 1
    else:
        word_frequencies[word] += 1


max_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word]/max_frequency

sentences_tokens = [sent for sent in doc.sents]
# print(len(sentences_tokens))
sentence_organizer = {k:v for v,k in enumerate(sentences_tokens)}
# print(sentence_organizer)


embeddings = {}
for word in word_to_id:
    learning = one_hot_encode(word_to_id[word], len(word_to_id))
    result = forward(model, [learning], return_cache=False)[0]
    ind = np.argpartition(result, -10)[-10:]
    embeddings[word] = result[ind].sum()


sentence_scores = {}
for sent in sentences_tokens:
    for word in sent:
        if word.text.lower() not in punctuation:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()] * embeddings[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()] * embeddings[word.text.lower()]
            else:
                continue


x = sentence_scores
top_n_sentences = [k for k, v in sorted(x.items(), key=lambda item: item[1])][::-1][:len(sentence_scores)//3]

mapped_sentences = [ (sentence, sentence_organizer[sentence]) for sentence in top_n_sentences]
mapped_top_n_sentences = sorted(mapped_sentences, key = lambda x: x[1])
ordered_sentence = [sentence[0] for sentence in mapped_top_n_sentences]
summary = " "
for sent in ordered_sentence:
    summary += sent.text