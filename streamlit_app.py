import streamlit as st
from openai import OpenAI
import os

# 1. Setup the Grok Client
client = OpenAI(
    api_key=os.environ.get("GROK_API_KEY"),
    base_url="https://api.x.ai/v1",
)

st.set_page_config(page_title="Grok AI Assistant", page_icon="🚀")
st.title("🚀 My Grok AI Chatbot")
st.caption("Testing live connection via xAI API")

# 2. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Logic
if prompt := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Using 'grok-latest' is the safest way to avoid 'Model not found' errors
        response = client.chat.completions.create(
            model="grok-latest", 
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Something went wrong: {e}")


