import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# AB YHA PE HUM LOAD KRENGE ENVIROMENT VARIABLES KO
load_dotenv()

#NOW LET DESIGN THE PAGE CONFIRGURATION FOR THE STREAMLIT APP

st.set_page_config(
    page_title='Chat with Infinity-Loop',
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# NOW WE ARE GOING TO SET UP THE GOOGLE GEMINI PRO MODEL
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# NOW BASICALLY WE ARE GIVING THE FUCNTION TO TRANSLATE THE ROLES BETWEEN THE GEMINI AND STREAMLIT TERMINOLOGIES
def translate_role_for_streamlit(user_role):
    if user_role == 'modal':
        return "assistant"
    else:
        return user_role

# NOW WE ARE GOING TO APPLY THE CHAT_SESSION WHICH BASICALLY HOLDS OUT THE CHAT WHICH WE HAVE DONE TILL NOW

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# NOW DISPLAY THE CHATBOT TYPO OF THE LOGO ON THE PAGE

st.title("Welcome to the Infinity-Loop worlds")

# DISPLAY THE CHAT HISTORY
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# NOW WE ARE GOING TO CREATE THE USER MESSAGE FIELD

user_prompt = st.chat_input("Ask with Infinity for times!")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    #NOW WE ARE GOING TO SEND MESSAGE TO GEMINI AND GET RESPOND
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    #DISPLAY THE RESPOSE
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

