
import streamlit as st
from streamlit_chat import message
from hugchat import hugchat

st.set_page_config(page_title="NelsonBot - Your Pediatric Knowledge Assistant")

# Sidebar contents
with st.sidebar:
    st.title("👶📚 NelsonBot")
    st.markdown('''
    ## About
    NelsonBot provides quick, evidence-based answers from the **Nelson Textbook of Pediatrics**.
    Ideal for healthcare professionals seeking precise pediatric information.
    - Symptoms & Diagnoses
    - Treatment Protocols
    - Developmental Milestones
    - Preventive Care

    🚀 Powered by Hugging Face models.
    ''')

# Initialize session state for storing chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello! I'm NelsonBot. How can I assist you with pediatric knowledge?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ["Hi!"]

# Layout of input/response containers
input_container = st.container()
response_container = st.container()

# User input function
def get_text():
    input_text = st.text_input("Your query:", "", key="input")
    return input_text

# Generate response function
def generate_response(prompt):
    chatbot = hugchat.ChatBot()
    system_message = (
        "You are NelsonBot, an assistant providing evidence-based pediatric information "
        "sourced exclusively from the Nelson Textbook of Pediatrics. "
        "Cite detailed references in your responses."
    )
    response = chatbot.chat(f"{system_message} {prompt}")
    return response

# User input and AI response
with input_container:
    user_input = get_text()

with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(st.session_state["generated"][i], key=str(i))
