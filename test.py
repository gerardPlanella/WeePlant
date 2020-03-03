import datetime
import time
import base64
"""
a = datetime.datetime.now()

#time.sleep(3)

#b = datetime.datetime.now()

min = datetime.datetime.now() - datetime.timedelta(seconds=10)

now = datetime.datetime.now()
ttwfnm = now - min
if (now + ttwfnm < now): ttwfnm = ttwfnm.total_seconds()
else: ttwfnm = 0"""


import base64
with open("RPI/images/1.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(len(my_string))

import base64
with open("RPI/images/2.jpeg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(len(my_string))

import base64
with open("RPI/images/3.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(len(my_string))

#print(ttwfnm)
