import streamlit as st
from langchain.chains import ConversationChain
from hugchat import hugchat
from hugchat.login import Login

# App configuration
st.set_page_config(page_title="Nelsonbot - Hugging Face Chatbot", layout="wide")
st.title("🤗💬 Nelsonbot - AI Assistant")

# Hugging Face Credentials
with st.sidebar:
    st.header("Hugging Face Login")
    hf_email = st.text_input("Enter E-mail:", type="password")
    hf_pass = st.text_input("Enter password:", type="password")
    st.markdown("📖 Learn more about this app [here](https://blog.streamlit.io)")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How may I assist you?"}]

# Function to generate responses using LangChain
def generate_response(prompt, email, password):
    try:
        # Hugging Face Login
        sign = Login(email, password)
        cookies = sign.login()
        sign.saveCookies()

        # Create chatbot using Hugging Face
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        chain = ConversationChain(llm=chatbot)
        return chain.run(input=prompt)
    except Exception as e:
        return f"Error: {e}"

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if prompt := st.chat_input(placeholder="Type your question here..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate assistant response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass)
                st.write(response)

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})