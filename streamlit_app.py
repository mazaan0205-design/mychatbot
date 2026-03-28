import streamlit as st
from openai import OpenAI
import os

# 1. Setup the Grok Client
# It uses the key from your Streamlit "Secrets" box
client = OpenAI(
    api_key=os.environ.get("GROK_API_KEY"),
    base_url="https://api.x.ai/v1",
)

# 2. Page Styling
st.set_page_config(page_title="Grok AI Assistant", page_icon="🤖")
st.title("🤖 My Grok AI Chatbot")
st.caption("Now powered by xAI Grok-2")

# 3. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Logic
if prompt := st.chat_input("Ask Grok anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Grok API
    try:
        # We use 'grok-2' or 'grok-latest' to avoid the "Model not found" error
        response = client.chat.completions.create(
            model="grok-2", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        answer = response.choices[0].message.content
        
        # Show assistant response
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        # This will show you exactly what is wrong if it fails again
        st.error(f"Something went wrong: {e}")
   
