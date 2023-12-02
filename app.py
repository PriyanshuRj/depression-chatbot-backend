
from flask import Flask, request
from flask_restful import Api, Resource



from logging.handlers import TimedRotatingFileHandler
import logging
import datetime
import os
from waitress import serve

from utils import chatbot_response


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



class MessagingRouter(Resource):
    def post(self):
        userText = request.form.get('msg')
        print(userText)
        reply = chatbot_response(userText)
        return {"Reply" : reply}
    
api.add_resource(MessagingRouter, "/message")

if __name__ =="__main__":
    serve(app, host="0.0.0.0", port=5000)