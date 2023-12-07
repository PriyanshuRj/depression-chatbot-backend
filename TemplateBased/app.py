from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)
# Define template responses
templates = {
    "greeting": ["Hello!", "Hi there!", "Greetings!"],
    "farewell": ["Goodbye!", "See you later!", "Farewell!"],
    "thanks": ["Thank you!", "Thanks a lot!", "Thanks!"],
    "default": ["I'm not sure how to respond to that.", "I didn't understand. Can you rephrase?"],
    "encouragement": ["I am feeling very low"],
    "self_care": ["How do i take care of myself"],
    "resources": ["can you give me some resources"],
}

# Define corresponding responses
responses = {
    "greeting": "Hello! How can I help you?",
    "goodbye": "Goodbye! Have a great day!",
    "question": "I'm doing well, thank you for asking.",
    "encouragement": "I'm sorry to hear you're feeling this way. Remember that you're not alone, and it's okay to ask for help. Things can get better.",
    "self_care": "Taking care of yourself is important. Try to get enough sleep, eat well, and engage in activities you enjoy.",
    "resources": "If you need professional help, consider reaching out to a mental health professional or a helpline. They are trained to provide support.",
}

def get_response(message):
    
    print(message)
    for intent, keywords in templates.items():
        for keyword in keywords:
            if keyword in message:
                return responses.get(intent, "I didn't understand that.")
    return "I didn't understand that."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    response = get_response(user_message)
    return jsonify({'response': response})

if __name__ =="__main__":
    serve(app, port=5000)