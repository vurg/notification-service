# Notification Service

The Notification Service notifies users through Gmail API whenever they book or cancel appointments.

# Installation

Clone the latest code

```
git clone git@git.chalmers.se:courses/dit355/2023/student-teams/dit356-2023-04/notification-service.git
```

Create .env file in the src directory:
```
MQTT_USERNAME=ADD_YOUR_MQTT_USERNAME_HERE
MQTT_PASSWORD=ADD_YOUR_MQTT_PASSWORD_HERE
MQTT_URI=ADD_YOUR_MQTT_BROKER_URI_HERE
PERMITTED_EMAILS=ADD_LIST_OF_PERMITTED_EMAILS_TO_PREVENT_OUTGOING_SPAM
```

Enable GMAIL API from Google Cloud with mailing service gmail account.
Place `credentials.json` file from GMAIL API in the src directory.

# Run it locally to obtain token.json

In src directory, run:

```
python .\mqtt_handler.py
```
Create, cancel, or repost a booking to prompt OAuth 2.0 authorization in browser. Sign-in with mailing service gmail account. You will receive a `token.json`.

# Run it with Docker
In src directory, run:

```
docker build -t notification-service .

docker run -p 4000:80 notification-service
```

## Concluding Remarks
This service has several restrictions in place to prevent spamming by the Gmail Service Account. Remove these restrictions at your own risk.
