#!/usr/bin/env python3

# sudo pip3 install pyzbar
# sudo apt-get install libzbar0

######################################################
import socket
import sys
import os
from PIL import Image, ImageFile
from io import BytesIO
from pyzbar import pyzbar
import cv2

DEBUG = True

OK = 1
KO = 0

IMAGE = 1
HUMIDITY = 2
EXIT = 3

BURST_SIZE = 200

ImageFile.LOAD_TRUNCATED_IMAGES = True

QR_TMP = "/tmp/qr_tmp.jpeg"

HOST = '192.168.1.143' 
PORT = 8003

class ESP32():
    __slots__ = ('sock', 'conn', 'addr', 'port', 'connected')

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.connected = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if DEBUG: print('# Socket created')

        # Create socket on port
        try:
            self.sock.bind((self.addr, self.port))
        except socket.error as msg:
            print('# Bind failed. ')
            return False
        
        if DEBUG: print('# Socket created')

        # Start listening on socket
        self.sock.listen(10)
        if DEBUG: print('# Socket now listening')
        

        # Wait for ESP32 client
        self.conn, self.addr = self.sock.accept()
        if DEBUG: print('# Connected to ' + self.addr[0] + ':' + str(self.addr[1]))

        self.connected = True

        return True
    
    def disconnect(self):
        self.conn.send(bytes([EXIT]))
        if DEBUG: print("EXIT SENT")
        self.sock.close()
        self.connected = False
    
    def getHumidity(self):
        humidity = 0

        if self.connected is True:
            self.conn.send(bytes([HUMIDITY]))
            humidity = float(self.conn.recv(1024))
            if DEBUG: print("Humidity Received " + str(humidity) + "\n")
            self.conn.send(bytes([OK]))
            if DEBUG: print("OK sent\n")
        return humidity
    
    def grabImage(self):
        img_bytes = bytes()
        start = 0
        end = 0

        if self.connected is True:
            self.conn.send(bytes([IMAGE]))
            img_len = int(self.conn.recv(1024))
            if DEBUG: print("Img Length " + str(img_len) + "\n")
            end = img_len

            while start != end :
                if int((end - start)/BURST_SIZE) > 0 : 
                    bytes_read = self.conn.recv(BURST_SIZE)
                else:
                    bytes_read = self.conn.recv((end - start)%BURST_SIZE)
                
                start += len(bytes_read)
                img_bytes += bytes_read
                #if DEBUG: print("Packet Read: " + str(start) + "/" + str(end) + "\n")

            if DEBUG: print("Image Read \n")
            self.conn.send(bytes([OK]))
            if DEBUG: print("OK sent\n")

            image_stream = BytesIO(img_bytes)
            image = Image.open(image_stream).convert("RGB")
            image_stream.close()

            return image
            

            
        return None

    def getImage(self, imagePath):
        image = self.grabImage()
        
        if image is not None:
            image.save(imagePath)
            if DEBUG: print("Image saved\n")
            return True
        return False

    def getQR(self):
        image = self.grabImage()
        qr_list = []

        if image is not None:
            image.save(QR_TMP)
            img = image = cv2.imread(QR_TMP)
            # find the barcodes in the image and decode each of the barcodes
            barcodes = pyzbar.decode(img)
            if DEBUG: print ("Barcodes Decoded \n")
            # loop over the detected barcodes
            for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                if(barcodeType == "QRCODE"):
                    qr_list.append(barcodeData)
                    if DEBUG: print("Barcode #" + i + ": " + str(barcodeData) + "\n")
        
            os.remove(QR_TMP)

        return qr_list

    
        

if __name__ == "__main__":
    
    esp32 = ESP32(HOST, PORT)
    if esp32.connect() is True:
        qr_list = esp32.getQR()

        if len(qr_list) > 0:
            for qr in qr_list:
                print(str(qr))

        esp32.getImage("test.jpeg")   

        esp32.disconnect() 





