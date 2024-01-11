# Notification service uses Gmail API to compose messages and send to users
# Credits to Redouane Niboucha and Abdeladim Fadheli for the attachment, build message, and send message methods used in this file.
# Source: https://thepythoncode.com/article/use-gmail-api-in-python

import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

def build_message(destination, obj, body, attachments=[]):
    if not attachments: # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = "toothcheck.app@gmail.com"
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = "toothcheck.app@gmail.com"
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, obj, body, attachments)
    ).execute()

def create_appointment_message(name, dentist_office, appointment_date, appointment_time, appointment_message, appointment_status):
    # Create the message string based on appointment status
    if appointment_status == "BOOKED":
        message = f"Hello {name},\n\nYour dentist appointment is scheduled for {appointment_date} at {appointment_time} at {dentist_office}. \n\nReason: {appointment_message} \n\nThanks,\nToothCheck App"
    elif appointment_status == "CANCELED":
        message = f"Hello {name},\n\nYour dentist appointment scheduled for {appointment_date} at {appointment_time} has been canceled at {dentist_office}. \n\nThanks,\nToothCheck App"
    else:
        message = "Invalid appointment status"

    return message

def main(name, email, dentist_office, appointment_date, appointment_time, appointment_message, appointment_status):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)

    # create message
    message = create_appointment_message(name, dentist_office, appointment_date, appointment_time, appointment_message, appointment_status) 

    # send email
    if appointment_status == "BOOKED":
        send_message(service, email, "Appointment Confirmation", message, ["appointment.ics"])
    elif appointment_status == "CANCELED":
       send_message(service, email, "Appointment Cancelled", message, ["appointment.ics"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()