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
import esp32
#from gpiozero import OutputDevice

sio = socketio.Client()
db = database.WeePlantDB()
#esp = esp32.ESP32()

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

    np = decodeQR(qr_content[0])
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

    return

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

#TODO: fer la funció a partir del string generat pel QR
def decodeQR(code):
    return {
        "name": "deictics plant",
        "pot_number": 404,
        "since": "'" + str(datetime.datetime.now()) + "'",
        "watering_time": 10,
        "moisture_threshold": .2,
        "moisture_period": 60,
        "photo_period": 500
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
    ttwfnm = now - min
    if (now + ttwfnm < now): ttwfnm = ttwfnm.total_seconds()
    else: ttwfnm = 0

    ret = {
        "time": ttwfnm,
        "plant": index,
        "type": type
    }

    return ret

def doMeasure(plant_id):
    print("moving UR to humidity tool")

    attempts = TOOL_ATTEMPTS

    value = esp.getHumidity()
    while (value == 0):
        if attempts == 0:
            print("moving UR to home")
            print("ERROR: unable to connect to the tool")
            return

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

    return

def takePicture(plant_id):
    print("moving UR to plant " + str(plant_id))

    time = datetime.datetime.now()
    esp.getImage("images/" + str(plant_id) + "_(" + str(time) + ").jpg")

    ## TODO:
    info = getPlantData()

    db.addImage(time, plant_id, open("images/" + str(plant_id) + "_(" + str(time) + ").jpg").read(), info["height"], info["colour"])

    return

def main():
    plantsInfo = requestTimings(db)
    if (len(plantsInfo) == 0): noplant = True

    while (noplant):
        sleep(1)

    lastMeasureInfo = requestTimestamps(db, plantsInfo)

    while (running):
        UR_home()

        nextMeasure = getTimeForEarliestMeasure()
        time.sleep(nextMeasure["time"])

        if (nextMeasure["type"] in "humidity"): doMeasure(nextMeasure["index"])
        elif (nextMeasure["type"] in "image"): takePicture(nextMeasure["index"])

    db.closeDB()

if __name__ == '__main__':

    sio.connect('http://localhost:2000')

    #main()
    sio.wait()

    #ur = UR("192.168.1.104")
    #ur.get_actual_joint_positions()
    #ur.moveJoints("Starting position", 0.1, 0.1)
