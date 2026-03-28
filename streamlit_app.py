import streamlit as st
from groq import groq
import os

# 1. THE "GET" STEP (Like your PowerShell setup)
# This pulls the 'GROK_API_KEY' you pasted in the Secrets dashboard
api_key = os.environ.get("GROK_API_KEY")

st.set_page_config(page_title="Grok Basic Mode", page_icon="🤖")
st.title("🤖 Grok: Basic Permission Mode")

if not api_key:
    st.error("❌ Environment Variable Not Found.")
    st.info("Ensure you pasted GROK_API_KEY = 'xai-...' in Streamlit Secrets.")
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

if prompt := st.chat_input("Ask Grok anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # THE UNIVERSAL MODEL: 'grok-beta' has the widest permissions
        response = client.chat.completions.create(
            model="grok-beta", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        # If this STILL says 'Invalid', we need to check the Key at console.x.ai
        st.error(f"⚠️ xAI Error: {e}")
