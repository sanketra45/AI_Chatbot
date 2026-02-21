import os
import streamlit as st
from mistralai import Mistral

def get_mistral_response(user_message):
    messages = [
        {"role":"system", 
         "content":"You are an expert with extensive knowledge about INDIAN places, cities and food. Keep your answers accurate and concise."},
        {"role":"user", 
         "content":user_message}
    ]

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        response_format={"type":"text"},
        temperature=0
    )

    return response.choices[0].message.content

st.title("Chatbot powered by Mistral ")

try:
    # load and read the secret key from .streamlit/secrets.toml
    MISTRAL_API_KEY = st.secrets["MISTRAL"]["api_key"]
except:
    st.error("Add your Mistral API key in .streamlit/secrets.toml")
    st.stop()

# initialize Mistral client and create connection to Mistral server
client = Mistral(api_key=MISTRAL_API_KEY)

# streamlit refreshes on every input, so we store chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.chat_input(placeholder="Namaskar! Boliye")
if user_input:
    # add the user's message to the chat history
    st.session_state.history.append({"role":"user", 
                                     "content":user_input})

    with st.spinner(":brain: Thinking..."):
        # fetch response from Mistral
        mistral_reply = get_mistral_response(user_input)

    # add the model's reply to chat history
    st.session_state.history.append({"role": "assistant", 
                                     "content": mistral_reply})

# st.write(st.session_state.history)
for chat in st.session_state.history:
    if chat["role"] == "user":
        message = st.chat_message("user",
                                  avatar=":material/face_6:")
        message.write(f"**You:** {chat['content']}")
    else:
        message = st.chat_message("ai",
                                  avatar=":material/bolt:")
        message.write(f"{chat['content']}")
        