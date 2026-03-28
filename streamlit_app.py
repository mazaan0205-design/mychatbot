import streamlit as st
from openai import OpenAI
import os

# 1. DEBUG: This checks if the 'hand' found the 'key' in the environment
raw_key = os.environ.get("GROK_API_KEY")

st.set_page_config(page_title="Grok 2026", page_icon="🚀")

if not raw_key:
    st.error("❌ THE CODE COULD NOT FIND THE KEY IN THE ENVIRONMENT.")
    st.info("Action: Go to Streamlit App Settings -> Secrets and paste: GROK_API_KEY = 'your-key-here'")
    st.stop()
else:
    st.success("✅ Environment Variable 'GROK_API_KEY' found!")

# We strip the key to remove any accidental spaces or quotes from the Secrets box
api_key = raw_key.strip().replace('"', '').replace("'", "")

# 2. Setup Client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

st.title("🚀 My Grok AI Chatbot")

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
        # 3. Use the mandatory March 2026 model name
        # We use grok-4.1-fast-non-reasoning as it is the most stable right now
        response = client.chat.completions.create(
            model="grok-4.1-fast-non-reasoning", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"⚠️ xAI Server Error: {e}")
