# The MQTT Handler is a modification of the HiveMQ MQTT documentation, see below:
#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import time
import os
from dotenv import load_dotenv
import paho.mqtt.client as paho
from paho import mqtt
from notification import main
from iCalendar import create_icalendar_file 


# load environment variables
load_dotenv()
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")
mqtt_uri = os.getenv("MQTT_URI")
permitted_emails = os.environ.get("PERMITTED_EMAILS")
permitted_emails_list = permitted_emails.split(',')

print(mqtt_username)
print(permitted_emails)
print(permitted_emails_list)

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    payload = msg.payload.decode("utf-8")

    try:
        data = json.loads(payload)

        name = data.get("patientName", "Sir/Madam")
        email = data.get("patientEmail")
        dentist_office = data.get("dentistName")
        appointment_date = data.get("date")
        appointment_date = appointment_date[0:10]
        appointment_time = data.get("time")
        appointment_message = data.get("message")
        appointment_status = data.get("status")

        if appointment_status == "BOOKED":
            print(f"A booking has been made. {name} ({email}) on {appointment_date} at {appointment_time}.")
        elif appointment_status == "CANCELED":
            print(f"A booking has been cancelled. {name} ({email}) on {appointment_date} at {appointment_time}.")
        else:
            message = "Invalid appointment status"

        if email in permitted_emails_list and (appointment_status == "BOOKED" or appointment_status == "CANCELED"):
            create_icalendar_file(name, email, dentist_office, appointment_date, appointment_time, appointment_message, appointment_status)
            main(name, email, dentist_office, appointment_date, appointment_time, appointment_message, appointment_status)
        else:
            print("Notification not processed.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="NotificationService", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(mqtt_username, mqtt_password)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(mqtt_uri, 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("booking", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish("notification/status", payload="alive", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()
