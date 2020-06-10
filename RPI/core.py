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
import signal
import sys

import numpy as np

from threading import Lock

import plant as plantcvlib
from sim_robot import UR_SIM

#TODO: AL FER WAITING, NO TORNA A HOME!!!!

#************************************************************CONFIGURABLE STUFF************************************************************

MODE_ESP32 = False
MODE_UR_SIM = True
USE_LOCALHOST = False

PUMP_TIME = 1

DEFAULT_HUMIDITY_NOESP32 = 0.1
DEFAULT_PATH_IMAGE_NOESP32 = "fakeImages/"#/weeplant_pres_22.jpg"

UR_SIM_IP = "25.120.137.245"
UR_SIM_PORT = 25852
#ESP32_IP = "192.168.1.36"
#ESP32_IP = "25.120.131.106"
ESP32_PORT = 8016

TOOL_ATTEMPTS = 5

#*********************************************************END OF CONFIGURABLE STUFF************************************************************

running = True
noplant = True
abort_plant = False

notifyWebToUpdate = False

plantsInfo = []
lastMeasureInfo = []

working_pot = -1

sio = socketio.Client()
db = database.WeePlantDB()

pictureNumber = 0
fake_image_number = 0

takePhotoMutex = Lock()
if MODE_UR_SIM:
    ur_sim = UR_SIM(UR_SIM_IP, UR_SIM_PORT)
    print("Connected with simulator.")
else:
    ur_sim = None

if (MODE_ESP32):
    esp = esp32.ESP32(ESP32_IP, ESP32_PORT)
    if(not esp.connect()):
        # TODO: Fer aixo beee
        print("Connection with esp32 failed")
        running = False
    else:
        print("Connection with esp32 established")
else:
    esp = None

if USE_LOCALHOST:
    WEB_HOST ="http://localhost:2000"
else:
    WEB_HOST = "http://www.weeplant.es:80"

DEFAULT_QR = [WEB_HOST + "/?name=Coolantus&watering_time=10&moisture_threshold=.2&moisture_period=60&photo_period=500",
            WEB_HOST + "/?name=Arrousus&watering_time=10&moisture_threshold=.2&moisture_period=30&photo_period=250",
            WEB_HOST + "/?name=GerSaules&watering_time=10&moisture_threshold=.2&moisture_period=180&photo_period=1000"]


def signal_handler(sig, frame):
    global ur_sim, esp, sio

    print('Goodbye!')

    if ur_sim is not None:
        ur_sim.disconnect()

    if esp is not None:
        esp.disconnect()
    if sio is not None:
        sio.disconnect()

    if takePhotoMutex.locked():
        takePhotoMutex.release()

    sys.exit(0)

"""
Not implemented.
@sio.on('[CHANGE_CONFIG]')
def on_message(data):
    global plantsInfo
    print("[WEB] Update local info")
    plantsInfo = requestTimings(db)
"""

@sio.on('[WEB_KNOWS_QR]')
def on_message(data):
    global working_pot

    takePhotoMutex.acquire()
    working_pot = int(data[0])
    add_plant(data[1])
    takePhotoMutex.release()


@sio.on('[ABORT_PLANT]')
def on_messasge(data):
    global abort_plant
    if (not MODE_ESP32): print("QR reading aborted. Please type a key to continue.")
    ur_sim.move("home")
    abort_plant = True

@sio.on('[ADD_PLANT]')
def on_msessage(data):
    global plantsInfo,working_pot,takePhotoMutex

    takePhotoMutex.acquire()
    working_pot = int(data)
    add_plant("")
    takePhotoMutex.release()
    return

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

def decodeQR(code):
    """Exemple: http://www.weeplant.es:80/?name=deictics_plant&watering_time=10&moisture_threshold=.2&moisture_period=60&photo_period=500"""
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
        "since": "'" + str(datetime.datetime.now()) + "'",
        "plant_ID": -1,
        "watering_time": attributes[1][1],
        "moisture_threshold": attributes[2][1],
        "moisture_period": attributes[3][1],
        "photo_period": attributes[4][1]
    }

