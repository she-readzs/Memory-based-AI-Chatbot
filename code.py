import os
import requests
import json
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Conversation memory
conversation_history = []

# Send message to Groq API
def get_groq_response():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": conversation_history
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# Add messages to history
def update_conversation(role, content):
    conversation_history.append({"role": role, "content": content})

# Chatbot loop
def chatbot():
    print("Groq Chatbot: Hello! Type 'exit' to quit.")

    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            print("Groq Chatbot: Goodbye!")
            break

        # Add user msg to memory
        update_conversation("user", user_message)

        # Get bot response
        bot_response = get_groq_response()

        # Add bot response to memory
        update_conversation("assistant", bot_response)

        print(f"Groq Chatbot: {bot_response}")

# Run chatbot
if __name__ == "__main__":
    chatbot()
