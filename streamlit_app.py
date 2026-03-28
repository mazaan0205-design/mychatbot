import streamlit as st
from groq import Groq
import os

# 1. THE MANUAL ENV GET
# This pulls the 'GROK_API_KEY' (or whatever you named it) from Secrets
api_key = os.environ.get("GROK_API_KEY")

st.set_page_config(page_title="Groq AI Assistant", page_icon="⚡")
st.title("⚡ Groq Fast Chat")

if not api_key:
    st.error("❌ Environment Variable 'GROK_API_KEY' not found in Streamlit Secrets.")
    st.stop()

# 2. Setup the ACTUAL Groq Client
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Groq..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 3. Use the most basic/stable Groq model (llama-3.3-70b-versatile)
        # This model has permissions for almost all basic API keys
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        
        answer = completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"⚠️ Groq Error: {e}")
