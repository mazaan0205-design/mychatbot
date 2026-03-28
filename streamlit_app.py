import streamlit as st
from openai import OpenAI
import os

# Connect to the key you saved in Streamlit Secrets
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title("🤖 My First AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat logic
if prompt := st.chat_input("What is on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
