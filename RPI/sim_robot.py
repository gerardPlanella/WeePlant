import socket
import time
import math as m


#Trama: speed.interpolation_steps.angle_base.angle_hombro.angle_colze.angle_endeffector\n

#PORT = 25852

class UR_SIM():

    __slots__ = ('address','port','s','positions')

    def __init__ (self, address,port):
        self.address = address 
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        err = self.s.connect((self.address, self.port))
        
        if err == 0:
            print("Error connectant amb la simulacio")

        self.positions = {
            "home": [90, 90, 90, 120,0],
            "pot 1":[156, 79, 128, 90,0],
            "pot 2":[156, 79, 128, 120,0],
            "pot 3":[156, 79, 128, 150,0],
            "watering tool":[169, 95, 128, -90, 0],
            "watering tool grab":[169, 95, 128, -90, 1],
            "watering tool release":[169, 95, 128, -90,3],
            "ground tool":[169, 95, 128, -20,0],
            "ground tool grab":[169, 95, 128, -20,2],
            "ground tool release":[169, 95, 128, -20,3],
            "second position" : [0,90,0,90,0]
        }

    def getAddress(self):
        return self.address

    def move(self,position_name,speed,interpolationSteps):
        trama = str(speed) + "." + str(interpolationSteps) + "."

        for e in self.positions[position_name]:
            trama += str(e) + "."

        #Ara una mica de Magia negra...
        trama = "\n".join(trama.rsplit(".", 1))
        
        self.s.sendall(trama.encode('ascii'))

        #Response ignored. Its used to block the program untill the simulation reaches its goal
        self.s.recv(1024).decode('ascii')

    #Pot number can be: 1 2 3
    def addPot(self,potNumber):
        if potNumber < 1 or potNumber > 3:
            print("Bad input in sim robot.")
            return
        self.s.sendall(("#"+str(potNumber) +"\n").encode('ascii'))
"""
if __name__ == "__main__":
    sim = UR_SIM("localhost", 25852)
    sim.move("home",20,50)
    sim.move("ground tool",20,50)
    sim.move("ground tool grab",20,50)
    sim.move("home",20,50)
""" 