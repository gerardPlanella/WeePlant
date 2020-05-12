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
            "pot 1":[156, 79, 128, 150,0],
            "pot 2":[156, 79, 128, 120,0],
            "pot 3":[156, 79, 128, 90,0],
            "pot foto 1":[135, 138, 90, 150,0],
            "pot foto 2":[135, 138, 90, 120,0],
            "pot foto 3":[135, 138, 90, 90,0],
            

            "watering tool before":[145, 95, 128, -90, 0],
            "watering tool grab":[169, 95, 128, -90, 1],
            "watering tool release":[169, 95, 128, -90,3],
          
            "humidity tool before":[145, 95, 128, -20,0],
            "humidity tool grab":[169, 95, 128, -20,2],
            "humidity tool release":[169, 95, 128, -20,3],
          
            "second position" : [0,90,0,90,0],

            "read QR":[137, 132, 48, 34, 0]
        }

    def getAddress(self):
        return self.address

    def disconnect(self):
        self.s.close()

    def move(self,position_name,speed = 40, interpolationSteps = 30):
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
    def removeAllPots(self):
        self.s.sendall(("#0\n").encode('ascii'))
"""
if __name__ == "__main__":
    sim = UR_SIM("localhost", 25852)
    sim.addPot(1)
    sim.addPot(2)
    sim.addPot(3)
    sim.move("home")
    sim.move("pot foto 1")

    sim.move("home")
    sim.move("pot foto 2")

    sim.move("home")
    sim.move("pot foto 3")

    sim.move("home",20,50)
    sim.move("humidity tool",20,50)
    sim.move("humidity tool grab",20,50)
    sim.move("home",20,50)
"""
