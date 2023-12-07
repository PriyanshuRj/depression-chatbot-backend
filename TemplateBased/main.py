import random

# Define a dictionary of templates
templates = {
    "greeting": ["Hello!", "Hi there!", "Greetings!"],
    "farewell": ["Goodbye!", "See you later!", "Farewell!"],
    "thanks": ["Thank you!", "Thanks a lot!", "Thanks!"],
    "default": ["I'm not sure how to respond to that.", "I didn't understand. Can you rephrase?"],
    "encouragement": ["I'm sorry to hear you're feeling this way. Remember that you're not alone, and it's okay to ask for help. Things can get better."],
    "self_care": ["Taking care of yourself is important. Try to get enough sleep, eat well, and engage in activities you enjoy."],
    "resources": ["If you need professional help, consider reaching out to a mental health professional or a helpline. They are trained to provide support."],
}

def template_based_chatbot(user_input):
    # Convert the user input to lowercase for case-insensitive matching
    user_input_lower = user_input.lower()

    # Check for specific keywords in the user input
    if any(keyword in user_input_lower for keyword in ["hello", "hi", "hey"]):
        return random.choice(templates["greeting"])
    elif any(keyword in user_input_lower for keyword in ["goodbye", "bye", "see you"]):
        return random.choice(templates["farewell"])
    elif any(keyword in user_input_lower for keyword in ["thanks", "thank you"]):
        return random.choice(templates["thanks"])
    else:
        return random.choice(templates["default"])

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Goodbye!")
        break
    response = template_based_chatbot(user_input)
    print("Chatbot:", response)