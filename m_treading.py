import cv2
import pyzbar.pyzbar as pyzbar
import pyttsx3
import time
import os.path
import threading
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
def add():
    global c_acc, c_status, key, last_time
    while True:
        if key:
            c_datetime=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print(userData)
            with open (log_file,'a') as log:
                log.write(f"ID: {c_acc}, Status: {c_status}, DateTime: {c_datetime}\n")
            text_speech.say(f"you are {c_status}")
            text_speech.runAndWait()
            last_time=time.time()
            key=False
        elif stoper:
            break
        else:
            time.sleep(2)
#gobal variables
last_read = "null" #to store late read data
last_time = time.time() #to sore last in or out time
userData=dict() #to store the current status
key=stoper=False
c_acc=c_status=""
log_file=create_folder()
text_speech = pyttsx3.init()
cap = cv2.VideoCapture(1)
t1=threading.Thread(target=add)
t1.start()
while True:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)
    if decodedObjects:
        data = ""
        if decodedObjects[0].data and decodedObjects[0].type=='CODE128' and not key:
            c_time=time.time()
            data = decodedObjects[0].data
            if last_read != data:
                print(data)
                read = str(data,'utf-8')
                if read in userData:
                        print("duplicate")
                        if userData[read] == "IN":
                            c_status,c_acc="OUT",read
                            userData[c_acc] = c_status
                            key=True
                            last_read = data
                        else:
                            c_status,c_acc="IN",read
                            userData[c_acc] = c_status
                            key=True
                            last_read = data
                else:
                    c_status,c_acc="IN",read
                    userData[c_acc] = c_status
                    key=True
                    last_read = data
            elif c_time-last_time>30 and last_read != 'null':
                last_read='null'
    cv2.imshow("Barcoder Reader", frame)
    if cv2.waitKey(1)==27:
        stoper=True
        break