import streamlit as st
import time
import os
import random

from getEmails import getEmailList
from extractTextFromHtml import extractTextFromHtml
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

from sendEmail import send_email
from helpers.getEmailBody import getEmailBody
from helpers.copyText import copyToClipboard
from helpers.checkCredentials import checkCredentials
from helpers.convertBytesToStr import convert_bytes_to_str
from helpers.getFlattenedList import getFlattenedList
from helpers.getFlattenedList import array_to_string


current_dir = os.path.dirname(__file__)
css_file_path = os.path.join(current_dir, 'style.css')
with open(css_file_path) as styles:
    st.markdown(f'<style>{styles.read()}</style>', unsafe_allow_html=True)

lm = None
chain = None
prompt = None

st.session_state["Answer"] = ""

if "selectedOption" not in st.session_state:
    st.session_state["selectedOption"] = None

if  "prevRadioValue" not in st.session_state:
    st.session_state["prevRadioValue"] = None

if  "textArea" not in st.session_state:
    st.session_state["textArea"] = None

if  "credentials" not in st.session_state:
    st.session_state["credentials"] = None

if  "loggedIn" not in st.session_state:
    st.session_state["loggedIn"] = None

with st.sidebar:
    with st.container():
        with st.popover("Email data", help="Please enter all values"):
            imapServer = st.text_input(label="IMAP", placeholder="imap.example.com")
            emailLogin = st.text_input(label="Login", placeholder="example@example.com")
            emailPassword = st.text_input(label="Password", type="password")

        if st.button("Sign out"):
            st.experimental_rerun()


# List of model options
models = ["Mistral", "Llama2", "GPT 3.5"]
[options, captions, preparedMessages] = getEmailList(imapServer, emailLogin, emailPassword)

st.session_state["credentials"] = [options, captions, preparedMessages]

if (checkCredentials(st.session_state["credentials"])):
    st.session_state["loggedIn"] = True
else:
    st.session_state["loggedIn"] = False

selectedModel = st.sidebar.selectbox("Choose a model", models)

emailFilter = st.sidebar.text_input(label="Filter your inbox here", placeholder="Чи буде у мене сьогодні зустріч?", key="search_input")
applyFilter = st.sidebar.button(label="Apply filter")

selectedEmail = st.sidebar.radio(
    "Inbox",
    options,
    format_func=lambda item: item[1],
    captions=captions
)

if selectedEmail != st.session_state["prevRadioValue"]:
    st.session_state["Answer"] = ""
    st.session_state["textArea"] = None
    st.session_state["selectedOption"] = None

        
st.title(":rainbow[Generative AI] email assistant")
st.write("**Selected model:**", selectedModel)
if 'GPT' in selectedModel:
    llm = ChatOpenAI(api_key=st.secrets["api_key"])
else:
    llm = Ollama(model="Llama2")

if not isinstance(selectedEmail, type(None)):
    st.write(selectedEmail[1])

if applyFilter:
    data = convert_bytes_to_str([options, captions, preparedMessages])
    preparedData = array_to_string(data)
    filteredEmails = llm.invoke("Серед цих електронних листів: ```" + 
                                preparedData + 
                                "``` потрібно знайти один який найкраще відповідає заданому фільтру: ```" + 
                                emailFilter +"```.")
    if selectedModel == "GPT 3.5":
        st.write(filteredEmails.content)
    else:
        st.write(filteredEmails)
        

newAnswer=""
with st.form("email"):
    st.session_state["prevRadioValue"] = selectedEmail
    if not isinstance(selectedEmail, type(None)):
        body = st.text_area("Content", extractTextFromHtml(getEmailBody(preparedMessages, selectedEmail)))

        submitted = st.form_submit_button('Summarize')
        if submitted:
            newAnswer = llm.invoke("Summarize this: ```" + body + "```")
            st.session_state["Answer"] = newAnswer
            st.session_state["selectedOption"] = "Summary"

        suggest = st.form_submit_button('Suggest an answer')
        if suggest:
            newAnswer = llm.invoke("Suggest an answer to this email: ```" + body + "```")
            st.session_state["Answer"] = newAnswer
            st.session_state["selectedOption"] = "Suggestion"

            
with st.container(border=True):
    newAnswer = st.session_state["Answer"]
    if newAnswer != "" and selectedModel == "GPT 3.5":
        st.session_state["textArea"] = [st.session_state["selectedOption"], newAnswer.content]
        newAnswer = newAnswer.content
    if newAnswer != "" and selectedModel == "Llama2":
        st.session_state["textArea"] = [st.session_state["selectedOption"], newAnswer]
    if newAnswer != "" and selectedModel == "Mistral":
        st.session_state["textArea"] = [st.session_state["selectedOption"], newAnswer]
    
    if st.session_state["textArea"] != None and st.session_state["selectedOption"] == "Suggestion":
        result = st.text_area(label=st.session_state["textArea"][0], value=st.session_state["textArea"][1])
        sent = st.button("Send")
        copied = st.button("Copy")

        if copied:
            copyToClipboard(result)
            st.success('Copied', icon="✅")
        
        if sent:
            recipient = selectedEmail[1].split()[-1].split('<')[1].split('>')[0]
            send_email(emailLogin, emailPassword, recipient, result)
            with st.spinner('Sending the message...'):
                time.sleep(1)
                st.balloons()

    if st.session_state["textArea"] != None and st.session_state["selectedOption"] == "Summary":
        result = st.text_area(label=st.session_state["textArea"][0], value=st.session_state["textArea"][1])
        copied = st.button("Copy")

        if copied:
            copyToClipboard(result)
            st.success('Copied', icon="✅")