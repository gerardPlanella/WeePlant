# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2

# load the input image
image = cv2.imread("/home/adria/Documents/Assignatures/Projectes_en_Robotica/Python/WeePlant/RPI/frame.png")

# find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)

# loop over the detected barcodes
for barcode in barcodes:
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type
	if(barcodeType == "QRCODE"):
		print(barcodeData)