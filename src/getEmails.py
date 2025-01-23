import imaplib
import email
from email.header import decode_header
import streamlit as st
import pandas as pd
import base64

from helpers.checkIMAPServer import checkIMAPServer
from helpers.getIMAPServerPort import getIMAPServerPort

# IMAP_SERVER = 'imap.hostinger.com'
# IMAP_PORT = 993
# EMAIL_ACCOUNT = 'kauzbot@nikcode.net'
# PASSWORD = 'euY5a3L3Ebv1zdTnZe11+'

# ZOHO
# eEL+8_R84C2Z$%6
# volodymyr.dolishnii@zohomail.eu
# imap.zoho.eu

def get_email_body(message):
    if message.is_multipart():
        # Iterate over email parts
        for part in message.walk():
            # Extract content type of email
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Look for plain text or HTML parts
            if "attachment" not in content_disposition and content_type in ["text/plain", "text/html"]:
                # Get email body
                email_body = part.get_payload(decode=True).decode()
                return email_body
    else:
        # If the message is not multipart, get the payload directly
        return message.get_payload(decode=True).decode()
    
def validSubject(subject):
    if len(subject) == 0:
        return "There is no subject"
    else:
        return subject

def getEmailList(IMAP_SERVER, EMAIL_ACCOUNT, PASSWORD):
    if len(IMAP_SERVER) == 0 or len(EMAIL_ACCOUNT) == 0 or len(PASSWORD) == 0:
        return ["", "", ""]
    
    if not checkIMAPServer(IMAP_SERVER):
        st.sidebar.error("Wrong IMAP server")
        return ["", "", ""]
    
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, getIMAPServerPort(IMAP_SERVER))
    
    try:
        mail.login(EMAIL_ACCOUNT, PASSWORD)
    except imaplib.IMAP4.error as e:
        st.sidebar.error("Please check your email credentials!")
        return ["", "", ""]
    
    mail.select('inbox')
    status, messages = mail.search(None, 'ALL')
    messages = messages[0].split()
    list = []

    for num in messages:
        result, data = mail.fetch(num, '(RFC822)')

        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        if ('=?' in email_message['From']):
            stripped_text = email_message['From'].strip()
            encoding, encoded_text = stripped_text.split('?B?')
            decoded_text = base64.b64decode(encoded_text).decode(encoding)
            item = [
                [num, "**From:** " + decoded_text + ' ' + email_message["From"].split('=')[len(email_message["From"].split('=')) - 1]],
                "Subject: " + validSubject(decode_header(email_message['Subject'])[0][0]), 
                [num, get_email_body(email_message)]
            ]
        else:
            item = [
                # [num, "**From:** " + "Володимир Долішній" + email_message['From'].split('=')[len(email_message['From'].split('=')) - 1]],
                # [num, "**From:** " + 'Володимир Долішній'],
                [num, "**From:** " + email_message['From']],
                "Subject: " + validSubject(decode_header(email_message['Subject'])[0][0]), 
                [num, get_email_body(email_message)]
            ]
        list.append(item)
    
    options = [item[0] for item in list]
    captions = [item[1] for item in list]
    preparedMessages = [item[2] for item in list]
    
    return [options, captions, preparedMessages]
