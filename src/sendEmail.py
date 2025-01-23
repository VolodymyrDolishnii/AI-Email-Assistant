import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# def send_email(sender_email, sender_password, recipient_email, message, smtp_server, smtp_port):
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.login(sender_email, sender_password)
    
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = "Answer to " + recipient_email
#     msg.attach(MIMEText(message, 'plain'))
#     server.send_message(msg)
#     server.quit()

# def sendEmail(login, password, recipient, body):
#     SMTP_SERVER = "smtp.hostinger.com"
#     SMTP_PORT = 465

#     EMAIL_ADDRESS = login
#     EMAIL_PASSWORD = password

#     message = MIMEMultipart()
#     message['From'] = EMAIL_ADDRESS
#     message['To'] = recipient
#     message['Subject'] = "Answer"

#     message.attach(MIMEText(body, 'plain'))

#     server = smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT)
#     # server = smtplib.SMTP()
#     # server.connect(SMTP_SERVER, SMTP_PORT)
#     # server.starttls()
#     # st.code(server)
#     server.ehlo_or_helo_if_needed()
#     server.starttls()
#     server.ehlo()

#     server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

#     text = message.as_string()
#     st.code(text)
#     server.sendmail(EMAIL_ADDRESS, recipient, text)

#     server.quit()


def send_email(sender_email, sender_password, recipient_email, message):
    # server = smtplib.SMTP('smtp.hostinger.com', 587)
    server = smtplib.SMTP_SSL('smtp.zoho.eu', 465)
    server.login(sender_email, sender_password)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Answer to " + recipient_email
    msg.attach(MIMEText(message, 'plain'))
    server.send_message(msg)
    server.quit()
