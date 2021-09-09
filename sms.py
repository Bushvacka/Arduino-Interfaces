#SMS Module for Alarm Project
from twilio.rest import Client#Import the twilio library
import time#Importing Time for timestamps

def createClient(sid, auth):
    """Returns a Twilio Client Object"""
    return Client(sid, auth)

def send_message(client, message, number):
    """Send a message to a number. Returns the message id"""
    mid = client.messages.create(
    body=message,
    from_='+15014564901',
    to=number
    )
    return mid#Return the message id

def createTimeStamp():
    """Returns a timestamp"""
    ts = time.strftime("%I:%M %p")#Timestamp Format: Hour:Minute AM/PM. Ex:07:20 PM
    #Strip a 0 from the front of a timestamp if it is there
    return ts

if __name__ == "__main__":
    print("Module Ran Directly. Redirecting to main.py")
    from alarm import main
    main()