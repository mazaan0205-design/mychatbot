import streamlit as st
from openai import OpenAI
import os

# 1. THE "GET" STEP
# This looks for the variable in the cloud environment
api_key = os.environ.get("GROK_API_KEY")

st.set_page_config(page_title="Grok 4.20 Agent", page_icon="🤖")
st.title("🤖 My Grok AI Chatbot")
st.caption("Running on xAI Grok-4.20")

if not api_key:
    st.error("❌ Environment Variable 'GROK_API_KEY' not found.")
    st.info("Please add it to your Streamlit Secrets dashboard.")
    st.stop()

# 2. Setup Client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Grok 4.20..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Using the specific 4.20 model you requested
        response = client.chat.completions.create(
            model="grok-beta", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"⚠️ xAI Error: {e}")