def requestTimings(db):
    pots,plants = db.getActualPlants()


    if MODE_UR_SIM:
        ur_sim.removeAllPots()
        ur_sim.move("home")
        for pot in pots:
            print("Adding pot " + str(pot))
            ur_sim.addPot(pot)

    ret = []

    for plant in plants:
        ret.append(db.getPlant(plant))

    return ret

def requestTimestamps(db, plantsInfo):
    ret = []
    for p in plantsInfo:
        aux = {
            "id": p["plant_ID"],
            "pot_number":db.getPlant(p["plant_ID"])["pot_number"],
            "humidity": db.getHumidityLast(p["plant_ID"]),
            "watering": db.getWateringLast(p["plant_ID"]),
            "image": db.getImageLastTime(p["plant_ID"])
        }
        ret.append(aux)
    return ret

def getTimeForEarliestMeasure(lastMeasureInfo, plantsInfo):
    pmin = datetime.datetime.now()
    index = -1
    ptype = "null"
    pot_number = -1

    for i in range(len(lastMeasureInfo)):
        measure = lastMeasureInfo[i]
        plant = plantsInfo[i]

        #TimeForNextMeasure
        tfnm = measure["humidity"]["time"] + datetime.timedelta(seconds=plant["moisture_period"])
        if (measure["image"] != -1): aux = measure["image"] + datetime.timedelta(seconds=plant["photo_period"])
        else: aux = datetime.datetime.now()

        if (index < 0):
            index = measure["id"]

            if (tfnm < aux):
                pmin = tfnm
                ptype = "humidity"
                pot_number = measure["pot_number"]

            else:
                pmin = aux
                ptype = "image"
                pot_number = measure["pot_number"]


        else:
            if (pmin > tfnm):
                pmin = tfnm
                index = measure["id"]
                ptype = "humidity"
                pot_number = measure["pot_number"]


            if (pmin > aux):
                pmin = aux
                index = measure["id"]
                ptype = "image"
                pot_number = measure["pot_number"]


    #Time To Wait For Next Measure
    now = datetime.datetime.now()
    ttwfnm = pmin - now
    if (now + ttwfnm > now): ttwfnm = ttwfnm.total_seconds()
    else: ttwfnm = 0

    ret = {
        "time": ttwfnm,
        "pot_number":pot_number,
        "plant": index,
        "type": ptype
    }

    return ret

def doMeasure(plant_id, pot_number, plantsInfo):
    global TOOL_ATTEMPTS, DEFAULT_HUMIDITY_NOESP32,MODE_ESP32, MODE_UR_SIM, notifyWebToUpdate, ur_sim,PUMP_TIME
    print("****DOING A MEASUREMENT****")
    print("UR going to humidity tool to check plant pot " + str(pot_number))

    if MODE_UR_SIM:
        ur_sim.move("humidity tool before")


    print("UR going to attach humidity tool")

    if MODE_UR_SIM:
        ur_sim.move("humidity tool grab")

    attempts = TOOL_ATTEMPTS

    if (MODE_ESP32): value = esp.getHumidity()
    else: value = DEFAULT_HUMIDITY_NOESP32

    while (value == 0):
        if attempts == 0:
            UR_home()


            print("ERROR: Unable to connect to the tool")
            return

        attempts -= 1

        if MODE_UR_SIM:
            ur_sim.move("humidity tool before")

        print("UR tries to connect again to the tool")
        if MODE_UR_SIM:
            ur_sim.move("humidity tool grab")

        value = esp.getHumidity()



    print("move UR from tool to plant pot " + str(pot_number))

    if MODE_UR_SIM:
        ur_sim.move("home")
        ur_sim.move("pot " + str(pot_number))
        print("\tMeasuring humidity...")
        time.sleep(1)
        ur_sim.move("home")
    else:
        print("Measuring humidity...")

    if (MODE_ESP32): value = esp.getHumidity()
    else: value = DEFAULT_HUMIDITY_NOESP32


    print("UR leaves the tool in its place")
    if MODE_UR_SIM:
        ur_sim.move("humidity tool before")
        ur_sim.move("humidity tool release")

    db.addHumidityValue(datetime.datetime.now(), plant_id, value)

    #sio.emit("REFRESH", working_pot)
    notifyWebToUpdate = True

    plantInfo = plantsInfo[0]
    for plant in plantsInfo:
        if plant["plant_ID"] == plant_id:
            plantInfo = plant
            break

    if (plantInfo["moisture_threshold"] * 100 > value):


        if MODE_UR_SIM:
            print("UR going to grab watering tool")
            ur_sim.move("watering tool before")
            ur_sim.move("watering tool grab")
            ur_sim.move("watering tool before")
            print("UR going to plant " + str(pot_number))
            ur_sim.move("home")
            ur_sim.move("pot " + str(pot_number))
            print("\tTurn on the pump")
            time.sleep(PUMP_TIME)
            print("\tTurn off the pump")
            print("UR leaves the tool in its place")
            ur_sim.move("home")
            ur_sim.move("watering tool before")
            ur_sim.move("watering tool release")
            db.addWateringValue(datetime.datetime.now(), plant_id, (float)(plantInfo["moisture_threshold"] * 100) - value)
            UR_home()
        else:
            print("UR to watering tool")
            print("UR to plant " + str(pot_number))
            print("Turn on the pump")
            time.sleep(PUMP_TIME)
            print("Turn off the pump")
            print("UR leaves the tool in its place")
    print("****END OF MEASUREMENT****")
    return True

