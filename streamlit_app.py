import streamlit as st
from openai import OpenAI
import os

# 1. Secret Diagnosis
api_key = os.environ.get("GROK_API_KEY")

st.set_page_config(page_title="Grok 2026 AI", page_icon="🤖")

if not api_key:
    st.error("❌ ERROR: 'GROK_API_KEY' not found in Streamlit Secrets.")
    st.info("Go to: Manage App -> Settings -> Secrets and add: GROK_API_KEY = 'your-key'")
    st.stop()

# 2. Setup Client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

st.title("🤖 My Grok AI Agent")
st.caption("Running on xAI Grok-4.1-Fast (March 2026)")

# 3. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Execution
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # We use the specific 2026 stable model ID here
        response = client.chat.completions.create(
            model="grok-4.1-fast-non-reasoning", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        # This will tell us if it's 'Model not found' or 'Invalid API Key'
        st.error(f"⚠️ API Error: {e}")
