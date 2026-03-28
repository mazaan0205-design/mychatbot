import streamlit as st
from openai import OpenAI
import os

# 1. THE "POWERSHELL" STEP (Manual Injection)
# This line is like typing '$env:GROK_API_KEY = "..."' in PowerShell
# Replace the text below with your actual key
os.environ["GROK_API_KEY"] = "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"

# 2. THE "GET" STEP
# Now the code can find it in the environment because we just put it there
api_key = os.environ.get("GROK_API_KEY")

st.set_page_config(page_title="Grok Manual Env", page_icon="🚀")
st.title("🚀 Grok Chatbot: Manual Env Mode")

if not api_key:
    st.error("❌ The environment injection failed.")
    st.stop()

# 3. Setup Client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Grok something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Using the March 2026 stable model
        response = client.chat.completions.create(
            model="grok-4.1-fast-non-reasoning", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"⚠️ xAI Error: {e}")
