#Alarm Project main file
#Meant to be run on a RPI communicating with arduino.
import os#Importing Operating System to access environment varaiables
import sms#Import sms module
import serial#Import the serial module to read data from serial ports
import time#Importing time to use as a timer

class Alarm(object):
    """Alarm Class. Handles Arming/Disarming/Triggering"""
    def __init__(self):
        account_sid = os.environ['T_SID']#Retrieve SID from environment variable
        auth_token = os.environ['T_AUTH']#Retrieve auth token from environment variable
        self.client = sms.createClient(account_sid, auth_token)#Create a Twilio Client
        self.number = '+18327075273'
        #Initializing bools to keep track of current state
        self.triggered = False
        self.armed = False
        #Initializing timer to keep track of when the door was opened
        self.timer = None

    def AlarmTriggered(self):
        """Send an "Alarm Triggered" message to the number"""
        self.triggered = True
        #mid = sms.send_message(self.client, "Alarm trigged at " + sms.createTimeStamp(), self.number)
        #print("Trigger Message Sent. MID: " + str(mid))

    def AlarmArmed(self):
        """Send an "Alarm Set" message to the number"""
        self.armed = True
        #mid = sms.send_message(self.client, "Alarm armed at " + sms.createTimeStamp(), self.number)
        #print("Armed Message Sent. MID: " + str(mid))

    def AlarmDisarmed(self):
        """Send an "Alarm Disarmed" message to the number"""
        #Update state booleans
        self.triggered = False
        self.armed = False

        #mid = sms.send_message(self.client, "Alarm disarmed at " + sms.createTimeStamp(), self.number)
        #print("Disarm Message Sent. MID: " + str(mid))

    def startTimer(self):
        """Starts the timer if the alarm is armed"""
        if self.armed:
            self.timer = time.time()
    
    def checkTimer(self):
        """Check if the door has been opened for too long without being disarmed"""
        if self.armed:
            if (time.time() - self.timer) >= 30:#If it has been 30 seconds or more since the door was opened
                self.AlarmTriggered()
        else:
            self.timer = None#Reset the timer


def readBytes(ser):
    """Read bytes in the serial moniter"""
    ser_bytes = ser.readline()#Read a line of serial data
    decoded_bytes = ser_bytes[0:len(ser_bytes)].decode("utf-8").strip("\n").strip("\r").strip(" ")#Decode the bites using utf-8
    return decoded_bytes

def encodeMessage(msg):
    """Encode a message into bytes"""
    encoded_msg = msg.strip("\n").strip("\r").encode("utf-8")#Encode the message into bytes
    return encoded_msg

def mainloop(a, ser):
    """Main Data Input/Logic Loop"""
    #Code only runs if data is being recieved
    if ser.in_waiting:#If there is available data
        serialMsg = readBytes(ser)#Read the data
        ######################
        #DO - Door Opened    #
        #AS - Alarm Set      #
        #AD - Alarm Disarmed #
        #TS - Time Stamp     #
        ######################
        if serialMsg == "DO":
            a.startTimer()
        elif serialMsg == "AS":
            a.AlarmArmed()
        elif serialMsg == "AD":
            a.AlarmDisarmed()
        elif serialMsg == "TS":
            ts = sms.createTimeStamp()
            ser.write(encodeMessage(ts))
        else:
            print("Invalid Value Recieved: " + serialMsg)
    
    #Code Always Runs
    if a.timer:
        a.checkTimer()

def main():
    a = Alarm()#Create an alarm object
    ser = serial.Serial("COM5", 9600)#Create a serial object
    run  = True
    while run:
        mainloop(a, ser)

if __name__ == "__main__":
    main()