def getPlantData(path):
    plant = plantcvlib.Plant(image_path=path, write_image_output=True, result_path= "./out_plant_debugg/plant_2_info.json", write_result=True)
    plant.calculate()

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

    ret = {"height": 0, "colour": colour}

    if plant.isFramed() is True:
        height = plant.getHeight()

        if (not (height is not False)):
            ret["height"] = -1
            return ret
        else:
            ret["height"] = height

        (red, green, blue) = plant.getColourHistogram()
        ret["colour"] = [red["value"], green["value"], blue["value"]]
    return ret

def heightFunction(pictureNumber):
    return 52#1.0 / (1.0 + np.exp(-pictureNumber)) 

def takePicture(plant_id, pot_number):
    global esp, MODE_ESP32, DEFAULT_PATH_IMAGE_NOESP32, notifyWebToUpdate, pictureNumber,fake_image_number
    
    print("****TAKING A PHOTO****")
    print("UR going to plant " + str(pot_number))

    if MODE_UR_SIM:
        ur_sim.move("pot foto " + str(pot_number))
        print("\tTaking a photo")
        time.sleep(1)

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
    timee = datetime.datetime.now()

    if (MODE_ESP32): 
        path = "images/" + str(plant_id) + "_(" + str(timee) + ").jpg"
    elif (plant_id == 2):
        path = DEFAULT_PATH_IMAGE_NOESP32 + str(fake_image_number)+".jpg"
        if (fake_image_number < 15):
            fake_image_number = fake_image_number + 1
    else:
        path = "./fakeImages/weeplant_pres_22.jpg"

    if (MODE_ESP32): esp.getImage(path)

    # This is for the PlantCV Library
    #info = getPlantData(path)

    db.addImage(timee, plant_id, open(path, 'rb').read(), heightFunction(pictureNumber), colour)
    #sio.emit("REFRESH", working_pot)
    notifyWebToUpdate = True

    if MODE_UR_SIM:
        ur_sim.move("home")
    
    pictureNumber = pictureNumber + 1
    print("****END OF TAKING A PHOTO****")
    #db.addImage(timee, plant_id, open("images/" + str(plant_id) + "_(" + str(timee) + ").jpg").read(), info["height"], info["colour"])
    return

def abortPlantIfNecessary():
    global abort_plant
    if abort_plant:
        print("Aborting plant addition due to user interaction in the webpage.")
        abort_plant = False
        UR_home()
        #Exit the function
        return True
    return False

