import cv2
import pyzbar.pyzbar as pyzbar
import time
import os.path
import threading
from datetime import datetime
import csv
from flask import Flask, render_template, Response, jsonify
from flask_qrcode import QRcode

# # gpio
# import RPi.GPIO as GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# bz=27
# GPIO.setup(bz,GPIO.OUT)

last_push = ""
def git_push():
    from git import Repo
    global last_push
    last_push = time.time()
    try:
        repo = Repo(os.path.join(os.getcwd(), '.git'))
        repo.git.add('.')
        repo.index.commit(datetime.now().strftime('%d-%m-%Y'))
        origin = repo.remote(name='origin')
        re = origin.push('master')
        print("git push done", re)
    except:
        print("error on git push")


def create_folder():
    year = datetime.now().year
    month = datetime.now().strftime("%B")
    date = datetime.now().strftime('%d-%m-%Y')
    if not os.path.exists("./attentence"):
        os.mkdir("./attentence")
    if not os.path.exists(f"./attentence/{year}"):
        os.mkdir(f"./attentence/{year}")
    if not os.path.exists(f"./attentence/{year}/{month}/"):
        os.mkdir(f"./attentence/{year}/{month}/")
    if not os.path.exists(f"./attentence/{year}/{month}/{date}.csv"):
        with open(f"./attentence/{year}/{month}/{date}.csv", 'w', newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['ADNo', 'NAME', 'BATCH', 'STATUS', 'DATE', 'TIME'])
    return f"/attentence/{year}/{month}/{date}.csv"



def addatt():
    global c_acc, c_status, w_key, last_time, read_json
    while True:
        if w_key:
            w_key = False 
            c_datetime = datetime.now()
            read_json={'name': c_acc[0],'adno': c_acc[2],'batch': c_acc[1],'status':c_status,'time': c_datetime.strftime('%H:%M:%S')}
            # GPIO.output(bz,GPIO.HIGH)
            print(userData, end='\r')
            with open(log_file, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([c_acc[2], c_acc[0], c_acc[1], c_status, c_datetime.strftime('%d/%m/%Y'),
                                    c_datetime.strftime('%H:%M:%S')])
            last_time = time.time()
            time.sleep(.5)
            print("beep")
            # GPIO.output(bz,GPIO.LOW)

        elif stoper:
            break
        elif time.time() - last_push > 180:
            git_push()
        else:
            time.sleep(.5)


# gobal variables
read_json= {}
last_read = "null"  # to store late read data
last_time = time.time()  # to sore last in or out time
userData = dict()  # to store the current status
w_key = stoper = False
c_acc = c_status = ""
log_file = create_folder()
git_push()
cap = cv2.VideoCapture(0)
t1 = threading.Thread(target=addatt)
t1.start()
def scan():
    global w_key, last_read,c_status, c_acc, read_json
    while True:
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        if decodedObjects:
            data = ""
            adNo = -1
            # show rectangle on qr and barcode
            (x, y, w, h) = decodedObjects[0].rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (127, 255, 0), 2)
            if decodedObjects[0].data and decodedObjects[0].type == 'QRCODE' and not w_key:
                c_time = time.time()
                data = decodedObjects[0].data
                if last_read != data:
                    read = str(data, 'utf-8').split("#")
                    if len(read) == 3:
                        adNo = read[2]
                    if adNo in userData:
                        if userData[adNo] == "IN":
                            c_status, c_acc = "OUT", read
                        elif userData[adNo] == "OUT":
                            c_status, c_acc = "IN", read
                        userData[adNo] = c_status
                        w_key = True
                        last_read = data
                    else:
                        c_status, c_acc = "IN", read
                        userData[adNo] = c_status
                        w_key = True
                        last_read = data
                elif c_time - last_time > 15 and last_read != 'null':
                    last_read = 'null'
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')





app = Flask(__name__)
QRcode(app)
@app.route('/')
def index():
    return render_template('index.html',qr="https://github.com/RANDDLABS/Attendance-Log/tree/master"+log_file)

@app.route('/video_feed')
def video_feed():
    return Response(scan(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/c_id')
def current_id():
    return jsonify(read_json)


if __name__ == "__main__":
    app.run(debug=True)
    stoper = True
    t1.join()