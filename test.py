import datetime
import time
"""
a = datetime.datetime.now()

#time.sleep(3)

#b = datetime.datetime.now()

min = datetime.datetime.now() - datetime.timedelta(seconds=10)

now = datetime.datetime.now()
ttwfnm = now - min
if (now + ttwfnm < now): ttwfnm = ttwfnm.total_seconds()
else: ttwfnm = 0"""
#print(ttwfnm)

"""
import base64
with open("./RPI/images/1.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string)

import base64
with open("./RPI/images/2.jpeg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(len(my_string))

import base64
with open("./RPI/images/3.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(len(my_string))"""

#format: http://www.weeplant.es:80/?name=plant&pot_number=2
def decodeQR(code):
    code = code.split("?")[1]
    attributesAux = code.split("&")
    attributes = []

    for a in attributesAux:
        aux = a.split("=")

        try:
            aux[1] = int(aux[1])
        except:
            try:
                aux[1] = float(aux[1])
            except:
                """"""

        attributes.append([aux[0], aux[1]])

    return {
        "name": attributes[0][1],
        "pot_number": attributes[1][1],
        "since": "'" + str(datetime.datetime.now()) + "'",
        "watering_time": attributes[2][1],
        "moisture_threshold": attributes[3][1],
        "moisture_period": attributes[4][1],
        "photo_period": attributes[5][1]
    }

example = {
    "name": "deictics plant",
    "pot_number": 404,
    "since": "'" + str(datetime.datetime.now()) + "'",
    "watering_time": 10,
    "moisture_threshold": .2,
    "moisture_period": 60,
    "photo_period": 500
    }

print(decodeQR("http://www.weeplant.es:80/?name=deictics_plant&pot_number=404&watering_time=10&moisture_threshold=.2&moisture_period=60&photo_period=500"))
print(example)
