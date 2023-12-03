
from flask import Flask, request
from flask_restful import Api, Resource



from logging.handlers import TimedRotatingFileHandler
import logging
import datetime
import os
from waitress import serve

from IntentModel import chatbot_response
from SBERT import SBERT_chatbot_response

if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
    os.mkdir(os.path.join(os.getcwd(), 'logs'))

log_formatter = logging.Formatter('%(asctime)s %(name)s  : %(message)s')
log_filename = f'logs/app_{datetime.datetime.now().strftime("%Y-%m-%d")}.log'
file_handler = TimedRotatingFileHandler(log_filename, when='midnight', interval=1, backupCount=30)
file_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)
app = Flask(__name__)

api = Api(app)



class MessagingRouterIntent(Resource):
    def post(self):
        userText = request.form.get('msg')
        print(userText)
        reply = chatbot_response(userText, 0.8)
        return {"Reply" : reply}

class MessagingRouterSBERT(Resource):
    def post(self):
        userText = request.form.get('msg')
        print(userText)
        reply = SBERT_chatbot_response(userText, 0.8)
        return {"Reply" : reply}
    
api.add_resource(MessagingRouterIntent, "/message-intent")
api.add_resource(MessagingRouterSBERT, "/message-sbert")

if __name__ =="__main__":
    serve(app, host="0.0.0.0", port=5000)