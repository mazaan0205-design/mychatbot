import streamlit as st
from openai import OpenAI
import os

# Setup Client
client = OpenAI(
    api_key=os.environ.get("GROK_API_KEY"),
    base_url="https://api.x.ai/v1",
)

st.set_page_config(page_title="Grok AI Assistant", page_icon="🚀")
st.title("🚀 My Grok AI Chatbot")
st.caption("Connected to xAI Infrastructure")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Trying the March 2026 stable fast model
        response = client.chat.completions.create(
            model="grok-4.1-fast-non-reasoning", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        # This will tell us if it's a key problem or a model name problem
        st.error(f"Error Details: {e}")
