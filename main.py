import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import pyttsx3
import time
import os.path
from datetime import datetime

def create_folder():
    year=datetime.now().year
    month=datetime.now().strftime("%B")
    if not os.path.exists("./attentence"):
        os.mkdir("./attentence")
    if not os.path.exists(f"./attentence/{year}"):
        os.mkdir(f"./attentence/{year}")
    if not os.path.exists(f"./attentence/{year}/{month}/"):
        os.mkdir(f"./attentence/{year}/{month}/")
    return f"./attentence/{year}/{month}/{datetime.now().strftime('%d-%m-%Y')}.txt"

#fuction to add attentence
def add(acc, y):
    global last_time
    userData[acc] = y
    print(userData)
    if y=="in":
        with open (log_file,'a') as log:
            log.write(f"ID: {acc}, Status: IN, DateTime: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        text_speech.say("you are in ")
        text_speech.runAndWait()
    else:
        with open(log_file, 'a') as log:
            log.write(f"ID: {acc}, Status: OUT, DateTime: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        text_speech.say("you are out ")
        text_speech.runAndWait()
    last_time=time.time()
#gobal variables
last_read = "null" #to store late read data
last_time = time.time() #to sore last in or out time
userData=dict() #to store the current status
log_file=create_folder()

text_speech = pyttsx3.init()
cap = cv2.VideoCapture(0)
while True:
    data = ""
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)
    if decodedObjects:
        if decodedObjects[0].data != "":
            data = decodedObjects[0].data
        if last_read != data:
            read = str(data,'utf-8')
            if read in userData:
                    print("duplicate")
                    if userData[read] == "in":
                        add(read,"out")
                        last_read = data
                    else:
                        add(read, 'in')
                        last_read = data
            else:
                add(read,"in")
                last_read = data
        elif time.time()-last_time>30 and last_read != 'null':
            print("wait")
            last_read='null'
        else:
            text_speech.say(f"wait {int(30-(time.time()-last_time))} seconds, to read again the same card ")
            text_speech.runAndWait()

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break