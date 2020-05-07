"""
Dependencies:
    socketio: https://python-socketio.readthedocs.io/en/latest/index.html
    psycopg:  https://www.psycopg.org/docs/install.html
"""

import socketio #https://python-socketio.readthedocs.io/en/latest/client.html
from robot import UR
import db as database
import time
import datetime
import fakeesp32
import plant
#from gpiozero import OutputDevice

MODE_NO_ESP32 = True

sio = socketio.Client()
db = database.WeePlantDB()

class ESP32:
    def __init__(self):
        self.a = 0.3
    def getHumidity(self):
        return self.a
esp = ESP32()
if (not MODE_NO_ESP32): esp = esp32.ESP32("192.168.1.148", 9008)


running = True
noplant = True
abort_plant = False

plantsInfo = []
lastMeasureInfo = []

TOOL_ATTEMPTS = 5

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

@sio.on('[CHANGE_CONFIG]')
def on_message(data):
    plantsInfo = requestTimings(db)

@sio.on('[ABORT_PLANT]')
def on_message(data):
    abort_plant = True

@sio.on('[ADD_PLANT]')
def on_message(data):
    print("Moving UR to empty pot")

    qr_content = []
    while (len(qr_content) == 0):
        qr_content = esp.getQR()

        if (abort_plant):
            print("moving UR to home")
            abort_plant = False
            return

    np = decodeQR(qr_content[0], data)
    nm = {
        "id": db.getLastPlantAdded(),
        "humidity": {
            "time": datetime.datetime.now() - datetime.timedelta(seconds=np["moisture_period"]),
            "value": 0
            },
        "watering": {
            "time": datetime.datetime.now() - datetime.timedelta(seconds=np["moisture_period"]),
            "value": 0
            },
        "image": datetime.datetime.now() - datetime.timedelta(seconds=np["photo_period"]),
    }

    plantsInfo.append(np)
    lastMeasureInfo.append(nm)

    db.addPlant(np["name"], np["pot_number"], np["since"], np["watering_time"], np["moisture_threshold"], np["moisture_period"], np["photo_period"])
    db.addWateringValue(nm["watering"]["time"], nm["id"], nm["watering"]["value"])
    db.addHumidityValue(nm["humidity"]["time"], nm["id"], nm["humidity"]["value"])

    noplant = False

    sio.emit('QRReading', db.getLastPK())
    return

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

#TODO: fer la funció a partir del string generat pel QR
"""Exemple: http://www.weeplant.es:80/?name=deictics_plant&watering_time=10&moisture_threshold=.2&moisture_period=60&photo_period=500"""
def decodeQR(code, potNum):
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
        "pot_number": potNum,
        "since": "'" + str(datetime.datetime.now()) + "'",
        "watering_time": attributes[1][1],
        "moisture_threshold": attributes[2][1],
        "moisture_period": attributes[3][1],
        "photo_period": attributes[4][1]
    }

def requestTimings(db):
    plants = db.getActualPlants()

    ret = []
    for plant in plants:
        ret.append(db.getPlant(plant))

    return ret

def requestTimestamps(db, plantsInfo):
    ret = []
    for p in plantsInfo:
        ret.append({
            "id": p["plant_ID"],
            "humidity": db.getHumidityLast(p["plant_ID"]),
            "watering": db.getWateringLast(p["plant_ID"]),
            "image": db.getImageLastTime(p["plant_ID"])
        })
    return ret

def getTimeForEarliestMeasure(lastMeasureInfo, plantsInfo):
    min = datetime.datetime.now()
    index = -1
    type = "null"

    for i in range(len(lastMeasureInfo)):
        measure = lastMeasureInfo[i]
        plant = plantsInfo[i]

        #TimeForNextMeasure
        tfnm = measure["humidity"]["time"] + datetime.timedelta(seconds=plant["moisture_period"])
        aux = measure["image"] + datetime.timedelta(seconds=plant["photo_period"])

        if (index < 0):
            index = measure["id"]

            if (tfnm < aux):
                min = tfnm
                type = "humidity"
            else:
                min = aux
                type = "image"

        else:
            if (min > tfnm):
                min = tfnm
                index = measure["id"]
                type = "humidity"

            if (min > aux):
                min = aux
                index = measure["id"]
                type = "image"

    #Time To Wait For Next Measure
    now = datetime.datetime.now()
    ttwfnm = min - now
    if (now + ttwfnm > now): ttwfnm = ttwfnm.total_seconds()
    else: ttwfnm = 0

    ret = {
        "time": ttwfnm,
        "plant": index,
        "type": type
    }

    return ret

