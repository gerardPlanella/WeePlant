#!/usr/bin/env python3

import socket
import sys
from PIL import Image, ImageFile
from io import BytesIO

HOST = '192.168.1.143' 
PORT = 8006

IMAGE = 1
HUMIDITY = 2
EXIT = 3

BURST_SIZE = 200

ImageFile.LOAD_TRUNCATED_IMAGES = True

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

conn.send(bytes([IMAGE]))
img_len = int(conn.recv(1024))

print("Img Length " + str(img_len) + "\n")

img_bytes = bytes()
start = 0
end = img_len


while(start != end):
    if int((end - start)/BURST_SIZE) > 0:
        bytes_read = conn.recv(BURST_SIZE)
    else:
        bytes_read = conn.recv((end-start)%BURST_SIZE)
    
    start += len(bytes_read)
    img_bytes += bytes_read
    print("Packet Read: " + str(start) + "/" + str(end) + "\n")

print("Image Read \n")

conn.send(bytes([1]))
print("OK sent\n")


img_stream = BytesIO(img_bytes)
img = Image.open(img_stream).convert("RGB")
img_stream.close()
img.save("test.jpeg")
print("Image saved\n")



conn.send(bytes([EXIT]))
print("EXIT SENT\n")


s.close()