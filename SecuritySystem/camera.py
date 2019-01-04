# This file handles taking a snapshot with a plugged
#   in webcam and sending the captured image via email
#    @authour Otto Holthe
#    1/3/2019
#

import numpy as np
import cv2
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime

sender_email = ""
receiver_email = ""
password = ""

# REQUIREMENT: Webcam plugged into Raspi
# Takes a single image and saves it as a png file named cap.png
def take_picture():
    cap = cv2.VideoCapture(0) # video capture source camera
    ret,frame = cap.read() # return a single frame in variable `frame`
    cv2.imwrite('cap.png', frame)
    cap.release()

# Sends the latest captured picture named 'cap.png' to the specified receiver_email
def send_picture():
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"

        image_data = open('cap.png', 'rb').read()
        message = MIMEMultipart()
        message['Subject'] = 'Security Camera Triggered'
        message['From'] = sender_email
        message['To'] = receiver_email

        text = MIMEText('The security system was triggered! Time {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M")))
        message.attach(text)
        image = MIMEImage(image_data, name='Capture.png')
        message.attach(image)

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(e)

# get credentials at program startup to avoid hardcoding password information
def setup_email():
    sender_email = input('Enter sender email: ')
    receiver_email = input('Enter receiver email: ')
    password = input('Enter password for sender email: ')

setup_email()
