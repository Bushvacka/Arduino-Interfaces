#Logs data from Arduino's Serial Moniter
import serial#Importing serial to read data from the arduino
import time#Importing time for timing events
import os#Importing os to deal with file/path stuff
import _thread as thread#Importing thread to take user input while running code


def readBytes():
    """Read bytes in the serial moniter"""
    ser_bytes = ser.readline()#Read a line of serial data
    decoded_bytes = ser_bytes[0:len(ser_bytes)].decode("utf-8").strip("\n").strip("\r")#Decode the bites using utf-8
    return decoded_bytes

def createLogFile():
    """Create a log text file"""
    idCounter = 1
    while idCounter < 100:
        path = "E:\Log Files\Backdoor Logs\BDL" + str(idCounter) + ".txt"#Create a path with new id
        if os.path.exists(path):#If the file already exists
            idCounter += 1#Increment the counter
        else:
            f = open(path, "w")#Creates the file in writing mode
            return f#Return the file
    print("Too many log files. Please delete some.")
    return None

def input_thread(user_input):
    """Takes user input while other code runs"""
    input()#Code stops here until user inputs something
    user_input.append(None)

def determineLogEntry(BD, serialMsg):
    """Determine if a log entry needs to be made"""
    if serialMsg != "Timeout" and serialMsg != "END":#If a timeout didnt occur
        try:
            serialMsg = int(serialMsg)
        except:
            print("Non-integer value given to recorder: " + serialMsg)
            return BD, False
        if not BD:#If this is the first cycle
            BD["state"] = "Open" if serialMsg > 96 else "Closed"
            BD["time"] = time.time()
            if BD["state"] == "Open":
                return BD, True
        else:#If this isn't the first cycle
            newState = "Open" if serialMsg > 96 else "Closed"
            if (newState == "Open") and (BD["state"] == "Closed") and (time.time() - BD["time"] >= 10):
                BD["state"] = newState
                BD["time"] = time.time()
                return BD, True
            elif (newState == "Closed") and (BD["state"] == "Open"):
                BD["state"] = newState
    return BD, False


ser = serial.Serial("COM6", 9600)#Create a serial object

while True:#Infinite Loop
    serialMsg = ""#Resets the serial message
    command  = input("Command:")#Take a command from the user

    if command == "Backdoor Start Recording":
        BD = {}#Backdoor: Saves Time & State
        print("Beginning to store backdoor events to log file. Press [Enter] to stop recording.")
        user_input = []#Create a variable to determine if the user wants to exit the loop
        thread.start_new_thread(input_thread, (user_input))#Create an input thread to check for user input
        byte_command = "Backdoor".encode("utf-8")#Encode the backdoor power on message
        f = createLogFile()#Open a new log file in write mode
        while not user_input:
            ser.write(byte_command)
            serialMsg = ""
            while serialMsg != "END":
                if ser.in_waiting:#If there is data waiting
                    serialMsg = readBytes()#Save the data
                    BD, log_bool = determineLogEntry(BD, serialMsg)
                    if serialMsg != "END":
                        print(serialMsg, end  =" ")
                        print(BD, end  = " ")
                        print(log_bool)
                    if(log_bool):#If a log entry need to be made
                        print("Creating Entry")
                        entry = time.strftime("%H:%M:%S") + ": Door Opened.\n"
                        f.write(entry)
        f.close()
    else:
        byte_command = command.encode("utf-8")#Encode the string into bytes
        ser.write(byte_command)#Write the command to the serial port
        while serialMsg != "END":
            if ser.in_waiting:#If there is data waiting
                serialMsg = readBytes()
                if serialMsg != "END":
                    print(serialMsg)