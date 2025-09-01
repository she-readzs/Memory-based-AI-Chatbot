import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Conversation memory
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Function to call Groq API
def get_groq_response():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": st.session_state.conversation_history
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot")

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user msg
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Get bot response
    bot_response = get_groq_response()

    # Save bot msg
    st.session_state.conversation_history.append({"role": "assistant", "content": bot_response})

# Display chat history
for msg in st.session_state.conversation_history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])
