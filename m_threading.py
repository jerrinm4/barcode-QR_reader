import cv2
import pyzbar.pyzbar as pyzbar
import pyttsx3
import time
import os.path
import threading
from datetime import datetime
import csv
def git_push():
    from git import Repo
    try:
        repo = Repo(os.path.join(os.getcwd(),'.git'))
        repo.git.add('.')
        repo.index.commit(datetime.now().strftime('%d-%m-%Y'))
        origin = repo.remote(name='origin')
        origin.push('master')
    except:
        print("error on git push")

def create_folder():
    year=datetime.now().year
    month=datetime.now().strftime("%B")
    date=datetime.now().strftime('%d-%m-%Y')
    if not os.path.exists("./attentence"):
        os.mkdir("./attentence")
    if not os.path.exists(f"./attentence/{year}"):
        os.mkdir(f"./attentence/{year}")
    if not os.path.exists(f"./attentence/{year}/{month}/"):
        os.mkdir(f"./attentence/{year}/{month}/")
    if not os.path.exists(f"./attentence/{year}/{month}/{date}.csv"):
        with open(f"./attentence/{year}/{month}/{date}.csv", 'w', newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['ID','STATUS','DATE','TIME'])
    return f"./attentence/{year}/{month}/{date}.csv"

#fuction to add attentence
def add():
    global c_acc, c_status, w_key, last_time
    while True:
        if w_key:
            c_datetime=datetime.now()
            print(userData)
            with open(log_file, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([c_acc,c_status,c_datetime.strftime('%d/%m/%Y'),c_datetime.strftime('%H:%M:%S')])
            text_speech.say(f"you are {c_status.lower()}")
            text_speech.runAndWait()
            last_time=time.time()
            w_key=False
        elif stoper:
            break
        else:
            time.sleep(1)
#gobal variables
last_read = "null" #to store late read data
last_time = time.time() #to sore last in or out time
userData=dict() #to store the current status
w_key=stoper=False
c_acc=c_status=""
log_file=create_folder()
#git_push()
text_speech = pyttsx3.init()
text_speech.setProperty("rate", 125)
text_speech.setProperty('voice', 'english_rp+f4')
cap = cv2.VideoCapture(0)
t1=threading.Thread(target=add)
t1.start()
while True:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)
    if decodedObjects:
        data = ""
        #show rectangle on qr and barcode
        (x, y, w, h) = decodedObjects[0].rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (127,255,0), 2)
        if decodedObjects[0].data and decodedObjects[0].type=='CODE128' and not w_key:
            c_time=time.time()
            data = decodedObjects[0].data
            if last_read != data:
                read = str(data,'utf-8')
                if read in userData:
                        print("duplicate")
                        if userData[read] == "IN":
                            c_status,c_acc="OUT",read
                            userData[c_acc] = c_status
                            w_key=True
                            last_read = data
                        else:
                            c_status,c_acc="IN",read
                            userData[c_acc] = c_status
                            w_key=True
                            last_read = data
                else:
                    c_status,c_acc="IN",read
                    userData[c_acc] = c_status
                    w_key=True
                    last_read = data
            elif c_time-last_time>30 and last_read != 'null':
                last_read='null'
    cv2.imshow("Barcoder Reader", frame)
    if cv2.waitKey(1)==27:
        stoper=True
        t1.join()
        break