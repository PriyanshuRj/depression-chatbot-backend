from sentence_transformers import SentenceTransformer
from torch import Tensor
import torch
import pickle
import json
import random
import os

BASE_PATH = os.getcwd()
BASE_PATH = os.path.join(BASE_PATH, 'SBERT')

INTENT_PATH = os.path.join(BASE_PATH, 'intents.json')
CLASSES_PATH = os.path.join(BASE_PATH, 'labels.pkl')
MODEL_PATH = os.path.join(BASE_PATH, 'similarity-LM')
intents = json.loads(open(INTENT_PATH).read())
classes = pickle.load(open(CLASSES_PATH,'rb'))
model = SentenceTransformer(MODEL_PATH)

def cos_sim(a: Tensor, b: Tensor):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))

def getResponse(ints, intents_json):
    print(ints)
    if(len(ints)==0):
        return "Sorry can't Process Your Message the bot is still in training"
    tag = ints[0]
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def SBERT_chatbot_response(message, threshold):

    message_emb = model.encode(message)
    doc_emb = model.encode(classes)

    #Compute dot score between query and all document embeddings
    scores = cos_sim(message_emb, doc_emb)[0].cpu().tolist()

    #Combine docs & scores
    doc_score_pairs = list(zip(classes, scores))

    #Sort by decreasing score
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    #Output passages & scores
    
    if(doc_score_pairs[0][1] > threshold):
        res = getResponse(doc_score_pairs[0], intents)
        return res
    
    else :
        return "Sorry can't Process Your Message the bot is still in training"