def doMeasure(plant_id, plantsInfo):
    print("moving UR to humidity tool to check plant " + str(plant_id))

    attempts = TOOL_ATTEMPTS

    value = esp.getHumidity()
    while (value == 0):
        if attempts == 0:
            print("moving UR to home")
            print("ERROR: unable to connect to the tool")
            return False

        attempts -= 1
        print("UR tries to connect again")

        value = esp.getHumidity()

    print("move UR from tool to plant " + str(plant_id))
    value = esp.getHumidity()

    print("UR leaves the tool")
    db.addHumidityMeasure(datetime.datetime.now(), plant_id, value)

    plantInfo = plantsInfo[0]
    for plant in plantsInfo:
        if plant["plant_ID"] == plant_id:
            plantInfo = plant
            break

    if (plantInfo["moisture_threshold"] < value):
        print("UR to watering tool")
        print("UR to plant " + str(plant_id))
        print("turn on the pump")
        print("UR leave the tool")

    return True

def getPlantData(path):
    plant = Plant(image_path=path, write_image_output=True, result_path= "./out_plant_debugg/plant_2_info.json", write_result=True)
    plant.calculate()

    ret = {"height": 0, "colour": 0}

    if plant.isFramed() is True:
        height = plant.getHeight()

        if (not (height is not False)):
            ret["height"] = -1
            return ret
        else:
            ret["height"] = height

        ret["colour"] = [plant.getColourHistogram()[0]["value"], plant.getColourHistogram()[1]["value"], plant.getColourHistogram()[2]["value"]]
    return ret

def takePicture(plant_id):
    print("moving UR to plant " + str(plant_id))

    time = datetime.datetime.now()
    esp.getImage("images/" + str(plant_id) + "_(" + str(time) + ").jpg")

    ## TODO:
    info = getPlantData("images/" + str(plant_id) + "_(" + str(time) + ").jpg")

    aux = []
    for i in range(3):
        aux.append([])
        for j in range(255): aux[i].append(j)

    db.addImage(time, plant_id, open("images/" + str(plant_id) + "_(" + str(time) + ").jpg").read(), info["height"], info["colour"])

    return

def UR_home():
    print("UR going to home position")

def main():
    plantsInfo = requestTimings(db)
    if (len(plantsInfo) == 0): noplant = True
    else: noplant = False

    while (noplant):
        time.sleep(1)

    while (running):
        lastMeasureInfo = requestTimestamps(db, plantsInfo)

        UR_home()

        nextMeasure = getTimeForEarliestMeasure(lastMeasureInfo, plantsInfo)

        print("Waiting until: " + str(nextMeasure))
        if (nextMeasure["time"] > 0): time.sleep(nextMeasure["time"])

        OK = True
        if (nextMeasure["type"] in "humidity"): doMeasure(nextMeasure["plant"], plantsInfo)
        elif (nextMeasure["type"] in "image"): takePicture(nextMeasure["plant"])

        #print(nextMeasure)
        print("\n" + "-"*80 + "\n")
        #sio.wait()

    db.closeDB()

if __name__ == '__main__':

    #sio.connect('http://www.weeplant.es:80')

    main()

    """
    if esp.connect() is True:

        while True:
            print("TAKE PICTURE CALL")
            takePicture(1)

            time.sleep(3)
    else:
        print("Not connected.")

    """

    sio.wait()

    #ur = UR("192.168.1.104")
    #ur.get_actual_joint_positions()
    #ur.moveJoints("Starting position", 0.1, 0.1)
