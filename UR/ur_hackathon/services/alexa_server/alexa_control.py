import asyncio
import json
import logging
import websockets
import socket
from time import sleep
import subprocess

commands = {
    "weather": 0,
    "traffic": 1,
    "flashbriefing": 2,
    "goodmorning": 3,
    "singasong": 4,
    "tellstory": 5
}

def handleLogin(username):
    with open('/tmp/loggedIn', 'r+') as f:
        f.write(username)
        f.truncate()

def handleAlexaCommand(command, value):
    base = 'bash /root/services/alexa_server/alexa.sh -d "Robot" '
    if (command == 'speak'):
        base = base + '-e speak:"' + value + '"'
    elif (command in commands):
        base = base + '-e ' + command
    elif (command == 'radio'):
        base = base + '-r "' + value + '"'
    elif (command == 'stop'):
        base = base + '-e pause'
    elif (command == 'vol'):
        base = base + '-e vol:' + value
    elif (command == 'login'):
        handleLogin(value)
        return
    else:
        base = base + '-e speak:"No entiendo lo que he recibido"'
        
    subprocess.call(base, shell=True)

logging.basicConfig()
sock_client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    while True:
        try:
            sock_client_server.bind(('0.0.0.0', 30102))
            sock_client_server.listen(64)
            break
        except:
            logging.error("Can not do the socket bind. Retrying...")
            sleep(0.5)

    logging.info('Waiting for Clients...')
    while (True):
        conn, addr = sock_client_server.accept()
        try:
            command = conn.recv(4096).decode()
            logging.info(command)
            action = json.loads(command)
            logging.info('Received: ' + command + ' from ' + str(addr))
            comanda = action['action'] 
            valor = action['value']
            handleAlexaCommand(comanda, valor)
            conn.send(('{"status":"0"}').encode())
            logging.info('Sending OK response') 
            conn.close()
        except Exception as err:
            conn.send(('{"status":"1", "reason":"' + str(err) + '"}').encode())
            logging.error('Sending KO response, reason: ' + str(err)) 
            conn.close()
    
except Exception as err:
    logging.info('Disconnecting due to exception ' + str(err))
    sock_client_server.close()
    
sock_client_server.close()
logging.info('Disconnecting...')
