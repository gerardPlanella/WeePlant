from firebase import firebase
import asyncio
import json
import logging
import websockets
import socket
import time

base = 'bash /root/services/alexa_server/alexa.sh -d "Robot" -e speak:'
logging.basicConfig()
firebase = firebase.FirebaseApplication('https://ur-hackathon.firebaseio.com/', None)

def returnActualUsername():
    with open('/tmp/loggedIn', 'r+') as f:
        text = f.read()
        if (text == ''):
            return 'No asignado'
        else:
            return text

def handleStatusBit(safety, robot):
    if (safety == '1028'):
        return 'Parada de proteccion, hasta que me habilites en la interficie no me movere'
    elif (safety == '1216'):
        return 'Aviso, paro de emergencia, repito, paro de emergencia'
    elif (safety == '1536'):
        return 'Error critico, por favor consulta la interficie para mas informacion'
    elif (safety == '1' and safety_status != safety):
        return 'Ya estoy de nuevo en modo normal'
    else:
        if (robot == '0'):
            return 'Apagando mis sistemas, hasta la proxima!'
        elif (robot == '1' and robot_status == '0'):
            return 'Buenas de nuevo, encendiendo sistemas'
        return ''
    return 'Estoy en un estado de desconocido.'

def updateFirebaseNotification(toStore):
    toStore['robot'] = '3'
    toStore['supervisor'] = returnActualUsername()
    toStore['date'] = int(round(time.time() * 1000))
    firebase.post('/notifications/unread', toStore)  
    firebase.put('/notifications', 'read_status', int(time.time()))

def updateRobotState(robot):
    toStore = {}
    if (robot == '0'):
        toStore['type'] = 1028
        toStore['message'] = 'Robot se ha apagado.'
        firebase.put('/status', 'on', 0)
    else:
        toStore['type'] = 1
        toStore['message'] = 'Robot se ha encendido.'
        firebase.put('/status', 'on', 1)
        time.sleep(10)
    updateFirebaseNotification(toStore)
        

def updateSafetyState(safety):
    toStore = {}
    toStore['type'] = int(safety)
    if (safety == '1028'):
        toStore['message'] = 'Parada de protección, inhabilitado hasta que se indique en la interfiere'
    elif (safety == '1216'):
        toStore['message'] = 'Paro de emergencia manual.'
    elif (safety == '1536'):
        toStore['message'] = 'Error critico, revisión del robot de inmediato.'
    elif (safety == '1' and safety_status != safety):
        toStore['message'] = 'Vuelta al estado normal'
    else:
        toStore['message'] = 'Estado de parada desconocido.'
    updateFirebaseNotification(toStore)
    
    
try:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    safety_status = '1'
    robot_status = '1'
    logging.info('Starting service...')
    conn.connect(('localhost', 30100)) 
    while (True):
        try:
            conn.send(('safety_status_bits').encode())
            safety = conn.recv(1024).decode()
            conn.send(('robot_status_bits').encode())
            robot = conn.recv(1024).decode()
            if (safety_status != safety or (robot_status != robot)):
                response = handleStatusBit(safety, robot)
                if response != '':
                    jsonResponse = {}
                    jsonResponse['action'] = 'speak'
                    jsonResponse['value'] = response
                    alexa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    alexa.connect(('localhost', 30102)) 
                    alexa.send((json.dumps(jsonResponse)).encode())
                    alexa.close()
                    logging.info('Changing status from ' + safety_status + ' to ' + safety)
                    logging.info('Sending to Alexa: ' + json.dumps(jsonResponse))
                    if (safety_status != safety):
                        updateSafetyState(safety)
                    else:
                        updateRobotState(robot)
                    safety_status = safety
                robot_status = robot
        except Exception as err:
            logging.error('Disconnecting due to exception ' + str(err))
            conn.close()
            time.sleep(2)
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(('localhost', 30100)) 
            
        time.sleep(1)
    
except Exception as err:
    logging.error('Disconnecting due to exception ' + str(err))
    conn.close()
    
conn.close()
logging.info('Disconnecting...')
