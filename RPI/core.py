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
<<<<<<< HEAD
#import fakeesp32
import esp32
import plant
#from gpiozero import OutputDevice
=======
import esp32 
import signal
import sys
>>>>>>> 809604bd49c7c6f6cc63d49463138cf133a34afe

import plant
from sim_robot import UR_SIM

MODE_ESP32 = True

TOOL_ATTEMPTS = 5

add_plant_request = False
action_in_progress = False

running = True
noplant = True
abort_plant = False

plantsInfo = []
lastMeasureInfo = []

UR_SIM_IP = "25.120.137.245"
UR_SIM_PORT = 25852

sio = socketio.Client()
db = database.WeePlantDB()

#ur_sim = UR_SIM(UR_SIM_IP, UR_SIM_PORT)

if (MODE_ESP32):
    esp = esp32.ESP32("192.168.1.36", 8018)
    if(not esp.connect()):
        print("Connection Error")
    else:
        print("Connection Established")



def signal_handler(sig, frame):
    print('Goodbye!')
    if esp is not None:
        esp.disconnect()
    if sio is not None:
        sio.disconnect()
    
    sys.exit(0)

@sio.on('newPotPython')
def on_message(data):
    #Move the robot and start the QR reading.
    #ur_sim.move()
    print("Moving robot to add plant number: " + str(data))
    #TODO: Actually move the robot.
    #When the robot is in position get the QR.
    #TODO: Get the QR code from the robot.
    #TODO: Update the DB with the new plant
    #Return to the web the plant PK
    sio.emit('QRReading', 1)

@sio.on('[CHANGE_CONFIG]')
def on_message(data):
    global plantsInfo
    plantsInfo = requestTimings(db)

@sio.on('[ABORT_PLANT]')
def on_message(data):
    global abort_plant
    abort_plant = True

@sio.on('[ADD_PLANT]')
def on_message(data):
    global action_in_progress
    global add_plant_request
    global noplant
    global plantsInfo

    if(noplant):
        add_plant()
        
        noplant = False
    else:
        add_plant_request = True
    return

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

#TODO: fer la funció a partir del string generat pel QR
"""Exemple: http://www.weeplant.es:80/?name=deictics_plant&watering_time=10&moisture_threshold=.2&moisture_period=60&photo_period=500"""

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
                pass
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
    pmin = datetime.datetime.now()
    index = -1
    ptype = "null"

    for i in range(len(lastMeasureInfo)):
        measure = lastMeasureInfo[i]
        plant = plantsInfo[i]

        #TimeForNextMeasure
        tfnm = measure["humidity"]["time"] + datetime.timedelta(seconds=plant["moisture_period"])
        aux = measure["image"] + datetime.timedelta(seconds=plant["photo_period"])

        if (index < 0):
            index = measure["id"]

            if (tfnm < aux):
                pmin = tfnm
                ptype = "humidity"
            else:
                pmin = aux
                ptype = "image"

        else:
            if (pmin > tfnm):
                pmin = tfnm
                index = measure["id"]
                ptype = "humidity"

            if (pmin > aux):
                pmin = aux
                index = measure["id"]
                ptype = "image"

    #Time To Wait For Next Measure
    now = datetime.datetime.now()
    ttwfnm = pmin - now
    if (now + ttwfnm > now): ttwfnm = ttwfnm.total_seconds()
    else: ttwfnm = 0

    ret = {
        "time": ttwfnm,
        "plant": index,
        "type": ptype
    }

    return ret

def doMeasure(plant_id, plantsInfo):
    global TOOL_ATTEMPTS

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
    db.addHumidityValue(datetime.datetime.now(), plant_id, value)

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
    global esp
    print("moving UR to plant " + str(plant_id))

    color1 = []
    color2 = []
    color3 = []
    for j in range (3):
        color1.append([])
        color2.append([])
        color3.append([])
        for i in range(255):
            color1[j].append(i % 255)
            color2[j].append((255 - i) % 255)
            color3[j].append(int((255*(i+.1)**(-1))%255))

    colour = [color1, color2, color3]
    time = datetime.datetime.now()

    path = "images/" + str(plant_id) + "_(" + str(time) + ").jpg"

    esp.getImage(path)

    #info = getPlantData("images/" + str(plant_id) + "_(" + str(time) + ").jpg")

    db.addImage(time, plant_id, open(path, 'rb').read(), 70, colour)

    #db.addImage(time, plant_id, open("images/" + str(plant_id) + "_(" + str(time) + ").jpg",'rb').read(),5,[233,222,222])

    '''
    aux = []
    for i in range(3):
        aux.append([])
        for j in range(255): aux[i].append(j)

    if (plant_id != 2): db.addImage(time, plant_id, open("images/" + str(plant_id) + ".jpg",'rb').read(),5, aux)
    else: db.addImage(time, plant_id, open("images/" + str(plant_id) + ".jpeg",'rb').read(),5, aux)
    '''

    #db.addImage(time, plant_id, open("images/" + str(plant_id) + "_(" + str(time) + ").jpg").read(), info["height"], info["colour"])
    return

def add_plant():
    global abort_plant
    global plantsInfo
    global noplant

    print("Moving UR to addition pose")
    qr_content = []
    while (len(qr_content) == 0):

        qr_content = esp.getQR()

        if (abort_plant):
            print("moving UR to home")
            abort_plant = False
            return

    np = decodeQR(qr_content[0])

    id = db.addPlant(np["name"], np["pot_number"], np["since"], np["watering_time"], np["moisture_threshold"], np["moisture_period"], np["photo_period"])

    nm = {
        "id": id,
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

    
    db.addWateringValue(nm["watering"]["time"], id, nm["watering"]["value"])
    db.addHumidityValue(nm["humidity"]["time"], id, nm["humidity"]["value"])

    noplant = False

    sio.emit('QRReading', db.getLastPK())
    

def UR_home():
    print("UR going to home position")

def main():
    global add_plant_request
    global action_in_progress
    global running
    global noplant
    global lastMeasureInfo

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

        action_in_progress = True

        OK = True
        if (nextMeasure["type"] in "humidity"): doMeasure(nextMeasure["plant"], plantsInfo)
        elif (nextMeasure["type"] in "image"): takePicture(nextMeasure["plant"])

        action_in_progress = False

        if(add_plant_request):
            add_plant()
            add_plant_request = False

        #print(nextMeasure)
        print("\n" + "-"*80 + "\n")
        #sio.wait()

    db.closeDB()

if __name__ == '__main__':

    sio.connect('http://www.weeplant.es:80')
<<<<<<< HEAD
=======
    signal.signal(signal.SIGINT, signal_handler)
    print("We Alive!")
>>>>>>> 809604bd49c7c6f6cc63d49463138cf133a34afe
    #sio.connect('http://localhost:2000')

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