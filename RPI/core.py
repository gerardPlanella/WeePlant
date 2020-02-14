"""
Dependencies:
    socketio: https://python-socketio.readthedocs.io/en/latest/index.html
    psycopg:  https://www.psycopg.org/docs/install.html
"""

import socketio #https://python-socketio.readthedocs.io/en/latest/client.html
from robot import UR
#from gpiozero import OutputDevice

sio = socketio.Client()

@sio.on('newPotPython')
def on_message(data):
    #Move the robot and start the QR reading.
    print("Moving robot to add plant number: " + str(data))
    #TODO: Actually move the robot.
    #When the robot is in position get the QR.
    #TODO: Get the QR code from the robot.
    #TODO: Update the DB with the new plant
    #Return to the web the plant PK
    sio.emit('QRReading', 1)

@sio.event
def connect():
    print('connection established')
    
@sio.event
def disconnect():
    print('disconnected from server')

if __name__ == '__main__':
    

    
    sio.connect('http://localhost:2000')
    sio.wait()

    #ur = UR("192.168.1.106")
    #ur.moveJoints("before any acquisition", COMMON_SPEED, COMMON_ACC)
