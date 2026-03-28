import streamlit as st
from openai import OpenAI
import os

# 1. Setup the Grok Client
# This looks for 'GROK_API_KEY' in your Streamlit Secrets
api_key = os.environ.get("GROK_API_KEY")

if not api_key:
    st.error("❌ Key not found! Go to Streamlit Settings -> Secrets and add GROK_API_KEY")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

st.set_page_config(page_title="Grok AI Assistant", page_icon="🚀")
st.title("🚀 My Grok AI Chatbot")
st.caption("Updated for March 2026 Models")

# 2. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Logic
if prompt := st.chat_input("Say hello..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # CHANGED LINE: This is the only name the server accepts right now
        response = client.chat.completions.create(
            model="grok-4.1-fast-non-reasoning", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Developer Log: {e}")
