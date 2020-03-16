import asyncio
import json
import logging
import websockets
import socket
from time import sleep
import traceback

logging.basicConfig()

def handleCommand(command, conn):
    if (command['command'] == 'action'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            s.connect(('localhost', 30102)) 
            action = {}
            action['action'] = 'speak'
            toSpeak = 'El usuario ' + command['user'] + ' des del panel de control'
            if (command['action'] == 'stop'):
                action['value'] = toSpeak + 'ha parado el robot. Motivo, ' + command['value']
            elif (command['action'] == 'play'):
                action['value'] = toSpeak + 'ha continuado con el programa.'
            elif (command['action'] == 'pause'):
                action['value'] = toSpeak + 'ha pausado el robot. Motivo, ' + command['value']
            elif (command['action'] == 'load'):
                action['value'] = toSpeak + 'ha cargado el programa al robot.'
            else:
                action['value'] = toSpeak + ' dice, ' + command['value']
            s.send(str(json.dumps(action)).encode())
        if (command['action'] == 'load'):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
                s.connect(('localhost', 30002)) 
                s.send(('movej([-1.58, -1.06, -1.2, -1.54, 1.59, 0.775], a=1.4, v=1.05, t=0, r=0)\n').encode())
                sleep(5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            s.connect(('localhost', 29999)) 
            if (command['action'] == 'load'):
                s.send(('load ' + command['value'] + '.urp\n').encode())
                s.send(('play\n').encode())
            else:
                s.send(str(command['action'] + '\n').encode())
    else:
        conn.send(str(command['command']).encode())
        return conn.recv(1024).decode()

async def handler(websocket, path):
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            s.connect(('localhost', 30100)) 
            jsonResponse = {}
            logging.info('Started service for client')
            while True:
                command = await websocket.recv()
                received = json.loads(command)
                response = handleCommand(received, s)
                jsonResponse['command'] = received['command']
                jsonResponse['value'] = response
                await websocket.send(json.dumps(jsonResponse))
    except Exception as err: 
        await websocket.send("Failed with error %s" %(err))
        logging.error("Client failed with error %s" %(err))
        logging.error(traceback.format_exc())

while True:
    try: 
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(handler, '0.0.0.0', 30101))
        asyncio.get_event_loop().run_forever()
    except Exception as err: 
        logging.error("Failed with error %s" %(err))
        logging.error(traceback.format_exc())
    sleep(1)
