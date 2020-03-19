from firebase import firebase
import time
import datetime
import logging
import socket
import traceback

logging.basicConfig()

firebase = firebase.FirebaseApplication('https://ur-hackathon.firebaseio.com/', None)

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn: 
            conn.connect(('localhost', 30100))
            toStore = {}
            while True:
                conn.send('actual_current'.encode())
                toStore['amp'] = conn.recv(1024).decode()
                conn.send('joint_temperatures'.encode())
                toStore['temp'] = conn.recv(1024).decode()
                conn.send('actual_joint_voltage'.encode())
                toStore['voltage'] = conn.recv(1024).decode()
                
                data = datetime.datetime.now()
                month = data.strftime("%m")
                day = data.strftime("%d")
                hour = data.strftime("%H")
                minute = data.strftime("%M")
                
                firebase.put('/events/' + month + '/' + day + '/' + hour, minute, toStore)  
                second = datetime.datetime.now().strftime("%S")
                time.sleep(60 - int(second))
    except Exception as err: 
        logging.error("Failed with error %s" %(err))
        logging.error(traceback.format_exc())
    time.sleep(5)

