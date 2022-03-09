import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import pyttsx3
import time
import os.path
import json
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
def add(acc, s):
    global last_time
    userData[acc] = s
    c_datetime=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(userData)
    with open (log_file,'a') as log:
        log.write(f"ID: {acc}, Status: {s}, DateTime: {c_datetime}\n")
    text_speech.say(f"you are {s} ")
    text_speech.runAndWait()
    last_time=time.time()
#gobal variables
last_read = "null" #to store late read data
last_time = time.time() #to sore last in or out time
userData=dict() #to store the current status
log_file=create_folder()

text_speech = pyttsx3.init()
cap = cv2.VideoCapture(1)
while True:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)
    if decodedObjects:
        print(decodedObjects)
        data = ""
        c_time=time.time()
        if decodedObjects[0].data != "":
            data = decodedObjects[0].data
        if last_read != data:
            read = str(data,'utf-8')
            if read in userData:
                    print("duplicate")
                    if userData[read] == "IN":
                        add(read,"OUT")
                        last_read = data
                    else:
                        add(read, 'IN')
                        last_read = data
            else:
                add(read,"IN")
                last_read = data
        elif c_time-last_time>30 and last_read != 'null':
            last_read='null'
        else:
            print("wait")
            text_speech.say(f"wait {int(30-(time.time()-last_time))} seconds, to read again the same card ")
            text_speech.runAndWait()

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break