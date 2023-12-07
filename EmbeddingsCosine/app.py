from flask import Flask, render_template, request, jsonify
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load spaCy model (you can use a larger model depending on your needs)
nlp = spacy.load("en_core_web_sm")

# Define a set of predefined supportive responses and their average word embeddings
supportive_responses = {
    "encouragement": "I'm sorry to hear you're feeling this way. Remember that you're not alone, and it's okay to ask for help. Things can get better.",
    "self_care": "Taking care of yourself is important. Try to get enough sleep, eat well, and engage in activities you enjoy.",
    "resources": "If you need professional help, consider reaching out to a mental health professional or a helpline. They are trained to provide support.",
}

# Calculate average word embeddings for predefined supportive responses
supportive_response_embeddings = {key: np.mean(list(nlp(value).vector)) for key, value in supportive_responses.items()}

def cosine_similarity_score(user_input, response_embedding):
    user_embedding = np.mean(list(nlp(user_input).vector))
    if user_embedding is not None and response_embedding is not None:
        # Calculate cosine similarity
        similarity_score = cosine_similarity([[user_embedding]], [response_embedding])[0][0]
        return similarity_score
    else:
        return 0  # Return a default value if embeddings are not available

def supportive_chatbot(user_input):
    # Calculate similarity scores for each predefined supportive response
    similarity_scores = {
        key: cosine_similarity_score(user_input, response_embedding)
        for key, response_embedding in supportive_response_embeddings.items()
    }

    # Identify the response with the highest similarity score
    best_response_key = max(similarity_scores, key=similarity_scores.get)

    # Return the best-matching supportive response
    return supportive_responses[best_response_key]


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = supportive_chatbot(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)