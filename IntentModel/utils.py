import nltk
nltk.download('popular')


import json
import random

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import pickle
import numpy as np
import os
from keras.models import load_model

BASE_PATH = os.getcwd()
BASE_PATH = os.path.join(BASE_PATH, 'IntentModel')

MODEL_PATH = os.path.join(BASE_PATH, 'model.h5')
INTENT_PATH = os.path.join(BASE_PATH, 'intents.json')
WORD_PATH = os.path.join(BASE_PATH, 'texts.pkl')
CLASSES_PATH = os.path.join(BASE_PATH, 'labels.pkl')

model = load_model(MODEL_PATH)
intents = json.loads(open(INTENT_PATH).read())
words = pickle.load(open(WORD_PATH,'rb'))
classes = pickle.load(open(CLASSES_PATH,'rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model, threshold):

    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = threshold
    
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    print(ints)
    result = ""
    if(len(ints)==0):
        return "Sorry can't Process Your Message the bot is still in training"
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg, threshold):
    print(msg)
    ints = predict_class(msg, model, threshold)
    res = getResponse(ints, intents)
    return res