import streamlit as st
from openai import OpenAI
import os

# This looks for the "GROK_API_KEY" you just saved in Streamlit Secrets
client = OpenAI(
    api_key=os.environ.get("GROK_API_KEY"),
    base_url="https://api.x.ai/v1",
)

st.set_page_config(page_title="Grok AI Assistant", page_icon="🤖")
st.title("🤖 My Grok AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask Grok anything..."):
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Grok API
    try:
        response = client.chat.completions.create(
            model="grok-beta", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Error: {e}")