def add_plant(qr_ss):
    global abort_plant, plantsInfo, noplant, working_pot, DEFAULT_QR, MODE_UR_SIM,sio

    np = ""

    if(qr_ss != ""):
        print("Decoding the qr provided trough the webpage")
        np = decodeQR(qr_ss)
    else:

        print("UR going to read the QR")
        if MODE_UR_SIM:
            ur_sim.move("read QR")

        if (MODE_ESP32):
            qr_content = []

            while (len(qr_content) == 0):

                qr_content = esp.getQR()

                if (abort_plant):
                    return

            if abortPlantIfNecessary():
                return

            np = decodeQR(qr_content[0])
        else:
            qr_used = DEFAULT_QR[working_pot - 1]
            np = decodeQR(qr_used)
            input("Enter a key to \"add a new qr\": \n")
            if abortPlantIfNecessary():
                return



    id = db.addPlant(np["name"], working_pot, np["since"], np["watering_time"], np["moisture_threshold"], np["moisture_period"], np["photo_period"])
    np['plant_ID'] = id

    nm = {
        "id": id,
        "humidity": {
            "time": datetime.datetime.now(),
            "value": 0
            },
        "watering": {
            "time": datetime.datetime.now(),
            "value": 0
            },
        "image": datetime.datetime.now()
    }

    plantsInfo.append(np)
    lastMeasureInfo.append(nm)

    db.addWateringValue(nm["watering"]["time"], id, nm["watering"]["value"])
    db.addHumidityValue(nm["humidity"]["time"], id, nm["humidity"]["value"])

    sio.emit('QRReading',"")

    if MODE_UR_SIM:
        ur_sim.addPot(working_pot)

    doMeasure(id,working_pot, plantsInfo)
    takePicture(id, working_pot)

    sio.emit("REFRESH", working_pot)
    
    UR_home()

    noplant = False


def UR_home():
    global MODE_UR_SIM,ur_sim

    print("UR going to home position")
    if MODE_UR_SIM:
        ur_sim.move("home")

def smartWaitPrint(nextMeasure):
    if (nextMeasure["type"] in "humidity"): print("Waiting " + str(nextMeasure["time"]) + " s to check the humidity levels in plant " + str(nextMeasure["pot_number"]))
    elif (nextMeasure["type"] in "image"): print("Waiting " + str(nextMeasure["time"]) + " s to take a photo of plant " + str(nextMeasure["pot_number"]))

def main():
    global running
    global noplant
    global lastMeasureInfo
    global plantsInfo
    global takePhotoMutex
    global notifyWebToUpdate
    global working_pot

    plantsInfo = requestTimings(db)
    if (len(plantsInfo) == 0): noplant = True
    else: noplant = False

    while (noplant):
        time.sleep(1)

    while (running):

        lastMeasureInfo = requestTimestamps(db, plantsInfo)

        nextMeasure = getTimeForEarliestMeasure(lastMeasureInfo, plantsInfo)

        if notifyWebToUpdate and nextMeasure["time"] > 0:
            print("****REQUESTING WEBPAGE REFRESH****")
            sio.emit("REFRESH", working_pot)
            notifyWebToUpdate = False

        if (nextMeasure["time"] > 0):
            smartWaitPrint(nextMeasure)

            time.sleep(nextMeasure["time"])

        takePhotoMutex.acquire()

        if (nextMeasure["type"] in "humidity"): doMeasure(nextMeasure["plant"],nextMeasure["pot_number"], plantsInfo)
        elif (nextMeasure["type"] in "image"): takePicture(nextMeasure["plant"],nextMeasure["pot_number"])

        if notifyWebToUpdate and nextMeasure["time"] > 0:
            print("****REQUESTING WEBPAGE REFRESH****")
            sio.emit("REFRESH", working_pot)
            notifyWebToUpdate = False

        takePhotoMutex.release()

        #print(nextMeasure)
        #print("\n" + "-"*80 + "\n")
        #sio.wait()

    db.closeDB()

if __name__ == '__main__':

    if (running):
        sio.connect(WEB_HOST)
        signal.signal(signal.SIGINT, signal_handler)
        print("We Alive!")

        main()

        sio.wait()
