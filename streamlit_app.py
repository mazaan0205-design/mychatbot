import streamlit as st
from openai import OpenAI

# 1. DIRECT ACCESS - This is what you wanted
# It pulls directly from the 'pasted' secret in the dashboard
try:
    api_key = st.secrets["GROK_API_KEY"]
except Exception:
    st.error("❌ Secrets Error: Could not find GROK_API_KEY in the dashboard.")
    st.stop()

# 2. Setup Client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

st.title("🚀 Grok AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Using the stable March 2026 'fast' model
        response = client.chat.completions.create(
            model="grok-4.1-fast-non-reasoning", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        # This will tell us if the key is 'Incorrect' or 'Expired'
        st.error(f"⚠️ xAI Error: {e}")
