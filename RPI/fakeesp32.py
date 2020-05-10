import random

class esp32:
    __init__(self):
        pass


    def getHumidity():
        return random.randint(0, 100) / 100

    def getImage(path):
        plant = random.randint(1, 12)
        open("fakeImages/" + str(plant) + ".jpg").read().write(path)

    def getQR(self):
        return "http://www.weeplant.es:80/?name=Wisconsin_Fast_Plants&watering_time=30&moisture_threshold=.3&moisture_period=60&photo_period=90"
