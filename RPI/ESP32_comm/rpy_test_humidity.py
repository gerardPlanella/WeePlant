#!/usr/bin/env python3

import socket
import sys

HOST = '192.168.1.40' 
PORT = 8006


IMAGE = 1
HUMIDITY = 2
EXIT = 3




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('# Socket created')

# Create socket on port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('# Bind failed. ')
    sys.exit()

print('# Socket bind complete')

# Start listening on socket
s.listen(10)
print('# Socket now listening')

# Wait for client
conn, addr = s.accept()
print('# Connected to ' + addr[0] + ':' + str(addr[1]))

# Receive data from client

conn.send(bytes([HUMIDITY]))   
humidity = (conn.recv(1024))
print(str(humidity) + "Read val")
humidity = float(humidity)
print("Humidity Received " + str(humidity) + "\n") 
conn.send(bytes([1]))
print("OK sent\n")

conn.send(bytes([EXIT]))
print("EXIT SENT")

s.close()
            
            

