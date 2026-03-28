import streamlit as st
from openai import OpenAI
import os

# 1. Get the raw key
raw_key = os.environ.get('grok_api_key")

st.set_page_config(page_title="Grok 2026", page_icon="🚀")

if not raw_key:
    st.error("❌ KEY NOT FOUND: Please check your Streamlit Secrets.")
    st.stop()

# 2. THE SANITIZER: This removes invisible spaces and accidental quotes
# This is the "thing we missed" that causes the 'Incorrect API key' error
api_key = raw_key.strip().replace('"', '').replace("'", "")

# 3. Setup Client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

st.title("🚀 My Grok AI Agent")
st.caption("Active Model: Grok 4.1 Fast (March 2026)")

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
        # 4. Use the specific stable March 2026 Model ID
        response = client.chat.completions.create(
            model="grok-4.1-fast-non-reasoning", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        # If this still says 'Incorrect API key', your key isn't active in console.x.ai
        st.error(f"⚠️ xAI Server Error: {e}")
